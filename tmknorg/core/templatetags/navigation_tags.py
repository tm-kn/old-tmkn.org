from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def navigation_items(context):
    request = context['request']
    yield request.site.root_page
    for page in request.site.root_page.get_children().live().public():
        yield page
