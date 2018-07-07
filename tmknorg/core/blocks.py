from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False)

    class Meta:
        template = 'core/blocks/image.html'


class BodyBlock(blocks.StreamBlock):
    paragraph = blocks.RichTextBlock()
    h2 = blocks.CharBlock(template='core/blocks/h2.html')
    h3 = blocks.CharBlock(template='core/blocks/h3.html')
    image = ImageBlock()

    class Meta:
        template = 'core/blocks/body.html'
