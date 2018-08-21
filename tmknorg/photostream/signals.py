from django.dispatch import receiver
from django.db.models.signals import pre_delete

from wagtail.core.signals import page_published
from wagtail.contrib.frontend_cache.utils import PurgeBatch

from .models import PhotoPage, PhotoIndex


def photo_page_changed(photo_page):
    batch = PurgeBatch()
    for index in PhotoIndex.objects.live().ancestor_of(photo_page):
        batch.add_page(index)
    batch.purge()


@receiver(page_published, sender=PhotoPage)
def photo_published_handler(instance, **kwargs):
    photo_page_changed(instance)


@receiver(pre_delete, sender=PhotoPage)
def photo_deleted_handler(instance, **kwargs):
    photo_page_changed(instance)
