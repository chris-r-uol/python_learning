# Project — corridor reliability

Weeks 4 and 5. Groups of 3 or 4. You are analysts working for a transport
authority, and these two sessions are studios: short teaching at the start,
then working time, with the instructor and the TA circulating.

**Read [`brief.md`](brief.md) first.**

| | |
|---|---|
| `data/` | The corridor dataset — about 97,000 rows, untidy on purpose |
| `data_sources.md` | The catalogue of real national datasets, for the extension |
| `starter/corridor.py` | A skeleton with function stubs; use it or start from an empty file |
| `starter/fetch_external.py` | A complete, worked example of fetching a national dataset |

---

## The ideas

Two techniques carry the whole project. Everything else you need, you
already have.

### 1. Group, summarise, compare

Almost every question in the brief has the same underlying shape: *split the
records into groups, compute one number per group, and put the groups side
by side.* Journey time by time of day is that shape — group the trips by
departure hour, summarise each group, compare across the day. The worst
segment is that shape twice — group by segment and period, summarise, and
then compare each segment against its own off-peak self rather than against
the others.

If you have ever built a pivot table, you have already done this. The rows
box of a pivot table is the *grouping*; the values box, set to average or
count, is the *summary*. In pandas the same operation is one line:

```python
arrivals.groupby("stop_id")["dwell_s"].median()
```

Read it in three pieces. `groupby("stop_id")` conceptually sorts every row
into one bucket per stop. `["dwell_s"]` says which column you care about
within each bucket. `.median()` collapses each bucket to a single number.
The result is a labelled table — one row per stop, one median per row — and
it arrives in seconds. You can group by two things at once
(`groupby(["stop_id", "direction"])`), which is how "worst segment *and*
time period" becomes answerable.

The line is easy. The thinking is in three choices that the line quietly
encodes, and every group will make them differently:

- **What defines a group.** Hour of day? Hour and direction? Segment and
  period? Choose the grouping that matches the question the authority
  actually asked, not the one that is easiest to type.
- **Which single number honestly summarises the group.** The mean is the
  default and it is frequently the wrong default: journey times are skewed —
  a few terrible runs drag the mean upward — and requirement 2 exists
  precisely because a mean can hide what the authority is asking about.
  Medians resist the drag; percentiles (the 90th, say) *describe* it, and
  "how bad are the bad days" is usually a percentile question. Deciding
  which number is honest here is the same judgement as deciding a design
  percentile in engineering — you have made this kind of choice before.
- **What the comparison is against.** The slowest segment on the corridor is
  probably the longest one, and that finding is worth nothing. A segment
  compared *against its own normal* — peak against off-peak, this week
  against the average week — is where the real finding lives.

When a grouped result surprises you, apply the week 3 checks before you
believe it — pick one group, pull its raw rows, and work the number out by
hand. A wrong grouped answer does not look wrong; it looks like a tidy,
plausible table. And one warning from bitter experience: **group by
identifiers, never by names.** Names get renamed and misspelled; identifiers
do not. If you group this data by `stop_name`, one stop will quietly split
into two groups, both plausible, neither complete — and nothing will warn
you. Count what comes out: eighteen stops in, then eighteen groups out, and
if you get nineteen, stop and find out why.

### 2. Joining datasets

The extension brings in a second dataset, and combining two datasets is one
of exactly three operations. The project deliberately needs no others.

- **A key join.** Rows in two tables match because they share a value — join
  `arrivals` to `stops.csv` on `stop_id`, and every arrival acquires its
  stop's coordinates and sequence position. The one discipline that makes
  joins safe is **counting rows before and after, every single time**. A join
  can silently drop rows that found no partner, and it can silently
  *multiply* rows when a key you assumed was unique appears twice — both
  produce healthy-looking tables and wrong answers. If 94,878 rows go into a
  join and 92,000 come out, those 2,878 rows are a question you must be able
  to answer before you use the result.
- **A bounding-box filter.** Keep only the rows whose latitude and longitude
  fall inside a rectangle around your study area — four comparisons, nothing
  more. Its honesty problem is its shape: a rectangle around an 11 km
  corridor covers many square kilometres of city, and most of what falls in
  the box has nothing to do with your bus route. A bounding box is a first
  cut that makes the data small, never a final answer — say so when you use
  one.
- **A distance.** How far is this casualty from the nearest stop? The trap
  is units: coordinates are in degrees, and **degrees are not metres, and
  degrees of longitude are not even degrees of latitude**. At this city's
  latitude, one degree of latitude spans about 111 km while one degree of
  longitude spans about 68 km — treat them as equal and every east–west
  distance inflates by more than half. For the short distances this project
  needs, it is enough to convert both to metres before applying Pythagoras —
  ask the assistant for exactly that, in those words, and verify it on one
  pair of stops whose spacing you can sanity-check against the segment
  lengths in `segments.csv`.

The scope rule in [`data_sources.md`](data_sources.md) explains why these
three operations are the whole toolkit, and what to say when an assistant
proposes something heavier.

---

## The demonstrations

Two worked examples anchor the studios. `starter/corridor.py` is the shape of
the core analysis — the function names and docstrings describe the pipeline
we will be looking for. `starter/fetch_external.py` is a finished, working
example of pulling a national dataset down to the corridor: run it, read it,
and copy its pattern (source stated, data pulled, rows counted at every cut,
small local copy saved) for whichever source your extension uses.

## The work

The core requirements and the extension menu are in [`brief.md`](brief.md).
Before you analyse anything: look at the data. Open it, sort it, count
things. There are at least five problems in `arrivals.csv`, and the dangerous
ones will not crash your code — they will quietly give you a wrong answer
that looks reasonable. You saw exactly this in week 3.

## The deliverable people forget

**Your repository must run from a clean clone.** In week 5, another group
will download your code onto a different machine and try to run it. Roughly
half of all groups fail this on the first attempt, for avoidable reasons: a
path that only exists on one laptop, a data file that was never committed, a
library that nobody wrote down.

Test it on yourselves first. Clone your own repository into a fresh folder,
on a different machine if you can, and run it.
