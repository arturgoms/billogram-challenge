from django.db import models
from commons.models.subquery import SubqueryCount


class UserDiscountQuerySet(models.QuerySet):
    pass


class UserDiscountManager(models.Manager.from_queryset(UserDiscountQuerySet)):
    pass
