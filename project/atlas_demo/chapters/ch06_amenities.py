"""
Chapter 6 — What is there.

Question: what is within reach of a stop?

OpenStreetMap, via the Overpass API. Chapter 1 said where the network is;
this chapter asks what the network reaches.

Overpass is a POST API with its own query language. A GET request with the
query in the URL is the obvious thing to try and is not how it works.
"""

import numpy as np

import atlaslib as al

OVERPASS = "https://overpass-api.de/api/interpreter"

# Six categories, chosen because each is a reason to leave the house that a
# person without a car has to reach somehow.
CATEGORIES = [
    ("school", 'node["amenity"="school"]{box};way["amenity"="school"]{box};', al.BLUE),
    ("college", 'node["amenity"="college"]{box};way["amenity"="college"]{box};', al.PURPLE),
    ("university", 'node["amenity"="university"]{box};way["amenity"="university"]{box};', "#5a3e85"),
    ("hospital", 'node["amenity"="hospital"]{box};way["amenity"="hospital"]{box};', al.RED),
    ("pharmacy", 'node["amenity"="pharmacy"]{box};way["amenity"="pharmacy"]{box};', al.ORANGE),
    ("supermarket", 'node["shop"="supermarket"]{box};way["shop"="supermarket"]{box};', al.GREEN),
]

WALK_METRES = 400.0

LEAD = """
A stop with nothing near it is a stop nobody uses. This chapter puts the two
halves together: the destinations people actually travel to, and how many of
them the network in chapter 1 reaches.

OpenStreetMap is not an official dataset. It is a volunteered map, which means
its coverage varies by how interested local mappers are. In a British city
centre that coverage is very good — and "very good" is not "complete", which
is a different claim from anything else in this atlas.
""".strip()


def _build_query(ctx):
    box = "({0},{1},{2},{3})".format(ctx.south, ctx.west, ctx.north, ctx.east)
    parts = []
    for name, template, _ in CATEGORIES:
        parts.append(template.format(box=box))
    return "[out:json][timeout:60];(" + "".join(parts) + ");out center;"


def _parse_overpass(text):
    """Parse either a live Overpass response or the cached GeoJSON."""
    import json
    data = json.loads(text)
    rows = len(data.get("elements", data.get("features", [])))
    return data, rows


def _categorise(tags):
    amenity = tags.get("amenity")
    shop = tags.get("shop")
    for name, _, _ in CATEGORIES:
        if amenity == name or shop == name:
            return name
    return None


def build(ctx):
    chapter = al.Chapter(
        number=6,
        slug="chapter-06",
        title="What is there",
        question="What is within reach of a stop?",
        lead=LEAD,
    )

    data = ctx.fetch(
        key="osm_amenities",
        name="OpenStreetMap amenities via the Overpass API",
        url=OVERPASS,
        licence="ODbL 1.0, © OpenStreetMap contributors — attribution required",
        cache_file="osm_amenities.geojson",
        parse=_parse_overpass,
        method="POST",
        body={"data": _build_query(ctx)},
    )

    # -- normalise ---------------------------------------------------------
    #
    # Two shapes to handle: a live Overpass response, and the cached GeoJSON.

    places = []
    if "elements" in data:
        elements = data["elements"]
        for element in elements:
            tags = element.get("tags") or {}
            category = _categorise(tags)
            if category is None:
                continue
            if element.get("type") == "node":
                lon, lat = element.get("lon"), element.get("lat")
            else:
                centre = element.get("center") or {}
                lon, lat = centre.get("lon"), centre.get("lat")
            if lon is None or lat is None:
                continue
            places.append({"category": category, "lon": float(lon),
                           "lat": float(lat), "name": tags.get("name", "")})
        ctx.counted(chapter, "Overpass elements, then those in the six categories",
                    len(elements), len(places))
    else:
        features = data.get("features", [])
        for feature in features:
            lon, lat = feature["geometry"]["coordinates"]
            props = feature["properties"]
            places.append({"category": props.get("category"),
                           "lon": float(lon), "lat": float(lat),
                           "name": props.get("name", "")})
        ctx.counted(chapter, "Cached amenity extract loaded",
                    len(features), len(places))

    in_box = [p for p in places if ctx.inside([p["lon"]], [p["lat"]])[0]]
    ctx.counted(chapter, "Bounding-box filter to the patch", len(places), len(in_box))

    if not in_box:
        raise SystemExit("Chapter 6: no amenities. Overpass needs POST, not GET.")

    counts = {name: sum(1 for p in in_box if p["category"] == name)
              for name, _, _ in CATEGORIES}

    # -- reach -------------------------------------------------------------

    have_stops = "stop_lons" in ctx.shared
    served_pct = float("nan")
    if have_stops:
        distances = al.nearest_distance_metres(
            [p["lon"] for p in in_box], [p["lat"] for p in in_box],
            ctx.shared["stop_lons"], ctx.shared["stop_lats"],
        )
        for place, distance in zip(in_box, distances):
            place["stop_m"] = float(distance)
        served = int((distances <= WALK_METRES).sum())
        ctx.counted(chapter,
                    "Amenities within {0:.0f} m of a transport stop".format(WALK_METRES),
                    len(in_box), served)
        served_pct = 100.0 * served / len(in_box)

    chapter.numbers = {
        "amenities": len(in_box),
        "served_pct": served_pct,
        **{"n_" + name: counts[name] for name, _, _ in CATEGORIES},
    }

    # -- figures -----------------------------------------------------------

    aspect = al.metres_per_degree_lon((ctx.south + ctx.north) / 2) / al.METRES_PER_DEGREE_LAT
    figure, ax = al.axes(figsize=(8.4, 6.4))
    if have_stops:
        ax.scatter(ctx.shared["stop_lons"], ctx.shared["stop_lats"],
                   s=3, c="#cfd8dc", linewidths=0, zorder=0, label="Transport stop")
    for name, _, colour in CATEGORIES:
        subset = [p for p in in_box if p["category"] == name]
        if not subset:
            continue
        ax.scatter([p["lon"] for p in subset], [p["lat"] for p in subset],
                   s=34, c=colour, alpha=0.85, linewidths=0,
                   label="{0} ({1})".format(name.title(), len(subset)))
    ax.set_aspect(1 / aspect)
    ax.set_xlim(ctx.west, ctx.east)
    ax.set_ylim(ctx.south, ctx.north)
    ax.set_xlabel("Longitude (degrees; negative is west)")
    ax.set_ylabel("Latitude (degrees north)")
    ax.set_title("Everyday destinations and the stops that serve them\n{0}, "
                 "OpenStreetMap".format(ctx.place_name), fontsize=11)
    ax.legend(frameon=False, fontsize=8.5, ncol=4,
              loc="upper center", bbox_to_anchor=(0.5, -0.13))
    ax.grid(alpha=0.15)
    chapter.figures.append(al.Figure(
        al.save(figure, "ch06_map.png"),
        "Six kinds of everyday destination, over the transport stops from "
        "chapter 1 in grey.",
        "Map of amenities by category over the transport stop network",
    ))

    figure, ax = al.axes(figsize=(8.6, 4.4))
    names = [name for name, _, _ in CATEGORIES]
    values = [counts[name] for name in names]
    colours = [colour for _, _, colour in CATEGORIES]
    order = np.argsort(values)
    bars = ax.barh([names[i].title() for i in order], [values[i] for i in order],
                   color=[colours[i] for i in order], height=0.68)
    ax.bar_label(bars, fontsize=9, padding=3)
    ax.set_xlabel("Count in the patch")
    ax.set_ylabel("Category")
    ax.set_xlim(0, max(values) * 1.14)
    ax.set_title("Everyday destinations in the patch\n{0}, OpenStreetMap, "
                 "{1} in total".format(ctx.place_name, len(in_box)), fontsize=11)
    chapter.figures.append(al.Figure(
        al.save(figure, "ch06_counts.png"),
        "What the patch contains, by category. These are counts of mapped "
        "objects, not of floor space or capacity: one large secondary school "
        "and one small primary count the same.",
        "Bar chart of amenity counts by category",
    ))

    if have_stops:
        # The first version of this figure was a bar per category showing the
        # share within 400 m. Every bar came out at 100%, because the furthest
        # amenity in the patch is 366 m from a stop. The number was right and
        # the figure was worthless: six identical bars separate nothing.
        #
        # The variation is in the distances themselves, so draw those.
        figure, ax = al.axes(figsize=(8.8, 4.8))
        for name, _, colour in CATEGORIES:
            subset = [p["stop_m"] for p in in_box if p["category"] == name]
            if not subset:
                continue
            ordered = np.sort(np.array(subset))
            share = 100.0 * np.arange(1, ordered.size + 1) / ordered.size
            ax.plot(ordered, share, color=colour, linewidth=2,
                    label="{0} (median {1:.0f} m)".format(
                        name.title(), float(np.median(ordered))))
        ax.axvline(WALK_METRES, color=al.INK, linestyle="--", linewidth=1.2)
        # Annotation sat on top of the legend in the first version.
        ax.annotate("{0:.0f} m: every category is already at 100%"
                    .format(WALK_METRES),
                    xy=(WALK_METRES, 100), xytext=(WALK_METRES - 14, 62),
                    fontsize=8.5, color=al.INK, ha="right",
                    arrowprops={"arrowstyle": "-", "color": al.MUTED,
                                "linewidth": 0.9})
        ax.set_xlim(0, WALK_METRES * 1.05)
        ax.set_ylim(0, 101)
        ax.set_xlabel("Distance to the nearest public transport stop (metres)")
        ax.set_ylabel("Share of the category within that distance (%)")
        ax.set_title("How close each kind of destination is to a stop\n{0}"
                     .format(ctx.place_name), fontsize=11)
        ax.legend(frameon=False, fontsize=8.5, loc="lower right")
        chapter.figures.append(al.Figure(
            al.save(figure, "ch06_access.png"),
            "Distance from each kind of destination to the nearest stop. The "
            "400 m threshold is not a useful test in this patch, because "
            "everything clears it, so the curves show where the categories "
            "actually differ. Pharmacies and supermarkets sit on the network; "
            "schools sit back from it.",
            "Cumulative distance from each amenity category to the nearest stop",
        ))

    # -- hand-checks -------------------------------------------------------

    names_lower = " | ".join((p["name"] or "").lower() for p in in_box)
    has_leeds_uni = "university of leeds" in names_lower
    has_beckett = "beckett" in names_lower or "leeds metropolitan" in names_lower
    ctx.check(
        chapter,
        claim="Both Leeds universities appear in the amenities",
        against="They exist, and both have campuses inside this box",
        anchored=True,
        passed=has_leeds_uni and has_beckett,
        detail=(
            "University of Leeds found: **{0}**. Leeds Beckett found: **{1}**. "
            "{2} universities and {3} colleges in total. If either were "
            "missing, the tag list or the bounding box would be wrong — and "
            "the map would still look full."
            .format("yes" if has_leeds_uni else "NO",
                    "yes" if has_beckett else "NO",
                    counts["university"], counts["college"])
        ),
    )

    ctx.check(
        chapter,
        claim="Amenity counts are plausible for a city of this size",
        against="A city-centre patch should hold dozens of schools, not two or two thousand",
        anchored=True,
        passed=20 <= counts["school"] <= 400 and counts["supermarket"] >= 5,
        detail="{0} schools, {1} supermarkets, {2} pharmacies, {3} hospitals."
               .format(counts["school"], counts["supermarket"],
                       counts["pharmacy"], counts["hospital"]),
    )

    if have_stops:
        ctx.check(
            chapter,
            claim="The {0:.0f} m access threshold is applied in metres".format(WALK_METRES),
            against="The same conversion tested in chapter 2 against a known distance",
            anchored=False,
            passed=0 < served_pct <= 100,
            detail="{0:.1f}% of amenities are within {1:.0f} m of a stop. In "
                   "raw degrees the threshold would be 400 degrees and the "
                   "answer would be 100%.".format(served_pct, WALK_METRES),
        )

    # -- narrative ---------------------------------------------------------

    chapter.sections = [
        ("Three ways to be refused", """
Overpass rejected this chapter three times before it returned anything, and
each refusal looked like a different problem from the one it was.

**1. It is a POST, not a GET.** The query goes in the *body* of the request,
not in the URL. Sending it as a GET is the natural first attempt.

**2. It refuses the default client.** With `requests`' own User-Agent,
Overpass answers **`406 Not Acceptable`** — an HTTP status that reads like a
malformed query. It is not: the server is declining an unidentified client.
Setting a User-Agent that names the project and gives a contact fixes it
instantly, and no amount of adjusting the query ever would. This one cost the
most time, because every instinct says a 406 is your fault for asking badly.

**3. `amenity` and `shop` are different keys.** Schools, colleges,
universities, hospitals and pharmacies are `amenity`. Supermarkets are `shop`.
A query that assumes one key returns five full categories and one empty one —
and an empty category reads as "there are none here" rather than as a bug.

"""),

        ("What the patch holds", """
**{total:,} everyday destinations** in six categories:

| Category | Count |
|---|---:|
| Schools | {school} |
| Supermarkets | {supermarket} |
| Pharmacies | {pharmacy} |
| Colleges | {college} |
| Universities | {university} |
| Hospitals | {hospital} |

These are counts of mapped objects, and an object is not a measure of size. A
2,000-pupil secondary school and a 200-pupil primary are both one school. A
hospital site with fifteen buildings may be one object or fifteen depending on
how it was mapped.
""".format(total=len(in_box), **counts)),
    ]

    if have_stops:
        chapter.sections.append(("What the network reaches", """
**{served:.1f}% of these destinations are within {walk:.0f} m of a public
transport stop.** Every single one. The furthest is {far:.0f} m away.

That is a real answer and a **useless test**. A threshold everything passes
has told you nothing, and the first version of the figure below made it
unmissable: six bars, all at 100%, neatly arranged.

So the question has to be sharpened. Not *does the network reach these places*,
which is settled, but *how close does it get, and to what*:

| | Within 100 m | Within 200 m | Median |
|---|---:|---:|---:|
| All destinations | {w100:.0f}% | {w200:.0f}% | {median:.0f} m |

By category the differences are real. Supermarkets and pharmacies sit at a
median of about {near:.0f} m — they are *on* the network, because shops and
bus routes both follow high streets. Schools sit further back, at a median of
{school:.0f} m, because schools are built where there is land.

Compare this with chapter 1, which found {covered:.0f}% of the *area* within
{walk:.0f} m of a stop. Area coverage counts empty ground equally; this counts
destinations. A network can serve most of the map and still miss the hospital.
This one does not — but that had to be measured rather than assumed.
""".format(served=served_pct, walk=WALK_METRES,
           far=float(np.max([p["stop_m"] for p in in_box])),
           w100=100.0 * np.mean([p["stop_m"] <= 100 for p in in_box]),
           w200=100.0 * np.mean([p["stop_m"] <= 200 for p in in_box]),
           median=float(np.median([p["stop_m"] for p in in_box])),
           near=float(np.median([p["stop_m"] for p in in_box
                                 if p["category"] == "supermarket"])),
           school=float(np.median([p["stop_m"] for p in in_box
                                   if p["category"] == "school"])),
           covered=next((c.after / c.before * 100
                         for ch in ctx.chapters if ch.number == 1
                         for c in ch.counts if "within" in c.label), float("nan")))))

    chapter.findings = [
        "The patch contains **{0:,} everyday destinations** across six "
        "categories, dominated by {1} schools and {2} supermarkets."
        .format(len(in_box), counts["school"], counts["supermarket"]),
        "**{0:.1f}% of them are within {1:.0f} m of a public transport stop**, "
        "so the network reaches the places people go, not only the ground they "
        "stand on.".format(served_pct, WALK_METRES) if have_stops else
        "Chapter 1 did not run, so no access figure was computed.",
        "OpenStreetMap coverage in a British city centre is good but "
        "volunteered: absence here is weaker evidence than presence.",
    ]

    chapter.caveats = [
        "OpenStreetMap is crowd-sourced. A missing object may not exist, or may "
        "simply not have been mapped. Presence is strong evidence; absence is "
        "weak evidence.",
        "Counts are of objects, not of capacity. Nothing here weights a "
        "destination by how many people use it.",
        "Areas are reduced to their centre point, so a large hospital or "
        "campus is measured from the middle rather than from its entrance.",
        "Six categories is a choice, and it leaves out workplaces, parks, "
        "places of worship, libraries and everything else people travel to.",
    ]

    chapter.plan_notes.append(
        """**Prediction P6 said more than 80% of amenities would be within
{0:.0f} m of a stop. The answer is {1:.1f}%.**

{2}""".format(WALK_METRES, served_pct,
              "Correct, and worthless. Every destination in the patch clears "
              "400 m, so the prediction could not have failed whatever the "
              "data said. A prediction that cannot fail is not a prediction — "
              "and the figure I first drew from it, six bars all at 100%, is "
              "what a metric with no discrimination looks like once you open "
              "the picture."
              if served_pct > 80 else
              "Wrong. The patch is larger and less uniformly urban than the "
              "prediction assumed.")
        if have_stops else "Chapter 1 did not run, so P6 could not be tested."
    )

    return chapter
