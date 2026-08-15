---
title: The project — finding the data
---

# Weeks 4 and 5 — Your Patch

Choose a British town or city district. Build a **transport atlas** of it:
seven chapters, each from a different national dataset, built by one
command.

The programming is not the hard part. You can already write a loop, a
function and a figure, and an assistant will write most of the rest.

**The hard part is the data.** Finding it. Working out what its columns
mean. Noticing what it does not tell you. Cutting it down to your patch
without losing rows you needed.

<div class="grid cards" markdown>

-   :material-clipboard-text-outline: **[The brief](brief.md)**

    ---

    What you build, how to choose a patch, the shape of every chapter, and
    how to save your work with Git.

-   :material-database-search: **[Data discovery](data_sources.md)**

    ---

    The seven sources: addresses, licences, and the problem in each one that
    nobody writes down.

-   :material-robot-outline: **[Directing an agent](agent_guide.md)**

    ---

    How to delegate this much work and still know whether it is right. Read
    before you build anything.

</div>

## The seven chapters

Chapter 1 comes first. It sets the bounding box every other chapter uses.
After that, any order.

| # | Chapter | What it answers | Source |
|---|---|---|---|
| 1 | The patch and its stops | Where is public transport, and where is it not? | NaPTAN |
| 2 | Road safety | Where have people walking and cycling been hurt? | STATS19 |
| 3 | Deprivation | Where does your patch sit in England's range? | IMD 2019 |
| 4 | Who has no car | Who depends on walking, cycling and the bus? | Census 2021 |
| 5 | Cycling potential | What does the national model say cycling could be? | PCT |
| 6 | What is there | Schools, surgeries, shops. What do the stops serve? | OpenStreetMap |
| 7 | A year of weather | What is the weather your patch operates in? | open-meteo |

## Three things that cost time

All three are covered in [Data discovery](data_sources.md).

!!! warning "Area codes cannot be guessed"

    Three chapters need an area code before they return anything. All three
    look guessable. West Yorkshire is ATCO `450`. York is `329`. Bristol is
    `010`. The Propensity to Cycle Tool calls Bristol `avon`, because its
    regions are historic counties.

    Ask an assistant for any of these and you get a confident wrong answer.
    The ATCO codes are in the repository, at
    `project/data/external/atco_area_codes.csv`.

!!! warning "The codes inside the files cannot be guessed either"

    In STATS19, `casualty_type` `0` is a pedestrian, and severity `1` means
    **fatal**, not slight. In the deprivation data, decile **1 is the most
    deprived**. None of this is written in the files.

!!! warning "A bounding box is not a place"

    A rectangle around a town centre includes areas you would not call your
    patch. Filtering by box is the right first step. It is not the final
    answer. Say which one your figure used.

## If a source is down

Every dataset has a copy in `project/data/external/`, taken on a known date
and listed in `SOURCES.md` beside it. Use it and record the date.
