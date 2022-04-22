from celery import states, exceptions


class BaseTask:
    def __init__(self, task):
        self._task = task

    def fail(self, message, params=None, exc=None):
        """
        Explicit fail task.
        """
        self._task.update_state(
            state=states.FAILURE,
            meta={
                "exc_type": (exc.__class__ if exc else exceptions.TaskError).__name__,
                "exc_message": message.format(**(params or {})),
            },
        )

        raise exceptions.Ignore()

    def execute(self, **kwargs):
        """
        Override this to perform the task action.
        """
        raise NotImplementedError()
