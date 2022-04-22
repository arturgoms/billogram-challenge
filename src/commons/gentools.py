import builtins
import itertools


def gen(seq):
    """
    Converts any sequence into a generator.
    """
    return (x for x in seq)


def cycle(seq):
    """
    Returns generator for a cycle statement.
    """
    return gen(itertools.cycle(seq))


def map(func, seq):  # noqa
    """
    Returns generator for a mapped sequence.
    """
    return gen(builtins.map(func, seq))
