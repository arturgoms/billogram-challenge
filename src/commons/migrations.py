import os

from django.apps import apps
from django.db import router
from django.db.migrations.operations.base import Operation


class RunSQLFile(Operation):
    """
    Run some raw SQL file. A reverse SQL statement may be provided.

    Also accept a list of operations that represent the state change effected
    by this SQL change, in case it's custom column/table creation/deletion.
    """

    def __init__(self, path, reverse_path=None, hints=None, elidable=False):
        self.path = path
        self.reverse_path = reverse_path
        self.hints = hints or {}
        self.elidable = elidable

    def deconstruct(self):
        kwargs = {
            "path": self.path,
        }
        if self.reverse_path is not None:
            kwargs["reverse_path"] = self.reverse_path
        if self.hints:
            kwargs["hints"] = self.hints
        return (self.__class__.__qualname__, [], kwargs)

    @property
    def reversible(self):
        return self.reverse_path is not None

    def state_forwards(self, app_label, state):
        # RunPython objects have no state effect. To add some, combine this
        # with SeparateDatabaseAndState.
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        if router.allow_migrate(
            schema_editor.connection.alias, app_label, **self.hints
        ):
            self._run_sql(schema_editor, app_label, self.path)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        if self.reverse_path is None:
            raise NotImplementedError("You cannot reverse this operation")
        if router.allow_migrate(
            schema_editor.connection.alias, app_label, **self.hints
        ):
            self._run_sql(schema_editor, app_label, self.reverse_path)

    def describe(self):
        return "SQL File operation"

    def _run_sql(self, schema_editor, app_label, path):
        app = apps.get_app_config(app_label)
        abs_path = os.path.join(app.path, path)

        if not os.path.exists(abs_path):
            raise RuntimeError(f'File "{abs_path}" not found.')

        with open(abs_path, "r") as f:
            statements = schema_editor.connection.ops.prepare_sql_script(f.read())
            for statement in statements:
                schema_editor.execute(statement, params=None)
