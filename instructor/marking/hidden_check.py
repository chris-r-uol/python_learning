"""
Hidden correctness check for the project. Instructor only.

    python instructor/marking/hidden_check.py <path-to-group-cleaned.csv>

Groups are told a hidden check exists. They are not told what it tests.

It checks the things that have exactly one right answer - the cleaning outcomes
and the bottleneck - and stays out of the way on the things that are genuinely
a matter of judgement (which reliability metric, how to treat the negative
dwell rows, what counts as a complete trip).
"""

import os
import sys

import pandas as pd

TRUTH = {
    "raw_rows": 97278,
    "duplicate_rows": 2400,
    "rows_after_dedup": 94878,
    "renamed_stop_id": "S009",
    "renamed_names": {"Northgate Retail", "Northgate Retail Park"},
    "negative_dwell_rows_raw": 71,          # 71 in the raw file...
    "negative_dwell_rows_deduped": 69,      # ...69 once duplicates are removed
    "negative_dwell_vehicle": "BUS_2837",
    "rows_past_midnight": 90,
    "under_reporting_vehicle": "BUS_2841",
    "under_reporting_days_missing": 3,
    "worst_segment": "SEG06",
    "worst_hours": {16, 17, 18},
    "worst_direction": "outbound",
}


def check(label, passed, detail=""):
    print("  [{0}] {1:<42} {2}".format("PASS" if passed else "FAIL", label, detail))
    return bool(passed)


def check_cleaned(path):
    """Run against a group's exported cleaned arrivals table."""
    frame = pd.read_csv(path)
    score = 0

    print("CLEANING")
    print("-" * 70)

    # 1. Duplicates removed - the single most common miss.
    no_dupes = not frame.duplicated().any()
    score += check("no exact duplicate rows remain", no_dupes,
                   "" if no_dupes else f"{int(frame.duplicated().sum())} left")

    # 2. Row count in the right region. Allow latitude: groups may legitimately
    #    also drop the ghost-vehicle rows or the negative-dwell rows.
    rows = len(frame)
    plausible = 90000 <= rows <= 95000
    score += check("row count in plausible cleaned range", plausible,
                   f"{rows} rows (expected 90k-95k)")

    # 3. The renamed stop was reconciled, not left split.
    if "stop_id" in frame.columns and "stop_name" in frame.columns:
        names = frame.groupby("stop_id")["stop_name"].nunique()
        reconciled = int((names > 1).sum()) == 0
        score += check("S009 reconciled to a single name", reconciled,
                       "" if reconciled else "still split")
    else:
        score += check("S009 reconciled to a single name", False, "columns missing")

    # 4. Negative dwell handled somehow - nulled or dropped, either is fine.
    if "dwell_s" in frame.columns:
        remaining = int((pd.to_numeric(frame["dwell_s"], errors="coerce") < 0).sum())
        score += check("negative dwell times handled", remaining == 0,
                       "" if remaining == 0 else f"{remaining} remain")
    else:
        score += check("negative dwell times handled", True, "column dropped - acceptable")

    print()
    return score


def check_finding(segment, hour, direction):
    """Run against the group's stated requirement 4 answer."""
    print("REQUIREMENT 4 FINDING")
    print("-" * 70)
    score = 0
    score += check("worst segment", segment == TRUTH["worst_segment"],
                   "said {0}, truth {1}".format(segment, TRUTH["worst_segment"]))
    score += check("worst period", int(hour) in TRUTH["worst_hours"],
                   "said {0}, truth {1}".format(hour, sorted(TRUTH["worst_hours"])))
    score += check("direction", direction == TRUTH["worst_direction"],
                   f"said {direction}")
    print()
    return score


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("Ground truth:")
        for key, value in TRUTH.items():
            print(f"  {key:<30} {value}")
        return

    path = sys.argv[1]
    if not os.path.exists(path):
        print("No such file:", path)
        return

    print("=" * 70)
    print("HIDDEN CHECK:", os.path.basename(path))
    print("=" * 70)
    score = check_cleaned(path)
    print(f"Cleaning score: {score}/4")
    print()
    print("Run check_finding(segment, hour, direction) against their stated answer.")


if __name__ == "__main__":
    main()
