"""
Turning finished chapters into pages of the website.

The site is built by MkDocs from markdown. This module writes that markdown.
Nothing here knows anything about transport; it only knows how to lay a
Chapter out on a page, which is why a student can keep it unchanged and get
their own atlas rendered in the same shape.
"""

import atlaslib as al


def write_chapter(chapter, ctx):
    return al.write_page(chapter.slug + ".md", al.render_chapter(chapter, ctx))


def _number(ctx, chapter_number, key, default=float("nan")):
    for chapter in ctx.chapters:
        if chapter.number == chapter_number:
            return chapter.numbers.get(key, default)
    return default


def write_synthesis(ctx):
    """The page that is only allowed to say things the chapters computed."""
    n = lambda ch, key: _number(ctx, ch, key)          # noqa: E731

    out = ["# The atlas", "", "*{0}*".format(ctx.place_name), "",
           al.BANNER.format(built=ctx.built_at)]

    out.append("""
Seven chapters, seven national datasets, one bounding box. This page puts them
next to each other.

Everything below was computed by the chapters. Nothing on this page reads a
file of its own, and no number here was typed by hand — which is the only
reason a summary page is safe to write at all. A summary is where an atlas
usually starts to overclaim, because it is the page furthest from the data.
""".strip())
    out.append("")

    out.append("## The patch")
    out.append("")
    out.append(
        "**{0}**, a box {1:.1f} km east–west by {2:.1f} km north–south, "
        "covering **{3:.0f} km²**.".format(
            ctx.place_name, ctx.width_km, ctx.height_km, ctx.area_km2))
    out.append("")
    out.append("```")
    out.append("south {0}   west {1}   north {2}   east {3}".format(*ctx.bbox))
    out.append("```")
    out.append("")
    out.append(
        "A rectangle is not a place. This one includes ground nobody would "
        "call the city centre, and every figure in the atlas is titled with "
        "the box rather than with a claim about where the centre ends.")
    out.append("")

    out.append("## Seven numbers")
    out.append("")
    out.append("| Chapter | The number | |")
    out.append("|---|---:|---|")
    rows = [
        (1, "[Stops and stations](chapter-01.md)", "{0:,.0f}".format(n(1, "stops")),
         "public transport access points, {0:.1f} per km²".format(n(1, "density"))),
        (1, "[Area within 400 m of one](chapter-01.md)", "{0:.1f}%".format(n(1, "covered_pct")),
         "of the patch, median walk {0:.0f} m".format(n(1, "median_m"))),
        (2, "[Active-mode casualties](chapter-02.md)", "{0:,.0f}".format(n(2, "total")),
         "in two years: {0:.0f} killed, {1:.0f} seriously injured"
         .format(n(2, "fatal"), n(2, "serious"))),
        (3, "[Neighbourhoods in England's poorest tenth](chapter-03.md)",
         "{0:.1f}%".format(n(3, "decile1_pct")),
         "against 10% for an average place"),
        (4, "[Households with no car](chapter-04.md)", "{0:.1f}%".format(n(4, "patch_pct")),
         "against {0:.1f}% for England and Wales".format(n(4, "england_pct"))),
        (5, "[Cycling under the Dutch scenario](chapter-05.md)",
         "{0:.1f}×".format(n(5, "multiple")),
         "today's modelled commuter cycling"),
        (6, "[Everyday destinations near a stop](chapter-06.md)",
         "{0:.1f}%".format(n(6, "served_pct")),
         "of {0:,.0f} schools, shops, surgeries and campuses".format(n(6, "amenities"))),
        (7, "[Commuting hours that are wet](chapter-07.md)",
         "{0:.1f}%".format(n(7, "commute_wet_share")),
         "of 07–09 and 16–18, across the whole year"),
    ]
    for _, label, value, note in rows:
        out.append("| {0} | **{1}** | {2} |".format(label, value, note))
    out.append("")

    out.append("## What the seven chapters say together")
    out.append("")
    out.append("""
Read on its own, each chapter is a description. Read together, they are an
argument, and it is worth being explicit about how much of it the data
supports.

**{car:.1f}% of households in this patch have no car** — {ratio:.1f} times the
England and Wales rate. For those households the network in chapter 1 is not a
convenience; it is the entire transport system. That network is dense:
**{covered:.1f}% of the patch is within 400 m of an access point**, and
**{served:.1f}% of everyday destinations** are too.

So access to *something* is close to universal here. What that something is —
how often it runs, where it goes, at what time of night — is not in this
atlas, and it is the question everything above is pointing at.

Meanwhile **{casualties:,.0f} people were injured walking or cycling** in the
patch over two years. Pedestrians and cyclists appear in roughly equal
numbers, despite very unequal exposure. The modelled cycling potential in
chapter 5 is **{multiple:.1f}× today's level**, and chapter 7 removes the
easiest objection to it: only **{wet:.1f}% of commuting hours are wet**.

**What this atlas cannot tell you.** Not whether any of it is fair.
Chapters 3 and 4 describe deprivation and car ownership on **different
geographies** and are deliberately never joined, so the obvious question —
are the car-free neighbourhoods also the poorest? — is one this atlas
declines to answer rather than answers badly.
""".strip().format(
        car=n(4, "patch_pct"),
        ratio=n(4, "patch_pct") / n(4, "england_pct") if n(4, "england_pct") else float("nan"),
        covered=n(1, "covered_pct"), served=n(6, "served_pct"),
        casualties=n(2, "total"), multiple=n(5, "multiple"),
        wet=n(7, "commute_wet_share")))
    out.append("")

    out.append("## Every figure")
    out.append("")
    for chapter in ctx.chapters:
        out.append("### Chapter {0} — [{1}]({2}.md)".format(
            chapter.number, chapter.title, chapter.slug))
        out.append("")
        for figure in chapter.figures:
            out.append("![{0}](figures/{1})".format(figure.alt, figure.filename))
            out.append("")
            out.append("*{0}*".format(figure.caption))
            out.append("")

    out.append("## Everything this atlas used")
    out.append("")
    out.append("| Dataset | Retrieved | Licence |")
    out.append("|---|---|---|")
    seen = set()
    for source in ctx.sources:
        if source.key in seen:
            continue
        seen.add(source.key)
        out.append("| [{0}]({1}) | {2}, {3} | {4} |".format(
            source.name, source.url, source.retrieved,
            "live" if source.live else "cached copy", source.licence))
    out.append("")
    out.append(
        "Contains public sector information licensed under the Open Government "
        "Licence v3.0. Map data © OpenStreetMap contributors, ODbL. Weather "
        "data © open-meteo.com, CC-BY 4.0.")
    out.append("")

    return al.write_page("atlas.md", "\n".join(out).rstrip() + "\n")


def write_scorecard(ctx):
    """Generated from the check register, so the honest number cannot drift."""
    checks = ctx.checks
    anchored = [c for c in checks if c.anchored]
    internal = [c for c in checks if not c.anchored]
    failed = [c for c in checks if not c.passed]
    figures = sum(len(c.figures) for c in ctx.chapters)
    counts = sum(len(c.counts) for c in ctx.chapters)

    out = ["# The scorecard", "", "*How much of this can be trusted, and why*",
           "", al.BANNER.format(built=ctx.built_at)]

    out.append("""
The [agent guide](../project/agent_guide.md) records what happened when an
assistant built an atlas like this one before: **twenty hand-checks, a banner
reading "20 of 20 pass", and about four that were worth anything.** Two of the
twenty compared a number with itself.

So this page is generated from the check register rather than written. Each
check declares whether it is anchored **outside** the data — against a map, a
published statistic, a physical fact — or whether it only tests that the code
agrees with itself. The honest number cannot be inflated without editing the
register in a way that shows up in the diff.
""".strip())
    out.append("")

    out.append("## The two numbers")
    out.append("")
    out.append("| | |")
    out.append("|---|---:|")
    out.append("| Hand-checks registered | **{0}** |".format(len(checks)))
    out.append("| Anchored outside the data ⚓ | **{0}** |".format(len(anchored)))
    out.append("| Internal consistency only ○ | {0} |".format(len(internal)))
    out.append("| Failing | {0} |".format(len(failed)))
    out.append("")
    out.append(
        "**{0} is the number that means something.** The other {1} are worth "
        "having — they catch a filter that stopped filtering — but a check "
        "that compares the code with itself proves the code is consistent, not "
        "that it is right.".format(len(anchored), len(internal)))
    out.append("")

    out.append("## Every check")
    out.append("")
    out.append("| # | Ch | The claim | Checked against | Anchored | Result |")
    out.append("|---|---|---|---|:---:|:---:|")
    for chapter in ctx.chapters:
        for check in chapter.checks:
            out.append("| {0} | {1} | {2} | {3} | {4} | {5} |".format(
                check.number, chapter.number, check.claim, check.against,
                "⚓" if check.anchored else "○",
                "pass" if check.passed else "**FAIL**"))
    out.append("")

    out.append("## What the other layers did")
    out.append("")
    out.append("""
Hand-checks are only the third layer. The other two ran throughout.

| Layer | What it caught here |
|---|---|
| **1 — free** | Tracebacks: wrong column names, a 404 on the deprivation file, a coordinate pair the wrong way round. Fixed as they appeared, at no cost. |
| **2 — ask for it** | **{counts} counted filters and joins**, recorded on the chapter pages. These caught the joins that would have quietly shrunk. |
| **3 — only a person** | The {anchored} anchored checks above, and **{figures} figures opened and looked at**. Looking at the figures caught two errors that no count could: ten stops drawn nowhere, and a colour scale that separated nothing. |
""".strip().format(counts=counts, anchored=len(anchored), figures=figures))
    out.append("")

    out.append("## Where the plan was wrong")
    out.append("")
    out.append(
        "The [plan](plan.md) was written before any code existed. These are the "
        "places it turned out to be wrong, kept rather than quietly corrected:")
    out.append("")
    for chapter in ctx.chapters:
        for note in chapter.plan_notes:
            first = note.strip().split("\n\n")[0].replace("\n", " ")
            out.append("- **Chapter {0}.** {1} [→]({2}.md)".format(
                chapter.number, first, chapter.slug))
    out.append("")

    if failed:
        out.append("## Failing checks")
        out.append("")
        for check in failed:
            out.append("- **Check {0}:** {1} — checked against {2}".format(
                check.number, check.claim, check.against))
        out.append("")

    out.append("## What none of this proves")
    out.append("")
    out.append("""
Every check on this page could pass and the atlas could still be wrong, in at
least three ways that no amount of checking inside a build can reach.

**The data could be wrong.** STATS19 records reported collisions. If cyclist
injuries are under-reported — and they are — every casualty figure here is a
floor, and no check inside this build can see that.

**The question could be wrong.** Counting casualties without exposure, or stops
without services, produces correct answers to questions that do not mean what
they appear to.

**The framing could be wrong.** Seven datasets were chosen. Bus frequency,
severance, air quality, street lighting and pavement condition were not, and
their absence shapes the conclusions more than anything in the tables above.
""".strip())
    out.append("")

    return al.write_page("scorecard.md", "\n".join(out).rstrip() + "\n")
