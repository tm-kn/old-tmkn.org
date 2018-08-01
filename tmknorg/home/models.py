from wagtail.core.models import Page

from tmknorg.core.mixins import SocialFields


class HomePage(SocialFields, Page):
    parent_page_types = ['wagtailcore.Page']
    promote_panels = Page.promote_panels + SocialFields.promote_panels
