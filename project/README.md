# Project — Your Patch: a transport atlas

Weeks 4 and 5. **An individual project: your own place, your own atlas, and
nothing graded.** The sessions are studios — short teaching at the start,
then production time, with the instructor and the TA circulating.

**Read [`brief.md`](brief.md) first.**

| | |
|---|---|
| `brief.md` | The project: seven chapters, one patch, one command |
| `data_sources.md` | The source catalogue — addresses, licences, and known traps |
| `starter/atlas.py` | The atlas skeleton: chapter stubs and the report builder's shape |
| `starter/fetch_external.py` | A complete, worked chapter fetcher (STATS19), the pattern for all of them |
| `data/` | The corridor dataset used by the week 3 task, and `data/external/` cached fallbacks |

---

## The ideas

Two techniques carry every chapter. Everything else you need, you already
have.

### 1. Group, summarise, compare

Almost every chapter's figure has the same underlying shape: *split the
records into groups, compute one number per group, and put the groups side by
side.* Casualties by year and severity — group, count, compare. Deprivation
by decile — group, count, compare. Stops by locality, rain by month: the
same move every time.

If you have ever built a pivot table, you have already done this. In pandas
it is one line:

```python
casualties.groupby("severity").size()
```

Read it in two pieces: `groupby("severity")` conceptually sorts every row
into one bucket per severity value; `.size()` collapses each bucket to a
count. Swap `.size()` for `.median()` or `.mean()` on a chosen column and
you have the whole family. You can group by two things at once —
`groupby(["year", "severity"])` — which is how most two-series figures in
your atlas will start.

The line is easy; the thinking is in two choices it quietly encodes. *What
defines a group* — choose the grouping that matches the chapter's question,
not the easiest column. And *which single number honestly summarises the
group* — counts are safe; means are frequently not, because skewed data
drags a mean away from the typical case, and a median or a percentile often
says what you actually mean. When a grouped result surprises you, apply the
week 3 checks before believing it: pull one group's raw rows and work the
number out by hand. In grouped data, a wrong answer looks like a tidy,
plausible table.

One warning from bitter experience: **group by identifiers, never by
names.** Names get renamed, misspelled, and duplicated; codes do not. You
met the consequences in the week 3 data.

### 2. Joining and cutting datasets

Every chapter starts with a national file and ends with your patch. Getting
from one to the other is one of exactly three operations — the atlas
deliberately needs no others:

- **A key join.** Rows in two tables match because they share a code — an
  LSOA code joins your patch's areas to their IMD deciles. The discipline
  that makes joins safe is **counting rows before and after, every time**. A
  join silently drops rows that found no partner, and silently *multiplies*
  rows when a key you assumed unique appears twice; both produce
  healthy-looking tables and wrong figures. Know your counts and both
  failures announce themselves.
- **A bounding-box filter.** Keep rows whose coordinates fall inside your
  patch's rectangle — four comparisons. Be honest about what a rectangle is:
  it will include fringes you do not think of as your patch. Defining the
  box *is* defining the patch, which is why chapter 1 comes first.
- **A distance.** How far is each casualty from the nearest stop? The trap
  is units: coordinates are in degrees, and **degrees are not metres, and
  degrees of longitude are not degrees of latitude** — at British latitudes
  one degree of latitude spans about 111 km and one degree of longitude
  about 68 km. Convert both to metres before applying Pythagoras — ask the
  assistant for exactly that, in those words — and sanity-check one distance
  against a map before trusting thousands.

The scope rule in [`data_sources.md`](data_sources.md) explains why these
three operations are the whole toolkit, and what to say when an assistant
proposes something heavier.

---

## The demonstrations

The instructor builds the same atlas, live, for **Leeds** — chapters 1 and 2
in the week 4 session, with the assistant, thinking aloud, including at least
one wrong generation caught by a row count. That build is your worked
reference for every chapter shape.

`starter/fetch_external.py` is the finished pattern on paper: one complete
chapter fetcher, from national file to counted, cached, patch-sized copy.
`starter/atlas.py` is the skeleton the whole atlas hangs on.

## The one command

**`python atlas.py` should rebuild your entire atlas from scratch on a
machine that is not yours.** No hardcoded paths, dependencies written down,
sources recorded, no step that needs you standing over it. That sentence is
the finish line, and testing it costs five minutes: fresh folder, clean
copy, one command.
