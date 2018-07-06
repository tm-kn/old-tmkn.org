from django.db import models

from wagtail.images.models import (
    Image as WagtailImage, AbstractImage, AbstractRendition)


class CustomImage(AbstractImage):
    admin_form_fields = WagtailImage.admin_form_fields


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, models.CASCADE,
                              related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
