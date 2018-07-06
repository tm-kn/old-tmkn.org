from django.dispatch import receiver
from django.db.models.signals import pre_delete

from wagtail.core.signals import page_published
from wagtail.contrib.frontend_cache.utils import PurgeBatch

from .models import BlogIndex, BlogPage


def blog_page_changed(blog_page):
    batch = PurgeBatch()
    for index in BlogIndex.objects.live().ancestor_of(blog_page):
        batch.add_page(index)

    batch.purge()


@receiver(page_published, sender=BlogPage)
def blog_published_handler(instance, **kwargs):
    blog_page_changed(instance)


@receiver(pre_delete, sender=BlogPage)
def blog_deleted_handler(instance, **kwargs):
    blog_page_changed(instance)
