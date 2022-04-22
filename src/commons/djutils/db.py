from collections import OrderedDict
from typing import Optional, Union, Any, Tuple

from django.db import connections, DEFAULT_DB_ALIAS


class DatabaseResult:
    __slots__ = ("columns", "result")

    def __init__(self, columns, result):
        self.columns = columns
        self.result = result

    def as_dict(self):
        """
        Map the result into a dictionary.

        Returns:
            list
        """
        return list(map(lambda row: OrderedDict(zip(self.columns, row)), self.result))

    def __iter__(self):
        return iter(self.result)

    def __len__(self):
        return len(self.result)

    def __repr__(self):
        return f"<{type(self).__name__}: {len(self.result)!r} Results>"


class Database:
    def __init__(self, using=None):
        self.using: str = using or DEFAULT_DB_ALIAS

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.using}>"

    @property
    def connection(self):
        """
        Returns database connection to being used to execute commands.

        Returns:
            django.db.ConnectionHandler
        """
        return connections[self.using]

    def using(self, using: str) -> "Database":  # pylint: disable=E0202
        """
        Returns a new database instance to execute query using a different database.

        Args:
            using (str, required): Database to use.

        Returns:
            Database
        """
        cls = type(self)
        return cls(using)

    def select(self, query: str, params: Optional[dict] = None) -> "DatabaseResult":
        """
        Execute SQL select query on database.

        Args:
            query (str, required): Query to be executed.
            params (dict, optional): Parameters to embed into the query.

        Returns:
            DatabaseResult
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query.format(**(params or {})))
            result = cursor.fetchall()
            columns = list(map(lambda x: x[0], cursor.description))

            return DatabaseResult(columns=columns, result=result)

    def select_one(
        self, query: str, params: Optional[dict] = None
    ) -> Union[Any, Tuple]:
        """
        Execute SQL query on database that returns a single value.

        Args:
            query (str, required): Query to be executed.
            params (dict, optional): Parameters to embed into the query.

        Returns:
            Any
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query.format(**(params or {})))
            data = cursor.fetchone()
            return data[0] if len(data) == 1 else data

    def execute(self, query: str, params: Optional[dict] = None) -> None:
        """
        Executes any query on a database and it does not return anything.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query.format(**(params or {})))
