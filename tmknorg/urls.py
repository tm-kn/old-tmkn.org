"""tmknorg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_control
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


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', frontendcache(HomeView.as_view()), name='home'),
    path('id_rsa.pub', frontendcache(SSHKeyView.as_view()), name='ssh-key'),
    path('public.asc', frontendcache(PGPKeyView.as_view()), name='pgp-key'),
    path('favicon.ico', FaviconView.as_view(), name='favicon'),
]
