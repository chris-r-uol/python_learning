# Week 3 task — build something, then prove it works

**Done in class, with the instructor and TA present. About 2 hours. Finish
anything unfinished before week 4.**

You will build a small tool with AI assistance. Building it is the easy
part. The exercise is proving to yourself that it is correct.

Nothing is collected. Verify it anyway, because after this course nobody
else will.

Try something for ten minutes, then ask. "How do I check this?" is a better
question than "why is this broken?", though both are welcome.

---

## The task

Create a file `journey_time.py` in this folder (`week3_ai/`).

It works on the arrival records at `project/data/arrivals.csv`, measured
from the top of the repository.

Given a *from* stop, a *to* stop, and a time band such as 08:00 to 09:00,
your tool should:

1. Find the journey time between those two stops for every trip that leaves
   within the band.
2. Report the mean, the median and the 90th percentile.
3. State how many trips it used, how many it dropped, and why.

Point 3 is part of the task, not an extra.

You may use pandas. This course has not taught pandas. Ask the assistant for
help, and apply the checklist to everything it gives you. Section 2 of this
week's README covers enough about dictionaries and DataFrames to judge what
comes back.

### The three numbers

Fix the definitions before you ask for code. You cannot check a number whose
definition you never decided.

- **Mean.** Add the journey times, divide by how many there are. You wrote
  this in week 2.
- **Median.** Sort the journey times and take the middle one. With an even
  count, average the two middle values. The median is useful next to the
  mean because a few very slow trips pull the mean up but barely move the
  median. If your two numbers differ, that difference is a result.
- **90th percentile.** The value below which 90% of journeys fall. Nine
  journeys in ten were at least this quick.

There is more than one accepted way to calculate a percentile, and they
disagree slightly. `numpy.percentile(values, 90)` and pandas'
`.quantile(0.9)` use the same default. Either is fine.

**Say which one you used.** "The 90th percentile is 56.5 minutes, using
`numpy.percentile`'s default method" is a statement you can defend. "The
90th percentile is 56.5 minutes" is not, because the reader does not know
what you calculated.

### One thing you have not been taught

The data contains rows that appear more than once. Removing them is simple
with the right tool and very hard with only weeks 1 and 2.

Ask the assistant how to remove exact duplicate rows. Then count the rows
before and after, and check that the number removed is a number you can
explain.

It matters. On this data, leaving the duplicates in adds more than a tenth
to the number of trips counted in a morning peak. Every figure after that
still looks reasonable.

---

## What you end up with

Three files. You keep them. Nobody collects them.

### 1. `journey_time.py`

The tool.

### 2. `prompts.md`

Every prompt you used, in order, including the ones that did not work. If
you rewrote a prompt, include both versions and say what you changed.

The point is not elegant prompts. The point is knowing afterwards which ones
worked, and why.

### 3. `verification.md`

This is the part that matters. It has three sections.

**a. A hand-worked case.**

Choose one pair of stops and one trip. Work out the journey time yourself,
from the raw CSV, with a calculator or a spreadsheet. Show the two
timestamps and the arithmetic. Then show your tool's answer for the same
trip, and say whether they agree.

If they do not agree, write down what you found and what you did about it.

**b. The awkward cases.**

For each case below, find out what your tool does, and say whether that is
correct.

Some of these cases exist in the data and some may not. If you check and
find that a case does not occur, say so. That check is part of the work.
Then test your tool on a small input you build yourself, so you still know
how it behaves.

- A trip with no record at one of the two stops
- A journey time that comes out negative
- A trip that crosses midnight
- A stop that appears under two different names
- Rows that appear twice

You will not have thought of all of these in advance. Finding out which ones
your tool handles is the exercise. A tool that handles three of five, with
the other two written down honestly, is worth more than one that claims all
five with no evidence.

**c. One sentence per function.**

For every function in your file, write one sentence saying what it does. If
you cannot write that sentence, ask the assistant what the function does.
Keep asking until you can.

---

## Where the value is

The tool is not the valuable part. The assistant writes most of it.

The verification is the part you could not have produced three weeks ago,
and the part that makes the tool trustworthy.

In the project weeks, and afterwards, nobody will check your numbers. The
only thing between a wrong number and a decision made on it is whether you
looked.

---

## Two habits to avoid

**Keeping code you cannot explain.** Say what each function does out loud,
to yourself, before moving on. It takes a minute and finds the lines you
accepted without understanding.

**Writing "I tested it and it worked."** That is not evidence. Evidence
contains numbers.
