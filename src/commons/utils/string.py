import re
import unicodedata


def pluralize(singular, plural, number):
    """
    Returns a pluralized string based on a number.

    Parameters:
        singular (str, required): Singular string to be returned.
        plural (str, required): Plural string to be returned.
        number (int, required): Number to compare.

    Returns:
         str
    """
    number = abs(number)
    return plural if number == 0 or number > 1 else singular


def digits(s):
    """
    Returns only digits from string.

    Parameters:
         s (str, required): String to extract digits.

    Returns:
        str
    """
    return str.join("", filter(lambda x: x.isdigit(), s))


def strip_accents(s):
    """
    Strip all accents from string.

    Parameters:
        s (str, required): String to strip accents.

    Returns:
        str
    """
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("utf-8")


def match(pattern, s):
    """
    Checks if a given string matches with provided pattern.

    Can Use * character to represent (.+) pattern.

    Parameters:
        pattern (str, required): Pattern to match.
        s (str, required): Value to match.

    Returns:
        bool
    """
    pattern = pattern.replace("*", "(.+)").lstrip("^").rstrip("$")

    return bool(re.match(rf"^{pattern}$", s))
