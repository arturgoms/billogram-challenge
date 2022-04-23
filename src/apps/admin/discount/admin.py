from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from apps.api.shortcuts import generate_user_token
from apps.domain import models
from commons.admin.mixins import SmartAdminMixin
from commons.admin.permissions.mixins import PermissionsAdminMixin
from django.utils.translation import gettext_lazy as _


@admin.register(models.Discount)
class DiscountAdmin(PermissionsAdminMixin, SmartAdminMixin, admin.ModelAdmin):
    list_display = ["code", "description", "quantity", "balance_field", "brand"]
    search_fields = ["code", "quantity", "brand"]
    group = _("Discounts")

    fieldsets = (
        (
            None,
            {"fields": ["code", "description", "brand"]},
        ),
        (_("Data"), {"fields": ["quantity", "balance_field"]}),
    )

    readonly_fields = ["balance_field"]
    autocomplete_fields = ["brand"]

    def get_queryset(self, request):
        return super().get_queryset(request).with_used()

    # Custom Field

    @admin.display(description=_("Balance"), ordering="balance")
    def balance_field(self, obj):
        """
        Returns annotated ``balance`` field.
        """
        balance = obj.quantity - obj.used
        return balance

    # Permissions

    def has_add_permission(self, request):
        """
        Disable django default create view.
        """
        return True

    def has_change_permission(self, request, obj=None):
        return True
