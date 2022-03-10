"""Utility methods for creating PostgreSQL queries and parsing PostgreSQL query results."""

import re

from psycopg2.extras import NumericRange


def get_integral_numeric_range_bounds(nr: NumericRange) -> tuple[int, int]:
    """
    Separate the numeric range into its lower and upper bounds.

    :param nr: the numeric range of some PSQL data
    :return: the lower and upper bounds of the numeric range as Python ints
    :exception TypeError: invalid numeric range
    """
    p = re.compile(r"\[(\d+), (\d+)\)")
    if (m := p.match(str(nr))) is None:
        raise TypeError("Invalid numeric range")
    return int(m.group(1)), int(m.group(2))
