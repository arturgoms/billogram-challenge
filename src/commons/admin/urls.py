from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _

from commons.admin.utils import admin_url_pattern

admin.site.site_title = getattr(settings, "ADMIN_SITE_TITLE", _("Site Administration"))
admin.site.site_header = getattr(
    settings, "ADMIN_SITE_HEADER", _("Site Administration")
)
admin.site.index_title = getattr(settings, "ADMIN_SITE_INDEX_TITLE", _("Home"))
admin.site.site_url = getattr(settings, "ADMIN_SITE_URL", None)


urlpatterns = [
    path(admin_url_pattern(), admin.site.urls),
]
