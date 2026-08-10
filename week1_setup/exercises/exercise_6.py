"""
Exercise 6.

Run this script. Read the error. Fix it. Run it again.

When it is fixed, it prints the average count for eastbound traffic, to one
decimal place - or a sensible message if there is no eastbound traffic at all.

Hint: the data file has northbound rows and southbound rows. It has no
eastbound rows. Your fix should handle that case honestly, rather than
pretending it cannot happen. When there is no data, print exactly:

    ANSWER: no eastbound data
"""
from _shared import load_rows

rows = load_rows()

counts = []
for row in rows:
    if row[2] == "eastbound":
        counts.append(row[3])

average = sum(counts) / len(counts)

print("ANSWER:", round(average, 1))
