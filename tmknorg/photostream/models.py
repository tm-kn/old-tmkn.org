from django.core.paginator import (EmptyPage, InvalidPage, PageNotAnInteger,
                                   Paginator)
from django.db import models
from django.shortcuts import redirect
from django.utils.functional import cached_property

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.models import Orderable, Page
from wagtail.images import get_image_model_string
from wagtail.images.edit_handlers import ImageChooserPanel

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from tmknorg.core.mixins import SocialFields


class PhotoIndex(SocialFields, Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['photostream.PhotoPage']

    promote_panels = Page.promote_panels + SocialFields.promote_panels

    def serve(self, request, *args, **kwargs):
        try:
            return super().serve(request, *args, **kwargs)
        except (EmptyPage, PageNotAnInteger, InvalidPage):
            return redirect(self.relative_url(
                getattr(request, 'site', None),
                request=request
            ))

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        qs = PhotoPage.objects.live().public().child_of(self) \
                                              .order_by('-first_published_at')
        paginator = Paginator(qs, 20)
        page = request.GET.get('page', 1)
        context['photo_pages'] = paginator.page(page)
        return context


class PhotoPagePhoto(Orderable, ClusterableModel):
    page = ParentalKey('photostream.PhotoPage', related_name='photos')
    photo = models.ForeignKey(get_image_model_string(), models.CASCADE,
                              related_name='+')
    panels = [
        ImageChooserPanel('photo'),
    ]


class PhotoPage(SocialFields, Page):
    parent_page_types = ['photostream.PhotoIndex']
    subpage_types = []

    promote_panels = Page.promote_panels + SocialFields.promote_panels

    content_panels = Page.content_panels + [
        FieldPanel('first_published_at'),
        InlinePanel('photos', label="Photos", min_num=1),
    ]

    @cached_property
    def photos_qs(self):
        return self.photos.select_related('photo').prefetch_related(
            'photo__renditions'
        )
