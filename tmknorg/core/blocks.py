from django.utils.html import mark_safe

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False)

    class Meta:
        template = 'core/blocks/image.html'


class CodeBlock(blocks.StructBlock):
    language = blocks.CharBlock(required=False)
    caption = blocks.CharBlock(required=False)
    code = blocks.TextBlock()

    class Meta:
        icon = 'code'
        template = 'core/blocks/code.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        try:
            lexer = get_lexer_by_name(value['language'], stripall=True)
        except ClassNotFound:
            lexer = TextLexer(stripall=True)
        formatter = HtmlFormatter(linenos=None, cssclass='codehilite',
                                  noclasses=False)
        context['html_code'] = highlight(value['code'], lexer, formatter)
        context['html_code'] = mark_safe(context['html_code'])
        return context


class BodyBlock(blocks.StreamBlock):
    code = CodeBlock()
    paragraph = blocks.RichTextBlock()
    h2 = blocks.CharBlock(template='core/blocks/h2.html')
    h3 = blocks.CharBlock(template='core/blocks/h3.html')
    image = ImageBlock()

    class Meta:
        template = 'core/blocks/body.html'
