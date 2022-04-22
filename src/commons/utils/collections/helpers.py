from typing import Sequence


def chunks(seq, n):
    """
    Yield successive n-sized chunks from sequence.

    Parameters:
        seq (Sequence, required) - Sequence to be worked on.
        n (int, required) - Chunk size.

    Returns:
        generator
    """
    assert isinstance(seq, Sequence), "Parameter 'seq' must be a valid Sequence."

    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def first_or_default(seq, func=lambda x: True, default=None):
    """
    Returns the first or default value that matches with a condition.

    Parameters:
        seq (Sequence, required) - Sequence to be worked on.
        func (Function, optional) - Function that define query rule.
        default: (Any, optional) - Default value to be returned if no match was found.

    Return:
        Any
    """
    assert isinstance(seq, Sequence), "Parameter 'seq' must be a valid Sequence."

    try:
        value = next(filter(func, seq))

    except StopIteration:
        return default

    else:
        return value


def coalesce(seq, default=None):
    """
    Returns the first valid element in sequence or
    the default defined value.

    Parameters:
        seq (Sequence, required) - Sequence to be worked on.
        default: (Any, optional) - Default value to be returned if no match was found.

    Return:
        Any
    """
    assert isinstance(seq, Sequence), "Parameter 'seq' must be a valid Sequence."

    return first_or_default(seq, func=None, default=default)
