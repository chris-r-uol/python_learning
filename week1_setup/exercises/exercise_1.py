"""
Exercise 1.

Run this script. Read the error. Fix it. Run it again.

When it is fixed, it prints the total northbound traffic across both days.
"""
from _shared import load_rows

rows = load_rows()

total = 0
for row in rows:
    direction = row[2]
    if direction == "northbound":
        total = total + row[3]

print("ANSWER:", totl)
