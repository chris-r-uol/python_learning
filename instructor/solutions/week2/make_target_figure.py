"""
Produces the week 2 task 2 target figure that students must reproduce.

    python instructor/solutions/week2/make_target_figure.py

Deliberately different from the worked example: it splits weekday from weekend
rather than northbound from southbound, and plots two-way total. So students
cannot copy the worked example - they have to work out that they need the day
of the week, which is not a column in the file.

That is the intended difficulty. The date is there; the weekday is not. They
have to derive it.
"""

import csv
import os
from datetime import date

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
DATA = os.path.join(ROOT, "week2_programming", "data", "traffic_counts.csv")
OUTPUT = os.path.join(ROOT, "week2_programming", "drills", "target_figure.png")

BLUE = "#2a78d6"
ORANGE = "#eb6834"


def load():
    rows = []
    with open(DATA) as handle:
        reader = csv.reader(handle)
        next(reader)
        for row in reader:
            year, month, day = (int(part) for part in row[0].split("-"))
            rows.append({
                "weekend": date(year, month, day).weekday() >= 5,
                "hour": int(row[1]),
                "count": int(row[3]),
            })
    return rows


def two_way_profile(rows, weekend):
    totals = [0] * 24
    days = [0] * 24
    for row in rows:
        if row["weekend"] == weekend:
            totals[row["hour"]] += row["count"]
            days[row["hour"]] += 1
    # Two directions per day, so dividing by the number of rows gives the mean
    # per direction; multiply by two for the two-way total.
    return [2 * totals[hour] / days[hour] if days[hour] else 0.0
            for hour in range(24)]


def main():
    rows = load()
    weekday = two_way_profile(rows, weekend=False)
    weekend = two_way_profile(rows, weekend=True)

    figure, axes = plt.subplots(figsize=(9, 5))
    axes.plot(range(24), weekday, color=BLUE, linewidth=2, label="Weekday")
    axes.plot(range(24), weekend, color=ORANGE, linewidth=2, label="Weekend")

    axes.set_xlabel("Hour of day")
    axes.set_ylabel("Average two-way flow (vehicles per hour)")
    axes.set_title("Weekday and weekend demand profiles\n"
                   "Count site A34/012, 2-15 March 2026")
    axes.set_xticks(range(0, 24, 2))
    axes.set_xlim(0, 23)
    axes.set_ylim(0, max(weekday) * 1.15)
    axes.grid(axis="y", alpha=0.25)
    axes.spines["top"].set_visible(False)
    axes.spines["right"].set_visible(False)
    axes.legend(frameon=False)

    figure.tight_layout()
    figure.savefig(OUTPUT, dpi=150)
    print("wrote", os.path.relpath(OUTPUT, ROOT))
    print()
    print("Marking key - values students should land within ~1% of:")
    print("  weekday peak hour:  {0:02d}:00 at {1:.0f} veh/h".format(
        weekday.index(max(weekday)), max(weekday)))
    print("  weekend peak hour:  {0:02d}:00 at {1:.0f} veh/h".format(
        weekend.index(max(weekend)), max(weekend)))
    print(f"  weekday 08:00:      {weekday[8]:.0f} veh/h")
    print(f"  weekend 08:00:      {weekend[8]:.0f} veh/h")


if __name__ == "__main__":
    main()
