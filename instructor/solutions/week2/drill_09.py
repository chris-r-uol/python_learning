"""
Drill 9 * - hourly_totals

SOLUTION. Instructor copy. Verify with:

    python check.py

This drill is starred: harder, and entirely optional. Finish the nine
unstarred drills first.

"""


def hourly_totals(rows):
    """`rows` is a list of (hour, count) pairs, in no particular order, with
    hours possibly repeated and possibly missing.

    Return a list of 24 numbers: the total count in each hour, 0 where there
    were no rows.

    hourly_totals([(8, 100), (8, 50), (17, 90)])
        -> [0,0,0,0,0,0,0,0,150,0,0,0,0,0,0,0,0,90,0,0,0,0,0,0]

    Idea: list repetition to start the counters, and rows that hold several
    values at once (Part 1, section 3).
    """
    totals = [0] * 24
    for hour, count in rows:
        totals[hour] = totals[hour] + count
    return totals
