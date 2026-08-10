"""Helper used by the exercises. You do not need to change this file."""
import os

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "..", "..", "..", "week1_setup", "data", "site_counts_small.csv")


def load_rows(path=DATA):
    """Return a list of [date, hour, direction, count] with hour/count as ints."""
    with open(path) as handle:
        lines = handle.readlines()[1:]
    rows = []
    for line in lines:
        parts = line.strip().split(",")
        rows.append([parts[0], int(parts[1]), parts[2], int(parts[3])])
    return rows
