"""
Exercise 4.

Run this script. Read the error. Fix it. Run it again.

When it is fixed, it prints how many rows the data file contains.

Hint: the file you want is in the data folder next to this one. Look at what
that folder actually contains before you guess at the fix.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "site_counts.csv")

with open(DATA) as handle:
    lines = handle.readlines()[1:]

print("ANSWER:", len(lines))
