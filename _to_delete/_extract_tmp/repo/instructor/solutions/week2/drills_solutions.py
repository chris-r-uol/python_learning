"""
Week 2 drills - SOLUTIONS. Instructor copy.

Original:

    python drills.py

Fill in each function where it says TODO, then run the file. It will tell you
which ones pass. Do them in order - they get harder.

Drills marked * are stretch. Get the other nine first.

You are not expected to know these already. Look things up, ask the person next
to you, read the worked example again. The only wrong way to do this is to read
the solutions.
"""

import numpy as np


# ---------------------------------------------------------------------------
# 1. Text to numbers
# ---------------------------------------------------------------------------

def to_minutes(clock):
    hours, minutes = clock.split(":")
    return int(hours) * 60 + int(minutes)


# ---------------------------------------------------------------------------
# 2. Finding things in a list
# ---------------------------------------------------------------------------

def busiest_hour(counts):
    """`counts` has 24 numbers, one per hour. Return the hour (0-23) with the
    highest count. If two hours tie, return the earlier one.

    busiest_hour([1, 9, 3, ...]) -> 1
    """
    return counts.index(max(counts))


# ---------------------------------------------------------------------------
# 3. Looping with a condition
# ---------------------------------------------------------------------------

def count_above(counts, threshold):
    """Return how many values in `counts` are strictly greater than `threshold`.

    count_above([10, 20, 30], 15) -> 2
    """
    found = 0
    for value in counts:
        if value > threshold:
            found = found + 1
    return found


# ---------------------------------------------------------------------------
# 4. Accumulating
# ---------------------------------------------------------------------------

def total_flow(counts):
    """Return the sum of `counts`.

    Do this with a loop, not with the built-in sum(). You are practising the
    machinery, not the shortcut.

    total_flow([10, 20, 30]) -> 60
    total_flow([]) -> 0
    """
    running = 0
    for value in counts:
        running = running + value
    return running


# ---------------------------------------------------------------------------
# 5. Slicing
# ---------------------------------------------------------------------------

def peak_period_total(counts, start_hour, end_hour):
    """Return the total flow from `start_hour` up to AND INCLUDING `end_hour`.

    peak_period_total([0,1,2,3,4,5], 1, 3) -> 6      (1 + 2 + 3)
    """
    return sum(counts[start_hour:end_hour + 1])


# ---------------------------------------------------------------------------
# 6. Branching
# ---------------------------------------------------------------------------

def congestion_band(volume_capacity_ratio):
    """Classify a volume/capacity ratio.

        below 0.7          -> "free flow"
        0.7 up to 0.9      -> "busy"
        0.9 up to 1.0      -> "at capacity"
        1.0 and above      -> "over capacity"

    Watch the boundaries. 0.7 is "busy", not "free flow".
    """
    if volume_capacity_ratio < 0.7:
        return "free flow"
    elif volume_capacity_ratio < 0.9:
        return "busy"
    elif volume_capacity_ratio < 1.0:
        return "at capacity"
    else:
        return "over capacity"


# ---------------------------------------------------------------------------
# 7. The empty case
# ---------------------------------------------------------------------------

def average(values):
    """Return the mean of `values`, or None if there are none.

    Most real bugs live in the empty case. Handle it deliberately.

    average([2, 4, 6]) -> 4.0
    average([]) -> None
    """
    if len(values) == 0:
        return None
    return sum(values) / len(values)


# ---------------------------------------------------------------------------
# 8. Building a new list
# ---------------------------------------------------------------------------

def every_nth(values, n):
    """Return a new list containing every nth value, starting with the first.

    every_nth([0,1,2,3,4,5,6], 3) -> [0, 3, 6]
    """
    return values[::n]


# ---------------------------------------------------------------------------
# 9. * Reshaping rows into a profile
# ---------------------------------------------------------------------------

def hourly_totals(rows):
    """`rows` is a list of (hour, count) pairs, in no particular order, with
    hours possibly repeated and possibly missing.

    Return a list of 24 numbers: the total count in each hour, 0 where there
    were no rows.

    hourly_totals([(8, 100), (8, 50), (17, 90)])
        -> [0,0,0,0,0,0,0,0,150,0,0,0,0,0,0,0,0,90,0,0,0,0,0,0]
    """
    totals = [0] * 24
    for hour, count in rows:
        totals[hour] = totals[hour] + count
    return totals


# ---------------------------------------------------------------------------
# 10. NumPy: arithmetic on a whole array
# ---------------------------------------------------------------------------

def volume_capacity(counts, capacity):
    """`counts` is a NumPy array of hourly flows. Return a NumPy array of the
    volume/capacity ratio for each hour.

    No loop. One line.

    volume_capacity(np.array([900, 1800]), 1800) -> array([0.5, 1.0])
    """
    return counts / capacity


# ---------------------------------------------------------------------------
# 11. * NumPy: boolean masks
# ---------------------------------------------------------------------------

def hours_over(counts, threshold):
    """`counts` is a NumPy array of 24 hourly flows. Return a NumPy array of
    the HOUR NUMBERS where flow exceeds `threshold`.

    Hint: np.where, or index an arange with a mask.

    hours_over(np.array([10]*24), 5) -> array([0,1,2,...,23])
    """
    return np.arange(len(counts))[counts > threshold]


# ---------------------------------------------------------------------------
# 12. * NumPy: combining arrays
# ---------------------------------------------------------------------------

def two_way_flow(northbound, southbound):
    """Both arguments are NumPy arrays of 24 hourly flows. Return a single
    array of the two-way total in each hour.

    two_way_flow(np.array([1,2]), np.array([10,20])) -> array([11, 22])
    """
    return northbound + southbound


# ===========================================================================
# Marking. You do not need to read below this line - but you may find it
# useful, because this is roughly what checking your own work looks like.
# ===========================================================================

PROFILE = [40, 25, 20, 18, 30, 120, 380, 900, 1450, 1100, 800, 780,
           820, 810, 850, 980, 1240, 1390, 1050, 700, 480, 350, 220, 110]


def _tests():
    yield "1  to_minutes", lambda: (
        to_minutes("00:00") == 0
        and to_minutes("08:45") == 525
        and to_minutes("23:59") == 1439
    )
    yield "2  busiest_hour", lambda: (
        busiest_hour(PROFILE) == 8
        and busiest_hour([5, 5, 1]) == 0
    )
    yield "3  count_above", lambda: (
        count_above([10, 20, 30], 15) == 2
        and count_above(PROFILE, 1000) == 5
        and count_above([], 0) == 0
    )
    yield "4  total_flow", lambda: (
        total_flow([10, 20, 30]) == 60
        and total_flow([]) == 0
        and total_flow(PROFILE) == sum(PROFILE)
    )
    yield "5  peak_period_total", lambda: (
        peak_period_total([0, 1, 2, 3, 4, 5], 1, 3) == 6
        and peak_period_total(PROFILE, 7, 9) == 3450
    )
    yield "6  congestion_band", lambda: (
        congestion_band(0.5) == "free flow"
        and congestion_band(0.7) == "busy"
        and congestion_band(0.89) == "busy"
        and congestion_band(0.9) == "at capacity"
        and congestion_band(1.0) == "over capacity"
        and congestion_band(1.4) == "over capacity"
    )
    yield "7  average", lambda: (
        average([2, 4, 6]) == 4.0
        and average([]) is None
        and abs(average(PROFILE) - sum(PROFILE) / 24) < 1e-9
    )
    yield "8  every_nth", lambda: (
        every_nth([0, 1, 2, 3, 4, 5, 6], 3) == [0, 3, 6]
        and every_nth([1, 2], 1) == [1, 2]
    )
    yield "9* hourly_totals", lambda: (
        hourly_totals([(8, 100), (8, 50), (17, 90)])
        == [0] * 8 + [150] + [0] * 8 + [90] + [0] * 6
        and hourly_totals([]) == [0] * 24
    )
    yield "10 volume_capacity", lambda: np.allclose(
        volume_capacity(np.array([900, 1800, 2700]), 1800), [0.5, 1.0, 1.5]
    )
    yield "11* hours_over", lambda: (
        np.array_equal(hours_over(np.array(PROFILE), 1000), np.array([8, 9, 16, 17, 18]))
        and len(hours_over(np.array(PROFILE), 99999)) == 0
    )
    yield "12* two_way_flow", lambda: np.array_equal(
        two_way_flow(np.array([1, 2]), np.array([10, 20])), np.array([11, 22])
    )


def main():
    print("=" * 60)
    print("WEEK 2 DRILLS")
    print("=" * 60)

    passed = 0
    total = 0
    for name, test in _tests():
        total += 1
        try:
            result = test()
        except Exception as error:                     # noqa: BLE001
            print("  ERROR  {0:<22} {1}: {2}".format(
                name, type(error).__name__, error))
            continue
        if result:
            print("  PASS   {0}".format(name))
            passed += 1
        else:
            print("  FAIL   {0:<22} runs, but gives the wrong answer".format(name))

    print("-" * 60)
    print("{0} of {1} passed.".format(passed, total))
    if passed == total:
        print("All twelve. You have the four moves: store, decide, repeat, package.")
    elif passed >= 9:
        print("The core nine are the ones that matter. Stretch drills are a bonus.")
    print("=" * 60)


if __name__ == "__main__":
    main()
