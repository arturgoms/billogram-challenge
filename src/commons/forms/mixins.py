class ContextFormMixin:
    """
    Provides the ability to receive extra context
    information to process the form.
    """

    def __init__(self, *args, **kwargs):
        """
        Remove context from kwargs and set to instance if exists.
        """
        self.context = kwargs.pop("context", {})
        super().__init__(*args, **kwargs)
