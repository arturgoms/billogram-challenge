from itertools import groupby

from django.forms import Form
from django.utils.module_loading import import_string


def build_dynamic_config_form_class(params):
    """
    Returns the dynamic config form based on saved values.
    """
    fieldsets = []
    fields = {}

    for group, parameters in groupby(params, key=lambda x: x.get("group")):
        group_fields = {}

        for parameter in parameters:
            key = parameter["key"]
            field_class = import_string(parameter["form_field"])
            widget = parameter.get("form_field_widget")
            validators = parameter.get("validators") or []

            group_fields[key] = field_class(
                label=parameter["name"],
                help_text=parameter.get("description"),
                initial=parameter["value"],
                validators=[
                    import_string(validator)(**params)
                    for validator, params in validators
                ],
                required=parameter.get("required") or False,
                widget=import_string(widget) if widget else field_class.widget,
            )

        fieldsets.append((group, {"fields": group_fields.keys()}))
        fields.update(group_fields)

    form = type("DynamicConfigForm", (Form,), fields)
    return form, fieldsets
