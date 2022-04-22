from django import forms


class Fieldsets:
    """
    Converts a form into a django admin fieldset.
    """

    def __init__(self, form, fieldsets=None):
        self.form = form
        self._fieldsets = fieldsets or ((None, {"fields": list(form.fields.keys())}),)

    def get_field(self, name, is_readonly, is_first, is_last):
        try:
            formfield = self.form[name]

        except KeyError:
            return None

        else:
            return {
                "field": formfield,
                "is_first": is_first,
                "is_last": is_last,
                "is_readonly": is_readonly,
                "is_checkbox": isinstance(formfield.field.widget, forms.CheckboxInput),
            }

    def get_fieldset(self, name, **options):
        fields = options.get("fields") or []
        readonly_fields = options.get("fields") or []
        description = options.get("description")

        if not fields:
            return None

        return {
            "form": self.form,
            "name": name,
            "description": description,
            "readonly_fields": readonly_fields,
            "fields": filter(
                None,
                [
                    self.get_field(
                        name,
                        is_readonly=name in readonly_fields,
                        is_first=i == 1,
                        is_last=i == len(fields),
                    )
                    for i, name in enumerate(fields, start=1)
                ],
            ),
        }

    def __iter__(self):
        for name, options in self._fieldsets:
            fieldset = self.get_fieldset(name, **(options or {}))

            if not fieldset:
                continue

            yield fieldset
