from django import forms
from django.contrib.admin import widgets
from django.utils.translation import gettext_lazy as _

from apps.domain import models
from commons.admin.permissions.helper import permission_helper
from commons.forms.mixins import ContextFormMixin


class UserInviteAdminForm(ContextFormMixin, forms.ModelForm):
    roles = forms.MultipleChoiceField(
        label=_("Roles"),
        widget=widgets.FilteredSelectMultiple(
            verbose_name=_("Roles"), is_stacked=False
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["roles"].choices = permission_helper.get_all_permissions()

    class Meta:
        model = models.PanelUser
        fields = ["name", "email", "roles"]
