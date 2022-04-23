from django.db import models


class BrandQuerySet(models.QuerySet):
    def include_discounts(self):
        return self.prefetch_related("brand_discount")


class BrandManager(models.Manager.from_queryset(BrandQuerySet)):
    pass
