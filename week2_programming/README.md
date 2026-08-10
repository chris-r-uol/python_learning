# Week 2 — Actually programming

**By the end of this week you can:** use variables and lists, write a loop with
a conditional inside it, package repeated work into a function, do arithmetic
on a NumPy array, and produce a labelled figure.

## In the session

`worked_example.py` is built live, in six stages, from a raw CSV file to a
finished figure. It answers one question: *what does an average day look like
at this count site, and when is the peak?*

With your virtual environment active:

```
cd week2_programming
python worked_example.py
```

Stages 1 to 3 solve the problem the long way, with loops. Stage 4 turns the
repeated work into a function. Stage 5 solves the whole thing again in a few
lines of NumPy — which only makes sense because you wrote the loop first.
Stage 6 produces the figure.

## Homework (about 3 hours)

**1. The drills.** Twelve short exercises in `drills/drills.py`. Fill in each
function where it says TODO, then run the file — it marks itself.

```
cd week2_programming/drills
python drills.py
```

Nine out of twelve is a pass. The three marked with a star are harder, and
they are optional.

**2. Reproduce the figure.** The file `drills/target_figure.png` shows weekday
and weekend demand profiles, drawn from the same dataset as the worked
example. Write a script that produces a matching plot.

This task is more difficult than it first appears, for one specific reason:
the data file has a date column, but no day-of-the-week column, and you will
need to know which dates are weekends. Python's standard library can tell you.
Look up the `datetime` module, and in particular what
`date(2026, 3, 2).weekday()` returns. Finding and reading that piece of
documentation is part of the exercise — it is a small version of something you
will do constantly from week 3 onwards.

## The rule that starts now

**A figure with an unlabelled axis is not finished.** From here to the end of
the course, every plot you produce needs axis labels with units, and a title
that a reader could understand without you in the room.
