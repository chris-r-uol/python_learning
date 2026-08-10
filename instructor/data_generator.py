"""
Seeded generator for all course datasets.

    python instructor/data_generator.py

Change SEED for a new cohort. The planted defects move, so last year's
answers do not transfer.

Produces:
    week1_setup/data/site_counts_small.csv     tiny, for the first script
    week2_programming/data/traffic_counts.csv  hourly counts, one site, 14 days
    week3_ai/failure_demo/data/link_speeds.csv small, with a sentinel trap
    project/data/arrivals.csv                  stop-level actual vs scheduled
    project/data/stops.csv
    project/data/segments.csv
    project/data/boardings.csv
"""

import csv
import os
from datetime import datetime, timedelta

import numpy as np

SEED = 20260810
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

rng = np.random.default_rng(SEED)


def out(*parts):
    path = os.path.join(HERE, *parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def write_csv(path, header, rows):
    with open(path, "w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)
    print("  {0:<48} {1:>8} rows".format(os.path.relpath(path, HERE), len(rows)))


# ---------------------------------------------------------------------------
# Shared shape: a plausible urban weekday/weekend demand profile
# ---------------------------------------------------------------------------

# Relative demand by hour of day, 0-23. Two peaks, morning sharper than evening.
WEEKDAY_PROFILE = np.array([
    0.04, 0.02, 0.02, 0.02, 0.05, 0.18, 0.48, 0.86, 1.00, 0.72, 0.55, 0.52,
    0.56, 0.55, 0.58, 0.70, 0.88, 0.95, 0.74, 0.48, 0.34, 0.25, 0.16, 0.08,
])
WEEKEND_PROFILE = np.array([
    0.09, 0.06, 0.04, 0.03, 0.03, 0.06, 0.12, 0.20, 0.31, 0.45, 0.60, 0.72,
    0.80, 0.82, 0.80, 0.76, 0.70, 0.62, 0.54, 0.45, 0.38, 0.32, 0.24, 0.15,
])


def profile_for(day):
    return WEEKEND_PROFILE if day.weekday() >= 5 else WEEKDAY_PROFILE


# ---------------------------------------------------------------------------
# Week 1 + Week 2: hourly traffic counts at one site
# ---------------------------------------------------------------------------

def make_traffic_counts(n_days=14, start=datetime(2026, 3, 2)):
    """One count site, two directions, hourly, clean. Weeks 1-2 need clean data -
    students are learning to read code, not to clean."""
    rows = []
    base = {"northbound": 1450, "southbound": 1310}
    for offset in range(n_days):
        day = start + timedelta(days=offset)
        profile = profile_for(day)
        for direction, peak_flow in base.items():
            # Directional bias: north is the am tidal direction.
            bias = np.ones(24)
            if direction == "northbound":
                bias[6:10] *= 1.22
                bias[16:19] *= 0.85
            else:
                bias[6:10] *= 0.82
                bias[16:19] *= 1.25
            expected = profile * bias * peak_flow
            counts = rng.poisson(np.maximum(expected, 1.0))
            for hour in range(24):
                rows.append([
                    day.strftime("%Y-%m-%d"),
                    hour,
                    direction,
                    int(counts[hour]),
                ])
    return rows


# ---------------------------------------------------------------------------
# Week 3: small file with a sentinel-value trap
# ---------------------------------------------------------------------------

def make_link_speeds():
    """Link speeds where missing observations are recorded as -1.

    This is the failure demo. A lazy prompt produces code that averages the
    column including the -1s, giving a mean that is plausible, professional
    looking, and wrong. Small enough that a student can check it by hand.
    """
    rows = []
    links = ["A101", "A101", "A102", "A102", "A103", "A103", "B201", "B201"]
    hours = [8, 17, 8, 17, 8, 17, 8, 17]
    speeds = [14.2, 11.8, 22.6, 19.4, 9.1, 7.6, 31.5, 28.9]
    for link, hour, speed in zip(links, hours, speeds):
        for day in range(1, 11):
            observed = speed + rng.normal(0, 1.4)
            # 15% of observations are missing, recorded as the sentinel -1.
            if rng.random() < 0.15:
                observed = -1.0
            rows.append([
                "2026-04-{0:02d}".format(day),
                link,
                hour,
                round(float(observed), 1),
            ])
    return rows


# ---------------------------------------------------------------------------
# Project: bus corridor
# ---------------------------------------------------------------------------

STOP_NAMES = [
    "Cathedral Square", "Market Street", "Rivergate", "Bridge Foot",
    "Wellington Road", "Albion Park", "Hollow Lane", "St Chad's",
    "Northgate Retail", "Fairfield Avenue", "The Locks", "Brunswick Road",
    "Queen's Hospital", "Sandpits", "Ashcroft Green", "University West",
    "Beckhampton Road", "Longmoor Terminus",
]

# Segment 6->7 (Hollow Lane approach) is the planted bottleneck: an unsignalled
# junction that fails badly in the pm peak. This is the answer to core
# requirement 4, and it should be findable but not obvious.
BOTTLENECK_SEGMENT = 6

RENAME_FROM = "Northgate Retail"
RENAME_TO = "Northgate Retail Park"
RENAME_AFTER_DAY = 15          # defect: stop renamed part-way through the period
GHOST_VEHICLE = "BUS_2841"     # defect: this vehicle stops reporting
GHOST_DAYS = (11, 12, 13)


def make_corridor(n_days=28, start=datetime(2026, 4, 1)):
    n_stops = len(STOP_NAMES)

    # --- stops ---------------------------------------------------------
    stop_rows = []
    lat, lon = 52.4820, -1.8990
    for index, name in enumerate(STOP_NAMES):
        stop_rows.append([
            "S{0:03d}".format(index + 1),
            name,
            round(lat + index * 0.0061 + float(rng.normal(0, 0.0004)), 6),
            round(lon + index * 0.0028 + float(rng.normal(0, 0.0004)), 6),
            index + 1,
        ])

    # --- segments ------------------------------------------------------
    segment_rows = []
    lengths = rng.uniform(380, 940, n_stops - 1)
    for index in range(n_stops - 1):
        segment_rows.append([
            "SEG{0:02d}".format(index + 1),
            "S{0:03d}".format(index + 1),
            "S{0:03d}".format(index + 2),
            int(round(lengths[index])),
        ])

    # Free-flow run time per segment, seconds. ~22 km/h plus dwell allowance.
    free_flow = lengths / 6.1 + 14.0

    # --- arrivals ------------------------------------------------------
    arrival_rows = []
    vehicles = ["BUS_{0:04d}".format(number) for number in range(2830, 2854)]
    trip_counter = 0

    for offset in range(n_days):
        day = start + timedelta(days=offset)
        date_string = day.strftime("%Y-%m-%d")
        weekend = day.weekday() >= 5
        profile = profile_for(day)

        # Departure headway varies by time of day.
        departures = []
        minute = 5 * 60 + 40                       # first bus 05:40
        while minute < 23 * 60 + 30:               # last bus before 23:30
            hour = min(int(minute // 60), 23)
            demand = profile[hour]
            headway = 15.0 if weekend else (7.0 if demand > 0.75 else 12.0)
            departures.append(minute)
            minute += headway + float(rng.normal(0, 0.8))

        for direction in ("outbound", "inbound"):
            for departure in departures:
                trip_counter += 1
                trip_id = "T{0:06d}".format(trip_counter)
                vehicle = vehicles[trip_counter % len(vehicles)]

                scheduled = float(departure) * 60.0     # seconds past midnight
                actual = scheduled + float(rng.normal(20, 55))

                for stop_index in range(n_stops):
                    if stop_index > 0:
                        segment = stop_index          # 1-based segment number
                        base_run = free_flow[stop_index - 1]

                        hour = int(min(actual // 3600, 23))
                        congestion = 1.0 + 0.55 * profile[hour] ** 1.6
                        if weekend:
                            congestion = 1.0 + 0.18 * profile[hour]

                        # The planted bottleneck: severe pm peak delay on one
                        # segment, in the peak direction only.
                        if segment == BOTTLENECK_SEGMENT and not weekend:
                            if 16 <= hour <= 18 and direction == "outbound":
                                congestion *= 2.35
                            elif 7 <= hour <= 9 and direction == "outbound":
                                congestion *= 1.30

                        run = base_run * congestion
                        run *= float(rng.lognormal(0, 0.17))    # right-skewed

                        scheduled += base_run * (1.0 + 0.22 * profile[hour])
                        actual += run

                    stop_id = "S{0:03d}".format(stop_index + 1)
                    name = STOP_NAMES[stop_index]

                    # DEFECT: stop renamed part-way through the period.
                    if name == RENAME_FROM and offset >= RENAME_AFTER_DAY:
                        name = RENAME_TO

                    # DEFECT: one vehicle stops reporting for three days.
                    if vehicle == GHOST_VEHICLE and offset in GHOST_DAYS:
                        continue

                    dwell = max(float(rng.normal(11, 6)), 0.0)

                    # DEFECT: a small number of negative dwell times, from a
                    # door-sensor fault on one vehicle.
                    if vehicle == "BUS_2837" and rng.random() < 0.02:
                        dwell = -abs(float(rng.normal(40, 15)))

                    arrival_rows.append([
                        trip_id,
                        stop_id,
                        name,
                        direction,
                        date_string,
                        seconds_to_clock(scheduled),
                        seconds_to_clock(actual),
                        round(dwell, 1),
                        vehicle,
                    ])

    # DEFECT: the depot logged one day twice. Duplicate rows, exactly.
    duplicate_day = (start + timedelta(days=7)).strftime("%Y-%m-%d")
    duplicates = [row for row in arrival_rows if row[4] == duplicate_day][:2400]
    arrival_rows.extend(duplicates)
    rng.shuffle(arrival_rows)

    # --- boardings -----------------------------------------------------
    boarding_rows = []
    # Demand is not uniform: the hospital and university stops dominate.
    weights = np.array([
        1.9, 1.4, 0.8, 0.7, 1.0, 0.6, 0.5, 0.9,
        1.2, 0.7, 0.4, 0.8, 2.4, 0.5, 0.9, 2.1, 0.7, 1.1,
    ])
    for offset in range(n_days):
        day = start + timedelta(days=offset)
        profile = profile_for(day)
        for stop_index in range(n_stops):
            for hour in range(5, 24):
                expected = profile[hour] * weights[stop_index] * 26
                boarding_rows.append([
                    day.strftime("%Y-%m-%d"),
                    "S{0:03d}".format(stop_index + 1),
                    hour,
                    int(rng.poisson(max(expected, 0.2))),
                ])

    return stop_rows, segment_rows, arrival_rows, boarding_rows


def seconds_to_clock(seconds):
    """HH:MM:SS. Deliberately allows hours past 24 so that trips running after
    midnight sort correctly as text - students who parse this naively will find
    23:58 sorting after 24:06, which is the lesson."""
    seconds = int(round(seconds))
    return "{0:02d}:{1:02d}:{2:02d}".format(
        seconds // 3600, (seconds % 3600) // 60, seconds % 60
    )


def main():
    print("Generating course datasets (seed {0})".format(SEED))
    print("-" * 62)

    write_csv(
        out("week1_setup", "data", "site_counts_small.csv"),
        ["date", "hour", "direction", "count"],
        make_traffic_counts(n_days=2),
    )
    write_csv(
        out("week2_programming", "data", "traffic_counts.csv"),
        ["date", "hour", "direction", "count"],
        make_traffic_counts(n_days=14),
    )
    write_csv(
        out("week3_ai", "failure_demo", "data", "link_speeds.csv"),
        ["date", "link_id", "hour", "speed_kph"],
        make_link_speeds(),
    )

    stops, segments, arrivals, boardings = make_corridor()
    write_csv(
        out("project", "data", "stops.csv"),
        ["stop_id", "stop_name", "lat", "lon", "sequence"],
        stops,
    )
    write_csv(
        out("project", "data", "segments.csv"),
        ["segment_id", "from_stop", "to_stop", "length_m"],
        segments,
    )
    write_csv(
        out("project", "data", "arrivals.csv"),
        ["trip_id", "stop_id", "stop_name", "direction", "service_date",
         "scheduled_time", "actual_time", "dwell_s", "vehicle_id"],
        arrivals,
    )
    write_csv(
        out("project", "data", "boardings.csv"),
        ["service_date", "stop_id", "hour", "boardings"],
        boardings,
    )

    print("-" * 62)
    print("Done.")


if __name__ == "__main__":
    main()
