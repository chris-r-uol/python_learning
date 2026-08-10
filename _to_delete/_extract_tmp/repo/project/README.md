# Project — corridor reliability

Weeks 4 and 5. Groups of 3–4. You are analysts for a transport authority.

**Read [`brief.md`](brief.md) first.**

| | |
|---|---|
| `data/` | The corridor dataset. ~97,000 rows. Messy on purpose. |
| `starter/corridor.py` | Skeleton with function stubs. Use it or don't. |

## Before you analyse anything

Go and look at the data. Open it, sort it, count things. There are at least five
things wrong with `arrivals.csv`, and the dangerous ones are the ones that will
not crash your code — they will quietly give you a wrong answer that looks fine.

You saw exactly this in week 3.

## The one deliverable people forget

**Your repo must run from a clean clone.** Someone else will download it onto a
different machine in week 5 and try. About half of all groups fail this the
first time — hardcoded paths, a data file that was never committed, a library
nobody wrote down.

Test it yourself before then. Clone your own repo into a fresh folder and run it.
