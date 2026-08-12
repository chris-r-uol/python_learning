"""
Drill 1 - to_minutes

SOLUTION. Instructor copy. Verify with:

    python check.py

"""


def to_minutes(clock):
    """Convert a "HH:MM" string into minutes past midnight.

    to_minutes("00:00") -> 0
    to_minutes("08:45") -> 525

    Idea: text and numbers (Part 1, section 1).
    """
    hours, minutes = clock.split(":")
    return int(hours) * 60 + int(minutes)
