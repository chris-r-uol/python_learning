"""
Atlas skeleton.

Using this file is optional. Its shape is the one the sessions teach: one
function per chapter, the same steps inside every chapter, and a main() that
rebuilds everything in order.

    python atlas.py

The steps, in every chapter:

    fetch (record the source and date)
      -> cut to the patch (count what you cut)
      -> clean (count again)
      -> figure (labelled axes, units, place name in the title)
      -> record the numbers your three sentences will use

Build ONE chapter at a time with the assistant. Check it before starting the
next. The method is the week 3 method. This file is only the skeleton.
"""

import os

# ---------------------------------------------------------------------------
# The patch. Chapter 1 replaces these four numbers with a bounding box you
# have drawn on a map.
# south, west, north, east - in that order, in decimal degrees.
# ---------------------------------------------------------------------------

PLACE_NAME = "Leeds city centre"          # replace with your patch
BBOX = (53.75, -1.62, 53.83, -1.49)       # replace with your box

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(HERE, "atlas_output")   # figures and the report go here
CACHE = os.path.join(HERE, "cache")           # raw downloads, fetched once


# ---------------------------------------------------------------------------
# Chapters. Each returns a dict of the numbers its three sentences will use.
# Returning them, rather than only printing them, lets the report builder
# reuse them. It also gives you something to hand-check.
# ---------------------------------------------------------------------------

def chapter_1_stops():
    """The patch and its stops (NaPTAN).

    Fetch the stops for your ATCO area, cut to BBOX, drop stops marked
    inactive, figure: where the stops are, sized or coloured by type.

    Look up your ATCO area code in data/external/atco_area_codes.csv. Do
    not guess it. Do not ask the assistant. The codes look guessable and are
    not. If your bounding-box filter leaves zero stops, check the area code
    first.

    Hand-check: take one stop you know, and confirm its coordinates put it
    where it really is.
    """
    raise NotImplementedError


def chapter_2_safety():
    """Road safety (STATS19, two years).

    fetch_external.py in this folder is this chapter, finished. Read it,
    run it, then adapt it. Do not retype it.
    """
    raise NotImplementedError


def chapter_3_deprivation():
    """Deprivation (IMD 2019 + the ONS point-in-LSOA lookup).

    The trap: IMD 2019 uses 2011 LSOA codes. The boundary service returns
    2021 codes. Count how many rows survive the join.
    """
    raise NotImplementedError


def chapter_4_car_free():
    """Who has no car (Census 2021, table TS045, via the Nomis API)."""
    raise NotImplementedError


def chapter_5_cycling_potential():
    """Cycling potential (PCT route network for your region)."""
    raise NotImplementedError


def chapter_6_what_is_there():
    """What is there (OpenStreetMap via Overpass. Use POST, never GET)."""
    raise NotImplementedError


def chapter_7_weather():
    """A year of weather (open-meteo archive. JSON, no key needed)."""
    raise NotImplementedError


# ---------------------------------------------------------------------------
# The report. Plain HTML is enough: one page per chapter, each with its
# figure and your three sentences. Ask the assistant for a small function
# that writes this from a list of (title, figure_path, text) entries. Read
# what it gives you before you run it.
#
# Writing a file is the one new thing here. Reading used open(path). Writing
# is the same call with "w" added. It REPLACES whatever was in the file:
#
#     with open("atlas_output/index.html", "w") as handle:
#         handle.write("<h1>My patch</h1>")
#
# Two things to know. The folder must already exist. That is what the
# os.makedirs call in main() is for. And writing a file prints nothing, so
# open the file afterwards and check it.
# ---------------------------------------------------------------------------

def build_report(chapters):
    """Write atlas_output/index.html, combining every chapter."""
    raise NotImplementedError


def main():
    os.makedirs(OUTPUT, exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)
    print("Atlas of:", PLACE_NAME)
    print("Bounding box (S, W, N, E):", BBOX)
    print()
    print("No chapters are written yet. Start with chapter_1_stops().")
    print("It defines the patch that every other chapter uses.")


if __name__ == "__main__":
    main()
