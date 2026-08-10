"""
Project starter skeleton.

You do not have to use this. If you would rather start from an empty file, do.
But the function names and the shape of the pipeline here are the ones we will
be looking for, and the docstrings tell you what each piece needs to do.

Run it:

    python starter/corridor.py

Right now it loads the data and stops. That is the honest starting point.
"""

import os

# You will probably want pandas. You were not taught it - that is week 3's
# point. Use the assistant, then check what it gives you.

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")


# ===========================================================================
# 1. LOAD AND CLEAN
# ===========================================================================

def load_raw():
    """Read the four CSVs. Return them however you like - four objects, a dict,
    whatever you find easiest to work with.

    Do NOT clean anything here. Loading and cleaning are separate steps so that
    you can count what changed between them.
    """
    raise NotImplementedError


def clean(arrivals):
    """Return (cleaned_arrivals, report).

    `report` should be something you can print - a dict or a list of strings -
    recording what you changed and by how much. It goes straight into your
    two-page brief, so write it for a reader, not for yourself.

    Before you write this function, go and look at the data. Open the CSV. Sort
    it. Count things. You are looking for at least five problems and you will
    not find them by guessing.

    Questions worth asking of any dataset:
      - How many rows? How many after each step?
      - Are there exact duplicates?
      - Does every id have exactly one name?
      - Are all the values in a sensible range? Any negatives that shouldn't be?
      - Does every entity have the same amount of data as the others?
      - Do the timestamps do anything strange at the ends of the day?
    """
    raise NotImplementedError


# ===========================================================================
# 2. JOURNEY TIME  (core requirement 2)
# ===========================================================================

def journey_times(arrivals):
    """End-to-end journey time per trip.

    Careful: a trip with missing stops will give you a journey time that is too
    short, and nothing will warn you. Decide what counts as a complete trip and
    say so in your brief.
    """
    raise NotImplementedError


# ===========================================================================
# 3. HEADWAYS  (core requirement 3)
# ===========================================================================

def headways(arrivals, stop_id):
    """Gaps between consecutive buses at one stop.

    Two traps: you must sort before you difference, and you must not difference
    across a day boundary or across directions.
    """
    raise NotImplementedError


# ===========================================================================
# 4. SEGMENT PERFORMANCE  (core requirement 4)
# ===========================================================================

def segment_runtimes(arrivals):
    """Run time between each consecutive pair of stops, per trip.

    You need the NEXT stop's arrival time on the same trip. Sorting matters.
    """
    raise NotImplementedError


def worst_segment(runtimes):
    """Return the segment and time period that performs worst.

    Think about what "worst" means before you code it. The slowest segment is
    probably just the longest one. What you want is the segment that is slowest
    RELATIVE TO ITS OWN normal - so you need a baseline.

    Whatever you choose, justify it in the brief. There is more than one
    defensible answer here and we are marking the reasoning.
    """
    raise NotImplementedError


# ===========================================================================
# 5. THE FIGURE  (core requirement 5)
# ===========================================================================

def make_figure(arrivals, output_path="figure.png"):
    """One figure. Labelled axes with units. A title that states the finding.

    Not "Journey times by hour" - that describes the chart.
    Try "Outbound journey times rise 30% in the PM peak" - that is the finding.
    """
    raise NotImplementedError


# ===========================================================================

def main():
    print("Loading from", os.path.relpath(DATA, HERE))
    print()
    print("Nothing implemented yet. Start with load_raw(), then go and look at")
    print("what you loaded before you write clean().")


if __name__ == "__main__":
    main()
