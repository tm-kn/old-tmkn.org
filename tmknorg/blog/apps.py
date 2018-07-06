from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'tmknorg.blog'

    def ready(self):
        from . import signals  # noqa
