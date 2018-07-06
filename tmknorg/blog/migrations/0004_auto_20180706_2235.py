# Generated by Django 2.0.6 on 2018-07-06 22:35

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180706_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.RichTextBlock()), ('h2', wagtail.core.blocks.CharBlock(template='core/blocks/h2.html')), ('h3', wagtail.core.blocks.CharBlock(template='core/blocks/h3.html')), ('image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.CharBlock(required=False))], template='core/blocks/image.html'))]),
        ),
    ]