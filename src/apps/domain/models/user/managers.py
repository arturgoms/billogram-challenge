from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction

from apps.domain.models.user import emails


class UserManager(BaseUserManager):
    def make_random_password(
        self, length=10, allowed_chars="ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    ):
        """
        Generate a random password with the given length and given
        allowed_chars. The default value of allowed_chars does not have "I" or
        "O" or letters and digits that look similar -- just to avoid confusion.
        """
        return super().make_random_password(length=length, allowed_chars=allowed_chars)

    def set_roles(self, instance, roles):  # noqa
        """
        Set the given collections of roles to user.
        """
        from apps.domain.models import UserRole

        UserRole.objects.filter(user_id=instance.pk).delete()

        UserRole.objects.bulk_create(
            [UserRole(user_id=instance.pk, role=role) for role in roles]
        )

    def create_user(self, name, email, password=None, **kwargs):
        """
        Create an user.

        Args:
            name (str, required): User's name.
            email (str, required): User's email.
            password (str, optional): User's password.
            kwargs (dict, optional): Extra properties.
        """
        roles = kwargs.pop("roles", None)

        with transaction.atomic():
            instance = self.model(name=name, email=email, **kwargs)

            if password is not None:
                # set password if defined.
                instance.set_password(password)

            instance.save()

            if roles:
                # set roles if defined.
                self.set_roles(instance, roles)

        return instance

    def create_superuser(self, name, email, password=None, **kwargs):
        """
        Create an user with superuser status.

        Args:
            name (str, required): User's name.
            email (str, required): User's email.
            password (str, optional): User's password.
            kwargs (dict, optional): Extra properties.
        """
        # define superuser status.
        kwargs["is_superuser"] = True

        # create user.
        return self.create_user(name, email, password, **kwargs)

    def invite_user(self, name, email, roles=None, **kwargs):
        """
        Create a new user able to access administration panel.

        Args:
            name (str, required): User name.
            email (str, required): User email.
            roles (list<str>, optional): User roles.
        """
        kwargs.setdefault("status", self.model.Status.ACTIVE)

        # generate user password.
        password = self.make_random_password(length=8)

        with transaction.atomic():
            # create user with password.
            instance = self.create_user(
                name, email, password=password, roles=roles, **kwargs
            )

        # send welcome email
        emails.send_user_invite_email(instance, password=password)

        return instance

    def reset_password(self, instance):
        """
        Reset user's password.

        Args:
            instance (domain.User, required): Affected user instance.
        """
        # generate user password.
        password = self.make_random_password(length=8)

        # update user password.
        instance.set_password(password)
        instance.save()

        # send new password email.
        emails.send_new_password_email(instance, password=password)

        return instance

    def promote_to_superuser(self, instance):  # noqa
        """
        Promote user to superuser status.

        Args:
            instance (domain.User, required): Affected user instance.
        """
        instance.is_superuser = True
        instance.save()
        return instance

    def demote_from_superuser(self, instance):  # noqa
        """
        Promote user to superuser status.

        Args:
            instance (domain.User, required): Affected user instance.
        """
        instance.is_superuser = False
        instance.save()
        return instance
