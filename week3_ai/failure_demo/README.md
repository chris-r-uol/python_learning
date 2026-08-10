# The failure demo

This folder holds the demonstration that opens week 3, kept here so you can
return to it. If you have not seen the session yet, you can read on — but the
demonstration lands harder if you meet it live first.

## What happened

The instructor typed a reasonable-sounding request into an AI assistant:

> *"analyse this traffic data and tell me the average speed on each link"*

and attached `data/link_speeds.csv`. The assistant produced something very
close to `lazy_analysis.py`. Run it:

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

This output looks right. It is formatted, it has units, the values are the
right general size for urban roads, and the ranking is believable — A103
slowest, B201 fastest. Nothing on the screen suggests a problem.

## What was wrong

Open the CSV and look at the `speed_kph` column. Some of the values are `-1`.

`-1` is the sensor's code for *no observation was made*. It is not a speed.
Nothing in the file says so — you would have to ask, or notice, or read a data
dictionary that nobody sent you. The lazy version averaged those `-1` values
in as if they were real measurements, and dragged every mean down.

The corrected version excludes them and reports what it excluded:

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

## The three things worth remembering

**1. The ranking did not change.** A103 is still slowest and B201 still
fastest, so every quick sanity check a busy person would apply still passes.
That is why this kind of error survives review.

**2. The magnitudes are badly wrong.** B201's true mean is 30.0 kph, not
23.8 — an error of about 21%. If the next step is a journey time calculation,
a compliance assessment, or a business case, that error flows straight into a
number somebody will sign.

**3. The warning was on the screen the whole time.** `N obs` reads exactly 20
for every link. Real sensor data is never that tidy. The lazy version counted
the missing rows as observations and reported it, in a column nobody read.

## The point

The assistant did not make a mistake. It did exactly what it was asked to do.
It had no way of knowing what `-1` meant, and it did not say that it was
guessing. **Noticing that is your job now.**

This will keep happening, with every tool and every dataset, because every
dataset has a convention that lives in somebody's head rather than in the
file: a code for missing data, a unit, a time zone, a stop that was renamed.
The assistant cannot see those. You can — but only if you look.

You will meet exactly this class of problem in the project data.
`arrivals.csv` has several conventions that nobody is going to tell you about.

## What to do with this

Write the request again, properly. A usable specification names the columns
and their types, states what `-1` means and what to do with it, and describes
the output you expect. The difference between the lazy prompt and that
specification is the whole of this week — and the first specification you
write for yourself is this week's task.
