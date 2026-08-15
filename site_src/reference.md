---
title: Quick reference
---

# Quick reference

Things to look up, in one place. Each one is taught properly somewhere in
the weeks. This page is only the lookup.

## When something breaks

Read the **last line** of the error first. It says what went wrong. The line
number above it says where.

| Error | What it usually means | Explained in |
|---|---|---|
| `NameError` | A name that was never defined, often a typo | [Week 1](week1_setup/README.md) |
| `TypeError` | Two types that do not fit. Usually text where a number was needed | [Week 1](week1_setup/README.md) |
| `IndexError` | You asked a list for a position it does not have | [Week 1](week1_setup/README.md) |
| `FileNotFoundError` | You are in the wrong folder. Check with `ls` or `dir` | [Week 1](week1_setup/README.md) |
| `IndentationError` | Lines do not line up. The program never started | [Week 1](week1_setup/README.md) |
| `ZeroDivisionError` | Something divided by zero, often an empty input | [Week 1](week1_setup/README.md) |

## The terminal

| Command | What it does |
|---|---|
| `cd foldername` | Move into a folder |
| `cd ..` | Move up one folder |
| `ls` / `dir` | List this folder (macOS, Linux and Codespaces / Windows) |
| `python script.py` | Run a script |
| Ctrl-C | Stop a program that is not stopping by itself |

**Activate your environment in every new terminal.** Without it, `python` is
the wrong Python.

=== "macOS, Linux, Codespaces"

    ```bash
    source .venv/bin/activate
    ```

=== "Windows"

    ```powershell
    .venv\Scripts\activate
    ```

Your prompt shows `(.venv)` when it worked.

## Python you will keep looking up

```python
int("1703")            # text to whole number
float("3.1")           # text to decimal
f"Total: {total}"      # put a value inside text
f"{value:.1f}"         # one decimal place
f"{value:>8}"          # pad to 8 characters, right-aligned
f"{hour:02d}"          # pad a number to two digits: 8 becomes 08

counts[0]              # first item — positions start at zero
counts[-1]             # last item
counts[1:3]            # positions 1 and 2. The second number is excluded
[0] * 24               # a list of twenty-four zeros
len(counts)            # how many items

for value in counts:            # over items
for i in range(len(counts)):    # over positions
range(0, 24, 2)                 # 0, 2, 4 … 22
```

## Reading pandas

You will read more of this than you write. Six lines cover most of it.

| You see | Read it as |
|---|---|
| `len(df)` | how many rows |
| `df["speed"]` | one named column |
| `df[df["stop_id"] == "S001"]` | keep only the rows where this is true |
| `df["speed"].mean()` | one number summarising a column |
| `df.groupby("stop_id")["speed"].mean()` | one number per group |
| `left.merge(right, on="trip_id")` | join two tables on a shared column |

!!! tip "One habit"

    Print `len(df)` before and after every filter and every join.

    A filter that matches nothing gives an empty table. A merge on a repeated
    key multiplies rows. Neither prints a warning. Both give you a tidy table
    and a wrong answer.

## Git, for keeping your progress

```bash
git status                       # what has changed
git add .                        # stage everything
git commit -m "chapter 2 works"  # save a snapshot
git log --oneline                # every snapshot so far
git restore atlas.py             # undo a file back to the last snapshot
```

Save a version every time something works. Then you can try something
ambitious, because going back costs one line.

## Project lookups you must not guess

| You need | Where it comes from |
|---|---|
| ATCO area code | `project/data/external/atco_area_codes.csv`, all 150 |
| PCT region name | The list in [Data discovery](project/data_sources.md). Historic counties, so Bristol is `avon` |
| Local-authority code | The deprivation file itself, beside the district name |
| ONS boundary service address | Copy it from [Data discovery](project/data_sources.md). Do not retype it |

| Code | Means |
|---|---|
| STATS19 `casualty_type` `0` / `1` | pedestrian / cyclist |
| STATS19 severity `1` / `2` / `3` | **fatal** / serious / slight |
| IMD decile `1` | the **most** deprived tenth of England |
| `-1` in a sensor feed | usually "no observation", not a measurement |

## The four checks

Applied to any code you did not write yourself.

1. **Does it run?**
2. **Does it give the right answer on a case you already know?** Work five
   rows out by hand. Compare.
3. **What does it do with the awkward cases?** Missing values, duplicates,
   zeros, empty inputs, the full file rather than the sample.
4. **Can you explain every line?**

The full version is the
[verification checklist](week3_ai/verification_checklist.md). Print it.
