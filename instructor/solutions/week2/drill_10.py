"""
Drill 10 - volume_capacity

SOLUTION. Instructor copy. Verify with:

    python check.py

"""

import numpy as np


def volume_capacity(counts, capacity):
    """`counts` is a NumPy array of hourly flows. Return a NumPy array of the
    volume/capacity ratio for each hour.

    No loop. One line.

    volume_capacity(np.array([900, 1800]), 1800) -> array([0.5, 1.0])

    Idea: arithmetic on a whole array at once (Part 1, section 5).
    """
    return counts / capacity
