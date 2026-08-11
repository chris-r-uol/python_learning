"""
The same task, done properly.

The difference between this file and lazy_analysis.py is not programming
skill. It is that someone asked what -1 meant.
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
print(f"{'Link':<10} {'Mean kph':>10} {'N used':>8} "
      f"{'N missing':>10} {'% missing':>12}")

for link in sorted(speeds_by_link):
    values = speeds_by_link[link]
    missing = missing_by_link[link]
    total = len(values) + missing
    mean_speed = sum(values) / len(values)
    print(f"{link:<10} {mean_speed:>10.1f} {len(values):>8} "
          f"{missing:>10} {100 * missing / total:>11.0f}%")

print()
print("Note: speed_kph = -1 is the sensor's code for 'no observation'.")
print("It is not a measured speed. Averaging it in drags every mean down.")
