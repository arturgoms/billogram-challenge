import builtins
import functools

from collections.abc import Sequence

from commons.utils.collections import first_or_default


class Queryable(Sequence):
    def __init__(self, sequence):
        self._sequence = list(sequence)
        self._len = len(self._sequence)

    def __len__(self):
        return self._len

    def __getitem__(self, i):
        return self._sequence[i]

    def __iter__(self):
        return iter(self._sequence)

    def filter(self, func):
        """
        Return filtered items of the sequence for which function(item) is true.
        If function is None, return the items that are true.

        Parameters:
            func (callable, required): Function to test each item in sequence.

        Returns:
            Queryable
        """
        return Queryable(filter(func, self._sequence))

    def map(self, func):
        """
        Executes a specified function for each item in the sequence.

        Parameters:
            func (callable, required): Function to modify each item in sequence.

        Returns:
            Queryable
        """
        return Queryable(map(func, self._sequence))

    def reduce(self, func):
        """
        Apply the function of two arguments cumulatively to the items of the sequence,
        from left to right, so as to reduce the sequence to a single value.

        Parameters:
            func (callable, required): Function to apply to sequence items.

        Returns:
            Any
        """
        return functools.reduce(func, self._sequence)

    def any(self, func):
        """
        Return True if bool(x) is True for any x in the iterable.

        If the iterable is empty, return False.

        Parameters:
            func (callable, required): Function to test each value in sequence.

        Returns:
            bool
        """
        return builtins.any([func(item) for item in self._sequence])

    def all(self, func):
        """
        Return True if bool(x) is True for all values x in the iterable.

        If the iterable is empty, return True.

        Parameters:
            func (callable, required): Function to test each value in sequence.

        Returns:
            bool
        """
        return builtins.all([func(item) for item in self._sequence])

    def sort(self, key=None):
        """
        Return a new Queryable containing all items from the sequence in ascending order.

        A custom key function can be supplied to customize the sort order.

        Parameters:
            key (callable, required): Function to test each value in sequence.

        Returns:
            Queryable
        """
        return Queryable(sorted(self._sequence, key=key))

    def reverse(self):
        """
        Return a reversed Queryable over the values of the given sequence.

        Returns:
            Queryable
        """
        return Queryable(reversed(self.to_list()))

    def count(self, value):
        """
        Return number of elements that matches with defined value.

        Parameters:
            value (Any, required): Value to compare with each item in sequence.

        Returns:
            int
        """
        result = Queryable(
            self.filter(value if callable(value) else lambda x: x == value)
        )
        return len(result)

    def first(self):
        """
        Return the first sequence element.

        Returns:
            Any
        """
        return self.first_or_default()

    def first_or_default(self, func=lambda x: True, default=None):
        """
        Return the first sequence element that matches with given condition.

        Default value is returned if no elements match.

        Parameters:
            func (callable, optional): Function to test each sequence element.
            default (Any, optional): Default value to return if no elements match.

        Returns:
            Any
        """
        return first_or_default(self._sequence, func=func, default=default)

    def last(self):
        """
        Return the last sequence element.

        Returns:
            Any
        """
        return self.last_or_default()

    def last_or_default(self, func=lambda x: True, default=None):
        """
        Return the last sequence element that matches with given condition.

        Default value is returned if no elements match.

        Parameters:
            func (callable, optional): Function to test each sequence element.
            default (Any, optional): Default value to return if no elements match.

        Returns:
            Any
        """
        return first_or_default(self.reverse(), func=func, default=default)

    def to_list(self):
        """
        Return the sequence as a list.

        Returns:
            list
        """
        return list(self._sequence)

    def __repr__(self):
        if self._len > 10:
            head, tail = ", ".join(map(repr, self._sequence[:8])), repr(self.last())
            return f"{type(self).__name__}([{head}, ..., {tail}])"

        return f"{type(self).__name__}({self._sequence!r})"
