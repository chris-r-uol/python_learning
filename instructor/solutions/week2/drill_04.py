"""
Drill 4 - total_flow

SOLUTION. Instructor copy. Verify with:

    python check.py

"""


def total_flow(counts):
    """Return the sum of `counts`.

    Do this with a loop, not with the built-in sum(). You are practising the
    machinery, not the shortcut.

    total_flow([10, 20, 30]) -> 60
    total_flow([]) -> 0

    Idea: the accumulator (Part 1, section 3).
    """
    running = 0
    for value in counts:
        running = running + value
    return running
