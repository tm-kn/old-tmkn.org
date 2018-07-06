from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False)


class BodyBlock(blocks.StreamBlock):
    paragraph = blocks.RichTextBlock()
    h2 = blocks.CharBlock(template='core/blocks/h2.html')
    h3 = blocks.CharBlock(template='core/blocks/h3.html')
    image = ImageBlock(template='core/blocks/image.html')
