from django.utils import translation


# pylint: disable=invalid-name
class translator:
    """
    Give the ability to change current language
    in a context block.
    """

    def __init__(self, language):
        self.language = language
        self.old_language = translation.get_language()

    def __enter__(self):
        """
        Activate scoped language.
        """
        translation.activate(self.language)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Activate old language back.
        """
        translation.activate(self.old_language)
