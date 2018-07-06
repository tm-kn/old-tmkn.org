from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField

from tmknorg.core.blocks import BodyBlock


class BlogIndex(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['blog.BlogPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['blog_pages'] = (
            self.get_children().live().public().order_by('-first_published_at')
        )
        return context


class BlogPage(Page):
    parent_page_types = ['blog.BlogIndex']
    subpage_types = []
    body = StreamField(BodyBlock())
    content_panels = Page.content_panels + [
        FieldPanel('first_published_at'),
        StreamFieldPanel('body'),
    ]
