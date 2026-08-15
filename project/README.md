# Project — Your Patch: a transport atlas

Weeks 4 and 5. **Your own project: your own place, your own atlas.**

Nothing here is graded, collected or shown to anyone. The sessions are
studios: a short teach at the start, then working time, with the instructor
and the TA there when you want them.

**Read [`brief.md`](brief.md) first.**

| | |
|---|---|
| `brief.md` | The project: seven chapters, one patch, one command |
| `agent_guide.md` | **Read before you build.** How to direct an agent at this much work |
| `data_sources.md` | The data catalogue: addresses, licences, known problems |
| `starter/atlas.py` | The skeleton: chapter stubs and the report builder |
| `starter/fetch_external.py` | One finished chapter fetcher, as the pattern for the rest |
| `data/` | The week 3 task data, and cached copies in `data/external/` |

---

## Two techniques

These carry the whole project. You already have everything else.

### 1. Group, summarise, compare

Most chapters have the same shape: **split the records into groups, work out
one number per group, then compare the groups.**

Casualties by year and severity: group, count, compare. Deprivation by
decile: group, count, compare. Stops by locality, rain by month. The same
move.

If you have used a pivot table, you have done this. In pandas it is one
line:

```python
casualties.groupby("severity").size()
```

Read it in two parts. `groupby("severity")` sorts every row into a group,
one per severity value. `.size()` reduces each group to a count.

Replace `.size()` with `.median()` or `.mean()` on a column and you have the
whole family. Group by two things at once with
`groupby(["year", "severity"])`.

The line is easy. The thinking is in two choices it hides.

**What defines a group.** Choose the grouping that answers the chapter's
question, not the easiest column.

**Which number summarises the group.** Counts are safe. Means often are not.
Skewed data pulls a mean away from the typical value, so a median or a
percentile is often closer to what you mean.

When a grouped result surprises you, apply the week 3 checks. Take one
group, pull its rows, work the number out by hand. A wrong grouped answer
does not look wrong. It looks like a tidy table.

One rule from experience: **group by codes, never by names.** Names get
renamed, misspelled and duplicated. Codes do not. You saw the result of this
in the week 3 data.

### 2. Joining and cutting data

Every chapter starts with a national file and ends with your patch. Getting
from one to the other uses three operations. The atlas needs no others.

**A key join.** Rows in two tables match because they share a code. An LSOA
code joins your patch's areas to their deprivation deciles.

**Count the rows before and after, every time.** A join drops rows that
found no match. A join also *multiplies* rows when a key you thought was
unique appears twice. Both give you a healthy-looking table and a wrong
figure. Knowing your counts catches both.

**A bounding box filter.** Keep rows whose coordinates fall inside your
rectangle. That is four comparisons.

Be honest about what a rectangle is. It includes edges you would not call
your patch. Defining the box is defining the patch, which is why chapter 1
comes first.

**A distance.** How far is each casualty from the nearest stop?

The problem is units. Coordinates are in degrees. **Degrees are not metres,
and a degree of longitude is not a degree of latitude.** At British
latitudes one degree of latitude is about 111 km and one degree of longitude
about 68 km.

Convert both to metres before using Pythagoras. Ask the assistant for
exactly that. Then check one distance against a map before trusting a
thousand of them.

The scope rule in [`data_sources.md`](data_sources.md) explains why these
three are the whole toolkit, and what to say when an assistant suggests
something heavier.

## The worked examples

The instructor builds the same atlas for **Leeds**, live, in the week 4
session: chapters 1 and 2, with the assistant, thinking aloud. That build is
your reference for every chapter shape.

`starter/fetch_external.py` is one finished chapter fetcher: from national
file to a counted, cached, patch-sized copy.

`starter/atlas.py` is the skeleton the atlas hangs on.

## Before you analyse anything

Look at the data. Open it, sort it, count things.

There are at least five problems in the week 3 data, and the dangerous ones
do not stop your code. They give you a wrong answer that looks reasonable.

## The one command

**`python atlas.py` rebuilds your whole atlas from nothing.**

No fixed paths, dependencies written down, sources recorded, no step that
needs you watching it.

Test it: copy your project to a new folder, delete anything the script
should create, run the one command.
