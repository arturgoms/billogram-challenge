from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.http import Http404
from django.shortcuts import get_object_or_404

from commons.urls import querystring


class HierarchyModelAdmin(admin.ModelAdmin):
    parent_model = None
    parent_url_arg = None
    parent_model_field = None

    group_hidden = True

    change_list_template = "admin/hierarchy_admin/change_list.html"
    add_form_template = "admin/hierarchy_admin/change_form.html"
    change_form_template = "admin/hierarchy_admin/change_form.html"
    delete_confirmation_template = "admin/hierarchy_admin/delete_confirmation.html"
    object_history_template = "admin/hierarchy_admin/object_history.html"

    def _include_parent_url_arg(self, request, url):
        return querystring(
            url, includes={self.parent_url_arg: request.GET.get(self.parent_url_arg)}
        )

    def _get_parent_url_arg(self, request):
        return request.GET.get(self.parent_url_arg) or None

    def get_parent_object(self, request):
        _cached_prop = "_cached_parent_object"

        if not hasattr(self, _cached_prop):
            parent_url_arg = self._get_parent_url_arg(request)

            if not parent_url_arg:
                raise Http404()

            setattr(
                self,
                _cached_prop,
                get_object_or_404(self.parent_model, pk=parent_url_arg),
            )

        return getattr(self, _cached_prop)

    def get_changelist(self, request, **kwargs):
        include_parent_url_arg = getattr(self, "_include_parent_url_arg")

        class CustomChangeList(ChangeList):
            def url_for_result(self, result):
                """
                Ensures that response URL will be always provided.
                """
                result = super().url_for_result(result)
                return include_parent_url_arg(request, result)

        return CustomChangeList

    def response_add(self, request, obj, post_url_continue=None):
        response = super().response_add(request, obj, post_url_continue)
        response["Location"] = self._include_parent_url_arg(
            request, response["Location"]
        )
        return response

    def response_change(self, request, obj):
        response = super().response_change(request, obj)
        response["Location"] = self._include_parent_url_arg(
            request, response["Location"]
        )
        return response

    def response_delete(self, request, obj_display, obj_id):
        response = super().response_delete(request, obj_display, obj_id)
        response["Location"] = self._include_parent_url_arg(
            request, response["Location"]
        )
        return response

    def get_parent_context(self, request):
        return {
            "opts": getattr(self.parent_model, "_meta"),
            "object": self.get_parent_object(request),
            "url_arg": self.parent_url_arg,
        }

    def changelist_view(self, request, extra_context=None):
        return super().changelist_view(
            request,
            extra_context={
                **(extra_context or {}),
                "parent": self.get_parent_context(request),
            },
        )

    def change_view(self, request, object_id, form_url="", extra_context=None):
        return super().change_view(
            request,
            object_id=object_id,
            form_url=self._include_parent_url_arg(request, form_url),
            extra_context={
                **(extra_context or {}),
                "parent": self.get_parent_context(request),
            },
        )

    def add_view(self, request, form_url="", extra_context=None):
        return super().add_view(
            request,
            form_url=self._include_parent_url_arg(request, form_url),
            extra_context={
                **(extra_context or {}),
                "parent": self.get_parent_context(request),
            },
        )

    def delete_view(self, request, object_id, extra_context=None):
        return super().delete_view(
            request,
            object_id=object_id,
            extra_context={
                **(extra_context or {}),
                "parent": self.get_parent_context(request),
            },
        )

    def history_view(self, request, object_id, extra_context=None):
        return super().history_view(
            request,
            object_id=object_id,
            extra_context={
                **(extra_context or {}),
                "parent": self.get_parent_context(request),
            },
        )

    def get_changeform_initial_data(self, request):
        return {
            **super().get_changeform_initial_data(request),
            **{self.parent_model_field: self.get_parent_object(request)},
        }

    def get_queryset(self, request):
        lookup_field = self.parent_model_field or self.parent_url_arg

        return (
            super()
            .get_queryset(request)
            .filter(**{lookup_field: request.GET.get(self.parent_url_arg)})
        )

    # - Permissions

    def has_module_permission(self, request):
        """
        Grant access when the module has a correct parent url parameter.
        """
        return self.parent_url_arg in request.GET
