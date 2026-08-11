"""
Atlas skeleton.

You do not have to use this file, but its shape is the one the studio
teaches: one function per chapter, every chapter with the same internal
rhythm, and a main() that rebuilds everything in order.

    python atlas.py

The rhythm, for every chapter:

    fetch (state the source and date)
      -> cut to the patch (count what you cut)
      -> clean (count again)
      -> figure (labelled axes, units, place name in the title)
      -> write the numbers you will mention in your three sentences

Build ONE chapter at a time, with the assistant, and verify it before
starting the next. The week 3 method is the whole method; this file is only
its skeleton.
"""

import os

# ---------------------------------------------------------------------------
# The patch. Chapter 1's first job is to replace these four numbers with a
# bounding box you have drawn on a map and can defend as "my patch".
# south, west, north, east - in that order, in decimal degrees.
# ---------------------------------------------------------------------------

PLACE_NAME = "Leeds city centre"          # replace with your patch
BBOX = (53.75, -1.62, 53.83, -1.49)       # replace with your box

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(HERE, "atlas_output")   # figures and the report go here
CACHE = os.path.join(HERE, "cache")           # raw downloads, fetched once


# ---------------------------------------------------------------------------
# Chapters. Each returns a dict of the numbers its three sentences will use -
# returning them (rather than only printing) lets the report builder reuse
# them, and gives you something concrete to hand-check.
# ---------------------------------------------------------------------------

def chapter_1_stops():
    """The patch and its stops (NaPTAN).

    Fetch the stops for your ATCO area, cut to BBOX, drop stops marked
    inactive, figure: where the stops are, sized or coloured by type.

    Look your ATCO area code up in data/external/atco_area_codes.csv - do
    not guess it and do not ask the assistant, because the codes look
    guessable and are not. If your bounding-box filter leaves you with zero
    stops, suspect the area code before anything else.

    Hand-check: pick one stop you know personally and confirm its
    coordinates put it where it really is.
    """
    raise NotImplementedError


def chapter_2_safety():
    """Road safety (STATS19, two years).

    fetch_external.py in this folder is this chapter, finished. Read it,
    run it, then adapt rather than retype.
    """
    raise NotImplementedError


def chapter_3_deprivation():
    """Deprivation (IMD 2019 + the ONS point-in-LSOA lookup).

    The known trap: IMD 2019 carries 2011 LSOA codes and the boundary
    service returns 2021 codes. Count what survives your join.
    """
    raise NotImplementedError


def chapter_4_car_free():
    """Who has no car (Census 2021, table TS045, via the Nomis API)."""
    raise NotImplementedError


def chapter_5_cycling_potential():
    """Cycling potential (PCT route network for your region)."""
    raise NotImplementedError


def chapter_6_what_is_there():
    """What is there (OpenStreetMap via Overpass - POST, never GET)."""
    raise NotImplementedError


def chapter_7_weather():
    """A year of weather (open-meteo archive; JSON, no key needed)."""
    raise NotImplementedError


# ---------------------------------------------------------------------------
# The report. Plain HTML is enough: one page per chapter, each with its
# figure and your three sentences. Ask the assistant for a small function
# that writes this from a list of (title, figure_path, text) entries -
# and read what it gives you before you run it.
#
# Writing a file is the one thing here you have not done before. Reading
# used open(path) - writing is the same call with "w" added, and it
# REPLACES whatever was there:
#
#     with open("atlas_output/index.html", "w") as handle:
#         handle.write("<h1>My patch</h1>")
#
# Two things to know. The folder must already exist, which is what the
# os.makedirs call in main() below is for. And a script that writes a file
# succeeds silently - there is no output to tell you it worked, so check
# the file afterwards rather than assuming.
# ---------------------------------------------------------------------------

def build_report(chapters):
    """Write atlas_output/index.html pulling every chapter together."""
    raise NotImplementedError


def main():
    os.makedirs(OUTPUT, exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)
    print("Atlas of:", PLACE_NAME)
    print("Bounding box (S, W, N, E):", BBOX)
    print()
    print("No chapters are implemented yet. Start with chapter_1_stops() -")
    print("it defines the patch every other chapter reuses.")


if __name__ == "__main__":
    main()
