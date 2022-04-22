from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import TemplateView


class ApiDocView(TemplateView):
    template_name = "api/redoc.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return {
            **context,
            **admin.site.each_context(self.request),
            "title": _("API Docs"),
            "spec_url": reverse("api-docs-specs"),
        }


class ApiDocSpecView(View):
    template_name = "api/redoc.html"
    api_spec_path = "docs/api.openapi.json"

    @property
    def file(self):
        with open(settings.BASE_DIR / self.api_spec_path) as f:
            return f.read()

    def get(self, request):
        return HttpResponse(self.file, content_type="application/json")
