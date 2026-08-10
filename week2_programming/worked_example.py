"""
Week 2 worked example - built live, in six stages.

The question: at this count site, what does an average day look like, and when
is the peak?

Run it:

    python worked_example.py

Each STAGE below is a step we take together in the session. The stages build
on each other, but each one produces output of its own - you can comment out
the later ones and the earlier ones still run.

Stages 1-3 solve the problem with loops, deliberately spelled out. Stage 4
packages the repeated work into a function. Stage 5 solves the same problem
again in NumPy - the contrast with stage 3 is the point. Stage 6 is the figure.
"""

import csv

import matplotlib
matplotlib.use("Agg")            # write figures to file rather than a window
import matplotlib.pyplot as plt
import numpy as np

DATA_FILE = "data/traffic_counts.csv"
DIRECTION = "northbound"

# Two-series colours, checked for colourblind separation.
BLUE = "#2a78d6"
ORANGE = "#eb6834"


# ===========================================================================
# STAGE 1 - Store. Get the data into variables.
# ===========================================================================
#
# New here: variables, strings, integers, lists.

dates = []
hours = []
directions = []
counts = []

# `csv.reader` does the same job as the `split(",")` we used in week 1 - it
# cuts each line at the commas - but it is the standard tool, and it handles
# awkward cases (such as commas inside quoted text) that `split` does not.
# `next(reader)` reads one row and moves past it; here, that removes the header.
with open(DATA_FILE) as handle:
    reader = csv.reader(handle)
    next(reader)                       # skip the header row
    for row in reader:
        dates.append(row[0])
        hours.append(int(row[1]))      # text -> number
        directions.append(row[2])
        counts.append(int(row[3]))

print("STAGE 1")
print("  rows read:      ", len(counts))
print("  first 5 counts: ", counts[:5])
print("  biggest count:  ", max(counts))
print()


# ===========================================================================
# STAGE 2 - Decide. Keep only the rows we want.
# ===========================================================================
#
# New here: `if`, and comparison.
#
# Note we build a SECOND pair of lists rather than modifying the first. Deleting
# from a list while looping over it is a classic way to get a wrong answer with
# no error message.

chosen_hours = []
chosen_counts = []

for index in range(len(counts)):
    if directions[index] == DIRECTION:
        chosen_hours.append(hours[index])
        chosen_counts.append(counts[index])

print("STAGE 2")
print("  direction:      ", DIRECTION)
print("  rows kept:      ", len(chosen_counts))
print()


# ===========================================================================
# STAGE 3 - Repeat. Average the count in each hour of the day.
# ===========================================================================
#
# New here: nested loops, accumulating a total, integer division.
#
# This is deliberately long-winded. You need to see the machinery once before
# we hide it.

average_by_hour = []

for hour_of_day in range(24):
    total = 0
    number_of_days = 0

    for index in range(len(chosen_counts)):
        if chosen_hours[index] == hour_of_day:
            total = total + chosen_counts[index]
            number_of_days = number_of_days + 1

    if number_of_days == 0:
        average_by_hour.append(0.0)          # never divide by zero
    else:
        average_by_hour.append(total / number_of_days)

print("STAGE 3")
for hour_of_day in range(24):
    bar = "#" * int(average_by_hour[hour_of_day] / 40)
    print("  {0:02d}:00  {1:7.1f}  {2}".format(
        hour_of_day, average_by_hour[hour_of_day], bar))
print()


# ===========================================================================
# STAGE 4 - Package. The same block, but reusable.
# ===========================================================================
#
# New here: `def`, arguments, `return`.
#
# We wrote stage 3 for northbound. We now want southbound too. Rather than
# copying and pasting it and changing one word - which is how bugs get in -
# we give it a name and hand it the direction we want.

def hourly_average(direction):
    """Return a list of 24 average counts, one per hour, for this direction."""
    result = []
    for hour_of_day in range(24):
        total = 0
        number_of_days = 0
        for index in range(len(counts)):
            if directions[index] == direction and hours[index] == hour_of_day:
                total = total + counts[index]
                number_of_days = number_of_days + 1
        result.append(total / number_of_days if number_of_days else 0.0)
    return result


def peak_hour(averages):
    """Return the hour with the highest average count."""
    return averages.index(max(averages))


northbound = hourly_average("northbound")
southbound = hourly_average("southbound")

print("STAGE 4")
print("  northbound peak hour: {0:02d}:00  ({1:.0f} veh/h)".format(
    peak_hour(northbound), max(northbound)))
print("  southbound peak hour: {0:02d}:00  ({1:.0f} veh/h)".format(
    peak_hour(southbound), max(southbound)))
print()

# Check that stage 4 agrees with stage 3. If they disagree, one of them is
# wrong, and we would rather find out here than in the figure. `assert` stops
# the program with the given message if the condition is false; if the
# condition is true, nothing happens and the program carries on.
assert abs(northbound[8] - average_by_hour[8]) < 0.001, "stage 3 and 4 disagree"


# ===========================================================================
# STAGE 5 - NumPy. The same thing again, without the loop.
# ===========================================================================
#
# New here: arrays, boolean masks, vectorised arithmetic.
#
# Everything above still stands - this is not a better answer, it is the same
# answer written shorter. You now know what it is doing underneath, which is
# why we did it the long way first.

hours_array = np.array(hours)
counts_array = np.array(counts)
directions_array = np.array(directions)

# A boolean mask: True wherever the condition holds. This replaces the `if`.
mask = directions_array == DIRECTION

# One line replaces the whole of stage 3.
numpy_average = np.array([counts_array[mask & (hours_array == h)].mean()
                          for h in range(24)])

print("STAGE 5")
print("  loop result and NumPy result agree:",
      np.allclose(numpy_average, average_by_hour))
print("  peak hour:", int(numpy_average.argmax()))
# The standard deviation at the peak is surprisingly large. That is not a
# mistake - it is telling you that the days in this file are not all alike.
# Task 2 will find out why.
print("  std dev at peak: {0:.0f} veh/h".format(
    counts_array[mask & (hours_array == numpy_average.argmax())].std()))
print()


# ===========================================================================
# STAGE 6 - The figure.
# ===========================================================================
#
# New here: matplotlib.
#
# Rule for the rest of this course: a figure with an unlabelled axis is not
# finished. Someone should be able to read it with no other context.

figure, axes = plt.subplots(figsize=(9, 5))

axes.plot(range(24), northbound, color=BLUE, linewidth=2, label="Northbound")
axes.plot(range(24), southbound, color=ORANGE, linewidth=2, label="Southbound")

# Mark the peak so the reader does not have to hunt for it.
peak = peak_hour(northbound)
axes.plot(peak, northbound[peak], "o", color=BLUE, markersize=9)
axes.annotate(
    "AM peak {0:02d}:00\n{1:.0f} veh/h".format(peak, northbound[peak]),
    xy=(peak, northbound[peak]),
    xytext=(peak + 1.4, northbound[peak] - 210),
    fontsize=9,
    arrowprops={"arrowstyle": "-", "color": "#999999", "linewidth": 1},
)

axes.set_xlabel("Hour of day")
axes.set_ylabel("Average flow (vehicles per hour)")
axes.set_title("Average hourly flow by direction\nCount site A34/012, 2-15 March 2026")
axes.set_xticks(range(0, 24, 2))
axes.set_xlim(0, 23)
axes.set_ylim(0, max(max(northbound), max(southbound)) * 1.15)
axes.grid(axis="y", alpha=0.25)          # recessive: the data is the subject
axes.spines["top"].set_visible(False)
axes.spines["right"].set_visible(False)
axes.legend(frameon=False)

figure.tight_layout()
figure.savefig("peak_profile.png", dpi=150)
print("STAGE 6")
print("  figure written to peak_profile.png")
