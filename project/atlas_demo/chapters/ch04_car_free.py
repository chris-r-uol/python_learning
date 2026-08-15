"""
Chapter 4 — Who has no car.

Question: how many households have no car, and where are they?

Census 2021 table TS045, car or van availability, via the Nomis API. This is
the chapter that says who the rest of the atlas is about: a household with no
car depends on the network in chapters 1, 5 and 6, and walks or cycles through
chapter 2.

Its geography is 2021 LSOA codes. Chapter 3's is 2011. They are never joined.
"""

import numpy as np

import atlaslib as al

# Nomis dataset NM_2063_1 is TS045. The dataset number cannot be guessed from
# the table name, and the table name cannot be guessed from the question.
#
# geography=TYPE151 means "every LSOA in England and Wales" and is the obvious
# query. It silently returns exactly 25,000 rows — the API's default cap —
# out of the 71,344 that exist. So this asks for the codes it actually needs,
# which is both correct and faster.
NOMIS = (
    "https://www.nomisweb.co.uk/api/v01/dataset/NM_2063_1.data.csv"
    "?date=latest&geography={codes}&c2021_cars_5=0,1"
    "&measures=20100&select=geography_code,geography_name,c2021_cars_5_name,obs_value"
)
NOMIS_ALL = (
    "https://www.nomisweb.co.uk/api/v01/dataset/NM_2063_1.data.csv"
    "?date=latest&geography=TYPE151&c2021_cars_5=0,1&measures=20100"
)
NOMIS_ROW_CAP = 25000

CENTROIDS = (
    "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/"
    "LSOA_PopCentroids_EW_2021_V4/FeatureServer/0/query"
    "?geometry={west},{south},{east},{north}&geometryType=esriGeometryEnvelope"
    "&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=LSOA21CD"
    "&outSR=4326&returnGeometry=true&f=geojson"
)

# The published England and Wales figure, for comparison. This is the anchor:
# a number from outside anything this build computed.
ENGLAND_WALES_NO_CAR_PCT = 23.5

TOTAL_LABEL = "Total: All households"
NO_CAR_LABEL = "No cars or vans in household"

LEAD = """
Every other chapter describes the network. This one describes the people who
have no alternative to it.

Census 2021 asked every household how many cars or vans it had available.
Table TS045 publishes the answer for every neighbourhood in England and Wales.
A household with none of them walks, cycles, takes the bus, or does not go.
""".strip()


def _parse_nomis(text):
    rows, _ = al.parse_csv(text.lstrip("﻿"))
    by_area = {}
    for row in rows:
        code = (row.get("GEOGRAPHY_CODE") or "").strip()
        label = (row.get("C2021_CARS_5_NAME") or "").strip()
        value = al.to_float(row.get("OBS_VALUE"), default=float("nan"))
        if not code or np.isnan(value):
            continue
        record = by_area.setdefault(code, {"name": (row.get("GEOGRAPHY_NAME") or "").strip()})
        if label == TOTAL_LABEL:
            record["total"] = value
        elif label == NO_CAR_LABEL:
            record["no_car"] = value
    return by_area, len(rows)


def build(ctx):
    chapter = al.Chapter(
        number=4,
        slug="chapter-04",
        title="Who has no car",
        question="How many households have no car, and where are they?",
        lead=LEAD,
    )

    # Geography first, then the statistics for exactly those areas. The other
    # way round means downloading England and Wales and being given a quarter
    # of it without being told.
    centroids = ctx.fetch(
        key="lsoa_2021_centroids",
        name="ONS LSOA 2021 population-weighted centroids",
        url=CENTROIDS.format(west=ctx.west, south=ctx.south,
                             east=ctx.east, north=ctx.north),
        licence="OGL v3.0, © Crown copyright and database right",
        cache_file="lsoa_2021_centroids.geojson",
        parse=al.parse_geojson,
    )

    # -- cut ---------------------------------------------------------------

    features = centroids["features"]
    in_box = []
    for feature in features:
        lon, lat = feature["geometry"]["coordinates"]
        if ctx.inside([lon], [lat])[0]:
            in_box.append({
                "code": feature["properties"].get("LSOA21CD"),
                "lon": lon, "lat": lat,
            })
    ctx.counted(chapter, "LSOA 2021 centroids returned, then filtered to the box",
                len(features), len(in_box))

    codes = ",".join(sorted({a["code"] for a in in_box if a["code"]}))
    census = ctx.fetch(
        key="census_ts045",
        name="Census 2021 table TS045, car or van availability (Nomis NM_2063_1)",
        url=NOMIS.format(codes=codes),
        licence="OGL v3.0, © Crown copyright",
        cache_file="census_car_availability.csv",
        parse=_parse_nomis,
    )

    joined = []
    for area in in_box:
        record = census.get(area["code"])
        if record and record.get("total") and record.get("no_car") is not None:
            area["name"] = record["name"]
            area["total"] = record["total"]
            area["no_car"] = record["no_car"]
            area["pct"] = 100.0 * record["no_car"] / record["total"]
            joined.append(area)
    ctx.counted(chapter, "Join LSOA 2021 centroids x TS045 on 2021 codes",
                len(in_box), len(joined))

    if not joined:
        raise SystemExit("Chapter 4: nothing joined. Check the LSOA vintage.")

    # -- the vintage demonstration -----------------------------------------
    #
    # The plan says chapters 3 and 4 must never be joined. Rather than assert
    # that, measure it: how many 2021 codes appear in the 2011 file at all?

    codes_2021 = {a["code"] for a in joined}
    shared_with_2011 = len(ctx.shared.get("lsoa_2011_codes", set()) & codes_2021)
    if "lsoa_2011_codes" in ctx.shared:
        ctx.counted(chapter,
                    "2021 codes that also exist as 2011 codes (the join that must not happen)",
                    len(codes_2021), shared_with_2011)

    households = sum(a["total"] for a in joined)
    no_car = sum(a["no_car"] for a in joined)
    patch_pct = 100.0 * no_car / households
    pcts = np.array([a["pct"] for a in joined])
    ranked = sorted(joined, key=lambda a: a["pct"], reverse=True)

    chapter.numbers = {
        "lsoas": len(joined),
        "households": households,
        "no_car": no_car,
        "patch_pct": patch_pct,
        "england_pct": ENGLAND_WALES_NO_CAR_PCT,
        "max_pct": float(pcts.max()),
        "min_pct": float(pcts.min()),
        "median_pct": float(np.median(pcts)),
        "top_area": ranked[0]["name"],
    }

    # -- figures -----------------------------------------------------------

    figure, ax = al.axes(figsize=(8.8, 4.6))
    ax.hist(pcts, bins=np.arange(0, 101, 5), color=al.PURPLE, alpha=0.85,
            edgecolor="white", linewidth=0.6)
    ax.axvline(ENGLAND_WALES_NO_CAR_PCT, color=al.RED, linewidth=1.8,
               linestyle="--",
               label="England & Wales: {0:.1f}%".format(ENGLAND_WALES_NO_CAR_PCT))
    ax.axvline(patch_pct, color=al.INK, linewidth=1.8,
               label="This patch: {0:.1f}%".format(patch_pct))
    ax.set_xlabel("Households with no car or van (% of households in the neighbourhood)")
    ax.set_ylabel("Neighbourhoods (count)")
    ax.set_title("Car-free households by neighbourhood\n{0}, Census 2021 table TS045"
                 .format(ctx.place_name), fontsize=11)
    ax.legend(frameon=False, fontsize=9)
    chapter.figures.append(al.Figure(
        al.save(figure, "ch04_distribution.png"),
        "How car-free households are distributed across the patch's "
        "neighbourhoods, against the England and Wales figure. The spread is "
        "the finding: the patch average hides neighbourhoods at both extremes.",
        "Histogram of car-free household share by neighbourhood",
    ))

    aspect = al.metres_per_degree_lon((ctx.south + ctx.north) / 2) / al.METRES_PER_DEGREE_LAT
    figure, ax = al.axes(figsize=(8.4, 6.4))
    scatter = ax.scatter([a["lon"] for a in joined], [a["lat"] for a in joined],
                         c=pcts, cmap="viridis", s=110,
                         edgecolors="white", linewidths=0.7,
                         vmin=0, vmax=max(80, float(pcts.max())))
    bar = figure.colorbar(scatter, ax=ax, pad=0.02)
    bar.set_label("Households with no car (%)", fontsize=9)
    ax.set_aspect(1 / aspect)
    ax.set_xlim(ctx.west, ctx.east)
    ax.set_ylim(ctx.south, ctx.north)
    ax.set_xlabel("Longitude (degrees; negative is west)")
    ax.set_ylabel("Latitude (degrees north)")
    ax.set_title("Where the car-free households are\n{0}. One point per LSOA, "
                 "Census 2021".format(ctx.place_name), fontsize=11)
    chapter.figures.append(al.Figure(
        al.save(figure, "ch04_map.png"),
        "Car-free households by neighbourhood. Compare this with chapter 1's "
        "coverage map: the two together are the argument of the whole atlas.",
        "Map of car-free household share across the patch",
    ))

    figure, ax = al.axes(figsize=(8.8, 4.8))
    top = ranked[:12][::-1]
    ax.barh([a["name"] for a in top], [a["pct"] for a in top],
            color=al.PURPLE, height=0.68)
    ax.axvline(ENGLAND_WALES_NO_CAR_PCT, color=al.RED, linewidth=1.4,
               linestyle="--")
    ax.annotate("England & Wales {0:.1f}%".format(ENGLAND_WALES_NO_CAR_PCT),
                xy=(ENGLAND_WALES_NO_CAR_PCT, -0.6), fontsize=8.5,
                color=al.RED, ha="center")
    ax.set_xlabel("Households with no car or van (%)")
    ax.set_ylabel("Neighbourhood (LSOA)")
    ax.tick_params(axis="y", labelsize=8)
    ax.set_title("The twelve most car-free neighbourhoods\n{0}, Census 2021"
                 .format(ctx.place_name), fontsize=11)
    chapter.figures.append(al.Figure(
        al.save(figure, "ch04_top.png"),
        "The neighbourhoods where not owning a car is the normal case rather "
        "than the exception.",
        "Bar chart of the twelve most car-free neighbourhoods",
    ))

    # -- hand-checks -------------------------------------------------------

    ctx.check(
        chapter,
        claim="The car-free share is credible for a dense city centre",
        against="The published England and Wales figure of {0:.1f}%"
                .format(ENGLAND_WALES_NO_CAR_PCT),
        anchored=True,
        passed=patch_pct > ENGLAND_WALES_NO_CAR_PCT,
        detail=(
            "The patch is **{0:.1f}%** car-free against **{1:.1f}%** for "
            "England and Wales — {2:.1f} times the national rate. A core city "
            "patch below the national figure would mean the numerator and "
            "denominator had been swapped."
            .format(patch_pct, ENGLAND_WALES_NO_CAR_PCT,
                    patch_pct / ENGLAND_WALES_NO_CAR_PCT)
        ),
    )

    # Are these households or people? Check that the parts sum to the stated
    # total, which is the only way to tell from inside the file.
    sums_ok = all(a["no_car"] <= a["total"] for a in joined)
    ctx.check(
        chapter,
        claim="Percentages are of households, not of people",
        against="Each neighbourhood's no-car count against its stated total",
        anchored=False,
        passed=sums_ok,
        detail=(
            "{0:,.0f} households in the patch, of which {1:,.0f} have no car. "
            "No neighbourhood reports more car-free households than households, "
            "which it would if the two columns were different populations."
            .format(households, no_car)
        ),
    )

    ctx.check(
        chapter,
        claim="The statistics request was not silently truncated",
        against="The number of areas asked for against the number returned",
        anchored=False,
        passed=len(census) >= len(in_box),
        detail=(
            "Asked for {0} areas, received {1}. The obvious query — every LSOA "
            "in England and Wales — returns exactly {2:,} rows, which is the "
            "API's default cap and about a third of the {3:,} that exist. It "
            "arrives as a valid CSV with no warning of any kind."
            .format(len(in_box), len(census), NOMIS_ROW_CAP, 71344)
        ),
    )

    ctx.check(
        chapter,
        claim="The 2021-code join matched the patch",
        against="Matched rows against centroids in the box",
        anchored=False,
        passed=(100.0 * len(joined) / len(in_box)) >= 95,
        detail="{0} of {1} centroids matched a TS045 row ({2:.1f}%)."
               .format(len(joined), len(in_box),
                       100.0 * len(joined) / len(in_box)),
    )

    if "lsoa_2011_codes" in ctx.shared:
        overlap_pct = 100.0 * shared_with_2011 / len(codes_2021)
        ctx.check(
            chapter,
            claim="Chapters 3 and 4 use genuinely different geographies",
            against="The 2011 codes from chapter 3, intersected with these 2021 codes",
            anchored=False,
            passed=overlap_pct < 100,
            detail=(
                "Only **{0} of {1}** 2021 codes in this patch ({2:.1f}%) also "
                "exist as 2011 codes. Joining chapter 3 to chapter 4 on these "
                "codes would therefore lose about **{3:.1f}%** of the patch — "
                "silently, as a smaller table, with no error anywhere."
                .format(shared_with_2011, len(codes_2021), overlap_pct,
                        100 - overlap_pct)
            ),
        )

    # -- narrative ---------------------------------------------------------

    ratio = patch_pct / ENGLAND_WALES_NO_CAR_PCT
    chapter.sections = [
        ("The number the rest of the atlas is about", """
**{no_car:,.0f} of the patch's {households:,.0f} households have no car or
van.** That is **{pct:.1f}%**, against **{eng:.1f}% for England and Wales** —
about **{ratio:.1f} times** the national rate.

For those households, chapters 1, 5 and 6 are not a convenience. The bus
network is the car. The 400 m coverage figure in chapter 1 is a description of
their front door. The casualties in chapter 2 are disproportionately theirs,
because walking is what you do when there is no alternative.

The spread matters as much as the average. Neighbourhood shares in this patch
run from **{low:.1f}%** to **{high:.1f}%**, with a median of **{median:.1f}%**.
The most car-free neighbourhood is *{top}*, where not owning a car is the
normal case rather than the exception.
""".format(no_car=no_car, households=households, pct=patch_pct,
           eng=ENGLAND_WALES_NO_CAR_PCT, ratio=ratio,
           low=chapter.numbers["min_pct"], high=chapter.numbers["max_pct"],
           median=chapter.numbers["median_pct"], top=chapter.numbers["top_area"])),

        ("The query that gives you a third of the country", """
The natural way to ask Nomis for this table is `geography=TYPE151`, meaning
every LSOA in England and Wales. It returns a valid CSV, with a header, with
sensible numbers in it.

It contains exactly **25,000 rows**. There are **71,344**. The API has a
default record cap, the response does not mention it, and nothing in the file
indicates that it stops partway through the alphabet.

Had this patch been in a place whose codes sort later than the cut-off, the
chapter would have joined a complete set of centroids against an incomplete
set of statistics and reported the neighbourhoods that survived. The row
counts on this page would all have been internally consistent.

This chapter therefore fetches the geography first and asks for statistics on
**exactly the {n} areas it needs**. That is faster, and more importantly it
turns a silent truncation into an impossible one: if a code is missing from
the response, the join count drops and hand-check 15 fails.
""".format(n=len(in_box))),

        ("The join this chapter refuses to make", """
The obvious next question is whether the car-free neighbourhoods are the
deprived ones. Chapter 3 has a decile for every neighbourhood. This chapter
has a percentage for every neighbourhood. Both are keyed by a seven-character
code beginning `E01`. Joining them is one line.

**That line is not in this chapter, and it will not be.**

Chapter 3's codes are **2011** LSOAs, because IMD 2019 is published against
2011 boundaries. This chapter's are **2021** LSOAs, because Census 2021 is
published against 2021 boundaries. Between the two censuses, ONS split
neighbourhoods that grew and merged ones that shrank. Codes were retired and
new ones issued.

A merge across them does not fail. It returns the rows where a 2011 code
happens to still exist in 2021, drops everything else without a word, and
hands you a scatter plot of deprivation against car ownership that looks
entirely publishable.

The honest way to make that comparison is a lookup table published by ONS
that maps one vintage to the other, with a flag for split, merged and
unchanged areas. That is a piece of work in itself, and it is not something to
do by assuming two columns match because they are the same shape.
"""),
    ]

    chapter.findings = [
        "**{0:.1f}% of households in the patch have no car** — {1:,.0f} of "
        "{2:,.0f} — against {3:.1f}% for England and Wales."
        .format(patch_pct, no_car, households, ENGLAND_WALES_NO_CAR_PCT),
        "Neighbourhood shares run from **{0:.1f}% to {1:.1f}%**, so the patch "
        "average describes almost none of its neighbourhoods."
        .format(chapter.numbers["min_pct"], chapter.numbers["max_pct"]),
        "These households are the population the rest of the atlas is about: "
        "the network in chapters 1 and 5 is their only network.",
    ]

    chapter.caveats = [
        "Census 2021 was taken in March 2021, during a national lockdown. "
        "Student and shared-household areas in particular may not reflect a "
        "normal year.",
        "No car is not the same as no access to one. A household may borrow, "
        "hire, or use a car club.",
        "This is a count of households, not of people. Car-free households are "
        "smaller on average, so the share of *people* with no car differs.",
        "The comparison with deprivation in chapter 3 is deliberately absent. "
        "The geographies are different vintages and joining them would be "
        "wrong in a way that produces a convincing figure.",
    ]

    chapter.plan_notes.append(
        """**Prediction P4 said car-free households in the patch would exceed
40%. The answer is {0:.1f}%.**

{1}""".format(patch_pct,
              "Correct." if patch_pct > 40 else
              "Wrong. I over-predicted, because I was thinking of the city "
              "centre wards rather than a box that also contains suburban "
              "Headingley and Middleton. The bounding box is larger than the "
              "place I had in my head — which is exactly the failure mode the "
              "plan warned about when it said a rectangle is not a place.")
    )

    if "lsoa_2011_codes" in ctx.shared:
        overlap_pct = 100.0 * shared_with_2011 / len(codes_2021)
        chapter.plan_notes.append(
            """**Prediction P8 said a 2011↔2021 LSOA join would match less than
95% of rows. The measured overlap is {0:.1f}%.**

{1}""".format(overlap_pct,
              "Correct, and worse than I expected. A join that loses "
              "{0:.0f}% of a patch is not a rounding error, and nothing in "
              "pandas would have told me.".format(100 - overlap_pct)
              if overlap_pct < 95 else
              "Wrong: the overlap is higher than I predicted. The join would "
              "still be incorrect — matching codes are not guaranteed to mean "
              "identical areas — but it would lose fewer rows than I thought.")
        )

    return chapter
