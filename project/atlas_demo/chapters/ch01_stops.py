"""
Chapter 1 — The patch and its stops.

Question: where can you catch something, and where can you not?

This chapter runs first because it fixes the bounding box that every other
chapter cuts to, and because it produces the stop coordinates that chapters
2 and 6 measure distance against.
"""

import numpy as np

import atlaslib as al

NAPTAN = "https://naptan.api.dft.gov.uk/v1/access-nodes?atcoAreaCodes={0}&dataFormat=csv"

# The lookup that cannot be guessed. West Yorkshire is 450; it is not the
# first three letters of anything. Area 910 is the national pseudo-area that
# holds every rail station in Great Britain.
BUS_AREA = "450"
RAIL_AREA = "910"

STOP_TYPE_NAMES = {
    "BCT": "Bus stop",
    "BCS": "Bus bay / stand",
    "BCQ": "Bus station bay",
    "RSE": "Rail station entrance",
    "RLY": "Rail station",
    "RPL": "Rail platform",
    "MET": "Metro / tram stop",
    "PLT": "Metro platform",
    "FTD": "Ferry terminal",
    "TXR": "Taxi rank",
}

GRID_METRES = 200.0
WALK_METRES = 400.0

LEAD = """
An atlas of public transport has to start by saying where public transport
*is*. That sounds like the easy chapter. It is not, for two reasons that both
show up below: the area code you need is unguessable, and the obvious query
returns an answer that is confidently incomplete.

NaPTAN is the national register of every point at which a passenger can join
a public transport service. It is published per administrative area, and each
area has a three-digit ATCO code. Leeds sits in **West Yorkshire, area 450** —
a number you cannot derive from the name of the place, cannot infer from any
pattern in the other codes, and which I would have got wrong if the repository
had not shipped `data/external/atco_area_codes.csv` with all 150 of them in it.
""".strip()


def _parse_stops(text):
    rows, _ = al.parse_csv(text.lstrip("﻿"))
    keep = []
    for row in rows:
        lon = al.to_float(row.get("Longitude"))
        lat = al.to_float(row.get("Latitude"))
        if np.isnan(lon) or np.isnan(lat):
            continue
        keep.append({
            "atco": (row.get("ATCOCode") or "").strip(),
            "name": (row.get("CommonName") or "").strip(),
            "locality": (row.get("LocalityName") or "").strip(),
            "type": (row.get("StopType") or "").strip(),
            "status": (row.get("Status") or "active").strip().lower(),
            "lon": lon,
            "lat": lat,
        })
    return keep, len(rows)


def build(ctx):
    chapter = al.Chapter(
        number=1,
        slug="chapter-01",
        title="The patch and its stops",
        question="Where can you catch something, and where can you not?",
        lead=LEAD,
    )

    # -- fetch -------------------------------------------------------------

    bus = ctx.fetch(
        key="naptan_bus",
        name="NaPTAN access nodes, ATCO area 450 (West Yorkshire)",
        url=NAPTAN.format(BUS_AREA),
        licence="OGL v3.0, © Crown copyright",
        cache_file="naptan_stops.csv",
        parse=_parse_stops,
    )
    rail = ctx.fetch(
        key="naptan_rail",
        name="NaPTAN access nodes, ATCO area 910 (national rail)",
        url=NAPTAN.format(RAIL_AREA),
        licence="OGL v3.0, © Crown copyright",
        cache_file="naptan_rail.csv",
        parse=_parse_stops,
    )

    # -- cut ---------------------------------------------------------------

    all_stops = bus + rail
    active = [s for s in all_stops if s["status"] == "active"]
    ctx.counted(chapter, "Drop stops marked inactive", len(all_stops), len(active))

    lons = np.array([s["lon"] for s in active])
    lats = np.array([s["lat"] for s in active])
    mask = ctx.inside(lons, lats)
    stops = [s for s, keep in zip(active, mask) if keep]
    ctx.counted(chapter, "Bounding-box filter to the patch", len(active), len(stops))

    if not stops:
        raise SystemExit("Chapter 1: no stops in the patch. Check the ATCO code first.")

    slon = np.array([s["lon"] for s in stops])
    slat = np.array([s["lat"] for s in stops])

    # Categories must partition the stops. The first version of this had two
    # categories, bus and rail, and ten rail-station ENTRANCES (RSE) belonged
    # to neither. They vanished from the map without any count changing.
    # See "Where the plan was wrong" below.
    RAIL_TYPES = ("RLY", "RPL")
    BUS_TYPES = ("BCT", "BCS", "BCQ")
    rail_stops = [s for s in stops if s["type"] in RAIL_TYPES]
    bus_stops = [s for s in stops if s["type"] in BUS_TYPES]
    other_stops = [s for s in stops
                   if s["type"] not in RAIL_TYPES + BUS_TYPES]
    partitioned = len(bus_stops) + len(rail_stops) + len(other_stops)
    other_kinds = sorted({s["type"] for s in other_stops})

    # -- coverage ----------------------------------------------------------
    #
    # A grid over the patch, one point every 200 m, each asking: how far is
    # the nearest stop? This is what turns a scatter of dots into a statement
    # about the places that have nothing.

    lat_step = GRID_METRES / al.METRES_PER_DEGREE_LAT
    lon_step = GRID_METRES / al.metres_per_degree_lon((ctx.south + ctx.north) / 2)
    grid_lats = np.arange(ctx.south, ctx.north, lat_step)
    grid_lons = np.arange(ctx.west, ctx.east, lon_step)
    mesh_lon, mesh_lat = np.meshgrid(grid_lons, grid_lats)
    nearest = al.nearest_distance_metres(
        mesh_lon.ravel(), mesh_lat.ravel(), slon, slat
    ).reshape(mesh_lon.shape)

    cells = nearest.size
    within_walk = int((nearest <= WALK_METRES).sum())
    ctx.counted(chapter, "Grid cells within {0:.0f} m of a stop".format(WALK_METRES),
                cells, within_walk)

    density = len(stops) / ctx.area_km2
    worst = float(nearest.max())
    worst_index = np.unravel_index(int(nearest.argmax()), nearest.shape)
    worst_lon = float(mesh_lon[worst_index])
    worst_lat = float(mesh_lat[worst_index])

    # Handed to chapters 2 and 6, which measure distance to these points.
    ctx.shared["stop_lons"] = slon
    ctx.shared["stop_lats"] = slat
    ctx.shared["stop_count"] = len(stops)

    chapter.numbers = {
        "stops": len(stops),
        "bus": len(bus_stops),
        "rail": len(rail_stops),
        "density": density,
        "covered_pct": 100.0 * within_walk / cells,
        "worst_m": worst,
        "worst_lon": worst_lon,
        "worst_lat": worst_lat,
        "median_m": float(np.median(nearest)),
    }

    # -- figures -----------------------------------------------------------

    aspect = al.metres_per_degree_lon((ctx.south + ctx.north) / 2) / al.METRES_PER_DEGREE_LAT

    figure, ax = al.axes(figsize=(8.4, 6.4))
    ax.scatter([s["lon"] for s in bus_stops], [s["lat"] for s in bus_stops],
               s=7, c=al.BLUE, alpha=0.55, linewidths=0, label="Bus stop ({0})".format(len(bus_stops)))
    if other_stops:
        ax.scatter([s["lon"] for s in other_stops], [s["lat"] for s in other_stops],
                   s=26, c=al.GREEN, marker="s", alpha=0.85, linewidths=0,
                   label="Station entrance ({0})".format(len(other_stops)))
    if rail_stops:
        ax.scatter([s["lon"] for s in rail_stops], [s["lat"] for s in rail_stops],
                   s=150, c=al.RED, marker="*", edgecolors="white", linewidths=0.8,
                   zorder=5, label="Rail station ({0})".format(len(rail_stops)))
        for s in rail_stops:
            ax.annotate(s["name"].replace(" Rail Station", ""),
                        xy=(s["lon"], s["lat"]), xytext=(4, 5),
                        textcoords="offset points", fontsize=7.5, color=al.INK)
    ax.set_aspect(1 / aspect)
    ax.set_xlim(ctx.west, ctx.east)
    ax.set_ylim(ctx.south, ctx.north)
    ax.set_xlabel("Longitude (degrees; negative is west)")
    ax.set_ylabel("Latitude (degrees north)")
    ax.set_title("Public transport access points\n{0}, NaPTAN, retrieved {1}"
                 .format(ctx.place_name, ctx.built_at[:10]), fontsize=11)
    ax.legend(frameon=True, framealpha=0.92, edgecolor="#cccccc",
              fontsize=8.5, loc="upper left")
    ax.grid(alpha=0.15)
    chapter.figures.append(al.Figure(
        al.save(figure, "ch01_stops.png"),
        "Every NaPTAN access point in the patch. Bus stops in blue, rail "
        "stations starred. The blank areas are the subject of the next figure.",
        "Map of bus stops and rail stations across the patch",
    ))

    figure, ax = al.axes(figsize=(8.4, 6.4))
    # The first version ran the scale to 2,000 m when the largest distance in
    # the patch is {0:.0f} m, so nine tenths of the map came out the same pale
    # yellow. A colour scale that separates nothing is a broken figure that
    # no row count can catch.
    top = float(np.ceil(nearest.max() / 100.0) * 100)
    levels = np.arange(0, top + 1, 100)
    contour = ax.contourf(mesh_lon, mesh_lat, nearest, levels=levels,
                          cmap="magma_r", extend="neither")
    ax.contour(mesh_lon, mesh_lat, nearest, levels=[WALK_METRES],
               colors=["#00d0ff"], linewidths=1.6)
    bar = figure.colorbar(contour, ax=ax, pad=0.02)
    bar.set_label("Distance to the nearest stop (metres)", fontsize=9)
    ax.set_aspect(1 / aspect)
    ax.set_xlabel("Longitude (degrees; negative is west)")
    ax.set_ylabel("Latitude (degrees north)")
    ax.set_title("How far to the nearest stop\n{0}. Blue line = {1:.0f} m"
                 .format(ctx.place_name, WALK_METRES), fontsize=11)
    chapter.figures.append(al.Figure(
        al.save(figure, "ch01_coverage.png"),
        "Walking distance to the nearest access point, on a {0:.0f} m grid. "
        "Inside the blue line you are within {1:.0f} m of a stop; {2:.1f}% of "
        "the patch is.".format(GRID_METRES, WALK_METRES,
                               chapter.numbers["covered_pct"]),
        "Heatmap of distance to the nearest stop across the patch",
    ))

    figure, ax = al.axes(figsize=(8.4, 4.2))
    ordered = np.sort(nearest.ravel())
    share = 100.0 * np.arange(1, ordered.size + 1) / ordered.size
    ax.plot(ordered, share, color=al.BLUE, linewidth=2)
    ax.axvline(WALK_METRES, color=al.RED, linewidth=1.2, linestyle="--")
    ax.annotate("{0:.0f} m\n{1:.1f}% of the patch"
                .format(WALK_METRES, chapter.numbers["covered_pct"]),
                xy=(WALK_METRES, chapter.numbers["covered_pct"]),
                xytext=(WALK_METRES + 130, max(12.0, chapter.numbers["covered_pct"] - 34)),
                fontsize=9, color=al.INK,
                arrowprops={"arrowstyle": "-", "color": al.MUTED})
    ax.set_xlim(0, ordered.max() * 1.02)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Distance to the nearest stop (metres)")
    ax.set_ylabel("Share of the patch within that distance (%)")
    ax.set_title("Cumulative access to public transport\n{0}".format(ctx.place_name),
                 fontsize=11)
    chapter.figures.append(al.Figure(
        al.save(figure, "ch01_cumulative.png"),
        "The same information as a curve. The steepness in the first 300 m is "
        "what a dense bus network looks like.",
        "Cumulative share of the patch within a given distance of a stop",
    ))

    # -- hand-checks -------------------------------------------------------

    # Check 1. Leeds City Bus Station is on Dyer Street. This is a fact about
    # the world, not about the file: it can be confirmed on any map, and it
    # is the kind of check an assistant cannot manufacture.
    bus_station_lon, bus_station_lat = -1.5372, 53.7975
    d = al.distance_metres(bus_station_lon, bus_station_lat, slon, slat)
    nearest_stop = stops[int(d.argmin())]
    ctx.check(
        chapter,
        claim="Leeds City Bus Station is in the data",
        against="Its real address on Dyer Street (53.7975 N, 1.5372 W)",
        anchored=True,
        passed=float(d.min()) < 150,
        detail=(
            "The nearest access point to the real bus station is **{0}** "
            "({1}), {2:.0f} m away. Anything under about 150 m is the bus "
            "station itself or a stand inside it."
            .format(nearest_stop["name"], nearest_stop["locality"], float(d.min()))
        ),
    )

    # Check 2. Leeds station must be here. Adding area 910 is the whole
    # reason it is; see the plan correction below.
    names = " | ".join(s["name"].lower() for s in rail_stops)
    ctx.check(
        chapter,
        claim="Leeds Rail Station is in the data",
        against="It exists, and it is the busiest station in the North outside Manchester",
        anchored=True,
        passed="leeds rail station" in names,
        detail=(
            "Rail stations found in the patch: {0}."
            .format(", ".join(sorted(s["name"] for s in rail_stops)) or "none")
        ),
    )

    # Check 3. Internal only: the filter did what a filter does.
    kept_inside = bool(
        (slat >= ctx.south).all() and (slat <= ctx.north).all()
        and (slon >= ctx.west).all() and (slon <= ctx.east).all()
    )
    ctx.check(
        chapter,
        claim="Every kept stop is inside the bounding box",
        against="The box coordinates themselves",
        anchored=False,
        passed=kept_inside,
        detail="Tests the filter, not the data. It would pass just as happily "
               "on the wrong ATCO area.",
    )

    # Check 4. Density, against a plausible urban range.
    ctx.check(
        chapter,
        claim="Stop density is credible for an English city",
        against="A plausible urban range of 5–40 stops per km²",
        anchored=True,
        passed=5 <= density <= 40,
        detail="{0:.1f} stops per km² across {1:.0f} km².".format(density, ctx.area_km2),
    )

    # Check 5. Added after looking at the first version of the map, where ten
    # stops were in the data, in the counts, and on no figure at all.
    ctx.check(
        chapter,
        claim="Every stop appears in exactly one category on the map",
        against="The category counts, summed against the total",
        anchored=False,
        passed=partitioned == len(stops),
        detail=(
            "{0:,} bus + {1} rail + {2} other = {3:,}, against {4:,} stops. "
            "The 'other' category is {5}, which the first version of this "
            "chapter drew nowhere."
            .format(len(bus_stops), len(rail_stops), len(other_stops),
                    partitioned, len(stops),
                    ", ".join("{0} ({1})".format(
                        STOP_TYPE_NAMES.get(k, k), k) for k in other_kinds)
                    or "empty")
        ),
    )

    # -- narrative ---------------------------------------------------------

    chapter.sections = [
        ("The query that looks right and is not", """
My plan said: fetch ATCO area 450, cut to the box, draw the stops. I ran it,
got **{bus:,} bus stops**, and the map looked entirely convincing.

Then I ran hand-check 2 — *Leeds Rail Station must be in here* — and it
failed. Not because of a bug. Because **NaPTAN does not put rail stations in
the local authority area at all.** Every railway station in Great Britain
lives in area **910**, a national pseudo-area, and a query for West Yorkshire
returns none of them.

This is the most instructive thing that happened in the whole build, so it is
worth being precise about why it is dangerous:

- Nothing failed. No traceback, no empty table, no zero row count.
- The map looked *better* without the stations, because {bus:,} evenly spread
  blue dots look like a complete network.
- Every summary statistic was internally consistent.
- An atlas of public transport in Leeds would have been published with Leeds
  Rail Station missing from it.

The row counts — layer 2 of the quality control — could never have caught
this, because the rows that were missing were never there to be counted. Only
a check anchored outside the data caught it: *a station I know exists is not
in my file.*
""".format(bus=len(bus_stops))),

        ("What the patch actually contains", """
With area 910 added, the patch holds **{stops:,} access points**: {bus:,} bus
stops, {rail} rail stations and {other} station entrances. Those three
numbers add to the total, which is a property this chapter had to be forced
to have — see the second correction below.

That is **{density:.1f} stops per km²** over {area:.0f} km², which is a dense
network by British standards and unremarkable for a core city.

Density on its own is a poor description, though. It is an average, and an
average over a rectangle tells you nothing about the corner of the rectangle
where nobody can catch anything. So the second figure asks a better question:
**from any point in the patch, how far is the nearest stop?**

A 200 m grid over the box, and a distance from each grid point to the nearest
access point. The answer is that **{covered:.1f}% of the patch is within
{walk:.0f} m of a stop** — roughly a five-minute walk — with a median distance
of **{median:.0f} m**.

The worst-served point in the patch is {worst:.0f} m from anything, at
{wlat:.4f} N, {wlon:.4f} W.
""".format(stops=len(stops), bus=len(bus_stops), rail=len(rail_stops),
           other=len(other_stops), density=density, area=ctx.area_km2,
           covered=chapter.numbers["covered_pct"], walk=WALK_METRES,
           median=chapter.numbers["median_m"], worst=worst,
           wlat=worst_lat, wlon=abs(worst_lon))),

        ("Degrees are not metres", """
Every distance on this page is in metres, and getting there took one function
rather than one line.

Coordinates arrive in degrees. At this latitude one degree of latitude is
about **111.1 km**, while one degree of longitude is about **{lon_km:.1f} km**,
because the meridians have converged by 53.8° north. Pythagoras on raw degrees
therefore stretches every east–west distance by a factor of about
**{ratio:.2f}** and produces numbers that are wrong, plausible, and in no
units at all.

`atlaslib.distance_metres` converts both axes before it measures. Hand-check 6,
in chapter 2, tests it against a distance I worked out independently.
""".format(lon_km=al.metres_per_degree_lon(53.79) / 1000,
           ratio=al.METRES_PER_DEGREE_LAT / al.metres_per_degree_lon(53.79))),
    ]

    chapter.findings = [
        "The patch contains **{0:,} public transport access points** — {1:,} bus "
        "stops and {2} rail stations — at {3:.1f} per km²."
        .format(len(stops), len(bus_stops), len(rail_stops), density),
        "**{0:.1f}% of the patch is within {1:.0f} m of a stop**, with a median "
        "walk of {2:.0f} m. Access to *something* is close to universal here."
        .format(chapter.numbers["covered_pct"], WALK_METRES, chapter.numbers["median_m"]),
        "The gaps are not distributed evenly: the worst-served point is "
        "{0:.0f} m from any access point, which is a fifteen-minute walk before "
        "the journey starts.".format(worst),
    ]

    chapter.caveats = [
        "A stop is not a service. NaPTAN records where you *could* board, not "
        "whether anything stops there, how often, or at what time of day. A "
        "stop served twice a day counts the same as one served every four "
        "minutes.",
        "Distance here is straight-line, not walked. Real walking distance is "
        "longer wherever a river, a railway or a dual carriageway is in the "
        "way — and this patch contains all three.",
        "The 400 m threshold is a convention, not a finding. It is roughly a "
        "five-minute walk on the flat, and Leeds is not flat.",
    ]

    chapter.plan_notes = [
        """**Plan §2 said chapter 1 answers "where can you catch something".
It planned a single query: ATCO area 450.**

Area 450 contains bus stops only. Rail stations are in area 910. The plan
would have produced a public transport atlas with no railway in it, and
nothing in the build would have complained.

Fixed by fetching both areas. The hand-check that caught it was written
*before* the code, in plan §5, which is the only reason it was ever run.""",

        """**Plan §6 listed "a figure is wrong but the script succeeds" as a
high risk. It happened on the first figure I drew.**

The first version of the map had two categories, bus and rail. Ten stops in
the patch are typed `RSE`, a rail station entrance, and belonged to neither.
They were fetched, they passed the filters, they were counted in every row
count on this page — and they were drawn nowhere.

Nothing failed. The count of stops was right. The legend added up to ten less
than the total, which is the only visible trace it left, and I found it by
reading the legend rather than by any check.

Fixed by making the categories a partition and adding check 5, which asserts
that they sum to the total. The lesson is the one the risk table already
predicted: **open the figure and look at it.**""",

        """**The first coverage map was a broken figure that ran perfectly.**

I set the colour scale to run from 0 to 2,000 m. The largest distance in the
patch is {0:.0f} m, so about nine tenths of the map came out in the same pale
yellow and the figure separated nothing.

A colour scale is a claim about the range of your data. This one was a claim
about a range that does not exist here. Fixed by fitting the levels to the
data and using a scale with more contrast.""".format(worst),

        """**Prediction P1 said the patch would hold between 800 and 1,600
NaPTAN stops. The answer is {0:,}.**

{1}""".format(len(stops),
              "Inside the range, but for the wrong reason: I was predicting bus "
              "stops without realising rail was a separate query. The prediction "
              "was right and the reasoning behind it was wrong, which is worth "
              "less than it looks."
              if 800 <= len(stops) <= 1600 else
              "Outside the range I predicted."),
    ]

    return chapter
