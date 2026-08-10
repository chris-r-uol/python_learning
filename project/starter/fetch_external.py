"""
Worked example: pulling a real national dataset down to your corridor.

    python starter/fetch_external.py

This script fetches STATS19 - the Department for Transport's register of every
reported road casualty in Great Britain - and cuts it down to the box your
corridor sits in. It is the only external fetcher provided in finished form.
The others described in `project/data_sources.md` you build yourselves, with
the assistant, using this file as the pattern.

The pattern is four steps, and it is the same for every source:

    1. Say where the data came from, in the file, in writing.
    2. Pull it.
    3. Cut it down to your study area - and COUNT what you cut.
    4. Save the small local copy. Never re-download in your analysis script.

Step 3 is the one that matters. A national file has 100,000+ rows and your
corridor has a few dozen. If you do not print the counts you will not notice
when a filter takes everything, or nothing.

Data: STATS19, (c) Crown copyright, Open Government Licence v3.0.
      https://www.data.gov.uk/dataset/road-accidents-safety-data
"""

import json
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
OUT = os.path.join(DATA, "external", "casualties.geojson")

BASE = "https://data.dft.gov.uk/road-accidents-safety-data"
YEARS = [2022, 2023]

# The corridor's bounding box, with about 500 m of margin so we catch casualties
# on the road beside a stop rather than exactly at it. Read off stops.csv - if
# you move the corridor, recompute this rather than trusting the numbers.
MARGIN_LAT = 0.005
MARGIN_LON = 0.008

# STATS19 codes. These are in the data guide, not in the file. This is exactly
# the "convention that lives outside the file" you met in week 3 - an assistant
# cannot know that casualty_type 0 is a pedestrian unless you tell it.
SEVERITY = {1: "fatal", 2: "serious", 3: "slight"}
CASUALTY_TYPE = {0: "pedestrian", 1: "cyclist"}


def corridor_bounds():
    """Return (south, west, north, east) around the corridor stops."""
    stops = pd.read_csv(os.path.join(DATA, "stops.csv"))
    return (
        stops["lat"].min() - MARGIN_LAT,
        stops["lon"].min() - MARGIN_LON,
        stops["lat"].max() + MARGIN_LAT,
        stops["lon"].max() + MARGIN_LON,
    )


def fetch_year(year):
    """Download one year of collisions and casualties. Returns two frames."""
    collisions = pd.read_csv(
        "{0}/dft-road-casualty-statistics-collision-{1}.csv".format(BASE, year),
        usecols=["collision_index", "longitude", "latitude",
                 "collision_severity", "speed_limit", "date"],
        dtype={"collision_index": str},
        low_memory=False,
    )
    casualties = pd.read_csv(
        "{0}/dft-road-casualty-statistics-casualty-{1}.csv".format(BASE, year),
        usecols=["collision_index", "casualty_severity", "casualty_type"],
        dtype={"collision_index": str},
        low_memory=False,
    )
    return collisions, casualties


def main():
    south, west, north, east = corridor_bounds()
    print("Corridor bounding box")
    print("  south {0:.4f}  north {1:.4f}".format(south, north))
    print("  west  {0:.4f}  east  {1:.4f}".format(west, east))
    print()

    features = []

    for year in YEARS:
        print("STATS19 {0}".format(year))
        collisions, casualties = fetch_year(year)
        print("  collisions downloaded (GB)      {0:>8}".format(len(collisions)))
        print("  casualties downloaded (GB)      {0:>8}".format(len(casualties)))

        # Coordinates arrive as text and some rows have none. Coercing to a
        # number turns those into NaN rather than crashing - which means they
        # will silently fail the bounding-box test below. That is the right
        # behaviour here, but only because we are about to count them.
        collisions["longitude"] = pd.to_numeric(collisions["longitude"], errors="coerce")
        collisions["latitude"] = pd.to_numeric(collisions["latitude"], errors="coerce")
        no_coords = int(collisions["longitude"].isna().sum())
        print("  collisions with no coordinates  {0:>8}".format(no_coords))

        in_box = collisions[
            collisions["latitude"].between(south, north)
            & collisions["longitude"].between(west, east)
        ]
        print("  collisions inside the box       {0:>8}".format(len(in_box)))

        # Only pedestrians and cyclists - the people a bus corridor's design
        # affects most, and the ones your brief is about.
        active = casualties[casualties["casualty_type"].isin(CASUALTY_TYPE)]

        # An inner merge. Count both sides: if this number is not what you
        # expect, the join key is wrong, and a wrong join key is the single
        # most common way to get a confident wrong answer out of pandas.
        joined = in_box.merge(active, on="collision_index", how="inner")
        print("  active-mode casualties in box   {0:>8}".format(len(joined)))
        print()

        for _, row in joined.iterrows():
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [round(row["longitude"], 6),
                                    round(row["latitude"], 6)],
                },
                "properties": {
                    "year": year,
                    "date": row["date"],
                    "mode": CASUALTY_TYPE[int(row["casualty_type"])],
                    "severity": SEVERITY.get(int(row["casualty_severity"]), "unknown"),
                    "speed_limit": row["speed_limit"],
                },
            })

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as handle:
        json.dump({
            "type": "FeatureCollection",
            "source": "STATS19, (c) Crown copyright, Open Government Licence v3.0",
            "retrieved_for_years": YEARS,
            "features": features,
        }, handle, indent=1)

    print("TOTAL active-mode casualties kept: {0}".format(len(features)))
    print("Written to {0}".format(os.path.relpath(OUT, HERE)))
    print()
    print("READ THIS BEFORE YOU USE THE FILE.")
    print()
    print("A bounding box is not a corridor. The box above is about 12 km by")
    print("4 km - roughly 50 square kilometres of inner Birmingham - and the")
    print("corridor is a line through the middle of it. Most of these")
    print("casualties happened nowhere near your bus route.")
    print()
    print("So this file is a starting point, not an answer. Your job is to")
    print("narrow it to casualties actually on the corridor - distance from")
    print("each casualty to the nearest stop, or to the line between stops -")
    print("and to say in your brief which you chose and what it excludes.")
    print()
    print("If you skip that step and report this number as 'casualties on the")
    print("47 corridor', you will have written a confident, professional,")
    print("wrong sentence. That is the week 3 lesson, at full scale.")


if __name__ == "__main__":
    main()
