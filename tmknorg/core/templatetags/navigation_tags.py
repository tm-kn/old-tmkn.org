from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def navigation_items(context):
    request = context['request']
    qs = request.site.root_page.get_children().live().public().in_menu()
    for page in qs:
        yield page
