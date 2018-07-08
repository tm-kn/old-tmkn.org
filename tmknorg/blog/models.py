from django.core.paginator import (EmptyPage, InvalidPage, PageNotAnInteger,
                                   Paginator)
from django.shortcuts import redirect

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField

from tmknorg.core.blocks import BodyBlock
from tmknorg.core.mixins import PageFeed


class BlogIndex(PageFeed, Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['blog.BlogPage']

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
        qs = BlogPage.objects.live().public().child_of(self) \
                                             .order_by('-first_published_at')
        paginator = Paginator(qs, 20)
        page = request.GET.get('page', 1)
        context['blog_pages'] = paginator.page(page)
        return context


class BlogPage(Page):
    parent_page_types = ['blog.BlogIndex']
    subpage_types = []
    body = StreamField(BodyBlock())
    content_panels = Page.content_panels + [
        FieldPanel('first_published_at'),
        StreamFieldPanel('body'),
    ]

    def get_feed_content(self):
        return self.body

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(self.get_parent().specific.get_feed_context(request))
        return context
