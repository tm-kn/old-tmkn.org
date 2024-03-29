from django.conf import settings
from django.contrib.syndication.views import Feed
from django.db import models
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.images import get_image_model_string
from wagtail.images.edit_handlers import ImageChooserPanel


class PageChildrenFeed(Feed):
    def __init__(self, *args, **kwargs):
        self.children = kwargs.pop('children', None)
        self.title = kwargs.pop('title', None)
        self.description = kwargs.pop('description', None)
        self.link = kwargs.pop('link', None)
        self.feed_type = kwargs.pop('feed_type', None)
        super().__init__(*args, **kwargs)

    def items(self):
        return self.children

    def item_link(self, item):
        return item.get_url()

    def item_description(self, item):
        return item.get_feed_content()

    def item_pubdate(self, item):
        return item.first_published_at


class PageFeed(RoutablePageMixin):
    def get_feed_items(self):
        return self.get_children().live().public() \
                                         .order_by('-first_published_at') \
                                         .specific()

    def base_feed(self, feed_type, request, *args, **kwargs):
        return PageChildrenFeed(
            feed_type=feed_type,
            children=self.get_feed_items(),
            link=self.relative_url(getattr(request, 'site', None),
                                   request=request),
            title=self.get_feed_title(),
        )(request, *args, *kwargs)

    def get_feed_title(self):
        return f"{settings.WAGTAIL_SITE_NAME} - {self.title}"

    @route(r'^rss/$', name='rss_feed')
    def rss_feed(self, request, *args, **kwargs):
        return self.base_feed(Rss201rev2Feed, request, *args, **kwargs)

    @route(r'^atom/$', name='atom_feed')
    def atom_feed(self, request, *args, **kwargs):
        return self.base_feed(Atom1Feed, request, *args, **kwargs)

    def get_feed_context(self, request):
        context = {}
        base_url = self.relative_url(getattr(request, 'site', None),
                                     request=request)
        context['rss_feed_url'] = (
            base_url + self.reverse_subpage('rss_feed')
        )

        context['rss_feed_title'] = f"{self.get_feed_title()} (RSS)"
        context['atom_feed_url'] = (
            base_url + self.reverse_subpage('atom_feed')
        )
        context['atom_feed_title'] = f"{self.get_feed_title()} (Atom)"
        return context

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(self.get_feed_context(request))
        return context

    def get_cached_paths(self):
        yield '/'
        yield self.reverse_subpage('rss_feed')
        yield self.reverse_subpage('atom_feed')


class SocialFields(models.Model):
    feed_image = models.ForeignKey(get_image_model_string(), models.SET_NULL,
                                   blank=True, null=True, related_name='+')

    promote_panels = [
        ImageChooserPanel('feed_image'),
    ]

    class Meta:
        abstract = True
