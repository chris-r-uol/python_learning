# Project — corridor reliability

Weeks 4 and 5. Groups of 3 or 4. You are analysts working for a transport
authority.

**Read [`brief.md`](brief.md) first.**

| | |
|---|---|
| `data/` | The corridor dataset — about 97,000 rows, untidy on purpose |
| `data_sources.md` | The catalogue of real national datasets, for the week 5 extension |
| `starter/corridor.py` | A skeleton with function stubs; use it or start from an empty file |
| `starter/fetch_external.py` | A complete, worked example of fetching a national dataset |

## Before you analyse anything

Look at the data. Open it, sort it, count things. There are at least five
problems in `arrivals.csv`, and the dangerous ones are those that will not
crash your code — they will quietly give you a wrong answer that looks
reasonable. You saw exactly this in week 3.

## The deliverable people forget

**Your repository must run from a clean clone.** In week 5, another group will
download your code onto a different machine and try to run it. Roughly half of
all groups fail this on the first attempt, for avoidable reasons: a path that
only exists on one laptop, a data file that was never committed, a library
that nobody wrote down.

Test it on yourselves first. Clone your own repository into a fresh folder, on
a different machine if you can, and run it.
