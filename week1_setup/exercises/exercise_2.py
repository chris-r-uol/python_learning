"""
Exercise 2.

Run this script. Read the error. Fix it. Run it again.

When it is fixed, it prints the largest single hourly count in the file.

Hint: something in this script is text when it should be a number. Look at
what `split` gives you - it always gives you strings, even when the strings
look like numbers.
"""
import os

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "..", "data", "site_counts_small.csv")

with open(DATA) as handle:
    lines = handle.readlines()[1:]

busiest = 0
for line in lines:
    parts = line.strip().split(",")
    count = parts[3]
    if count > busiest:
        busiest = count

print("ANSWER:", busiest)
