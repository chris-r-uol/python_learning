"""
THE LAZY PROMPT.

This is what came back from the request:

    "analyse this traffic data and tell me the average speed on each link"

It runs. It has a docstring. It prints a neat, professional-looking table with
one decimal place.

It is wrong.

Do not fix this file. It is kept broken on purpose, so that we can come back
to it.
"""

import csv
from collections import defaultdict

speeds_by_link = defaultdict(list)

with open("data/link_speeds.csv") as handle:
    reader = csv.DictReader(handle)
    for row in reader:
        speeds_by_link[row["link_id"]].append(float(row["speed_kph"]))

print("Average speed by link")
print("-" * 34)
print(f"{'Link':<10} {'Mean kph':>10} {'N obs':>10}")
for link in sorted(speeds_by_link):
    values = speeds_by_link[link]
    print(f"{link:<10} {sum(values) / len(values):>10.1f} {len(values):>10}")
