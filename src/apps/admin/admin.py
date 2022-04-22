import inspect

from django.contrib import admin

from commons.loaders import autodiscovery

# IMPORTANT: This piece of code is necessary to auto admin discovery by
# automatically loading all admin models into this file.
autodiscovery(
    "apps.admin",
    condition=lambda x: inspect.isclass(x) and issubclass(x, admin.ModelAdmin),
    resolver=lambda x: f"{x}.admin",
    _globals=globals(),
)
