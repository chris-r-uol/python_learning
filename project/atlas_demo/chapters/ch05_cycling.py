"""
Chapter 5 — Cycling potential.

Question: what could cycling here be, rather than what it is?

The Propensity to Cycle Tool models how many people would cycle to work on
each segment of the road network under different scenarios. Every other
chapter in this atlas measures something that happened. This one measures
something that has not.

Its region names are historic counties, which is why Bristol is `avon`.
"""

import numpy as np

import atlaslib as al

PCT_REGION = "west-yorkshire"
PCT_URL = ("https://npttile.vs.mythic-beasts.com/commute/v2/{region}/rnet.geojson"
           .format(region=PCT_REGION))

SCENARIOS = [
    ("bicycle", "Today", al.MUTED),
    ("govtarget_slc", "Government target", al.BLUE),
    ("dutch_slc", "Dutch scenario", al.GREEN),
]

LEAD = """
Every dataset so far has been a record. This one is a model.

The Propensity to Cycle Tool takes census commuting flows, the distance and
hilliness of each trip, and asks how many of those journeys would be cycled if
the population behaved as it does in a different policy world. The **Dutch
scenario** applies Dutch cycling rates for the same distances and gradients to
the English population.

That is a useful question and it is not a forecast. Nothing here says cycling
will rise. It says how much of the current commuting pattern is, on the
evidence of another country, cyclable.
""".strip()


def build(ctx):
    chapter = al.Chapter(
        number=5,
        slug="chapter-05",
        title="Cycling potential",
        question="What could cycling here be, rather than what it is?",
        lead=LEAD,
    )

    network = ctx.fetch(
        key="pct_rnet",
        name="Propensity to Cycle Tool, commute route network, {0}".format(PCT_REGION),
        url=PCT_URL,
        licence="OGL v3.0 / see pct.bike",
        cache_file="pct_rnet.geojson",
        parse=al.parse_geojson,
    )

    # -- cut ---------------------------------------------------------------

    features = network["features"]
    segments = []
    for feature in features:
        geometry = feature.get("geometry") or {}
        if geometry.get("type") != "LineString":
            continue
        coords = geometry.get("coordinates") or []
        if len(coords) < 2:
            continue
        lons = np.array([c[0] for c in coords], dtype=float)
        lats = np.array([c[1] for c in coords], dtype=float)
        if not ctx.inside(lons, lats).any():
            continue
        # Segment length in metres, summed along the line. Degrees converted
        # before measuring, as everywhere else in the atlas.
        length = float(al.distance_metres(lons[:-1], lats[:-1],
                                          lons[1:], lats[1:]).sum())
        props = feature.get("properties") or {}
        segments.append({
            "lons": lons, "lats": lats, "length_m": length,
            "bicycle": al.to_float(props.get("bicycle"), 0.0),
            "govtarget_slc": al.to_float(props.get("govtarget_slc"), 0.0),
            "dutch_slc": al.to_float(props.get("dutch_slc"), 0.0),
        })
    ctx.counted(chapter, "Network segments touching the patch",
                len(features), len(segments))

    if not segments:
        raise SystemExit("Chapter 5: no network segments. Check the PCT region name.")

    lengths = np.array([s["length_m"] for s in segments])
    total_km = float(lengths.sum() / 1000.0)

    # Cyclist-kilometres: the sensible way to total a network, because a
    # 20 m link with 50 cyclists is not comparable to a 2 km one with 50.
    totals = {}
    for key, label, _ in SCENARIOS:
        flows = np.array([s[key] for s in segments])
        totals[key] = float((flows * lengths / 1000.0).sum())

    today = totals["bicycle"]
    dutch = totals["dutch_slc"]
    govtarget = totals["govtarget_slc"]
    multiple = dutch / today if today > 0 else float("nan")

    with_any = int((np.array([s["dutch_slc"] for s in segments]) > 0).sum())
    ctx.counted(chapter, "Segments with any modelled Dutch-scenario cycling",
                len(segments), with_any)

    chapter.numbers = {
        "segments": len(segments),
        "network_km": total_km,
        "today_km": today,
        "govtarget_km": govtarget,
        "dutch_km": dutch,
        "multiple": multiple,
    }

    # -- figures -----------------------------------------------------------

    aspect = al.metres_per_degree_lon((ctx.south + ctx.north) / 2) / al.METRES_PER_DEGREE_LAT
    dutch_flows = np.array([s["dutch_slc"] for s in segments])
    top = float(np.percentile(dutch_flows[dutch_flows > 0], 97)) if (dutch_flows > 0).any() else 1.0

    figure, ax = al.axes(figsize=(8.4, 6.4))
    order = np.argsort(dutch_flows)
    cmap = matplotlib_cm()
    for index in order:
        segment = segments[index]
        value = min(segment["dutch_slc"], top) / top if top else 0
        ax.plot(segment["lons"], segment["lats"],
                color=cmap(value),
                linewidth=0.35 + 2.6 * value,
                alpha=0.35 + 0.6 * value,
                solid_capstyle="round")
    ax.set_aspect(1 / aspect)
    ax.set_xlim(ctx.west, ctx.east)
    ax.set_ylim(ctx.south, ctx.north)
    ax.set_xlabel("Longitude (degrees; negative is west)")
    ax.set_ylabel("Latitude (degrees north)")
    ax.set_title("Modelled cycling under the Dutch scenario\n{0}. PCT commute "
                 "route network".format(ctx.place_name), fontsize=11)
    import matplotlib as mpl
    norm = mpl.colors.Normalize(vmin=0, vmax=top)
    bar = figure.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                          ax=ax, pad=0.02, extend="max")
    bar.set_label("Modelled cyclists per day on the segment", fontsize=9)
    chapter.figures.append(al.Figure(
        al.save(figure, "ch05_network.png"),
        "The commuter cycling network the Dutch scenario implies. Line width "
        "and colour both carry the modelled flow, so the corridors are legible "
        "in greyscale as well as in colour.",
        "Map of the modelled cycling network under the Dutch scenario",
    ))

    figure, ax = al.axes(figsize=(8.4, 4.4))
    labels = [label for _, label, _ in SCENARIOS]
    values = [totals[key] for key, _, _ in SCENARIOS]
    colours = [colour for _, _, colour in SCENARIOS]
    bars = ax.bar(labels, values, color=colours, width=0.6)
    ax.bar_label(bars, fmt="%.0f", fontsize=9, padding=3)
    ax.set_ylabel("Cyclist-kilometres per day on the patch network")
    ax.set_xlabel("Scenario")
    ax.set_ylim(0, max(values) * 1.18)
    ax.set_title("Cycling today, and under two scenarios\n{0}, PCT commute model"
                 .format(ctx.place_name), fontsize=11)
    chapter.figures.append(al.Figure(
        al.save(figure, "ch05_scenarios.png"),
        "Daily cyclist-kilometres across the patch network. Cyclist-kilometres "
        "rather than cyclists, because a busy 20 m link and a busy 2 km "
        "corridor are not the same amount of cycling.",
        "Bar chart comparing cycling today with two modelled scenarios",
    ))

    # -- hand-checks -------------------------------------------------------

    ordering_ok = today <= govtarget <= dutch
    ctx.check(
        chapter,
        claim="The scenario columns are the right way round",
        against="The definitions: today ≤ government target ≤ Dutch, by construction",
        anchored=True,
        passed=ordering_ok,
        detail=(
            "Today **{0:,.0f}**, government target **{1:,.0f}**, Dutch "
            "**{2:,.0f}** cyclist-km per day. The Dutch scenario cannot be "
            "below today's level; if this ordering broke, the columns would be "
            "misread and every sentence here would invert."
            .format(today, govtarget, dutch)
        ),
    )

    ctx.check(
        chapter,
        claim="Segment lengths are in metres and are plausible",
        against="A city network: total length of the same order as the patch size",
        anchored=True,
        passed=10 <= total_km <= 2000,
        detail=(
            "{0:,.0f} km of network across {1:.0f} km² of city. Degrees treated "
            "as metres would have produced a total near {2:.2f}."
            .format(total_km, ctx.area_km2, total_km / 111.0)
        ),
    )

    ctx.check(
        chapter,
        claim="The region name is the right one",
        against="A non-empty network inside the patch",
        anchored=False,
        passed=len(segments) > 100,
        detail=(
            "`{0}` returned {1:,} segments touching the patch. PCT regions are "
            "**historic counties**: Leeds is `west-yorkshire`, but Bristol is "
            "`avon`, a county abolished in 1996. A wrong region name returns a "
            "valid, empty answer."
            .format(PCT_REGION, len(segments))
        ),
    )

    # -- narrative ---------------------------------------------------------

    chapter.sections = [
        ("A model, not a measurement", """
This is the only chapter in the atlas whose subject does not exist.

The PCT starts from Census commuting flows — real journeys between real
places — and asks a counterfactual: if the people making these journeys
cycled at the rates seen in the Netherlands for the same distances and
gradients, how many would cycle?

The answer for this patch: cycling today is about **{today:,.0f}
cyclist-kilometres a day** on the modelled commute network. Under the Dutch
scenario it is **{dutch:,.0f}** — about **{multiple:.1f} times** as much. The
government target scenario sits between, at **{gov:,.0f}**.

Three things that number is not:

- **Not a forecast.** Nothing predicts this will happen.
- **Not all cycling.** The commute layer covers journeys to work. Shopping,
  school and leisure trips are absent, and they are most of all cycling.
- **Not evenly available.** The model applies national relationships to local
  distances and hills. A corridor with high modelled potential and a hostile
  road is still a hostile road.
""".format(today=today, dutch=dutch, gov=govtarget, multiple=multiple)),

        ("Historic counties", """
The PCT publishes by region, and its regions are **historic counties**. Leeds
is in `west-yorkshire`, which is guessable. Bristol is in `avon` — a county
abolished in 1996 — which is not.

Ask an assistant for the PCT region name for Bristol and you will get
`bristol`, confidently. The request succeeds in the sense that it returns
something, and the something contains no segments, and a chapter built on it
produces an empty map rather than an error.

Hand-check 17 exists for exactly that: it asserts that the region returned a
network at all.
"""),

        ("Why cyclist-kilometres", """
The obvious way to total a network is to add up the flow on every segment.
That is wrong, and wrong in a way that flatters dense city centres.

Segments are not the same length. A 20 m link outside a station with 50
modelled cyclists is not the same quantity of cycling as a 2 km corridor with
50. Summing the flows treats them as equal.

So every total on this page is **flow × length**, in cyclist-kilometres per
day. The patch network is **{km:,.0f} km** long across {segments:,} segments,
and the totals are weighted by that length throughout.
""".format(km=total_km, segments=len(segments))),
    ]

    chapter.findings = [
        "The modelled commute network in the patch carries about **{0:,.0f} "
        "cyclist-kilometres a day today**, rising to **{1:,.0f}** under the "
        "Dutch scenario — a factor of **{2:.1f}**."
        .format(today, dutch, multiple),
        "**{0:,} segments** covering **{1:,.0f} km** of network fall inside the "
        "patch, of which {2:,} carry modelled cycling under the Dutch scenario."
        .format(len(segments), total_km, with_any),
        "The potential is concentrated on a small number of corridors rather "
        "than spread evenly, which is what makes the map more useful than the "
        "total.",
    ]

    chapter.caveats = [
        "Commuting only. The PCT commute layer models journeys to work, which "
        "are a minority of all trips and a small minority of cycling trips.",
        "Based on Census travel-to-work data, which is now several years old "
        "and was collected during a period of unusual working patterns.",
        "A scenario is not a plan. High modelled potential on a road with no "
        "cycling provision describes demand, not feasibility.",
        "Segments touching the patch are counted whole. A corridor that enters "
        "the box for 100 m contributes its full length here.",
    ]

    chapter.plan_notes.append(
        """**Prediction P5 said the Dutch scenario would be at least 5× current
cycling. The measured multiple is {0:.1f}×.**

{1}""".format(multiple,
              "Correct." if multiple >= 5 else
              "Wrong, and instructively so. Leeds already has more commuter "
              "cycling than I assumed when I wrote the prediction, so the "
              "multiplier is smaller. A prediction about a ratio is a "
              "prediction about both of its numbers, and I only thought about "
              "one of them.")
    )

    return chapter


def matplotlib_cm():
    """The colour ramp for the network map, kept out of the drawing loop."""
    import matplotlib
    return matplotlib.colormaps["plasma"]
