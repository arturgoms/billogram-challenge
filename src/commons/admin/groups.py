from django.urls import reverse, NoReverseMatch
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _


def resolve_registered_groups(request, site):
    default_group_label = _("Default")
    groups = []
    registry = getattr(site, "_registry")

    _groups = {}

    for model, model_admin in registry.items():
        group_name = str(getattr(model_admin, "group", default_group_label))
        _groups[group_name] = (_groups.get(group_name) or []) + [(model, model_admin)]

    for group_name, items in _groups.items():
        models = []

        for model, model_admin in items:
            opts = getattr(model, "_meta")

            # Ignore hidden admin.
            if getattr(model_admin, "group_hidden", False) is True:
                continue

            if not model_admin.has_module_permission(request):
                continue

            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if not any(perms.values()):
                continue

            model_dict = {
                "name": capfirst(opts.verbose_name_plural),
                "object_name": opts.object_name,
                "perms": perms,
                "admin_url": None,
                "add_url": None,
            }

            info = (opts.app_label, opts.model_name)

            if perms.get("change") or perms.get("view"):
                model_dict["view_only"] = not perms.get("change")
                try:
                    model_dict["admin_url"] = reverse("admin:%s_%s_changelist" % info)
                except NoReverseMatch:
                    pass

            if perms.get("add"):
                try:
                    model_dict["add_url"] = reverse("admin:%s_%s_add" % info)
                except NoReverseMatch:
                    pass

            models.append(model_dict)

        if not models:
            continue

        groups.append({"label": group_name, "models": models})

    # Sort the apps alphabetically.
    return sorted(
        groups,
        key=lambda x: x["label"].lower()
        if not x["label"].lower() == default_group_label.lower()
        else "zzz",
    )
