"""
Week 2 drills - the marker.

    python check.py

This runs every drill file in this folder and tells you which ones pass. It
does not tell you how to fix anything - that is the exercise.

Each drill lives in its own file, `drill_01.py` to `drill_12.py`. Open one,
fill in the function where it says TODO, save, and run this again. Work in
order; the drills get harder.

The three drills marked with a star are optional. Aim for the other nine.

You do not need to read the rest of this file - but you may find it useful,
because the tests below are roughly what checking your own work looks like,
and from week 3 onwards you will be writing checks like these yourself.
"""

import importlib
import os
import sys

import numpy as np

from _shared import PROFILE

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def load(number):
    """Import drill_NN.py fresh and hand back the module."""
    name = f"drill_{number:02d}"
    module = importlib.import_module(name)
    return importlib.reload(module)


# Each entry: (number, starred, function name, test)
# The test receives the function and returns True if it behaves correctly.
TESTS = [
    (1, False, "to_minutes", lambda f: (
        f("00:00") == 0 and f("08:45") == 525 and f("23:59") == 1439
    )),
    (2, False, "busiest_hour", lambda f: (
        f(PROFILE) == 8 and f([5, 5, 1]) == 0
    )),
    (3, False, "count_above", lambda f: (
        f([10, 20, 30], 15) == 2 and f(PROFILE, 1000) == 5 and f([], 0) == 0
    )),
    (4, False, "total_flow", lambda f: (
        f([10, 20, 30]) == 60 and f([]) == 0 and f(PROFILE) == sum(PROFILE)
    )),
    (5, False, "peak_period_total", lambda f: (
        f([0, 1, 2, 3, 4, 5], 1, 3) == 6 and f(PROFILE, 7, 9) == 3450
    )),
    (6, False, "congestion_band", lambda f: (
        f(0.5) == "free flow"
        and f(0.7) == "busy"
        and f(0.89) == "busy"
        and f(0.9) == "at capacity"
        and f(1.0) == "over capacity"
        and f(1.4) == "over capacity"
    )),
    (7, False, "average", lambda f: (
        f([2, 4, 6]) == 4.0
        and f([]) is None
        and abs(f(PROFILE) - sum(PROFILE) / 24) < 1e-9
    )),
    (8, False, "every_nth", lambda f: (
        f([0, 1, 2, 3, 4, 5, 6], 3) == [0, 3, 6] and f([1, 2], 1) == [1, 2]
    )),
    (9, True, "hourly_totals", lambda f: (
        f([(8, 100), (8, 50), (17, 90)])
        == [0] * 8 + [150] + [0] * 8 + [90] + [0] * 6
        and f([]) == [0] * 24
    )),
    (10, False, "volume_capacity", lambda f: np.allclose(
        f(np.array([900, 1800, 2700]), 1800), [0.5, 1.0, 1.5]
    )),
    (11, True, "hours_over", lambda f: (
        np.array_equal(f(np.array(PROFILE), 1000), np.array([8, 9, 16, 17, 18]))
        and len(f(np.array(PROFILE), 99999)) == 0
    )),
    (12, True, "two_way_flow", lambda f: np.array_equal(
        f(np.array([1, 2]), np.array([10, 20])), np.array([11, 22])
    )),
]


def main():
    print("=" * 64)
    print("WEEK 2 DRILLS")
    print("=" * 64)

    passed = 0
    core_passed = 0

    for number, starred, func_name, test in TESTS:
        label = f"drill_{number:02d}{'*' if starred else ' '} {func_name}"

        try:
            module = load(number)
        except SyntaxError as error:
            print(f"  BROKEN {label:<28} {type(error).__name__}: {error.msg}")
            print(f"         line {error.lineno} - the file will not even start")
            print()
            continue
        except Exception as error:                       # noqa: BLE001
            print(f"  BROKEN {label:<28} {type(error).__name__}: {error}")
            print()
            continue

        function = getattr(module, func_name, None)
        if function is None:
            print(f"  BROKEN {label:<28} no function called {func_name} in the file")
            print()
            continue

        try:
            result = test(function)
        except Exception as error:                       # noqa: BLE001
            print(f"  ERROR  {label:<28} {type(error).__name__}: {error}")
            print()
            continue

        if result:
            print(f"  PASS   {label}")
            passed += 1
            if not starred:
                core_passed += 1
        else:
            print(f"  TODO   {label:<28} runs, but not the right answer yet")

    print("-" * 64)
    print(f"{passed} of {len(TESTS)} passed  ({core_passed} of 9 unstarred).")
    if passed == len(TESTS):
        print("All twelve. You have the four moves: store, decide, repeat, package.")
    elif core_passed == 9:
        print("All nine unstarred drills done. The starred three are a bonus.")
    else:
        print("Keep going. Open the first file that is not passing and work on")
        print("that one alone - the drills are independent of each other.")
    print("=" * 64)


if __name__ == "__main__":
    main()
