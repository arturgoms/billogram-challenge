import uuid


class AuthenticatedUser:
    """
    Object to represent an authenticated user.
    """

    _db_representation_error = (
        "Django does not provide a DB representation for '{name}'."
    )

    USERNAME_FIELD = "pk"

    is_superuser = False
    is_staff = False
    is_anonymous = False
    is_authenticated = True
    is_active = True

    def __init__(self, pk, **kwargs):
        self.pk = self.id = uuid.UUID(pk)

        for key, val in kwargs.items():
            setattr(self, key, val)

    def __repr__(self):
        return f"<{type(self).__name__}: {self.pk}>"

    def get_username(self):
        return getattr(self, AuthenticatedUser.USERNAME_FIELD, None)

    def save(self):
        raise NotImplementedError(
            self._db_representation_error.format(name=type(self).__name__)
        )

    def delete(self):
        raise NotImplementedError(
            self._db_representation_error.format(name=type(self).__name__)
        )

    def set_password(self, raw_password):
        raise NotImplementedError(
            self._db_representation_error.format(name=type(self).__name__)
        )

    def check_password(self, raw_password):
        raise NotImplementedError(
            self._db_representation_error.format(name=type(self).__name__)
        )
