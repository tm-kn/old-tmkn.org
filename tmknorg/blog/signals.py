from django.dispatch import receiver
from django.db.models.signals import pre_delete

from wagtail.core.signals import page_published
from wagtail.contrib.frontend_cache.utils import PurgeBatch

from .models import BlogIndex, BlogPage


def blog_page_changed(blog_page):
    batch = PurgeBatch()
    for blog_index in BlogIndex.objects.live():
        if blog_page in blog_index.get_children():
            batch.add_page(blog_index)

    batch.purge()


@receiver(page_published, sender=BlogPage)
def blog_published_handler(instance, **kwargs):
    blog_page_changed(instance)


@receiver(pre_delete, sender=BlogPage)
def blog_deleted_handler(instance, **kwargs):
    blog_page_changed(instance)
