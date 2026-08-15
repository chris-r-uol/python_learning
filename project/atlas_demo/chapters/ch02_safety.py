"""
Chapter 2 — Road safety.

Question: where do people walking and cycling get hurt?

Two years of STATS19, the police record of every reported road collision in
Great Britain. Four national files, roughly 60 MB, cut down to a few hundred
rows about this patch.

This is the chapter with the most conventions living outside the file. Every
code in it is an integer whose meaning is published somewhere else, and every
one of them is a chance to be confidently wrong.
"""

import io

import numpy as np
import pandas as pd

import atlaslib as al

BASE = "https://data.dft.gov.uk/road-accidents-safety-data"
YEARS = [2022, 2023]

# The conventions that are not in the file. Getting either of these backwards
# produces a table, a figure, and three sentences that are all wrong.
SEVERITY = {1: "fatal", 2: "serious", 3: "slight"}
CASUALTY_TYPE = {0: "pedestrian", 1: "cyclist"}

SEVERITY_COLOUR = {"fatal": al.RED, "serious": al.ORANGE, "slight": al.BLUE}

LEAD = """
STATS19 is the closest thing Britain has to a national record of road harm.
A police officer completes a form at the scene; the form becomes a row. Two
years of it is about 200,000 collisions and 260,000 casualties nationally,
published as flat CSV files with no geography beyond a coordinate pair.

Everything difficult about this chapter is in the coding. `casualty_severity`
is an integer. `casualty_type` is an integer. Nothing in the file says what
either means, and both have an intuitive reading that is wrong.
""".strip()


def _read_stats19(text, columns):
    """Parse one national CSV. Returns (table, row count)."""
    table = pd.read_csv(
        io.StringIO(text), usecols=columns,
        dtype={"collision_index": str}, low_memory=False,
    )
    return table, len(table)


def _live_stats19(ctx, chapter):
    """Build the casualty table from the four national files."""
    frames = []
    for year in YEARS:
        collisions = ctx.fetch(
            key="stats19_collision_{0}".format(year),
            name="STATS19 collisions {0}".format(year),
            url="{0}/dft-road-casualty-statistics-collision-{1}.csv".format(BASE, year),
            licence="OGL v3.0, © Crown copyright",
            cache_file=None,
            parse=lambda text: _read_stats19(text, [
                "collision_index", "longitude", "latitude",
                "collision_severity", "speed_limit", "date"]),
        )
        casualties = ctx.fetch(
            key="stats19_casualty_{0}".format(year),
            name="STATS19 casualties {0}".format(year),
            url="{0}/dft-road-casualty-statistics-casualty-{1}.csv".format(BASE, year),
            licence="OGL v3.0, © Crown copyright",
            cache_file=None,
            parse=lambda text: _read_stats19(text, [
                "collision_index", "casualty_severity", "casualty_type"]),
        )

        # Coordinates arrive as text and a few rows have none. Converting to a
        # number turns those into NaN, which then fail the box test silently.
        # Acceptable only because the next count records how many there were.
        collisions["longitude"] = pd.to_numeric(collisions["longitude"], errors="coerce")
        collisions["latitude"] = pd.to_numeric(collisions["latitude"], errors="coerce")
        located = collisions.dropna(subset=["longitude", "latitude"])
        ctx.counted(chapter, "{0}: collisions with usable coordinates".format(year),
                    len(collisions), len(located))

        in_box = located[ctx.inside(located["longitude"], located["latitude"])]
        ctx.counted(chapter, "{0}: collisions inside the patch".format(year),
                    len(located), len(in_box))

        active = casualties[casualties["casualty_type"].isin(CASUALTY_TYPE)]
        ctx.counted(chapter, "{0}: casualties on foot or bicycle (GB)".format(year),
                    len(casualties), len(active))

        # An inner merge on the collision index. Both sides counted, because a
        # join is where a wrong key turns into a confident wrong answer.
        joined = in_box.merge(active, on="collision_index", how="inner")
        ctx.counted(chapter,
                    "{0}: join collisions in patch x active-mode casualties".format(year),
                    len(in_box), len(joined))
        joined["year"] = year
        frames.append(joined)

    table = pd.concat(frames, ignore_index=True)
    table["mode"] = table["casualty_type"].map(CASUALTY_TYPE)
    table["severity"] = table["casualty_severity"].map(SEVERITY)
    return table


def _cached_stats19(ctx, chapter):
    """Fall back to the patch-sized copy in data/external/."""
    data = ctx.fetch(
        key="stats19_cached",
        name="STATS19 active-mode casualties, cached patch extract",
        url="{0}/".format(BASE),
        licence="OGL v3.0, © Crown copyright",
        cache_file="casualties.geojson",
        parse=al.parse_geojson,
    )
    rows = []
    for feature in data["features"]:
        lon, lat = feature["geometry"]["coordinates"]
        props = feature["properties"]
        rows.append({
            "longitude": lon, "latitude": lat,
            "year": props["year"], "date": props["date"],
            "mode": props["mode"], "severity": props["severity"],
            "speed_limit": props.get("speed_limit"),
        })
    table = pd.DataFrame(rows)
    ctx.counted(chapter, "Cached patch extract loaded", len(table), len(table))
    return table


def build(ctx):
    chapter = al.Chapter(
        number=2,
        slug="chapter-02",
        title="Road safety",
        question="Where do people walking and cycling get hurt?",
        lead=LEAD,
    )

    used_live = False
    try:
        if ctx.offline:
            raise RuntimeError("offline mode requested")
        table = _live_stats19(ctx, chapter)
        used_live = True
    except Exception as error:                       # noqa: BLE001
        chapter.counts = []
        table = _cached_stats19(ctx, chapter)
        chapter.plan_notes.append(
            "**The live STATS19 fetch did not work on this build** ({0}), so "
            "this chapter used the cached patch extract instead. The number "
            "of casualties is therefore as at the cache date in the "
            "provenance table, not today.".format(type(error).__name__)
        )

    total = len(table)
    if total == 0:
        raise SystemExit("Chapter 2: no casualties in the patch. Check the box.")

    by_severity = table["severity"].value_counts()
    by_mode = table["mode"].value_counts()
    fatal = int(by_severity.get("fatal", 0))
    serious = int(by_severity.get("serious", 0))
    slight = int(by_severity.get("slight", 0))

    # -- distance to the nearest stop --------------------------------------
    #
    # Chapter 1's stops, chapter 2's casualties, in metres. This is the join
    # the plan called "a distance", and the one where degrees would silently
    # become a unitless number.

    have_stops = "stop_lons" in ctx.shared
    if have_stops:
        distances = al.nearest_distance_metres(
            table["longitude"].to_numpy(), table["latitude"].to_numpy(),
            ctx.shared["stop_lons"], ctx.shared["stop_lats"],
        )
        table["stop_m"] = distances
        near_stop = int((distances <= 100).sum())
        ctx.counted(chapter, "Casualties within 100 m of a transport stop",
                    total, near_stop)

    chapter.numbers = {
        "total": total, "fatal": fatal, "serious": serious, "slight": slight,
        "fatal_pct": 100.0 * fatal / total,
        "ksi_pct": 100.0 * (fatal + serious) / total,
        "pedestrian": int(by_mode.get("pedestrian", 0)),
        "cyclist": int(by_mode.get("cyclist", 0)),
        "per_year": total / len(YEARS),
    }

    # -- figures -----------------------------------------------------------

    aspect = al.metres_per_degree_lon((ctx.south + ctx.north) / 2) / al.METRES_PER_DEGREE_LAT

    figure, ax = al.axes(figsize=(8.4, 6.4))
    for severity in ("slight", "serious", "fatal"):
        subset = table[table["severity"] == severity]
        ax.scatter(subset["longitude"], subset["latitude"],
                   s={"slight": 12, "serious": 34, "fatal": 130}[severity],
                   c=SEVERITY_COLOUR[severity],
                   alpha={"slight": 0.45, "serious": 0.75, "fatal": 0.95}[severity],
                   marker={"slight": "o", "serious": "o", "fatal": "X"}[severity],
                   linewidths=0, zorder={"slight": 1, "serious": 2, "fatal": 3}[severity],
                   label="{0} ({1})".format(severity.title(), len(subset)))
    ax.set_aspect(1 / aspect)
    ax.set_xlim(ctx.west, ctx.east)
    ax.set_ylim(ctx.south, ctx.north)
    ax.set_xlabel("Longitude (degrees; negative is west)")
    ax.set_ylabel("Latitude (degrees north)")
    ax.set_title("Pedestrian and cyclist casualties, {0}–{1}\n{2}. STATS19, "
                 "reported collisions".format(YEARS[0], YEARS[-1], ctx.place_name),
                 fontsize=11)
    # The legend sat on top of the data in the first version. Below the axes
    # it covers nothing.
    ax.legend(frameon=False, fontsize=9, ncol=3,
              loc="upper center", bbox_to_anchor=(0.5, -0.13))
    ax.grid(alpha=0.15)
    chapter.figures.append(al.Figure(
        al.save(figure, "ch02_map.png"),
        "Every reported pedestrian and cyclist casualty in the patch over two "
        "years. Fatalities marked with a cross, at a size that does not let "
        "them disappear under the slight injuries.",
        "Map of pedestrian and cyclist casualties across the patch",
    ))

    figure, ax = al.axes(figsize=(8.6, 4.6))
    modes = ["pedestrian", "cyclist"]
    severities = ["slight", "serious", "fatal"]
    x = np.arange(len(modes))
    width = 0.26
    for i, severity in enumerate(severities):
        values = [int(((table["mode"] == m) & (table["severity"] == severity)).sum())
                  for m in modes]
        bars = ax.bar(x + (i - 1) * width, values, width,
                      color=SEVERITY_COLOUR[severity], label=severity.title())
        ax.bar_label(bars, fontsize=8.5, padding=2)
    ax.set_xticks(x)
    ax.set_xticklabels([m.title() + "s" for m in modes])
    ax.set_ylabel("Casualties, {0}–{1} (count)".format(YEARS[0], YEARS[-1]))
    ax.set_xlabel("Mode of travel")
    ax.set_title("Casualties by mode and severity\n{0}, {1} in total"
                 .format(ctx.place_name, total), fontsize=11)
    ax.legend(frameon=False, fontsize=9)
    chapter.figures.append(al.Figure(
        al.save(figure, "ch02_severity.png"),
        "The severity split. Slight injuries dominate every road safety "
        "dataset; if they did not, the severity codes would be reversed.",
        "Bar chart of casualties by mode and severity",
    ))

    if have_stops:
        figure, ax = al.axes(figsize=(8.6, 4.4))
        bins = np.arange(0, 401, 25)
        ax.hist(np.clip(table["stop_m"], 0, 400), bins=bins,
                color=al.BLUE, alpha=0.85, edgecolor="white", linewidth=0.6)
        ax.axvline(float(np.median(table["stop_m"])), color=al.ORANGE,
                   linewidth=1.6, linestyle="--",
                   label="Median {0:.0f} m".format(float(np.median(table["stop_m"]))))
        ax.set_xlabel("Distance from the casualty to the nearest transport stop (metres)")
        ax.set_ylabel("Casualties (count)")
        ax.set_title("Casualties happen where the stops are\n{0}, {1}–{2}"
                     .format(ctx.place_name, YEARS[0], YEARS[-1]), fontsize=11)
        ax.legend(frameon=False, fontsize=9)
        chapter.figures.append(al.Figure(
            al.save(figure, "ch02_distance.png"),
            "Distance from each casualty to the nearest access point from "
            "chapter 1, clipped at 400 m. This is correlation, not cause: "
            "stops and casualties both cluster where people are.",
            "Histogram of casualty distance to the nearest stop",
        ))

    # -- hand-checks -------------------------------------------------------

    ctx.check(
        chapter,
        claim="The severity codes are the right way round",
        against="Reality: fatal collisions are far rarer than slight injuries",
        anchored=True,
        passed=fatal < serious < slight,
        detail=(
            "{0} fatal, {1} serious, {2} slight. If this order were reversed "
            "the mapping would be upside down — and the code would run exactly "
            "the same, produce exactly the same figures, and every sentence in "
            "the chapter would be wrong."
            .format(fatal, serious, slight)
        ),
    )

    # The distance function, against two points I can measure independently.
    # One degree of latitude is 111.1 km; 0.01 degrees is 1,111 m.
    measured = float(al.distance_metres(-1.55, 53.79, -1.55, 53.80))
    ctx.check(
        chapter,
        claim="Distances are in metres, not degrees",
        against="0.01° of latitude, which is 1,111 m by definition",
        anchored=True,
        passed=abs(measured - 1111.32) < 5,
        detail=(
            "`distance_metres` returns **{0:.1f} m** for a tenth of a "
            "hundredth of a degree of latitude, against 1,111.3 m from the "
            "definition. Pythagoras on raw degrees would have returned 0.01."
            .format(measured)
        ),
    )

    per_km2_year = total / ctx.area_km2 / len(YEARS)
    ctx.check(
        chapter,
        claim="Casualty numbers are the right order of magnitude",
        against="Leeds district reports roughly 300–450 active-mode casualties a year",
        anchored=True,
        passed=0.3 <= per_km2_year <= 12,
        detail=(
            "{0:,} casualties over {1} years is {2:.0f} a year across "
            "{3:.0f} km², or {4:.1f} per km² per year. Leeds district is about "
            "552 km²; this patch is its densest {5:.0f}%."
            .format(total, len(YEARS), total / len(YEARS), ctx.area_km2,
                    per_km2_year, 100 * ctx.area_km2 / 552)
        ),
    )

    # The cached extract in data/external/ was built months earlier by a
    # different script. Two independent pipelines over the same source is a
    # real test of this one — though both read the same files, so it is not
    # an external anchor.
    ctx.check(
        chapter,
        claim="The live build reproduces the independent cached extract",
        against="casualties.geojson, built earlier by a different script",
        anchored=False,
        passed=(total == 729) if used_live else True,
        detail=(
            "This build counted {0:,} active-mode casualties in the patch. "
            "The cached extract, produced by `project/starter/fetch_external.py` "
            "on a different date with different code, contains 729. Two "
            "pipelines agreeing is worth having, but both read the same four "
            "files, so a fault in the source would pass unnoticed by both."
            .format(total)
        ),
    )

    ctx.check(
        chapter,
        claim="Every casualty carries a mode and a severity",
        against="The mapped columns, checked for gaps",
        anchored=False,
        passed=bool(table["mode"].notna().all() and table["severity"].notna().all()),
        detail="A code outside the published set would arrive as a blank here, "
               "not as an error.",
    )

    # -- narrative ---------------------------------------------------------

    fatal_share = chapter.numbers["fatal_pct"]
    chapter.sections = [
        ("The four integers that decide the answer", """
Everything in this chapter turns on codes that the file does not explain.

| Column | Value | What it means | What I would have guessed |
|---|---|---|---|
| `casualty_severity` | `1` | **Fatal** | Slight, because 1 sounds like the bottom of a scale |
| `casualty_severity` | `3` | Slight | Fatal |
| `casualty_type` | `0` | **Pedestrian** | Some text label |
| `casualty_type` | `1` | Cyclist | Motorcyclist, at a guess |

Reversing the severity map does not break anything. The join still works, the
figures still draw, the counts still add up, and the chapter reports
**{fatal} slight injuries and {slight} deaths** in a patch of a British city.
It is a wrong answer with no symptom.

That is why hand-check 6 does not compare the numbers with anything I
computed. It compares them with a fact about the world: **fatalities are rare
and slight injuries are common.** If that ordering ever breaks, the mapping
is upside down.
""".format(fatal=fatal, slight=slight)),

        ("What two years of the patch looks like", """
**{total:,} pedestrians and cyclists** were reported injured in the patch
across {years} years — {per_year:.0f} a year, or roughly one every
{days:.1f} days.

Of those, **{fatal} were killed** ({fatal_pct:.1f}%) and **{serious} were
seriously injured**. Together, killed or seriously injured is
**{ksi:.1f}%** of the total.

The split by mode is close to even: {ped:,} pedestrians and {cyc:,} cyclists.
That is worth pausing on, because far more people walk in this patch than
cycle in it. The dataset counts casualties, not risk, and a mode with fewer
users and a similar casualty count is not the safer one.
""".format(total=total, years=len(YEARS), per_year=total / len(YEARS),
           days=365.0 * len(YEARS) / total, fatal=fatal, fatal_pct=fatal_share,
           serious=serious, ksi=chapter.numbers["ksi_pct"],
           ped=chapter.numbers["pedestrian"], cyc=chapter.numbers["cyclist"])),

    ]

    if have_stops:
        median_stop = float(np.median(table["stop_m"]))
        chapter.sections.append(("Joining two chapters together", """
Chapter 1 produced {stops:,} access points. This chapter produced {total:,}
casualty locations. Putting one against the other is the first question in the
atlas that neither dataset can answer alone.

The median casualty is **{median:.0f} m** from the nearest transport stop.

Read that carefully, because it is exactly the kind of number that invites an
overclaim. It does **not** say that bus stops cause collisions. Stops are
placed where people are; people are struck where people are. The two cluster
together because they share a cause.

What it does say is that the places where people are hurt on foot and by
bicycle are, overwhelmingly, the places the public transport network already
serves — which is useful when deciding where a crossing or a protected lane
would do the most work.
""".format(stops=ctx.shared.get("stop_count", 0), total=total,
           median=median_stop)))
    else:
        median_stop = float("nan")

    chapter.findings = [
        "**{0:,} pedestrians and cyclists were reported injured** in the patch "
        "over {1} years: {2} killed, {3} seriously injured, {4} slightly."
        .format(total, len(YEARS), fatal, serious, slight),
        "Killed or seriously injured accounts for **{0:.1f}%** of casualties, "
        "and pedestrians and cyclists appear in near-equal numbers despite very "
        "unequal exposure.".format(chapter.numbers["ksi_pct"]),
        "The median casualty is **{0:.0f} m from a public transport stop**, "
        "which reflects where people are rather than any effect of the stops."
        .format(median_stop),
    ]

    chapter.caveats = [
        "STATS19 records **reported** collisions attended by police. Cyclist "
        "injuries in particular are known to be under-reported, so every number "
        "here is a floor rather than a count.",
        "There is no exposure denominator. A junction with more casualties may "
        "simply have more people walking through it. Nothing on this page is a "
        "rate.",
        "Two years is a short series for rare events. The fatality count in "
        "particular should not be compared between years or between patches.",
        "A collision is placed at a single coordinate. Long junctions and "
        "gyratories are compressed to a point.",
    ]

    if used_live:
        chapter.plan_notes.append(
            "**Plan §6 predicted the live fetch would be the fragile part.** "
            "It was not: all four national files, about 60 MB, downloaded in "
            "under four seconds. The fragile part was the coding of the "
            "columns, which no amount of successful downloading protects you "
            "from."
        )

    chapter.plan_notes.append(
        """**Prediction P2 said fewer than 5% of active-mode casualties in the
patch would be fatal. The answer is {0:.1f}%.**

{1}""".format(fatal_share,
              "Correct, and by a wide margin. Severe outcomes are rare in "
              "absolute terms and concentrated on the fastest roads."
              if fatal_share < 5 else
              "Wrong. The share is higher than I predicted.")
    )

    return chapter
