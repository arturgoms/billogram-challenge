# pylint: disable=invalid-name
class switch:
    def __init__(self, value):
        self._value = value
        self._cases = []

    def case(self, when, then):
        """
        Add a case expression into switch cases.

        Args:
            when (Any, required): Condition or expression to be solved to this case.
            then (Any, required): Value to be returned after test this condition.

        Returns:
            switch
        """
        self._cases.append((when, then))
        return self

    def value(self, default=None):
        """
        Returns the first result that matches a given condition.

        Args:
            default (Any, optional): Value to be returned if no case matches.

        Returns:
            Any
        """
        try:
            return next(
                (
                    then
                    for when, then in self._cases
                    if when == self._value or (callable(when) and when(self._value))
                )
            )

        except StopIteration:
            return default
