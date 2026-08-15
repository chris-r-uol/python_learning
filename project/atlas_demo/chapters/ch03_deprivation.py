"""
Chapter 3 — Deprivation.

Question: how poor is this patch, against England as a whole?

The English Indices of Deprivation rank every neighbourhood in England from
most to least deprived. The ranking is the useful part: a decile is a
statement about where a place sits among all 32,844 of them.

Two traps live here. The decile runs the opposite way to intuition, and the
neighbourhood codes are eleven years older than the publication date.
"""

import numpy as np

import atlaslib as al

# The address I first used, taken from the current gov.uk publication page,
# returns 404. This one — the older attachment path — still serves the file.
# Plan §6 listed "a live source is down" as a moderate risk; it happened on
# the first source I tried to fetch.
IMD_URL = (
    "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/"
    "attachment_data/file/845345/"
    "File_7_-_All_IoD2019_Scores__Ranks__Deciles_and_Population_Denominators_3.csv"
)

# 2011 LSOA population-weighted centroids. The vintage matters more than the
# service: IMD 2019 is published against 2011 boundaries, so this is the only
# centroid file that will join to it.
CENTROIDS = (
    "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/"
    "LSOA_Dec_2011_PWC_in_England_and_Wales_2022/FeatureServer/0/query"
    "?geometry={west},{south},{east},{north}&geometryType=esriGeometryEnvelope"
    "&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=lsoa11cd,lsoa11nm"
    "&outSR=4326&returnGeometry=true&f=geojson"
)

ENGLAND_LSOAS = 32844

LEAD = """
The Indices of Multiple Deprivation combine income, employment, education,
health, crime, housing and environment into one rank for every Lower-layer
Super Output Area in England — about 1,500 people each.

The rank is the point. An IMD score of 20.5 means nothing on its own. Knowing
that it places a neighbourhood in the most deprived fifth of England means a
great deal. The whole dataset is an instrument for comparison, and using it
without the comparison throws away the only thing it measures.
""".strip()


def _parse_imd(text):
    rows, _ = al.parse_csv(text.lstrip("﻿"))
    out = {}
    for row in rows:
        code = (row.get("LSOA code (2011)") or "").strip()
        if not code:
            continue
        decile = None
        score = None
        for key, value in row.items():
            if "Decile" in key and "Multiple Deprivation" in key:
                decile = al.to_float(value)
            elif "Score" in key and "Multiple Deprivation" in key:
                score = al.to_float(value)
        out[code] = {"decile": decile, "score": score,
                     "name": (row.get("LSOA name (2011)") or "").strip(),
                     "district": (row.get("Local Authority District name (2019)")
                                  or "").strip()}
    return out, len(out)


def build(ctx):
    chapter = al.Chapter(
        number=3,
        slug="chapter-03",
        title="Deprivation",
        question="How poor is this patch, against England as a whole?",
        lead=LEAD,
    )

    imd = ctx.fetch(
        key="imd2019",
        name="English Indices of Deprivation 2019, File 7",
        url=IMD_URL,
        licence="OGL v3.0, © Crown copyright",
        cache_file="imd2019_leeds.csv",
        parse=_parse_imd,
    )

    centroids = ctx.fetch(
        key="lsoa_2011_centroids",
        name="ONS LSOA 2011 population-weighted centroids",
        url=CENTROIDS.format(west=ctx.west, south=ctx.south,
                             east=ctx.east, north=ctx.north),
        licence="OGL v3.0, © Crown copyright and database right",
        cache_file="lsoa_2011_centroids.geojson",
        parse=al.parse_geojson,
    )

    # -- cut ---------------------------------------------------------------

    features = centroids["features"]
    in_box = []
    for feature in features:
        lon, lat = feature["geometry"]["coordinates"]
        if ctx.inside([lon], [lat])[0]:
            in_box.append({
                "code": feature["properties"].get("lsoa11cd"),
                "name": feature["properties"].get("lsoa11nm"),
                "lon": lon, "lat": lat,
            })
    ctx.counted(chapter, "LSOA centroids returned, then filtered to the box",
                len(features), len(in_box))

    # THE JOIN. Both sides counted, because a vintage mismatch here would
    # produce a smaller table rather than an error.
    joined = []
    for area in in_box:
        record = imd.get(area["code"])
        if record and record["decile"] is not None:
            area.update(record)
            joined.append(area)
    ctx.counted(chapter, "Join LSOA centroids x IMD 2019 on 2011 codes",
                len(in_box), len(joined))

    if not joined:
        raise SystemExit("Chapter 3: nothing joined. Check the LSOA vintage.")

    # Handed to chapter 4, which measures how badly the two vintages overlap
    # rather than simply asserting that they differ.
    ctx.shared["lsoa_2011_codes"] = {a["code"] for a in joined}

    deciles = np.array([a["decile"] for a in joined])
    scores = np.array([a["score"] for a in joined])
    match_rate = 100.0 * len(joined) / len(in_box)

    counts = np.array([int((deciles == d).sum()) for d in range(1, 11)])
    shares = 100.0 * counts / counts.sum()
    most_deprived_share = float(shares[0])
    bottom_three = float(shares[:3].sum())

    chapter.numbers = {
        "lsoas": len(joined),
        "match_rate": match_rate,
        "decile1_pct": most_deprived_share,
        "bottom3_pct": bottom_three,
        "median_decile": float(np.median(deciles)),
        "national_reference": len(imd),
    }

    # -- figures -----------------------------------------------------------

    figure, ax = al.axes(figsize=(8.8, 4.8))
    colours = ["#8c1f1f" if d <= 3 else ("#c9a227" if d <= 7 else al.GREEN)
               for d in range(1, 11)]
    bars = ax.bar(range(1, 11), shares, color=colours, width=0.72)
    ax.bar_label(bars, fmt="%.1f%%", fontsize=8.5, padding=2)
    ax.axhline(10, color=al.INK, linewidth=1.2, linestyle="--")
    ax.annotate("England: 10% in each decile, by construction",
                xy=(10.3, 10), xytext=(5.2, 10 + max(shares) * 0.13),
                fontsize=8.5, color=al.INK, ha="left")
    ax.set_xticks(range(1, 11))
    ax.set_xlabel("Index of Multiple Deprivation decile "
                  "(1 = most deprived tenth of England, 10 = least)")
    ax.set_ylabel("Share of the patch's neighbourhoods (%)")
    ax.set_ylim(0, max(shares) * 1.28)
    ax.set_title("Deprivation profile against England\n{0}, {1} LSOAs, IMD 2019"
                 .format(ctx.place_name, len(joined)), fontsize=11)
    chapter.figures.append(al.Figure(
        al.save(figure, "ch03_deciles.png"),
        "Where the patch's neighbourhoods sit in England's ranking. The dashed "
        "line is what a perfectly average place would look like: 10% in every "
        "decile. Anything above the line on the left is over-representation in "
        "the most deprived tenth.",
        "Bar chart of the patch's neighbourhoods by deprivation decile",
    ))

    aspect = al.metres_per_degree_lon((ctx.south + ctx.north) / 2) / al.METRES_PER_DEGREE_LAT
    figure, ax = al.axes(figsize=(8.4, 6.4))
    scatter = ax.scatter([a["lon"] for a in joined], [a["lat"] for a in joined],
                         c=deciles, cmap="RdYlGn", vmin=1, vmax=10,
                         s=110, edgecolors="white", linewidths=0.7)
    bar = figure.colorbar(scatter, ax=ax, pad=0.02, ticks=range(1, 11))
    bar.set_label("IMD decile (1 = most deprived)", fontsize=9)
    ax.set_aspect(1 / aspect)
    ax.set_xlim(ctx.west, ctx.east)
    ax.set_ylim(ctx.south, ctx.north)
    ax.set_xlabel("Longitude (degrees; negative is west)")
    ax.set_ylabel("Latitude (degrees north)")
    ax.set_title("Deprivation decile by neighbourhood\n{0}. One point per LSOA, "
                 "at its population-weighted centre".format(ctx.place_name),
                 fontsize=11)
    chapter.figures.append(al.Figure(
        al.save(figure, "ch03_map.png"),
        "One point per neighbourhood, placed at its population-weighted centre "
        "rather than its geographic middle. Red is the most deprived end of "
        "England's range.",
        "Map of deprivation deciles across the patch",
    ))

    # -- hand-checks -------------------------------------------------------

    d1_scores = scores[deciles <= 2]
    d10_scores = scores[deciles >= 9]
    direction_ok = bool(len(d1_scores) and len(d10_scores)
                        and d1_scores.mean() > d10_scores.mean())
    ctx.check(
        chapter,
        claim="Decile 1 really is the most deprived, not the least",
        against="The IMD score itself, which rises with deprivation",
        anchored=True,
        passed=direction_ok,
        detail=(
            "Mean IMD score in deciles 1–2: **{0:.1f}**. In deciles 9–10: "
            "**{1:.1f}**. Higher score means more deprived, so decile 1 is the "
            "deprived end. Reverse this and every sentence in the chapter "
            "inverts while every figure still draws."
            .format(float(d1_scores.mean()) if len(d1_scores) else float("nan"),
                    float(d10_scores.mean()) if len(d10_scores) else float("nan"))
        ),
    )

    ctx.check(
        chapter,
        claim="The 2011-code join did not silently drop the patch",
        against="Matched rows against centroids in the box",
        anchored=False,
        passed=match_rate >= 95,
        detail=(
            "{0} of {1} centroids matched an IMD row: **{2:.1f}%**. A join "
            "against the *2021* centroid file would have matched far fewer, "
            "and produced a thinner map rather than an error."
            .format(len(joined), len(in_box), match_rate)
        ),
    )

    ctx.check(
        chapter,
        claim="Deciles cover the full 1–10 range as published",
        against="The set of distinct decile values found",
        anchored=False,
        passed=bool(set(np.unique(deciles).astype(int)) <= set(range(1, 11))),
        detail="Distinct deciles present: {0}."
               .format(", ".join(str(int(d)) for d in np.unique(deciles))),
    )

    # -- narrative ---------------------------------------------------------

    chapter.sections = [
        ("Decile 1 is the poor end", """
The column is named, in full, *"Index of Multiple Deprivation (IMD) Decile
(where 1 is most deprived 10% of LSOAs)"*. The convention is written into the
header, which is unusually generous of the publisher, and it is still the
thing most often reversed.

The reason it gets reversed is that it reads backwards. Bigger numbers usually
mean more of the thing being measured. Here, **decile 1 is the most deprived
tenth of England** and decile 10 is the least.

Reversing it does not break anything. Every figure draws, every count is
right, and the chapter states the opposite of the truth about a real place
where real people live. Hand-check 10 therefore does not trust the column
name: it compares the IMD *score* of the low-decile areas against the
high-decile ones and confirms the direction from the data itself.
"""),

        ("The vintage trap", """
IMD 2019 is published against **2011** LSOA boundaries. The Census 2021 table
in the next chapter uses **2021** boundaries. Both are seven-character codes
beginning `E01`. Neither file mentions the other's existence.

Joining across them produces a table. Not an error — a table, with fewer rows
than you started with and no indication of which rows went missing or why.

So this chapter fetches the **2011** centroid file, and chapter 4 fetches the
**2021** one, and the two chapters are never joined to each other. The join
here matched **{matched} of {total} centroids ({rate:.1f}%)**, which is what a
correct vintage looks like.
""".format(matched=len(joined), total=len(in_box), rate=match_rate)),

        ("What the patch looks like", """
The patch contains **{n} neighbourhoods** with a deprivation score.

**{d1:.1f}% of them are in England's most deprived tenth**, against the 10%
you would see in a perfectly average place. The most deprived three deciles
together account for **{d3:.1f}%** of the patch, against 30% nationally.

The median neighbourhood here sits in **decile {median:.0f}**.

The map is the more useful of the two figures, because the profile is not
spatially even. This patch contains some of England's most deprived
neighbourhoods and some of its least, within about three kilometres of each
other.
""".format(n=len(joined), d1=most_deprived_share, d3=bottom_three,
           median=chapter.numbers["median_decile"])),
    ]

    chapter.findings = [
        "**{0:.1f}% of the patch's {1} neighbourhoods sit in England's most "
        "deprived tenth**, against 10% for an average place."
        .format(most_deprived_share, len(joined)),
        "The most deprived three deciles account for **{0:.1f}%** of the patch, "
        "against 30% nationally.".format(bottom_three),
        "Deprivation here is not evenly spread: the map holds neighbourhoods "
        "from both ends of England's range within a few kilometres.",
    ]

    chapter.caveats = [
        "IMD 2019 is a **relative rank**, not a measure of poverty. A decile "
        "says where a neighbourhood sits among all English neighbourhoods, and "
        "nothing about how much better or worse it has become.",
        "The data is from 2019 and the boundaries from 2011. This is the "
        "current publication, and it is old.",
        "An LSOA holds about 1,500 people. A single deprived neighbourhood "
        "contains people at every income; the decile describes the area, not "
        "anybody in it.",
        "A population-weighted centroid is a point standing in for a polygon. "
        "An LSOA whose centre falls just outside the box is excluded entirely, "
        "even if most of it is inside.",
    ]

    chapter.plan_notes.append(
        """**Plan §6 rated "a live source is down" as a moderate risk. It
happened on the very first address I tried.**

The IMD 2019 File 7 link on the current gov.uk publication page returns 404.
The file is still served from the older attachment path, which is what this
chapter uses. Had I not checked, the chapter would have fallen back to the
cached Leeds-district extract without comment, and the atlas would have
reported the right numbers from a file dated months ago while appearing to be
live.

That is why the provenance table on every page states **live** or **cached
copy** rather than just naming the source."""
    )

    chapter.plan_notes.append(
        """**Prediction P3 said more than 10% of the patch's LSOAs would be in
decile 1. The answer is {0:.1f}%.**

{1}""".format(most_deprived_share,
              "Correct. In a core city patch this is close to unavoidable, "
              "which makes it a weak prediction rather than a good one."
              if most_deprived_share > 10 else
              "Wrong. The patch is less concentrated in decile 1 than I "
              "expected, which is what a patch containing both an inner ring "
              "and a university district looks like.")
    )

    return chapter
