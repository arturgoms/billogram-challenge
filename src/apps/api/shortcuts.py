from apps.api.permissions import UserRoleEnum
from apps.domain import models
from commons import jwt


def generate_user_token(instance, exp=None):
    """
    Generate the correct token for a panel_user instance.

    WARNING: This method was created just to development and test purpose,
        never call this in a production environment.
    """
    if isinstance(instance, models.User):
        role = UserRoleEnum.USER.value

    elif isinstance(instance, models.Brand):
        role = UserRoleEnum.BRAND.value

    else:
        raise TypeError(
            "Instance must be 'domain.models.Brand' or 'domain.models.User' type."
        )

    return jwt.Jwt.generate(key=jwt.JWT_KEY, exp=exp, id=str(instance.pk), role=role)
