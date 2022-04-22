from django.utils import timezone as django_timezone


# pylint: disable=invalid-name
class timezone:
    """
    Give the ability to change current timezone in a context block.
    """

    def __init__(self, tz):
        self.tz = tz
        self.current_tz = django_timezone.get_current_timezone()

    def __enter__(self):
        """
        Activate scoped timezone.
        """
        django_timezone.activate(self.tz)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Revert timezone settings to previous configuration.
        """
        django_timezone.activate(self.current_tz)
