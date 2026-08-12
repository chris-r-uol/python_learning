"""
Drill 11 * - hours_over

SOLUTION. Instructor copy. Verify with:

    python check.py

This drill is starred: harder, and entirely optional. Finish the nine
unstarred drills first.

"""

import numpy as np


def hours_over(counts, threshold):
    """`counts` is a NumPy array of 24 hourly flows. Return a NumPy array of
    the HOUR NUMBERS where flow exceeds `threshold`.

    Hint: look up `np.where`, or index an `np.arange` with a mask. Neither
    has been taught - finding out what an unfamiliar function does is part
    of this starred drill, and good practice for week 3.

    hours_over(np.array([10]*24), 5) -> array([0,1,2,...,23])

    Idea: boolean masks (Part 1, section 5).
    """
    return np.arange(len(counts))[counts > threshold]
