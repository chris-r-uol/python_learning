# The failure demonstration

This folder holds the demonstration that opens week 3.

**The full walkthrough is Part 2 of [the week 3 README](../README.md)**: the
request, the data, both results, and what went wrong. Read it there. This
page describes the files.

## What is here

| File | What it is |
|---|---|
| `data/link_speeds.csv` | Eighty rows: date, link, hour, speed in kph. Thirteen speeds are `-1`, the sensor's code for "no observation" |
| `lazy_analysis.py` | What an AI assistant returned for a vague request. It runs, it looks correct, and it is wrong by about 21% |
| `correct_analysis.py` | The same task done properly. The `-1` values are removed, and the removals reported |

```
python lazy_analysis.py
python correct_analysis.py
```

**Do not fix `lazy_analysis.py`.** It stays broken so the session can return
to it.

> If the code is hard to read, that is expected. It uses dictionaries, which
> section 2 of [the week 3 README](../README.md) covers.

## Why this keeps happening

The assistant was asked to average a column, and it averaged that column
correctly. The failure was that nobody said one value in the column was not
a measurement.

Every dataset has a fact of this kind, held in someone's head rather than in
the file:

- a code for missing data: `-1`, `999`, `NA`, or an empty cell
- a unit that is not what you assumed: metres against kilometres, or a count
  per hour against a count per day
- a time zone, or a day that ends at 03:00 instead of midnight
- a site or stop renamed halfway through the period

None of these are visible to an assistant, and most are not visible in the
file. You find them in one of three ways: somebody tells you, you find the
documentation, or you look at the data closely enough to see something that
cannot be true.

The third one you can always do yourself. That is what the verification
checklist is for.

## Afterwards

The session rewrites the vague request as a proper specification: the
columns and their types, what `-1` means, what to do with it, and the
expected output. Run again with that, and the analysis is correct first
time.

Writing that specification yourself is [this week's task](../task.md).
