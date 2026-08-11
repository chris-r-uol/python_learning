# The failure demo

This folder holds the demonstration that opens week 3.

**The full walkthrough — the request, the data, both results, and what went
wrong — is Part 1 of [the week 3 README](../README.md).** Read it there; it
is written to be followed from beginning to end, and it is the version kept
up to date. This page is only a guide to the files.

## What is in here

| File | What it is |
|---|---|
| `data/link_speeds.csv` | Eighty rows: date, link, hour, speed in kph. Thirteen of the speeds are `-1`, the sensor's code for "no observation" |
| `lazy_analysis.py` | What an AI assistant returned for a vague request. It runs, it looks professional, and it is wrong by about 21% |
| `correct_analysis.py` | The same task done properly: the `-1` values excluded, and the exclusions reported |

```
python lazy_analysis.py
python correct_analysis.py
```

**Do not fix `lazy_analysis.py`.** It is kept broken deliberately, so that
the session can come back to it.

> If the code in these files is hard to read, that is expected: they use
> dictionaries, which the course covers in section 2 of
> [the week 3 README](../README.md). The demonstration makes much more sense
> once you can read the line that causes the error.

## Why this keeps happening

It is worth being clear that this was not a bad tool or an unlucky prompt.
The assistant was asked to average a column, and it averaged that column
correctly. The failure was that nobody told it — and nobody told *you* —
that one value in the column was not a measurement.

Every dataset you ever receive will have a convention of this kind, held in
somebody's head rather than in the file:

- a code for missing data — `-1`, `999`, `NA`, or an empty cell
- a unit that is not what you assumed — metres against kilometres, or a
  count per hour against a count per day
- a time zone, or a day that ends at 03:00 rather than midnight
- a site or a stop that was renamed halfway through the period

None of these are visible to an assistant, and most are not visible in the
file. They surface in one of three ways: somebody tells you, you find the
documentation, or you look at the data closely enough to notice something
that cannot be true. The third is the one you can always do for yourself,
and it is what the verification checklist is for.

## The follow-on

The session rewrites the vague request as a proper specification — one that
states the columns and their types, says what `-1` means and what to do with
it, and describes the expected output. Re-running with that specification
produces the correct analysis first time.

Writing that specification for yourself is [this week's task](../task.md).
