"""
Exercise 6.

Run it. Read the error. Fix it. Run it again.

What it should do: print the average count for eastbound traffic, to 1 decimal
place - or a sensible message if there is no eastbound traffic at all.

Hint: this file has northbound and southbound rows. It has no eastbound rows.
Your fix should handle that case rather than pretending it cannot happen.
Print exactly: ANSWER: no eastbound data
"""
from _shared import load_rows

rows = load_rows()

counts = []
for row in rows:
    if row[2] == "eastbound":
        counts.append(row[3])

if len(counts) == 0:
    print("ANSWER: no eastbound data")
else:
    average = sum(counts) / len(counts)
    print("ANSWER:", round(average, 1))
