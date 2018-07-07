from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed

from wagtail.contrib.routable_page.models import RoutablePageMixin, route


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
        return item.body


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
            title=f"{settings.WAGTAIL_SITE_NAME} - {self.title}",
        )(request, *args, *kwargs)

    @route(r'^rss/$')
    def rss_feed(self, request, *args, **kwargs):
        return self.base_feed(Rss201rev2Feed, request, *args, **kwargs)

    @route(r'^atom/$')
    def atom_feed(self, request, *args, **kwargs):
        return self.base_feed(Atom1Feed, request, *args, **kwargs)
