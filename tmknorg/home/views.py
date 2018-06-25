from django.http import HttpResponse
from django.templatetags.static import static
from django.views import View
from django.views.generic.base import RedirectView, TemplateView


class HomeView(TemplateView):
    template_name = 'home/home.html'


class FaviconView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return static('icons/favicon.ico')


class SSHKeyView(View):
    def get(self, request, *args, **kwargs):
        ssh_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDNBhT7EJCemeBx+oVa/EKMywhUvV6kRnRFYPtB/A0hcId7JrS6mZRsgKKgrUvKTvv1eR9VmzHQJzYUTqZVFvm5VzDXU+LqEV9BBapjJeYiJA9GXXeAZperFTKCZqCH6sBF0WAI3KPenSDsFzVL7GEHd/uar4aEcmDljlh2jEISUMNEpYFpMrr42Y7owS0bA0UVTABtnKg6yvzFubn9CfAadvT/8gzzR5LpVY8ymaHdcH3pSxnWUXEoY/hIwTaYy2MELz4qQ6aGyNDfvt/OKLOfD4LVkGvbZ6HA8UWxMFfEDXNs4RmBtRkD3GHx+29WX8pvs9slR/OAyzNG+/h6hrT8ozxXf8GuuSYf592gu0MgW+8jy2HcKlVsI9INpfTWB/eFRyetF5NBz5KwnSU9YgFTvkr9+uNTKv3enfMJcGtECqX8s3FvMWMdQrLefQfD87U3vcRearJ6hb5C+WcdJsQ0E2UxF/BVGIoQGQH2D6pZ282vhAT8ZiHXf4ow6I4r1y30zmvtBv6vELuOBtD+a+z7InppiTbhwTj9nlz6JelcTPKjvkMaEk20HRXTzEVh8DJ+zRJIID9wDwAYZ7MrwiiCpDJ/LxH3O0wPniuqa0eBAP8A5kHIp8VUrCdQCOGWyz6cdqMCJ0Js02ycOoWUEbIrOO92sOVPNHYM0zLL/o0VtQ== me@tmkn.org"  # noqa
        return HttpResponse(ssh_key, content_type='text/plain')


class PGPKeyView(View):
    def get(self, request, *args, **kwargs):
        pgp_key = """-----BEGIN PGP PUBLIC KEY BLOCK-----

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
=JRIa
-----END PGP PUBLIC KEY BLOCK-----"""
        return HttpResponse(pgp_key, content_type='application/pgp-keys')