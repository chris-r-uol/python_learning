"""
Exercise 5.

Run this script. Read the error. Fix it. Run it again.

When it is fixed, it prints how many hours had more than 1000 vehicles.

Hint: this one does not even start. Python is strict about indentation:
the lines inside a loop must all line up with each other.
"""
from _shared import load_rows

rows = load_rows()

busy = 0
for row in rows:
    count = row[3]
      if count > 1000:
        busy = busy + 1

print("ANSWER:", busy)
