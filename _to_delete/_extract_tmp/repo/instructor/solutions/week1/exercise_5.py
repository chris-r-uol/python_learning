"""
Exercise 5.

Run it. Read the error. Fix it. Run it again.

What it should do: print how many hours had more than 1000 vehicles.

Hint: this one will not even start. Python is strict about indentation -
the lines inside a loop must all line up.
"""
from _shared import load_rows

rows = load_rows()

busy = 0
for row in rows:
    count = row[3]
    if count > 1000:
        busy = busy + 1

print("ANSWER:", busy)
