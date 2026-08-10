"""
Reference solution for the project core requirements. Instructor copy.

    python instructor/solutions/project/reference_solution.py

This is not the only defensible answer - the metric choice in requirement 3 is
genuinely open, and groups that argue for a different one and justify it should
score well. But the cleaning results and the requirement 4 answer are ground
truth, and the numbers printed here are what the hidden check compares against.
"""

import os

import numpy as np
import pandas as pd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
DATA = os.path.join(ROOT, "project", "data")

BOTTLENECK_TRUTH = ("SEG06", 17, "outbound")


def clock_to_seconds(series):
    """Parse HH:MM:SS where HH may exceed 23. pandas' own time parsers reject
    24:06:00, which is the trap - trips that run past midnight are recorded as
    hour 24 and 25, not as the next day."""
    parts = series.str.split(":", expand=True).astype(int)
    return parts[0] * 3600 + parts[1] * 60 + parts[2]


def load_and_clean(verbose=True):
    arrivals = pd.read_csv(os.path.join(DATA, "arrivals.csv"))
    report = {"rows_in": len(arrivals)}

    # --- DEFECT 1: exact duplicate rows from a double-logged depot day -------
    before = len(arrivals)
    arrivals = arrivals.drop_duplicates()
    report["duplicates_removed"] = before - len(arrivals)

    # --- DEFECT 2: one stop renamed part-way through the period -------------
    # Group by stop_id, never stop_name. Groups that use the name silently
    # split S009 into two stops and lose half its trips.
    names = arrivals.groupby("stop_id")["stop_name"].nunique()
    report["stops_with_multiple_names"] = int((names > 1).sum())
    canonical = arrivals.groupby("stop_id")["stop_name"].agg(
        lambda values: values.value_counts().idxmax())
    arrivals["stop_name"] = arrivals["stop_id"].map(canonical)

    # --- DEFECT 3: negative dwell times from a door-sensor fault ------------
    negative = arrivals["dwell_s"] < 0
    report["negative_dwell_rows"] = int(negative.sum())
    report["negative_dwell_vehicles"] = sorted(
        arrivals.loc[negative, "vehicle_id"].unique().tolist())
    # Defensible: null them rather than drop the row. The arrival time is still
    # good; only the dwell measurement is suspect.
    arrivals.loc[negative, "dwell_s"] = np.nan

    # --- DEFECT 4: times past midnight ---------------------------------------
    arrivals["scheduled_s"] = clock_to_seconds(arrivals["scheduled_time"])
    arrivals["actual_s"] = clock_to_seconds(arrivals["actual_time"])
    report["rows_past_midnight"] = int((arrivals["actual_s"] >= 24 * 3600).sum())

    # --- DEFECT 5: a vehicle that stops reporting ---------------------------
    days_per_vehicle = arrivals.groupby("vehicle_id")["service_date"].nunique()
    expected_days = int(days_per_vehicle.max())
    short = days_per_vehicle[days_per_vehicle < expected_days]
    report["vehicles_with_missing_days"] = short.to_dict()

    arrivals["delay_s"] = arrivals["actual_s"] - arrivals["scheduled_s"]
    arrivals["hour"] = (arrivals["actual_s"] // 3600).clip(upper=23)

    if verbose:
        print("CLEANING REPORT")
        print("-" * 60)
        for key, value in report.items():
            print("  {0:<28} {1}".format(key, value))
        print("  {0:<28} {1}".format("rows_out", len(arrivals)))
        print()

    return arrivals, report


def segment_runtimes(arrivals):
    """Run time between consecutive stops, per trip. The join students most
    often get wrong - they forget to sort, or they join across trips."""
    ordered = arrivals.sort_values(["trip_id", "actual_s"])
    ordered["next_stop"] = ordered.groupby("trip_id")["stop_id"].shift(-1)
    ordered["next_actual"] = ordered.groupby("trip_id")["actual_s"].shift(-1)
    ordered["run_s"] = ordered["next_actual"] - ordered["actual_s"]

    runs = ordered.dropna(subset=["next_stop"]).copy()
    runs["segment_id"] = "SEG" + runs["stop_id"].str[1:].astype(int).map("{:02d}".format)
    # Guard against nonsense produced by the midnight rollover.
    runs = runs[(runs["run_s"] > 0) & (runs["run_s"] < 2000)]
    return runs


def core_analysis():
    arrivals, report = load_and_clean()

    # --- Requirement 2: journey time distribution by time of day ------------
    trips = arrivals.sort_values(["trip_id", "actual_s"]).groupby(
        ["trip_id", "direction"]).agg(
        start_s=("actual_s", "first"),
        end_s=("actual_s", "last"),
        stops=("stop_id", "nunique"),
    ).reset_index()
    trips = trips[trips["stops"] >= 17]              # complete runs only
    trips["journey_min"] = (trips["end_s"] - trips["start_s"]) / 60
    trips["hour"] = (trips["start_s"] // 3600).clip(upper=23).astype(int)

    print("REQ 2 - end-to-end journey time by departure hour (outbound)")
    print("-" * 60)
    print("{0:>6} {1:>8} {2:>8} {3:>8} {4:>8}".format(
        "hour", "n", "median", "p90", "spread"))
    outbound = trips[trips["direction"] == "outbound"]
    for hour, group in outbound.groupby("hour"):
        if len(group) < 20:
            continue
        median = group["journey_min"].median()
        p90 = group["journey_min"].quantile(0.9)
        print("{0:>6} {1:>8} {2:>8.1f} {3:>8.1f} {4:>8.1f}".format(
            hour, len(group), median, p90, p90 - median))
    print()
    print("  The point: the MEAN hides this. In the peaks the median rises by")
    print("  about 12 minutes AND the median-to-p90 spread roughly doubles")
    print("  against the midday baseline. The corridor gets slower and less")
    print("  predictable at the same time, and only the second of those is")
    print("  what passengers experience as unreliability.")
    print()

    # --- Requirement 3: headway regularity ----------------------------------
    first_stop = arrivals[arrivals["stop_id"] == "S001"].sort_values("actual_s")
    headways = []
    for (date, direction), group in first_stop.groupby(["service_date", "direction"]):
        gaps = group["actual_s"].diff().dropna() / 60
        gaps = gaps[(gaps > 0) & (gaps < 60)]
        for hour, gap in zip(group["hour"].iloc[1:], gaps):
            headways.append((int(hour), float(gap)))
    headway_frame = pd.DataFrame(headways, columns=["hour", "gap_min"])

    print("REQ 3 - headway regularity at the first stop")
    print("-" * 60)
    summary = headway_frame.groupby("hour")["gap_min"].agg(["count", "mean", "std"])
    summary["cv"] = summary["std"] / summary["mean"]
    for hour, row in summary[summary["count"] > 100].iterrows():
        flag = "  <- bunching" if row["cv"] > 0.45 else ""
        print("{0:>6} {1:>8.0f} {2:>8.1f} {3:>8.2f}{4}".format(
            hour, row["count"], row["mean"], row["cv"], flag))
    print()

    # --- Requirement 4: the worst segment / period --------------------------
    runs = segment_runtimes(arrivals)
    runs["hour"] = (runs["actual_s"] // 3600).clip(upper=23).astype(int)
    grouped = runs.groupby(["segment_id", "hour", "direction"])["run_s"].agg(
        ["count", "mean"])
    grouped = grouped[grouped["count"] >= 50]

    # Excess over each segment's own off-peak baseline - a segment being long
    # is not the same as a segment being congested.
    baseline = runs[runs["hour"].isin([10, 11, 12, 13])].groupby(
        "segment_id")["run_s"].mean()
    grouped["baseline"] = grouped.index.get_level_values("segment_id").map(baseline)
    grouped["excess_s"] = grouped["mean"] - grouped["baseline"]
    grouped["excess_pct"] = 100 * grouped["excess_s"] / grouped["baseline"]

    worst = grouped.sort_values("excess_s", ascending=False).head(6)
    print("REQ 4 - worst segment/hour by excess over its own off-peak baseline")
    print("-" * 60)
    print("{0:<10} {1:>5} {2:<10} {3:>8} {4:>9} {5:>9}".format(
        "segment", "hour", "direction", "n", "excess s", "excess %"))
    for (segment, hour, direction), row in worst.iterrows():
        print("{0:<10} {1:>5} {2:<10} {3:>8.0f} {4:>9.0f} {5:>8.0f}%".format(
            segment, hour, direction, row["count"], row["excess_s"],
            row["excess_pct"]))
    print()

    top = worst.index[0]
    print("  Ground truth: {0}".format(BOTTLENECK_TRUTH))
    print("  Found:        {0}".format(top))
    print("  MATCH" if top[0] == BOTTLENECK_TRUTH[0] else "  MISMATCH - investigate")
    print()

    return arrivals, trips, runs, report


if __name__ == "__main__":
    core_analysis()
