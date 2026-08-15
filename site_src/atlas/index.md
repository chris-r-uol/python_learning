---
title: The worked atlas
---

# The worked atlas

**A transport atlas of Leeds city centre, planned and built by Claude, an AI
assistant, and published as this website.**

!!! quote "Why this section reads differently"

    Everything else on this site is written to be plain. Short sentences.
    Simple words. Nothing decorative. That is a deliberate choice for
    instructions you have to follow while also learning to program.

    **This section is not written that way, and the contrast is the point.**

    It is what a capable assistant produces when asked to plan a large piece
    of work and then carry it out at length. It is longer, more confident and
    considerably more pleased with itself than the rest of the course.

    Read it for two things. First, what you can build in five weeks with an
    assistant and the habits weeks 1 to 3 teach. Second, the difference
    between writing that *sounds* rigorous and work that *is* rigorous — and
    how you would tell them apart.

---

## The rules it was given

The same ones the [project brief](../project/brief.md) gives you.

1. **Write down what the assistant will get wrong, before delegating.**
2. **Ask for the plan before the code.**
3. **Count the rows before and after every filter and every join.**
4. **Open every figure and look at it.**
5. **A hand-check anchored outside the data is worth more than twenty that
   are not.**
6. **One command rebuilds everything from nothing.**

It wrote [the plan](plan.md) first, including a list of things it expected to
get wrong about itself and eight numbered predictions it might fail. Then it
executed the plan. Where the plan turned out to be wrong, the chapters say so
rather than quietly correcting it.

---

## What it built

<div class="grid cards" markdown>

-   :material-clipboard-text-outline: **[The plan](plan.md)**

    ---

    Written before any code existed. The invention list, the architecture, the
    hand-check register, the risks, and eight falsifiable predictions.

-   :material-map-marker-radius: **[Chapter 1 — The patch and its stops](chapter-01.md)**

    ---

    Where you can catch something, and where you cannot. Contains the most
    instructive mistake in the build.

-   :material-alert-outline: **[Chapter 2 — Road safety](chapter-02.md)**

    ---

    Two years of STATS19. Four integers decide whether the whole chapter is
    true.

-   :material-home-group: **[Chapter 3 — Deprivation](chapter-03.md)**

    ---

    Where the patch sits in England's range, and why decile 1 is the poor end.

-   :material-car-off: **[Chapter 4 — Who has no car](chapter-04.md)**

    ---

    The chapter the rest of the atlas is about — and the join it refuses to
    make.

-   :material-bike: **[Chapter 5 — Cycling potential](chapter-05.md)**

    ---

    The only chapter whose subject does not exist yet.

-   :material-school-outline: **[Chapter 6 — What is there](chapter-06.md)**

    ---

    What the network reaches. Three ways to be refused by an API.

-   :material-weather-rainy: **[Chapter 7 — A year of weather](chapter-07.md)**

    ---

    8,760 hours, returned as parallel arrays with nothing holding them
    together but position.

-   :material-book-open-variant: **[The atlas](atlas.md)**

    ---

    All seven chapters together, every figure on one page, and what they say
    when read as one document.

-   :material-scale-balance: **[The scorecard](scorecard.md)**

    ---

    27 hand-checks. 14 anchored outside the data. Generated from the register,
    so the honest number cannot be inflated.

-   :material-content-duplicate: **[Build your own](build-your-own.md)**

    ---

    Two lines to change. How the website is generated, and how to publish
    yours.

</div>

---

## Four things it got wrong

Kept in, because they are more useful than the parts that worked.

!!! failure "A query that returned a confident, incomplete answer"

    Chapter 1 fetched ATCO area 450 and got 1,314 bus stops. The map looked
    complete. **Rail stations are in area 910**, a separate national
    pseudo-area, so the atlas of Leeds public transport had no Leeds Rail
    Station in it.

    Nothing failed. No traceback, no empty table, no zero count. The row
    counts could never have caught it, because the missing rows were never
    there to count. A hand-check written before the code — *a station I know
    exists must be in this file* — caught it.

!!! failure "Ten stops drawn nowhere"

    The first stop map had two categories, bus and rail. Ten access points are
    typed `RSE`, a station entrance, and belonged to neither. They were
    fetched, filtered, counted — and drawn on no figure.

    The only visible trace was a legend that added up to ten short of the
    total.

!!! failure "A figure that ran perfectly and showed nothing"

    Chapter 6 asked what share of everyday destinations sits within 400 m of a
    stop. The answer is 100%, correctly: the furthest school in the patch is
    366 m from a stop.

    So the first figure was six bars, all at 100%, neatly arranged and
    completely uninformative. A threshold everything clears is not a
    measurement. The figure was replaced with one that shows where the
    categories actually differ.

!!! failure "A source that was down on the first try"

    The deprivation file link on the current gov.uk page returns 404. Without
    checking, the chapter would have fallen back to a cached copy and reported
    months-old numbers while appearing to be live.

    That is why every page states **live** or **cached copy** for every
    dataset, rather than just naming the source.

---

## The honest number

The [agent guide](../project/agent_guide.md) records what happened when an
assistant built an atlas like this before: **twenty hand-checks, a banner
reading "20 of 20 pass", and about four that were worth anything.**

This build registers **27 hand-checks**, of which **14 are anchored outside
the data** — against a map, a published statistic, a physical fact.

The [scorecard](scorecard.md) is generated from the register rather than
written, so that number cannot be quietly improved.
