"""
The one command.

    python atlas.py

Fetches seven national datasets, cuts each to the patch, counts what it cut,
draws the figures, runs the hand-checks, and writes the whole atlas into the
website as markdown. From an empty output folder, in one run, with no manual
step anywhere.

To build an atlas of somewhere else, change the two lines under "The patch"
and run it again. Nothing else in the project needs to know.

    python atlas.py --offline     use the cached copies, fetch nothing
    python atlas.py --only 3      build one chapter (its figures only)
"""

import argparse
import importlib
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import atlaslib as al           # noqa: E402
import pages                    # noqa: E402

# ---------------------------------------------------------------------------
# The patch. These two lines are the whole configuration.
# south, west, north, east — decimal degrees.
# ---------------------------------------------------------------------------

PLACE_NAME = "Leeds city centre"
BBOX = (53.75, -1.62, 53.83, -1.49)

# The bounding box the cached fallback copies in data/external/ were cut to.
# If you change BBOX and a live fetch then fails, the cache is the wrong shape
# for your patch and the atlas says so rather than quietly using it.
CACHE_BBOX = (53.75, -1.62, 53.83, -1.49)

CHAPTER_MODULES = [
    "chapters.ch01_stops",
    "chapters.ch02_safety",
    "chapters.ch03_deprivation",
    "chapters.ch04_car_free",
    "chapters.ch05_cycling",
    "chapters.ch06_amenities",
    "chapters.ch07_weather",
]


def main():
    parser = argparse.ArgumentParser(description="Build the transport atlas.")
    parser.add_argument("--offline", action="store_true",
                        help="use the cached copies and fetch nothing")
    parser.add_argument("--only", type=int, default=None,
                        help="build a single chapter by number")
    args = parser.parse_args()

    ctx = al.Context(PLACE_NAME, BBOX, offline=args.offline)
    ctx.cache_bbox = CACHE_BBOX

    print("=" * 70)
    print("TRANSPORT ATLAS — {0}".format(PLACE_NAME))
    print("=" * 70)
    print("  patch      S {0}  W {1}  N {2}  E {3}".format(*BBOX))
    print("  size       {0:.1f} km x {1:.1f} km  ({2:.0f} km2)"
          .format(ctx.width_km, ctx.height_km, ctx.area_km2))
    print("  mode       {0}".format("offline, cached copies" if args.offline else "live fetch, cache on failure"))
    print()

    started = time.time()
    for module_name in CHAPTER_MODULES:
        number = int(module_name.split(".")[1][2:4])
        if args.only and number != args.only:
            continue
        module = importlib.import_module(module_name)
        t0 = time.time()
        print("CHAPTER {0}  {1}".format(number, module_name.split("_", 1)[1]))
        chapter = module.build(ctx)
        ctx.chapters.append(chapter)
        for count in chapter.counts:
            print("    {0:<48} {1:>9,} -> {2:>9,}  ({3:.1f}%)"
                  .format(count.label[:48], count.before, count.after, count.kept))
        for check in chapter.checks:
            print("    check {0:<2} {1:<52} {2}"
                  .format(check.number,
                          check.claim[:52],
                          ("PASS" if check.passed else "FAIL")
                          + (" (anchored)" if check.anchored else "")))
        for figure in chapter.figures:
            print("    figure  {0}".format(figure.filename))
        print("    {0:.1f}s".format(time.time() - t0))
        print()

        pages.write_chapter(chapter, ctx)

    if not args.only:
        pages.write_synthesis(ctx)
        pages.write_scorecard(ctx)
        ctx.write_ledgers()

    anchored = [c for c in ctx.checks if c.anchored]
    failed = [c for c in ctx.checks if not c.passed]

    print("=" * 70)
    print("  {0} chapters, {1} figures, {2} hand-checks"
          .format(len(ctx.chapters),
                  sum(len(c.figures) for c in ctx.chapters),
                  len(ctx.checks)))
    print("  {0} anchored outside the data  <- the number that means something"
          .format(len(anchored)))
    if failed:
        print("  {0} FAILED:".format(len(failed)))
        for check in failed:
            print("      check {0}: {1}".format(check.number, check.claim))
    print("  built in {0:.1f}s".format(time.time() - started))
    print("=" * 70)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
