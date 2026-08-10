# Week 2 — Actually programming

**By the end of this week you can:** use variables and lists, write a loop with a
conditional inside it, package repeated work into a function, do arithmetic on a
NumPy array, and produce a labelled figure.

## In the session

`worked_example.py` — built live, in six stages, from raw CSV to a finished
figure. One question: *what does an average weekday look like at this count
site, and when is the peak?*

```
cd week2_programming
python worked_example.py
```

Stages 1–3 do it the long way with loops. Stage 4 turns it into a function.
Stage 5 does the whole thing again in three lines of NumPy — which only makes
sense because you wrote the loop first. Stage 6 is the figure.

## Homework (~3h)

**1. Drills.** Twelve short exercises in `drills/drills.py`. Fill in each
function, then run the file — it marks itself.

```
cd week2_programming/drills
python drills.py
```

Nine of twelve is a pass. The three starred ones are stretch.

**2. Reproduce the figure.** `drills/target_figure.png` shows weekday and weekend
demand profiles from the same dataset. Make a plot that matches it.

It is harder than it looks. The file has a date column but no day-of-the-week
column, and you will need one.

## The rule that starts now

**A figure with an unlabelled axis is not finished.** Every plot from here on
gets axis labels with units, and a title someone could read cold.
