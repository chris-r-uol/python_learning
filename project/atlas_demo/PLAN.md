# The Plan

!!! quote "Before you read this"

    **This page and everything after it was written by Claude, an AI
    assistant.** It has not been edited into the house style of the rest of
    this course, and that is deliberate. The course text is deliberately
    plain — short sentences, simple words, nothing decorative. What follows
    is not. It is what a capable assistant produces when you let it write at
    length.

    Notice the difference as you read. Then notice that the difference is
    *style*, not *correctness*. The verbosity below does not make the atlas
    more right, and the plainness of the course does not make it less
    rigorous. Judge both on whether the numbers are true.

---

## 0. What this is

I was asked to build the project that weeks 4 and 5 set: a **transport atlas
of Leeds city centre**, assembled from seven national open datasets, rebuilt
from nothing by one command, and published as a website.

I was asked to plan it first and then execute the plan, using the principles
this course teaches. So that is what this page is — the plan, written before
any code existed, committed to the repository so it can be checked against
what actually happened.

Everything after this page is execution. Where the plan turned out to be
wrong, the execution pages say so rather than quietly correcting it. There
are four such places. They are the most useful thing in this section.

---

## 1. What I will get wrong

[`agent_guide.md`](../project/agent_guide.md) opens by saying that before you delegate
a large job, you should write down what your assistant is likely to invent.
I am the assistant, so I will do it about myself. This section exists because
the failure mode I am most exposed to is not writing broken code — the
tracebacks catch that — but writing *fluent, plausible, wrong* code about
data whose conventions live outside the file.

Every row below is something I could produce a confident sentence about
without ever having checked it.

| Thing | What I would guess | What is actually true | How I know |
|---|---|---|---|
| Leeds ATCO area code | `LDS`, or `033`, or `West Yorkshire` | **`450`** | `data/external/atco_area_codes.csv` |
| STATS19 `casualty_severity` | 1 = slight, ascending to worst | **1 = fatal**, 2 = serious, 3 = slight | STATS19 data guide |
| STATS19 `casualty_type` | Some string like `"pedestrian"` | **`0`** = pedestrian, `1` = cyclist | STATS19 data guide |
| IMD decile direction | 10 = worst, because bigger is worse | **1 = most deprived tenth** | Column name says so, in full |
| IMD LSOA vintage | Current codes | **2011** codes, in a 2019 publication | IMD file header |
| Census TS045 vintage | Same codes as IMD | **2021** codes. Different set | Nomis metadata |
| GeoJSON coordinate order | `[latitude, longitude]` — how people say it | **`[longitude, latitude]`** | GeoJSON specification |
| Distance from degrees | Pythagoras on raw degrees | One degree of latitude ≈ **111 km**; one of longitude at 53.8°N ≈ **66 km** | Trigonometry |
| Overpass request method | `GET` with a query string | **`POST`**, with the query as the body | Overpass usage policy |
| PCT region for Leeds | `leeds`, or `yorkshire` | **`west-yorkshire`** — and PCT regions are *historic counties*, so Bristol is `avon` | PCT site |
| open-meteo response | A list of records | **Parallel arrays** — `time[i]` matches `precipitation[i]` | open-meteo docs |

!!! danger "The one that would have done the most damage"

    Rows 5 and 6. IMD 2019 carries **2011** LSOA codes; Census 2021 TS045
    carries **2021** LSOA codes. Both are seven-character strings starting
    `E01`. Both look identical in a spreadsheet. A merge between them
    produces a table, not an error.

    If I had joined deprivation to car ownership without checking, I would
    have got a plausible number, drawn a scatter plot, and written three
    confident sentences about the relationship between poverty and car
    ownership in Leeds — and a large share of the rows would have been
    matched to the wrong neighbourhood or silently dropped.

    Chapters 3 and 4 therefore **do not join to each other**. They are
    reported side by side, on their own geographies, and the atlas says why.

---

## 2. The question

An atlas is not a pile of datasets. Each chapter has to answer a question a
person could actually ask, and the questions have to add up to something.

The organising question:

> **In Leeds city centre, who depends on not driving, what does the network
> give them, and where does it hurt them?**

Seven chapters, each one a question rather than a source:

| # | Question | Source | Depends on |
|---|---|---|---|
| 1 | Where can you catch something, and where can you not? | NaPTAN | — |
| 2 | Where do people walking and cycling get hurt? | STATS19 | 1 (for distance-to-stop) |
| 3 | How poor is this patch, against England as a whole? | IMD 2019 + ONS 2011 centroids | — |
| 4 | How many households have no car? | Census TS045 + ONS 2021 centroids | — |
| 5 | What could cycling here be, rather than what it is? | PCT | — |
| 6 | What is within reach of a stop? | OpenStreetMap | 1 |
| 7 | What weather does this all happen in? | open-meteo | — |

Chapter 1 runs first because it fixes the bounding box. Chapters 2 and 6 run
after it because they measure distance to its stops. The rest are
independent.

**The patch.** Leeds city centre and its inner ring:

```
south 53.75   west -1.62   north 53.83   east -1.49
```

That is roughly 8.9 km north–south by 8.6 km east–west — about 76 km². Big
enough that every chapter has data in it; small enough that no national file
takes more than a few seconds to cut down.

I should say plainly what a bounding box is not. This rectangle includes
Headingley, most of Hunslet and a corner of Middleton. Nobody in Leeds calls
all of that "the city centre". The box is a defensible working definition,
not a boundary, and every figure will be titled with the box rather than with
a claim about where Leeds city centre ends.

---

## 3. Architecture

### The constraint that shapes everything

> `python atlas.py` rebuilds the entire atlas from nothing.

Every design decision below follows from that one sentence, because it rules
out the things that make a project unreproducible: fixed paths, manual steps,
a figure that only exists because someone once ran a cell.

### The shape

```
project/atlas_demo/
    atlas.py              the one command
    atlaslib.py           the machinery every chapter shares
    chapters/
        ch01_stops.py     one module per chapter
        ...               each exporting build(ctx) -> Chapter
        ch07_weather.py
    PLAN.md               this file
```

Output does not land next to the code. It lands in the website:

```
site_src/atlas/
    figures/*.png         the figures
    chapter-01.md         generated pages
    ...
    scorecard.md          generated
```

### The four pieces of shared machinery

**1. A cache with provenance.** Every fetch goes through one function that
tries the live source, falls back to the copy in `data/external/`, and
records which one it used, when, from what URL, under what licence. No
chapter is allowed to call `requests` or `read_csv` on a URL directly. The
provenance ledger is written to `provenance.json` and rendered into every
page — so a reader can always see whether a number came from a live fetch or
a cached file from a known date.

This is the part students most often skip, and it is the part that decides
whether the atlas is a document or a screenshot.

**2. A counting filter.** Every filter and every join goes through a helper
that records the row count before and after, with a label. Not printed —
*recorded*, into a structure that ends up in the published page. The counts
are not debug output that scrolls past. They are part of the document.

**3. A figure house style.** One function returns a styled axes; one function
saves at a fixed size and DPI. Every figure gets both axes labelled with
units and a title naming the place and the period, because a figure with an
unlabelled axis is not finished.

**4. A check register.** Each chapter registers its hand-checks as data:
what was claimed, what it was compared against, whether that comparison is
anchored **outside** the dataset, and whether it passed. The scorecard page
is generated from this register. I cannot inflate the honest number without
editing the register in a way that is visible in the diff.

### Why generated pages rather than hand-written ones

The prose in each chapter is mine and is written by hand. Every **number** in
that prose is injected from the computation at build time.

This matters more than it looks. If I wrote "729 casualties" into a markdown
file by hand, that number would be correct exactly until the next time the
data changed, and then it would be quietly wrong forever. Instead the
narrative contains a placeholder that the builder fills. A number in the
published atlas cannot disagree with the number the code produced, because
they are the same number.

---

## 4. The quality-control contract

[`agent_guide.md`](../project/agent_guide.md) describes three layers. Here is how each
one lands in this build.

**Layer 1 — the agent finds it alone.** Tracebacks. Wrong column names,
missing files, type errors. Free. No design needed.

**Layer 2 — the agent does it, if asked.** So I am asking, in writing, and
holding myself to it:

> For every chapter: record the row count before and after each filter and
> each join, each with a label. State every approximation. Record the source
> URL, the licence, and the retrieval date. Do not invent a hand-check.

**Layer 3 — only a person can do it.** Checking that the answer is *true*.
I can compute a number and compare it with an expectation, but if I also
wrote the expectation, the comparison proves only that I am consistent with
myself. So the checks below are separated into two kinds, and only one kind
counts.

---

## 5. The hand-check register — written before the code

This is the section I would most like a student to copy. It is written
**now**, before any chapter exists, so that the checks are chosen to test the
answer rather than to pass.

Each check is marked ⚓ if it is anchored **outside** the data — a map, a
published statistic, a physical fact, somewhere a person has stood — or ○ if
it only tests internal consistency.

| # | Ch | The claim | Checked against | Anchored |
|---|---|---|---|---|
| 1 | 1 | Leeds City Bus Station appears in the stops | Its real address, Dyer Street. A stop should sit within ~150 m of 53.7975 N, 1.5372 W | ⚓ |
| 2 | 1 | Stop count is credible for the area | Density per km², against a plausible urban range | ○ |
| 3 | 1 | The bounding-box filter kept the right rows | Every kept stop's coordinates inside the box | ○ |
| 4 | 2 | Severity mapping is the right way round | Fatalities must be much rarer than slight injuries. If "fatal" outnumbers "slight" the mapping is reversed | ⚓ |
| 5 | 2 | Casualty totals are credible | Against the published DfT total for Leeds district, scaled by area | ⚓ |
| 6 | 2 | Distance-to-stop is in metres, not degrees | A hand-computed distance between two known points | ⚓ |
| 7 | 3 | Decile 1 really is the most deprived | The IMD *score* of decile-1 areas must be higher than decile-10 areas | ⚓ |
| 8 | 3 | The 2011-code join did not silently drop half the patch | Matched count against centroid count | ○ |
| 9 | 4 | Car-free share is credible | Against the published England and Wales figure of about 23.5% — a dense city centre must be well above it | ⚓ |
| 10 | 4 | Percentages are of households, not people | Each LSOA's category counts must sum to its stated total | ○ |
| 11 | 5 | The Dutch scenario exceeds current cycling | Dutch > govtarget > current, in that order, or the columns are misread | ⚓ |
| 12 | 6 | Both Leeds universities are present | The University of Leeds and Leeds Beckett both have city-centre campuses. If either is missing the query is wrong | ⚓ |
| 13 | 6 | The 400 m access threshold is applied in metres | Same conversion as check 6 | ○ |
| 14 | 7 | Annual rainfall is credible | Met Office 1991–2020 average near Leeds is about 660 mm | ⚓ |
| 15 | 7 | The year is complete and hourly | 8,760 rows, ± leap year | ○ |

**Fifteen checks. Nine anchored.** I am writing that ratio down before I know
whether the checks pass, because writing it down afterwards is how you end up
with twenty checks, twenty passes, and four that mean anything.

!!! warning "The trap I am trying to avoid"

    The `agent_guide` records what happened when an assistant built this
    atlas once before: it produced twenty hand-checks and a banner reading
    *20 of 20 pass*. Two of the twenty compared a number with itself. About
    four were worth anything.

    The number that matters is not how many checks pass. It is how many are
    anchored outside the data. Everything else is the code agreeing with
    itself.

---

## 6. Risks, and what I will do about each

| Risk | Likelihood | What I will do |
|---|---|---|
| A live source is down or slow | Moderate — seven sources, several government-hosted | Cached copy of every source in `data/external/`, dated. Fall back, record the fallback, carry on |
| The bounding box is empty for some chapter | Low, but silent | Every chapter asserts a non-zero row count after the box filter and fails loudly |
| A join drops most rows without complaining | **High** — this is the main risk in the whole build | Counted joins. Every merge records both input counts and the output count |
| I use degrees as if they were metres | High — the arithmetic runs fine either way | One conversion function, used everywhere, checked by hand against two known points |
| Chapters 3 and 4 get joined by mistake | Moderate — they look joinable | Structural: different vintages are never merged. Stated in the chapters |
| A figure is wrong but the script succeeds | **High** — no row count finds this | Every figure opened and looked at before publishing. Not "did it run" — looked at |
| Prose numbers drift from computed numbers | Certain, over time | Numbers injected at build time. No hand-typed figures in the narrative |

---

## 7. Build order

1. `atlaslib.py` — cache, counted filters, distance, figure style, check register, page writer.
2. **Chapter 1**, end to end, including its page. Nothing else starts until one chapter works completely, because chapter 1 is where every mistake in the machinery will show up.
3. Chapters 2 and 6, which depend on chapter 1's stops.
4. Chapters 3, 4, 5, 7, which are independent.
5. The synthesis page, which is only allowed to say things the chapters computed.
6. The scorecard, generated from the register.
7. Look at all seven figures. Fix what looks wrong. Rebuild.
8. Delete every output, run `python atlas.py` once, confirm the atlas comes back.

---

## 8. Definition of done

- [ ] `python atlas.py` rebuilds everything from an empty output folder
- [ ] Every chapter records counts before and after every filter and join
- [ ] Every chapter states its source, licence and retrieval date
- [ ] Every figure has labelled axes with units, and a title naming place and period
- [ ] Every figure has been looked at, not just generated
- [ ] Fifteen hand-checks registered; nine anchored outside the data
- [ ] The scorecard reports the honest number, generated from the register
- [ ] The site builds under `mkdocs build --strict`
- [ ] A student can clone the repository, change two lines, and get their own atlas website

---

## 9. Predictions

The plan is worth more if it is falsifiable, so here are numbers I am
committing to before running anything. I expect to be wrong about several.
The execution pages report each one.

| # | Prediction |
|---|---|
| P1 | The patch contains between 800 and 1,600 NaPTAN stops |
| P2 | Fewer than 5% of active-mode casualties in the patch are fatal |
| P3 | The patch is more deprived than England on average — more than 10% of its LSOAs in decile 1 |
| P4 | Car-free households in the patch exceed 40%, against 23.5% for England and Wales |
| P5 | The PCT Dutch scenario is at least 5× current cycling on the network |
| P6 | More than 80% of amenities are within 400 m of a stop |
| P7 | 2025 rainfall is within 20% of the 660 mm long-run average |
| P8 | The 2011↔2021 LSOA join, if attempted, matches less than 95% of rows |

---

## 10. What I expect to be the hardest part

Not the code. The code is seven variations on *fetch, cut, count, draw*, and
I can write that.

The hard part is **not overclaiming**. Every one of these datasets invites a
sentence slightly stronger than it can support. Casualty counts invite "this
junction is dangerous", when they measure reported collisions and not
exposure. Deprivation deciles invite conclusions about the people who live in
them. A cycling potential model invites being read as a forecast.

So the last rule, and the one I will need to apply on every page:

> **Describe what the data shows. Do not describe what it implies about
> people.**

---

Execution begins with [Chapter 1](chapter-01.md).
