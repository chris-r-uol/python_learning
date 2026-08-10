"""
The same task, done properly.

The difference is not skill. It is that someone asked what -1 meant.
"""

import csv
from collections import defaultdict

MISSING = -1.0

speeds_by_link = defaultdict(list)
missing_by_link = defaultdict(int)

with open("data/link_speeds.csv") as handle:
    reader = csv.DictReader(handle)
    for row in reader:
        speed = float(row["speed_kph"])
        if speed == MISSING:
            missing_by_link[row["link_id"]] += 1
            continue
        speeds_by_link[row["link_id"]].append(speed)

print("Average speed by link (missing observations excluded)")
print("-" * 58)
print("{:<10} {:>10} {:>8} {:>10} {:>12}".format(
    "Link", "Mean kph", "N used", "N missing", "% missing"))

for link in sorted(speeds_by_link):
    values = speeds_by_link[link]
    missing = missing_by_link[link]
    total = len(values) + missing
    print("{:<10} {:>10.1f} {:>8} {:>10} {:>11.0f}%".format(
        link, sum(values) / len(values), len(values), missing,
        100 * missing / total))

print()
print("Note: speed_kph = -1 is the sensor's code for 'no observation'.")
print("It is not a measured speed. Averaging it in drags every mean down.")
