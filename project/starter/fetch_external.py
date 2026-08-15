"""
Worked example: one complete atlas chapter fetcher.

    python starter/fetch_external.py

This is chapter 2 of the atlas, road safety, finished. Use it as the pattern
for every chapter you build. It fetches STATS19, the Department for
Transport's record of every reported road casualty in Great Britain, and cuts
it down to the patch defined below.

The pattern is four steps. It is the same for every source:

    1. Write down where the data came from, in the file.
    2. Download it.
    3. Cut it down to your patch, and COUNT what you cut.
    4. Save the small local copy. Never download again in analysis code.

Step 3 is the one that matters. A national file has 100,000 rows or more.
Your patch has a few hundred. Without printed counts, you will not notice a
filter that takes everything, or nothing.

Data: STATS19, (c) Crown copyright, Open Government Licence v3.0.
      https://www.data.gov.uk/dataset/road-accidents-safety-data
"""

import json
import os

import pandas as pd

# ---------------------------------------------------------------------------
# The patch. Replace with your own place and box. Chapter 1 defines them.
# south, west, north, east - decimal degrees.
# ---------------------------------------------------------------------------

PLACE_NAME = "Leeds city centre"
BBOX = (53.75, -1.62, 53.83, -1.49)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "external", "casualties.geojson")

BASE = "https://data.dft.gov.uk/road-accidents-safety-data"
YEARS = [2022, 2023]

# STATS19 codes. These are in the data guide, not in the file. An assistant
# cannot know that casualty_type 0 is a pedestrian unless you tell it.
# Severity 1 is FATAL, not slight. Assistants guess this wrong.
SEVERITY = {1: "fatal", 2: "serious", 3: "slight"}
CASUALTY_TYPE = {0: "pedestrian", 1: "cyclist"}


def fetch_year(year):
    """Download one year of collisions and casualties. Returns two tables."""
    collisions = pd.read_csv(
        f"{BASE}/dft-road-casualty-statistics-collision-{year}.csv",
        usecols=["collision_index", "longitude", "latitude",
                 "collision_severity", "speed_limit", "date"],
        dtype={"collision_index": str},
        low_memory=False,
    )
    casualties = pd.read_csv(
        f"{BASE}/dft-road-casualty-statistics-casualty-{year}.csv",
        usecols=["collision_index", "casualty_severity", "casualty_type"],
        dtype={"collision_index": str},
        low_memory=False,
    )
    return collisions, casualties


def main():
    south, west, north, east = BBOX
    print(f"Patch: {PLACE_NAME}")
    print(f"  south {south:.4f}  north {north:.4f}")
    print(f"  west  {west:.4f}  east  {east:.4f}")
    print()

    features = []

    for year in YEARS:
        print(f"STATS19 {year}")
        collisions, casualties = fetch_year(year)
        print(f"  collisions downloaded (GB)      {len(collisions):>8}")
        print(f"  casualties downloaded (GB)      {len(casualties):>8}")

        # Coordinates arrive as text, and a few rows have none. Converting
        # to a number turns those into NaN instead of stopping the program.
        # NaN rows then fail the bounding-box test below without a warning.
        # That is acceptable here only because the next line counts them.
        collisions["longitude"] = pd.to_numeric(collisions["longitude"], errors="coerce")
        collisions["latitude"] = pd.to_numeric(collisions["latitude"], errors="coerce")
        no_coords = int(collisions["longitude"].isna().sum())
        print(f"  collisions with no coordinates  {no_coords:>8}")

        in_box = collisions[
            collisions["latitude"].between(south, north)
            & collisions["longitude"].between(west, east)
        ]
        print(f"  collisions inside the patch     {len(in_box):>8}")

        # Only pedestrians and cyclists. Street design affects them most,
        # and this chapter is about them.
        active = casualties[casualties["casualty_type"].isin(CASUALTY_TYPE)]

        # An inner merge. Count both sides. If this number is not what you
        # expect, the join key is wrong. A wrong join key is the most common
        # way to get a wrong answer out of pandas that still looks right.
        joined = in_box.merge(active, on="collision_index", how="inner")
        print(f"  active-mode casualties in patch {len(joined):>8}")
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
            "place": PLACE_NAME,
            "source": "STATS19, (c) Crown copyright, Open Government Licence v3.0",
            "retrieved_for_years": YEARS,
            "features": features,
        }, handle, indent=1)

    print(f"TOTAL active-mode casualties kept: {len(features)}")
    print(f"Written to {os.path.relpath(OUT, HERE)}")
    print()
    print("Before using this, check the total against the size of your")
    print("patch. A town-sized box with two casualties in two years, or with")
    print("ten thousand, means the box or the filter is wrong. Find out")
    print("which before you draw the figure.")
    print("Remember what a box is. A rectangle includes edges you would not")
    print("call your patch. Defining the box is part of the chapter.")


if __name__ == "__main__":
    main()
