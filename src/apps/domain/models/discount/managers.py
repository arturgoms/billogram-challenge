from django.db import models
from commons.models.subquery import SubqueryCount


class DiscountQuerySet(models.QuerySet):

    def with_used(self):
        from apps.domain.models import UserDiscount

        balance_qs = UserDiscount.objects.filter(discount_id=models.OuterRef('id'))
        return self.annotate(used=SubqueryCount(balance_qs))


class DiscountManager(models.Manager.from_queryset(DiscountQuerySet)):
    pass
