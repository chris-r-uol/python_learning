"""Helper used by the exercises. You do not need to change this file.

It is worth reading. Several exercises call `load_rows()`. Knowing what it
returns tells you what those exercises are working with.
"""
import os

# Build the path to the data file from THIS file's location, so the
# exercises work from any folder.
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "..", "data", "site_counts_small.csv")


def load_rows(path=DATA):
    """Return the data as a list of rows.

    Each row is itself a list of four values, in this order:

        [date (text), hour (number), direction (text), count (number)]

    So for any row, position 0 is the date, 1 is the hour, 2 is the
    direction, and 3 is the count - counting from zero, as always.
    """
    with open(path) as handle:
        # Read every line, then drop the header row with [1:].
        lines = handle.readlines()[1:]

    rows = []
    for line in lines:
        # Split the line at the commas, then convert the two values we want
        # as numbers - hour and count - out of text and into integers.
        parts = line.strip().split(",")
        rows.append([parts[0], int(parts[1]), parts[2], int(parts[3])])
    return rows
