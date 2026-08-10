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

Two techniques carry the whole project. Everything else you need, you already
have.

### 1. Group, summarise, compare

Almost every analytical question in the brief has the same shape: *split the
records into groups, compute one number per group, and put the groups side by
side.* Journey time by hour of day — group by hour, summarise with a median,
compare across the day. The worst segment — group by segment and period,
summarise, compare each segment against its own baseline.

In pandas, the shape is one line:

```python
arrivals.groupby("stop_id")["dwell_s"].median()
```

The thinking is in the three choices, not the line: what defines a group,
which single number honestly summarises it, and what the comparison is
against. The mean is not always that number — requirement 2 exists because a
mean can hide exactly the thing the authority is asking about. When your
grouped result surprises you, apply the week 3 checks before you believe it:
in grouped data, a wrong answer usually looks like a plausible table.

One warning from bitter experience: **group by identifiers, never by names.**
Names change, get renamed, and get misspelled; identifiers are what they are.
This data will punish the other choice.

### 2. Joining datasets

The extension brings in a second dataset, and combining two datasets is one
of three operations — the project deliberately needs no others:

- **A key join:** rows match because they share a code. Count your rows
  before and after, every time; a join that silently drops rows is the most
  common wrong answer in data work.
- **A bounding-box filter:** keep rows whose coordinates fall inside your
  study area. Remember that a box around a corridor is much bigger than the
  corridor.
- **A distance:** how far is this record from the nearest stop. Remember
  that degrees are not metres.

The scope rule in [`data_sources.md`](data_sources.md) explains why these
three are the whole toolkit, and what to say when an assistant proposes
something heavier.

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
