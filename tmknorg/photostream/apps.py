from django.apps import AppConfig


class PhotostreamConfig(AppConfig):
    name = 'tmknorg.photostream'

    def ready(self):
        from . import signals  # noqa
