"""
Exercise 3.

Run it. Read the error. Fix it. Run it again.

What it should do: print how many rows are southbound.

Hint: the file has four columns. Count them starting from zero.
"""
from _shared import load_rows

rows = load_rows()

southbound = 0
for row in rows:
    if row[4] == "southbound":
        southbound = southbound + 1

print("ANSWER:", southbound)
