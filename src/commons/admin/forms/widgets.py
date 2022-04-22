import base64
import io
import json
import re
import uuid

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminTimeWidget, SELECT2_TRANSLATIONS
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import Media
from django.utils.translation import gettext_lazy as _, get_language

from commons import parser


class IntegerTimeWidget(AdminTimeWidget):
    """
    Input to represent an integer field as a time widget.

    The field value will be cast as seconds to time.
    """

    def format_value(self, value):
        if value is None:
            return None

        try:
            value = parser.time_from_seconds(int(value))

        except (TypeError, ValueError):
            return None

        return super().format_value(value)

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        return parser.time_to_seconds(value)


class Select2Widget(forms.Select):
    """
    Select widget mixin that loads options from AutocompleteJsonView via AJAX.

    Renders the necessary data attributes for select2 and adds the static form
    media.
    """

    def build_attrs(self, base_attrs, extra_attrs=None):
        """
        Set select2's AJAX attributes.

        Attributes can be set using the html5 data attribute.
        Nested attributes require a double dash as per
        https://select2.org/configuration/data-attributes#nested-subkey-options
        """
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        attrs.setdefault("class", "")
        attrs.update(
            {
                "data-theme": "admin-select",
                "data-allow-clear": json.dumps(not self.is_required),
                "data-placeholder": "",  # Allows clearing of the input.
                "class": attrs["class"]
                + (" " if attrs["class"] else "")
                + "admin-select",
            }
        )
        return attrs

    @property
    def media(self):
        extra = "" if settings.DEBUG else ".min"
        i18n_name = SELECT2_TRANSLATIONS.get(get_language())
        i18n_file = (
            ("admin/js/vendor/select2/i18n/%s.js" % i18n_name,) if i18n_name else ()
        )
        return forms.Media(
            js=(
                "admin/js/vendor/jquery/jquery%s.js" % extra,
                "admin/js/vendor/select2/select2.full%s.js" % extra,
            )
            + i18n_file
            + (
                "admin/js/jquery.init.js",
                "admin/js/select.js",
            ),
            css={
                "screen": (
                    "admin/css/vendor/select2/select2%s.css" % extra,
                    "admin/css/select.css",
                ),
            },
        )


class ImageCropperWidget(forms.TextInput):
    """
    This widget can be used to render an image input with a cropper.
    """

    template_name = "forms/widgets/image_cropper.html"
    input_text = _("Change")

    def __init__(self, attrs=None, aspect_ratio=None, filename=None, modifier=None):
        super().__init__(attrs)
        self.aspect_ratios = aspect_ratio or []
        self.modifier = modifier or (lambda x: x)
        self.filename = filename

    def is_initial(self, value):  # noqa
        """
        Return whether value is considered to be initial value.
        """
        return bool(value and getattr(value, "url", False))

    def format_value(self, value):
        """
        Return the file object if it has a defined url attribute.
        """
        return value if self.is_initial(value) else None

    def value_from_datadict(self, data, files, name):
        """
        Always receives the data as b64 image and convert
        to django.core.files.uploadedfile.InMemoryUploadedFile.
        """
        value = super().value_from_datadict(data, files, name)

        if not value:
            # skip blank values.
            return None

        # get content type and b64content.
        __, content_type, __, b64image = re.split(r"[,;:]", value)

        # apply the defined modifier to image bytes.
        stream = self.modifier(io.BytesIO(base64.b64decode(b64image)))
        stream.seek(0)

        return InMemoryUploadedFile(
            file=stream,
            content_type=content_type,
            field_name=name,
            name=(self.filename() if callable(self.filename) else self.filename)
            or f"{uuid.uuid4()}.jpg",
            size=stream.getbuffer().nbytes,
            charset=None,
        )

    def get_context(self, name, value, attrs):
        attrs = attrs or {}

        context = super().get_context(
            name,
            value,
            {
                **attrs,
                "class": " ".join(set(attrs.get("class", "").split() + ["hidden"])),
            },
        )

        context["widget"].update(
            {
                "is_initial": self.is_initial(value),
                "aspect_ratios": self.aspect_ratios,
                "input_text": self.input_text,
            }
        )

        return context

    @property
    def media(self):
        """
        ColorPickerInput's Media
        """
        return Media(
            js=["admin/cropper/cropper.min.js"],
            css={"all": ["admin/cropper/cropper.min.css"]},
        )
