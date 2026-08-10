"""
Exercise 4.

Run it. Read the error. Fix it. Run it again.

What it should do: print how many rows are in the data file.

Hint: the file you want is in the data folder next to this one. Look at what
is actually there before you guess.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "..", "week1_setup", "data", "site_counts_small.csv")

with open(DATA) as handle:
    lines = handle.readlines()[1:]

print("ANSWER:", len(lines))
