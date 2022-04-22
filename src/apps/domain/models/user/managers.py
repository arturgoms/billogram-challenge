from django.db import models
from django.db.models.functions import Concat


class UserQuerySet(models.QuerySet):
    def with_name(self):
        """
        Annotate ``name`` to queryset.
        """
        return self.annotate(
            name=Concat("first_name", models.Value(" "), "last_name", output_field=models.CharField())
        )

    def include_discounts(self):
        from apps.domain.models import UserDiscount

        user_discount_qs = UserDiscount.objects \
            .select_related('discount')

        return self.prefetch_related(
            models.Prefetch('user_discount', queryset=user_discount_qs, to_attr='discount')
        )


class UserManager(models.Manager.from_queryset(UserQuerySet)):
    pass
