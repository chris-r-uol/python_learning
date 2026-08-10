# The failure demo

**Instructor: run this in the first 15 minutes of week 3, before any teaching.**

## The setup

Say the task out loud, then type the prompt in front of them exactly as written:

> *"analyse this traffic data and tell me the average speed on each link"*

Attach `data/link_speeds.csv`. Whatever assistant you are using will produce
something very close to `lazy_analysis.py`. If it produces something better,
use the saved file instead and say so — the point survives either way.

Run it:

```
python lazy_analysis.py
```

```
Average speed by link
----------------------------------
Link         Mean kph      N obs
A101             12.6         20
A102             16.6         20
A103              6.5         20
B201             23.8         20
```

**Stop here. Ask the room: is this right?**

Let the silence run. It looks right. It is formatted, it has units, the numbers
are the right order of magnitude for an urban link, and the ranking is
plausible — A103 is the slowest, B201 is the fastest.

## The reveal

Open the CSV. Look at the `speed_kph` column. Some values are `-1`.

`-1` is the sensor's code for *no observation*. It is not a speed. Nothing in
the file says so — you would have to ask, or notice, or read a data dictionary
that nobody sent you.

Run the correct version:

```
python correct_analysis.py
```

```
Link         Mean kph   N used  N missing    % missing
A101             13.3       19          1           5%
A102             21.0       16          4          20%
A103              8.4       16          4          20%
B201             30.0       16          4          20%
```

## What to draw out

Three things, in this order:

**1. The ranking didn't change.** A103 is still slowest, B201 still fastest. Every
sanity check a busy person would apply still passes. This is why it survives.

**2. The magnitudes are badly wrong.** B201 is 30 kph, not 23.8 — a 21% error. If
the next step is a journey time calculation, or a speed limit compliance
assessment, or a business case, that error propagates into a number someone
signs.

**3. The tell was there.** `N obs` is exactly 20 for every link. Real sensor data
is never that tidy. The lazy version counted the missing rows as observations
and told you so, in a column nobody read.

Then the line that the rest of the course hangs on:

> The assistant did not make a mistake. It did exactly what it was asked. It
> had no way to know what `-1` meant, and it did not tell you it was guessing.
> **That is your job now.**

## Why it will keep happening

This is not a quirk of one tool or one prompt. Every dataset you will ever get
has a convention that lives in someone's head and not in the file: a sentinel
value, a unit, a time zone, a stop that got renamed. The assistant cannot see
those. You can — but only if you look.

You will meet exactly this class of problem in the project. `arrivals.csv` has
several conventions nobody has told you about.

## Follow-on

Rewrite the prompt together, out loud, until it contains: the columns and their
types, what `-1` means, what to do with it, and what the output should look
like. Re-run. Compare.

That rewritten prompt is the first thing they will write for themselves in the
homework.
