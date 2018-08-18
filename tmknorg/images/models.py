from django.db import models

from wagtail.images.models import (
    Image as WagtailImage, AbstractImage, AbstractRendition)


class CustomImage(AbstractImage):
    alternative_text = models.CharField(max_length=255, blank=True)
    admin_form_fields = WagtailImage.admin_form_fields + (
        'alternative_text',
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, models.CASCADE,
                              related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )

    @property
    def alt(self):
        return self.image.alternative_text or self.image.title

    @property
    def title(self):
        return self.image.title
