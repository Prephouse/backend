import re

from psycopg2.extras import NumericRange


def get_integral_numeric_range_bounds(nr: NumericRange) -> tuple[int, int]:
    p = re.compile(r"\[(\d+), (\d+)\)")
    m = p.match(str(nr))
    if m is None:
        raise TypeError("Invalid numeric range")
    return int(m.group(1)), int(m.group(2))
