# The scorecard

*How much of this can be trusted, and why*

!!! quote "Written by an AI assistant"

    This page was planned, built and written by Claude. The prose is
    hand-written; every number in it was injected from the computation
    at build time. Rebuilt 2026-08-15 11:42 UTC.

The [agent guide](../project/agent_guide.md) records what happened when an
assistant built an atlas like this one before: **twenty hand-checks, a banner
reading "20 of 20 pass", and about four that were worth anything.** Two of the
twenty compared a number with itself.

So this page is generated from the check register rather than written. Each
check declares whether it is anchored **outside** the data — against a map, a
published statistic, a physical fact — or whether it only tests that the code
agrees with itself. The honest number cannot be inflated without editing the
register in a way that shows up in the diff.

## The two numbers

| | |
|---|---:|
| Hand-checks registered | **27** |
| Anchored outside the data ⚓ | **14** |
| Internal consistency only ○ | 13 |
| Failing | 0 |

**14 is the number that means something.** The other 13 are worth having — they catch a filter that stopped filtering — but a check that compares the code with itself proves the code is consistent, not that it is right.

## Every check

| # | Ch | The claim | Checked against | Anchored | Result |
|---|---|---|---|:---:|:---:|
| 1 | 1 | Leeds City Bus Station is in the data | Its real address on Dyer Street (53.7975 N, 1.5372 W) | ⚓ | pass |
| 2 | 1 | Leeds Rail Station is in the data | It exists, and it is the busiest station in the North outside Manchester | ⚓ | pass |
| 3 | 1 | Every kept stop is inside the bounding box | The box coordinates themselves | ○ | pass |
| 4 | 1 | Stop density is credible for an English city | A plausible urban range of 5–40 stops per km² | ⚓ | pass |
| 5 | 1 | Every stop appears in exactly one category on the map | The category counts, summed against the total | ○ | pass |
| 6 | 2 | The severity codes are the right way round | Reality: fatal collisions are far rarer than slight injuries | ⚓ | pass |
| 7 | 2 | Distances are in metres, not degrees | 0.01° of latitude, which is 1,111 m by definition | ⚓ | pass |
| 8 | 2 | Casualty numbers are the right order of magnitude | Leeds district reports roughly 300–450 active-mode casualties a year | ⚓ | pass |
| 9 | 2 | The live build reproduces the independent cached extract | casualties.geojson, built earlier by a different script | ○ | pass |
| 10 | 2 | Every casualty carries a mode and a severity | The mapped columns, checked for gaps | ○ | pass |
| 11 | 3 | Decile 1 really is the most deprived, not the least | The IMD score itself, which rises with deprivation | ⚓ | pass |
| 12 | 3 | The 2011-code join did not silently drop the patch | Matched rows against centroids in the box | ○ | pass |
| 13 | 3 | Deciles cover the full 1–10 range as published | The set of distinct decile values found | ○ | pass |
| 14 | 4 | The car-free share is credible for a dense city centre | The published England and Wales figure of 23.5% | ⚓ | pass |
| 15 | 4 | Percentages are of households, not of people | Each neighbourhood's no-car count against its stated total | ○ | pass |
| 16 | 4 | The statistics request was not silently truncated | The number of areas asked for against the number returned | ○ | pass |
| 17 | 4 | The 2021-code join matched the patch | Matched rows against centroids in the box | ○ | pass |
| 18 | 4 | Chapters 3 and 4 use genuinely different geographies | The 2011 codes from chapter 3, intersected with these 2021 codes | ○ | pass |
| 19 | 5 | The scenario columns are the right way round | The definitions: today ≤ government target ≤ Dutch, by construction | ⚓ | pass |
| 20 | 5 | Segment lengths are in metres and are plausible | A city network: total length of the same order as the patch size | ⚓ | pass |
| 21 | 5 | The region name is the right one | A non-empty network inside the patch | ○ | pass |
| 22 | 6 | Both Leeds universities appear in the amenities | They exist, and both have campuses inside this box | ⚓ | pass |
| 23 | 6 | Amenity counts are plausible for a city of this size | A city-centre patch should hold dozens of schools, not two or two thousand | ⚓ | pass |
| 24 | 6 | The 400 m access threshold is applied in metres | The same conversion tested in chapter 2 against a known distance | ○ | pass |
| 25 | 7 | Annual rainfall is credible for this part of England | Met Office 1991–2020 average near Leeds, about 660 mm | ⚓ | pass |
| 26 | 7 | The year is complete and hourly | 8760 hours in a 365-day year | ⚓ | pass |
| 27 | 7 | The parallel arrays are still in step | The lengths of time, precipitation and temperature | ○ | pass |

## What the other layers did

Hand-checks are only the third layer. The other two ran throughout.

| Layer | What it caught here |
|---|---|
| **1 — free** | Tracebacks: wrong column names, a 404 on the deprivation file, a coordinate pair the wrong way round. Fixed as they appeared, at no cost. |
| **2 — ask for it** | **24 counted filters and joins**, recorded on the chapter pages. These caught the joins that would have quietly shrunk. |
| **3 — only a person** | The 14 anchored checks above, and **18 figures opened and looked at**. Looking at the figures caught two errors that no count could: ten stops drawn nowhere, and a colour scale that separated nothing. |

## Where the plan was wrong

The [plan](plan.md) was written before any code existed. These are the places it turned out to be wrong, kept rather than quietly corrected:

- **Chapter 1.** **Plan §2 said chapter 1 answers "where can you catch something". It planned a single query: ATCO area 450.** [→](chapter-01.md)
- **Chapter 1.** **Plan §6 listed "a figure is wrong but the script succeeds" as a high risk. It happened on the first figure I drew.** [→](chapter-01.md)
- **Chapter 1.** **The first coverage map was a broken figure that ran perfectly.** [→](chapter-01.md)
- **Chapter 1.** **Prediction P1 said the patch would hold between 800 and 1,600 NaPTAN stops. The answer is 1,328.** [→](chapter-01.md)
- **Chapter 2.** **Plan §6 predicted the live fetch would be the fragile part.** It was not: all four national files, about 60 MB, downloaded in under four seconds. The fragile part was the coding of the columns, which no amount of successful downloading protects you from. [→](chapter-02.md)
- **Chapter 2.** **Prediction P2 said fewer than 5% of active-mode casualties in the patch would be fatal. The answer is 2.1%.** [→](chapter-02.md)
- **Chapter 3.** **Plan §6 rated "a live source is down" as a moderate risk. It happened on the very first address I tried.** [→](chapter-03.md)
- **Chapter 3.** **Prediction P3 said more than 10% of the patch's LSOAs would be in decile 1. The answer is 42.4%.** [→](chapter-03.md)
- **Chapter 4.** **Prediction P4 said car-free households in the patch would exceed 40%. The answer is 42.6%.** [→](chapter-04.md)
- **Chapter 4.** **Prediction P8 said a 2011↔2021 LSOA join would match less than 95% of rows. The measured overlap is 94.3%.** [→](chapter-04.md)
- **Chapter 5.** **Prediction P5 said the Dutch scenario would be at least 5× current cycling. The measured multiple is 6.6×.** [→](chapter-05.md)
- **Chapter 6.** **Prediction P6 said more than 80% of amenities would be within 400 m of a stop. The answer is 100.0%.** [→](chapter-06.md)
- **Chapter 7.** **Prediction P7 said 2025 rainfall would be within 20% of the 660 mm long-run average. It came in at 756 mm, which is 114% of normal.** [→](chapter-07.md)

## What none of this proves

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
