from django.contrib import admin, messages
from django.contrib.auth.models import Group
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from commons.djutils.forms.shortcuts import get_form

from apps.admin.user.forms.change_roles_form import ChangeRolesAdminForm
from apps.admin.user.forms.invite_form import UserInviteAdminForm
from apps.domain import models
from commons.admin import decorators
from commons.admin.mixins import SmartAdminMixin
from commons.admin.permissions.mixins import PermissionsAdminMixin
from commons.admin.shortcuts import admin_url
from commons.forms.fieldsets import Fieldsets

if admin.site.is_registered(Group):
    # Remove default django permissions admin
    admin.site.unregister(Group)


@admin.register(models.User)
class UserAdmin(PermissionsAdminMixin, SmartAdminMixin, admin.ModelAdmin):
    list_display = ["name", "email_field", "last_login", "active_field"]
    list_filter = ["status", "last_login"]

    group = _("Administration")

    search_fields = ["name", "email"]

    fieldsets = (
        (None, {"fields": ["name", "is_superuser"]}),
        (_("Contact"), {"fields": ["email_field"]}),
        (_("Status"), {"fields": ["date_joined", "last_login", "active_field"]}),
    )

    object_tools = {
        "change": [
            {
                "title": _("Block"),
                "url": lambda opts, obj: admin_url("block", opts=opts, args=[obj.pk]),
                "permission": lambda request, obj: obj.pk != request.user.pk
                and obj.status == models.User.Status.ACTIVE,
                "attrs": {"class": "deletelink"},
            },
            {
                "title": _("Unblock"),
                "url": lambda opts, obj: admin_url("unblock", opts=opts, args=[obj.pk]),
                "permission": lambda request, obj: obj.status
                == models.User.Status.BLOCKED,
            },
            {
                "title": _("Promote"),
                "url": lambda opts, obj: admin_url("promote", opts=opts, args=[obj.pk]),
                "permission": lambda request, obj: request.user.is_superuser is True
                and obj.pk != request.user.pk
                and obj.is_superuser is False,
            },
            {
                "title": _("Demote"),
                "url": lambda opts, obj: admin_url("demote", opts=opts, args=[obj.pk]),
                "permission": lambda request, obj: request.user.is_superuser is True
                and obj.pk != request.user.pk
                and obj.is_superuser is True,
            },
            {
                "title": _("Change Roles"),
                "url": lambda opts, obj: admin_url(
                    "change-role", opts=opts, args=[obj.pk]
                ),
                "permission": lambda request, obj: request.user.is_superuser is True
                and obj.pk != request.user.pk,
            },
            {
                "title": _("Reset Password"),
                "url": lambda opts, obj: admin_url(
                    "reset-password", opts=opts, args=[obj.pk]
                ),
                "permission": lambda request, obj: request.user.is_superuser is True
                and obj.pk != request.user.pk,
            },
        ],
        "changelist": [
            {
                "title": _("Invite %(verbose_name)s"),
                "url": lambda opts, obj: admin_url("invite", opts=opts),
                "attrs": {"class": "addlink"},
            }
        ],
    }

    # Fields

    @decorators.admin_field(_("Email"))
    def email_field(self, obj):
        """
        Returns email as a link.
        """
        return mark_safe(f'<a href="mailto:{obj.email}">{obj.email}</a>')

    @decorators.admin_field(_("Active"), boolean=True)
    def active_field(self, obj):
        """
        Returns whether the user is active.
        """
        return obj.status == models.User.Status.ACTIVE

    # Views

    @decorators.admin_view(detail=False)
    def invite_view(self, request):
        """
        Invite a new user to administration panel.
        """
        next_url = request.GET.get("next")
        template_name = (
            f"admin/{self.opts.app_label}/{self.opts.model_name}/invite_form.html"
        )

        form = get_form(request, UserInviteAdminForm, context={"request": request})

        if request.method == "POST" and form.is_valid():
            # invite user.
            instance = models.User.objects.invite_user(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                roles=form.cleaned_data["roles"],
            )

            change_message = self.construct_change_message(
                request, form, None, add=True
            )
            self.log_addition(request, instance, change_message)
            return self.response_add(request, instance, next_url)

        return TemplateResponse(
            request,
            template=template_name,
            context={
                **self.admin_site.each_context(request),
                "title": _("Invite %(verbose_name)s")
                % {"verbose_name": self.opts.verbose_name},
                "media": self.media,
                "form": form,
                "fieldsets": Fieldsets(
                    form,
                    fieldsets=(
                        (None, {"fields": ["name", "email"]}),
                        (_("Permissions"), {"fields": ["roles"]}),
                    ),
                ),
                "opts": self.opts,
                "preserved_filters": self.get_preserved_filters(request),
            },
        )

    @decorators.admin_view(detail=True)
    def change_role_view(self, request, object_id):
        """
        Change role for user.
        """
        template_name = (
            f"admin/{self.opts.app_label}/{self.opts.model_name}/change_role_form.html"
        )
        instance = self.get_object(request, object_id)

        form = get_form(
            request,
            ChangeRolesAdminForm,
            initial={"roles": instance.roles},
            context={"request": request},
        )

        if request.method == "POST" and form.is_valid():
            # change role for user.
            models.User.objects.set_roles(instance, form.cleaned_data["roles"])

            change_message = self.construct_change_message(
                request, form, None, add=False
            )
            self.log_change(request, instance, change_message)

            change_url = admin_url("change", self.opts, args=[instance.pk])
            return self.redirect(
                request,
                next_url=change_url,
                message=_("The {name} “{obj}” was changed successfully."),
                params={
                    "name": self.opts.verbose_name,
                    "obj": format_html('<a href="{}">{}</a>', change_url, instance),
                },
                level=messages.SUCCESS,
            )

        return TemplateResponse(
            request,
            template=template_name,
            context={
                **self.admin_site.each_context(request),
                "title": _("Change Role for %(verbose_name)s")
                % {"verbose_name": self.opts.verbose_name},
                "media": self.media,
                "form": form,
                "fieldsets": Fieldsets(
                    form, fieldsets=((_("Permissions"), {"fields": ["roles"]}),)
                ),
                "opts": self.opts,
                "preserved_filters": self.get_preserved_filters(request),
            },
        )

    @decorators.admin_view(detail=True)
    def block_view(self, request, object_id):
        """
        Chance the user status to blocked.
        """
        next_url = request.GET.get("next") or admin_url(
            "change", self.opts, args=[object_id]
        )
        template_name = (
            f"admin/{self.opts.app_label}/{self.opts.model_name}/block_form.html"
        )
        obj = self.get_object(request, object_id)

        if request.method == "POST":
            obj.status = models.User.Status.BLOCKED
            obj.save()

            self.message_user(
                request,
                format_html(
                    _('The {name} "{obj}" was blocked successfully.'),
                    name=self.opts.verbose_name,
                    obj=format_html(
                        '<a href="{url}">{text}</a>',
                        url=admin_url("change", self.opts, args=[obj.pk]),
                        text=str(obj),
                    ),
                ),
                level=messages.SUCCESS,
            )

            self.log_change(request, obj, _("Blocked."))

            return HttpResponseRedirect(next_url)

        return TemplateResponse(
            request,
            template=template_name,
            context={
                **self.admin_site.each_context(request),
                "title": _("Are you sure?"),
                "media": self.media,
                "opts": self.opts,
                "original": obj,
                "object": obj,
                "preserved_filters": self.get_preserved_filters(request),
            },
        )

    @decorators.admin_view(detail=True)
    def unblock_view(self, request, object_id):
        """
        Chance the user status to active.
        """
        next_url = request.GET.get("next") or admin_url(
            "change", self.opts, args=[object_id]
        )
        obj = self.get_object(request, object_id)
        obj.status = models.User.Status.ACTIVE
        obj.save()

        self.message_user(
            request,
            format_html(
                _('The {name} "{obj}" was unblocked successfully.'),
                name=self.opts.verbose_name,
                obj=format_html(
                    '<a href="{url}">{text}</a>',
                    url=admin_url("change", self.opts, args=[obj.pk]),
                    text=str(obj),
                ),
            ),
            level=messages.SUCCESS,
        )

        self.log_change(request, obj, _("Unblocked."))

        return HttpResponseRedirect(next_url)

    @decorators.admin_view(detail=True)
    def promote_view(self, request, object_id):
        """
        Promote user to superuser
        """
        template_name = (
            f"admin/{self.opts.app_label}/{self.opts.model_name}/promote_form.html"
        )
        instance = self.get_object(request, object_id)

        if request.method == "POST":
            # promote to superuser.
            instance = self.model.objects.promote_to_superuser(instance)

            form = modelform_factory(models.User, fields=["is_superuser"])(
                {"is_superuser": instance.is_superuser}
            )
            change_message = self.construct_change_message(
                request, form, None, add=False
            )
            self.log_change(request, instance, change_message)

            change_url = admin_url("change", self.opts, args=[instance.pk])
            return self.redirect(
                request,
                next_url=change_url,
                message=_("The {name} “{obj}” was changed successfully."),
                params={
                    "name": self.opts.verbose_name,
                    "obj": format_html('<a href="{}">{}</a>', change_url, instance),
                },
                level=messages.SUCCESS,
            )

        return TemplateResponse(
            request,
            template=template_name,
            context={
                **self.admin_site.each_context(request),
                "title": _("Are you sure?"),
                "media": self.media,
                "opts": self.opts,
                "original": instance,
                "object": instance,
                "preserved_filters": self.get_preserved_filters(request),
            },
        )

    @decorators.admin_view(detail=True)
    def demote_view(self, request, object_id):
        """
        Demote user to superuser
        """
        template_name = (
            f"admin/{self.opts.app_label}/{self.opts.model_name}/demote_form.html"
        )
        instance = self.get_object(request, object_id)

        if request.method == "POST":
            # promote to superuser.
            instance = self.model.objects.demote_from_superuser(instance)

            form = modelform_factory(models.User, fields=["is_superuser"])(
                {"is_superuser": instance.is_superuser}
            )
            change_message = self.construct_change_message(
                request, form, None, add=False
            )
            self.log_change(request, instance, change_message)

            change_url = admin_url("change", self.opts, args=[instance.pk])
            return self.redirect(
                request,
                next_url=change_url,
                message=_("The {name} “{obj}” was changed successfully."),
                params={
                    "name": self.opts.verbose_name,
                    "obj": format_html('<a href="{}">{}</a>', change_url, instance),
                },
                level=messages.SUCCESS,
            )

        return TemplateResponse(
            request,
            template=template_name,
            context={
                **self.admin_site.each_context(request),
                "title": _("Are you sure?"),
                "media": self.media,
                "opts": self.opts,
                "original": instance,
                "object": instance,
                "preserved_filters": self.get_preserved_filters(request),
            },
        )

    @decorators.admin_view(detail=True)
    def reset_password_view(self, request, object_id):
        """
        Reset user password.
        """
        template_name = f"admin/{self.opts.app_label}/{self.opts.model_name}/reset_password_form.html"
        instance = self.get_object(request, object_id)

        if request.method == "POST":
            # reset user password.
            instance = self.model.objects.reset_password(instance)

            form = modelform_factory(models.User, fields=["password"])(
                {"password": instance.password}
            )
            change_message = self.construct_change_message(
                request, form, None, add=False
            )
            self.log_change(request, instance, change_message)

            change_url = admin_url("change", self.opts, args=[instance.pk])
            return self.redirect(
                request,
                next_url=change_url,
                message=_("The {name} “{obj}” was changed successfully."),
                params={
                    "name": self.opts.verbose_name,
                    "obj": format_html('<a href="{}">{}</a>', change_url, instance),
                },
                level=messages.SUCCESS,
            )

        return TemplateResponse(
            request,
            template=template_name,
            context={
                **self.admin_site.each_context(request),
                "title": _("Are you sure?"),
                "media": self.media,
                "opts": self.opts,
                "original": instance,
                "object": instance,
                "preserved_filters": self.get_preserved_filters(request),
            },
        )

    # Permissions

    def has_add_permission(self, request):
        """
        Disable django default create view.
        """
        return False

    def has_change_permission(self, request, obj=None):
        return False
