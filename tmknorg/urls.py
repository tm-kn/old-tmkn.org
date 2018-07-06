from itertools import chain

from django.conf import settings
from django.urls import include, path
from django.views.decorators.cache import cache_control

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls
from wagtail.core.models import Page
from wagtail.utils.urlpatterns import decorate_urlpatterns

from tmknorg.home.views import FaviconView, HomeView, PGPKeyView, SSHKeyView


frontendcache = cache_control(
    public=True,
    s_maxage=int(getattr(settings, 'FRONTEND_CACHE_CONTROL_S_MAXAGE',
                         4 * 60 * 60)),
    stale_while_revalidate=int(getattr(
        settings,
        'FRONTEND_CACHE_CONTROL_STALE_WHILE_REVALIDATE',
        30
    )),
)


urlpatterns = decorate_urlpatterns([
    path('', HomeView.as_view(), name='home'),
    path('id_rsa.pub', frontendcache(SSHKeyView.as_view()), name='ssh-key'),
    path('public.asc', frontendcache(PGPKeyView.as_view()), name='pgp-key'),
    path('favicon.ico', FaviconView.as_view(), name='favicon'),
], frontendcache)

urlpatterns = chain(urlpatterns, [
    path('cms/', include(wagtailadmin_urls)),
    path('blog/', include(wagtail_urls)),
    path('documents/', include(wagtaildocs_urls)),
])

urlpatterns = list(urlpatterns)


Page.serve = frontendcache(Page.serve)
