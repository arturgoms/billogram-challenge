from django.conf import settings
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _, gettext
from django.views.generic import FormView

from apps.admin.views.dynamic_config.form import build_dynamic_config_form_class
from apps.crosscutting.dynamic_config import dynamic_config
from commons.forms.fieldsets import Fieldsets


class DynamicConfigAdminView(FormView):
    template_name = "admin/dynamic_config/change_form.html"
    fieldsets = None

    def get_form_class(self):
        parameters = getattr(settings, "DYNAMIC_CONFIG", None) or []
        parameters = map(
            lambda x: dict(x, value=dynamic_config.get(x["key"])), parameters
        )
        form_class, self.fieldsets = build_dynamic_config_form_class(parameters)
        return form_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return {
            **context,
            **admin.site.each_context(self.request),
            "fieldsets": Fieldsets(context["form"], self.fieldsets),
            "title": _("Settings"),
        }

    def form_valid(self, form):
        for key, value in form.cleaned_data.items():
            dynamic_config.set(key, value)

        messages.success(
            self.request,
            str.format(
                gettext("The {name} was updated successfully!"), name=_("Settings")
            ),
        )

        next_url = self.request.GET.get("next") or self.request.get_full_path()
        return HttpResponseRedirect(next_url)
