---
title: The project — finding the data
---

# Weeks 4 and 5 — Your Patch

You choose a British town or city district, and build a **transport atlas** of
it: seven chapters, each drawn from a different national open dataset, all
assembled by one command.

The programming is not the hard part. You can already write a loop, a function
and a figure, and an assistant will write most of the rest. **The hard part is
the data** — finding it, working out what its columns actually mean, noticing
what it is quietly not telling you, and cutting it down to your patch without
losing rows you needed.

So this part of the course, and this part of the site, is organised around
that rather than around code.

<div class="grid cards" markdown>

-   :material-clipboard-text-outline: **[The brief](brief.md)**

    ---

    What you are building, how to choose a patch, the shape every chapter
    follows, and how to keep your progress with Git.

-   :material-database-search: **[Data discovery](data_sources.md)**

    ---

    The seven sources: addresses, licences, and — most usefully — the trap in
    each one that nobody writes down.

-   :material-robot-outline: **[Directing an agent](agent_guide.md)**

    ---

    How to delegate this much work without losing track of whether it is
    right. Read this before you build anything.

</div>

## The seven chapters

Each is a different national dataset, cut to your patch. Chapter 1 comes
first because it defines the bounding box every other chapter reuses; after
that, any order.

| # | Chapter | The question it answers | Source |
|---|---|---|---|
| 1 | The patch and its stops | Where is public transport, and where is it not? | NaPTAN |
| 2 | Road safety | Where have people walking and cycling been hurt? | STATS19 |
| 3 | Deprivation | How does your patch sit in England's distribution? | IMD 2019 |
| 4 | Who has no car | Who depends entirely on walking, cycling and the bus? | Census 2021 |
| 5 | Cycling potential | What does the national model think cycling could be? | PCT |
| 6 | What is there | Schools, surgeries, shops — what do the stops serve? | OpenStreetMap |
| 7 | A year of weather | What is the operating environment, in rain and degrees? | open-meteo |

## Three things that will cost you an afternoon

All three are covered fully in [Data discovery](data_sources.md), and they are
the reason that page exists.

!!! warning "The area identifiers are not guessable"

    Three chapters need an area code before they return anything, and all
    three *look* guessable. West Yorkshire is ATCO `450`, York is `329`,
    Bristol is `010`. The Propensity to Cycle Tool calls Bristol `avon`,
    because its regions are historic counties rather than cities. Ask an
    assistant for any of these and you will get a confident, wrong answer.

    Look them up instead — the ATCO codes ship in the repository, at
    `project/data/external/atco_area_codes.csv`.

!!! warning "The codes inside the files are not guessable either"

    In STATS19, `casualty_type` `0` is a pedestrian, and severity `1` means
    **fatal**, not slight. In the deprivation data, decile **1 is the most
    deprived**. None of this is written anywhere in the files themselves.

!!! warning "A bounding box is not a place"

    A rectangle around a town centre includes fringes you would never call
    your patch. Filtering by box is the right first cut and the wrong final
    answer — so say which one your figure used.

## If a source is down

Every dataset has a cached copy committed in `project/data/external/`, taken
on a known date and listed in `SOURCES.md` beside it. Use it, note the date in
your provenance record, and carry on. Public data services go down; working
around that is part of the job rather than a reason to stop.
