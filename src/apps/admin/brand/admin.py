from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from apps.api.shortcuts import generate_user_token
from apps.domain import models
from commons.admin.mixins import SmartAdminMixin
from commons.admin.permissions.mixins import PermissionsAdminMixin
from django.utils.translation import gettext_lazy as _


@admin.register(models.Brand)
class BrandAdmin(PermissionsAdminMixin, SmartAdminMixin, admin.ModelAdmin):
    list_display = ["name", "email", "website"]
    search_fields = ["name", "email", "website"]
    group = _("Users")

    fieldsets = (
        (
            None,
            {
                "fields": [
                    "name",
                ]
            },
        ),
        (_("Contact"), {"fields": ["email", "website"]}),
        (_("Settings"), {"fields": ["authentication_token_field"]}),
    )

    readonly_fields = ["authentication_token_field"]

    def get_queryset(self, request):
        return super().get_queryset(request)

    # Custom Field

    @admin.display(description=_("Authentication Token"), empty_value="-")
    def authentication_token_field(self, obj):
        # INFO: Depends on authentication service.
        if not obj.pk:
            return "-"

        return render_to_string(
            "admin/includes/copyable.html",
            context={
                "content": generate_user_token(obj),
                "field_id": "webhook-url",
                "help_text": mark_safe(_("Use this token to authenticate in API.")),
            },
        )
