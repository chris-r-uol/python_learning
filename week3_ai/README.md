# Week 3 — AI acceleration

**By the end of this week you can:** describe a task precisely enough that an
AI assistant produces correct code, check that code against a case you can
work out by hand, and build things in small steps that you verify as you go.

The session has three parts. First the ideas — what your job becomes when an
assistant writes the code, how to ask for what you want, and how to check
what comes back. Then a worked demonstration of the whole problem in one
page. Then a substantial task, done in class under supervision, which uses
everything from the first three weeks at once.

> **In the session, the demonstration comes first, and cold.** That is
> deliberate: it is far more convincing to be caught out by it than to be
> warned about it. If you are reading this before the session, you are
> welcome to do the same — jump to Part 2, work through it, and come back
> here afterwards. If you would rather have the ideas first, read straight
> through; Part 2 still asks you to judge the answer for yourself before it
> tells you anything.

---

## Part 1 — The ideas

### 1. You have been promoted

Until this week, you wrote every line yourself. From today, an assistant can
write most of the lines — which changes your job rather than removing it.
You are now the person who **specifies** the work and the person who **signs
it off**.

Engineering already has this role, and you know how seriously it is taken. A
senior engineer signs drawings they did not draft. The signature does not
mean "someone competent probably did this"; it means *I checked this, and I
answer for it*. The checking is the qualification. Nobody is impressed that
the drawings were produced quickly.

The same logic governs assistants. An assistant makes you faster at exactly
the rate at which you can check its output — that is the whole equation. A
person who cannot check the output is not being made faster. They are
producing unverified answers sooner, with better formatting, and the
formatting makes it worse, because polished output disarms suspicion. The
two skills this week teaches — specifying and verifying — are the two halves
of being the signature rather than the drafter. Both depend on your being
able to read code, which is what the last two weeks bought you.

### 2. Reading code you did not write

You cannot sign off what you cannot read, and from this week onwards the code
in front of you will contain things the course never taught. That is the
intended condition, not a failure of preparation — but it does mean you need
a reading-level grasp of the two constructions you are about to meet
constantly. Reading level means: you can look at a line and say what it does
and what it produces. You are not expected to write either of these from
memory. That is what the assistant is for.

#### Dictionaries — a list you index by label

The demonstration in Part 2 turns on three lines that would be hard to read
without this section:

```python
speeds_by_link = defaultdict(list)
reader = csv.DictReader(handle)
speeds_by_link[row["link_id"]].append(float(row["speed_kph"]))
```

A **dictionary** is like a list, with one difference: instead of reaching
items by their position, you reach them by a **label** of your choosing.
Compare the two directly:

```python
counts = [52, 22, 24]          # a list  - counts[0] is 52
speeds = {"A101": 12.6,        # a dictionary - speeds["A101"] is 12.6
          "A102": 16.6}
```

The label is called the **key** (here, `"A101"`), and what it points at is
the **value**. Curly brackets `{}` build a dictionary; square brackets still
do the looking-up. You add or overwrite an entry by assigning to a key:

```python
speeds["B201"] = 23.8
```

This is the natural tool for **grouping**, which is why it appears the
moment real data does. "All the speeds recorded on link A101" is a value you
want to reach by the label `A101`, not by remembering that A101 happened to
be the fourth link in the file.

Now the two unfamiliar names from the demonstration:

- `defaultdict(list)` is an ordinary dictionary with one convenience: if you
  reach for a key that does not exist yet, it quietly creates it with an
  empty list rather than raising an error. It exists so that the code can
  say "append this speed to link A101's list" without first checking
  whether A101 has been seen before.
- `csv.DictReader` reads the file so that each row is a dictionary keyed by
  the column names from the header. It is why the code says
  `row["speed_kph"]` instead of `parts[3]` — the same value, reached by
  column name rather than by counting positions. It is more readable, and it
  does not break when somebody inserts a column.

So the third line reads, in plain words: *take the speed from this row,
convert it from text to a decimal number, and add it to the list of speeds
belonging to this row's link.* Hold on to that sentence: in Part 2 it is the
whole of the analysis that goes wrong, and being able to read it is what
lets you see why.

#### DataFrames — a table you can question

The task uses `pandas`, and pandas hands you a **DataFrame**: a table with
named columns and numbered rows, much like one sheet of a spreadsheet. If
you can read a spreadsheet, you already have the mental model; what follows
is only the notation.

```python
import pandas as pd
arrivals = pd.read_csv("arrivals.csv")   # the whole file, as a table
```

Six things account for most of the pandas you will be handed:

| You see | Read it as |
|---|---|
| `len(arrivals)` | how many rows the table has |
| `arrivals["dwell_s"]` | one named column |
| `arrivals[arrivals["stop_id"] == "S001"]` | keep only the rows where this is true |
| `arrivals["dwell_s"].mean()` | one number, summarising that column |
| `arrivals.groupby("stop_id")["dwell_s"].mean()` | split into groups by stop, one mean per group |
| `left.merge(right, on="trip_id")` | join two tables wherever they share a trip id |

The filter line is worth reading twice, because it looks stranger than it
is. The inner part, `arrivals["stop_id"] == "S001"`, asks the question of
every row at once and produces a column of true and false answers. The outer
square brackets then keep the rows that answered true. It is the `if` inside
a loop from week 2, written in one line and applied to the whole table —
exactly the relationship NumPy masks had to loops.

#### The one habit that makes this safe

Whenever a line transforms a table, ask the same question immediately:
**how many rows do I have now, and is that the number I expected?**

```python
print(len(arrivals))          # before
arrivals = arrivals.drop_duplicates()
print(len(arrivals))          # after - what did that remove?
```

This is check 3 of the verification checklist, applied line by line. It is
the difference between using pandas and being used by it: a filter that
matches nothing gives you an empty table, and a merge on a key that repeats
silently *multiplies* your rows — and both of those produce a tidy,
professional, entirely wrong answer downstream. Neither announces itself.
The row count is how you hear them.

### 3. Specifying

Most requests fail for one reason: they leave everything important unsaid.
The demonstration in Part 2 is exactly this failure, and you will recognise
it when you get there. Look at the difference concretely first, using the
week 2 data you already know. Here is the request most people type:

> Analyse traffic_counts.csv and tell me the daily pattern.

And here is the same request as a specification:

> The file `traffic_counts.csv` has four columns: `date` (text, YYYY-MM-DD),
> `hour` (integer, 0–23), `direction` (text, either "northbound" or
> "southbound"), and `count` (integer, vehicles counted in that hour). There
> are two rows per hour per date, one per direction — I want them combined
> into a two-way total before averaging. Produce the average two-way count
> for each hour of the day, as 24 values in vehicles per hour. Peak values
> should land somewhere near 2,000–3,000; single figures or hundreds of
> thousands mean something is wrong. If any hour is missing for some date,
> report it — do not silently treat it as zero.

Every sentence in the second version closes a door through which a wrong
answer could walk. That is the entire craft, and it has four parts:

- **The shape of the input.** Columns, types, units. The specification above
  settles that `count` is vehicles per hour, not per day — without that, an
  assistant guesses, and either guess produces plausible output.
- **The conventions that live outside the file.** Nothing inside the CSV
  says there are two rows per hour. You know it; the assistant cannot. Every
  dataset has knowledge like this — a code for missing data, a unit, a
  renamed site — and it exists only in heads and documentation, never in the
  file itself. The demonstration in Part 2 turns entirely on one such
  convention.
- **The output you expect** — shape, units, and *rough size*. Saying "peaks
  near 2,000–3,000" costs one clause and buys you both a sanity check and a
  shared definition of nonsense.
- **The awkward cases.** Missing hours, duplicates, empty results. For each
  one, say what should happen. Any case you leave unspecified, the assistant
  will decide for you — silently, and with confidence.

Writing this down feels slow, and the feeling is misleading. Every item you
leave out becomes a guess; every guess is a place the code can be
confidently wrong; and finding a confident wrong answer later costs far more
than the specification would have. You have written specifications before —
a design brief, a lab protocol, a survey instruction sheet. This is that
skill, pointed at code.

### 4. Verifying

The full method is [`verification_checklist.md`](verification_checklist.md) —
print it and keep it beside you; it is written to remain useful long after
this course. Its heart is four checks, applied to any code you did not write
yourself.

1. **Does it run?** The lowest bar, and still worth stating, because a
   traceback read bottom-up (week 1) is the fastest possible feedback.
2. **Does it give the right answer on a case you already know?** This is the
   one people skip, so slow down on it. Take five rows of the real data.
   Compute the answer for those five rows *without the code* — by hand, or
   in a spreadsheet, which you can drive expertly. Then run the code on the
   same five rows and compare. The independence is the point: the check must
   not reuse the thing being checked, which is also why "the code agrees
   with itself" is not evidence. You saw this check in miniature in week 2 —
   the `assert` line comparing stage 4 against stage 3. If you cannot
   construct a case where you know the answer, stop: you do not yet
   understand the problem well enough to judge code that claims to solve
   it — and discovering that now is cheap.
3. **What does it do with the awkward cases?** Missing values, duplicates,
   zeros, empty inputs, the full file rather than the sample. Feed each one
   in deliberately and watch. Code that has only ever seen clean data has
   not been tested; it has been rehearsed.
4. **Can you explain every line?** Go through the code and narrate it. A
   line you cannot explain is a line you cannot defend in front of the
   person who asks — and in week 4, someone asks. Asking the assistant what
   a line does is always allowed, and asking until you actually understand
   is the skill. Skipping the line is the only wrong move.

### 5. Working in the loop

The failure pattern has a shape: ask for everything at once, receive two
hundred lines, discover the output is wrong, and have no idea which of the
two hundred lines to distrust. At that point your options are to debug
unfamiliar code — slow, miserable — or to start again — demoralising, and no
more likely to work the second time.

The alternative is to move in small, verified steps. Ask for one function —
*read the file, return the rows*. Run it. Check something about the result:
print the row count, print the first row, compare against what you know.
Only then ask for the next function. Each step is small enough that when
something breaks, the suspect list has one name on it — the piece that
changed since everything last worked.

And keep hold of that "last worked" state deliberately: save a copy, or make
a commit, every time the code reaches a state that runs and checks out. A
known-good version you can return to converts every failed experiment from a
crisis into a shrug. Small steps feel slower than the two-hundred-line leap.
Measure to the point where the answer is *verified*, rather than merely
generated, and they are much faster — this is the same edit → run → look
loop from week 1, with generation added.

### 6. Where this breaks

Honest limits, each with the form it actually takes:

- **Invisible domain assumptions.** The assistant assumes metres where the
  data is in kilometres, or that a day ends at midnight when your service
  runs past it — states the result confidently, and mentions the assumption
  nowhere.
- **Silent data loss.** A filter that drops rows with missing values when
  the missing rows were the finding; a merge that quietly discards
  everything without a match. The row count falls and nothing announces it —
  which is why the checklist has you compare counts at every step.
- **Plausible statistics.** A mean where the distribution is skewed and a
  median was needed; an average of averages that weights nothing correctly.
  The result is wrong by a factor small enough to look right — the hardest
  kind of wrong to catch, and check 2 is the tool that catches it.
- **The sample-versus-full-file gap.** Code rehearsed on a hundred clean
  rows meets the real file, which contains a duplicate day and one renamed
  site — and either crashes, or worse, does not.

Every one of these is caught by the four checks. None of them is caught by
reading the output and finding it believable — and believable output is
exactly what you are about to be shown, while it is 21% wrong.

---

## Part 2 — Demonstration: the failure

Everything above, happening at once, on half a page of real data. This is
the demonstration the session opens with, written out in full so you can
work through it alone.

Take it slowly, and stop where the text tells you to stop. There is a point
in the middle where you are asked to judge an answer for yourself, and the
whole demonstration depends on your doing that honestly before reading on —
including, and especially, if you already suspect where it is going.

### The data

A traffic authority has average speeds for four road links, measured at two
times of day over ten days — eighty rows in
`failure_demo/data/link_speeds.csv`:

```
date,link_id,hour,speed_kph
2026-04-01,A101,8,12.8
2026-04-02,A101,8,12.0
2026-04-03,A101,8,15.0
```

Four columns: the date, which link, the hour of day, and the speed in
kilometres per hour. Nothing complicated.

### The request

This exact sentence was typed into an AI assistant, with the file attached:

> *analyse this traffic data and tell me the average speed on each link*

It is the sort of request anybody would type. It is polite, it is clear
enough in English, and it names the file, the subject and the calculation.

### What came back

The assistant returned the program saved as `failure_demo/lazy_analysis.py`.
Its working part is four lines: read the file, collect every speed under its
link, then print the average of each.

```python
for row in reader:
    speeds_by_link[row["link_id"]].append(float(row["speed_kph"]))

for link in sorted(speeds_by_link):
    values = speeds_by_link[link]
    print(f"{link:<10} {sum(values) / len(values):>10.1f} {len(values):>10}")
```

Run it yourself:

```
cd week3_ai/failure_demo
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

### Stop here

Before reading on, decide for yourself: **is this right?**

Look at the table properly. It is neatly formatted. It carries units. The
values are the right sort of size for congested urban roads. The ranking is
believable — A103 is the slowest, B201 the fastest. Twenty observations per
link, and four links times twenty is the eighty rows we started with, so
nothing appears to be missing.

Most people conclude it is fine. It is not.

### What was wrong

Open the CSV and look down the `speed_kph` column. Thirteen of the eighty
values are `-1.0`:

```
2026-04-04,A101,17,-1.0
```

`-1` is the sensor's code for *no observation was made* — a fault, a gap, a
vehicle count too low to be meaningful. It is not a speed. No car travelled
at minus one kilometre per hour.

Nothing in the file says this. There is no note, no separate column, no
legend. You would have to already know, or ask, or read a data dictionary
that nobody sent you. The assistant could not have known — and, importantly,
it did not say that it was guessing.

So it averaged those thirteen `-1` values in as though they were measured
speeds, and every average came out too low.

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

### The three things to take from this

**1. The ranking did not change.** A103 is still slowest, B201 still
fastest. Every quick sanity check a busy person applies — does the order
make sense, are the magnitudes plausible — still passes. That is exactly why
this kind of error survives review and reaches a decision.

**2. The magnitudes are badly wrong.** B201's real average is 30.0 kph, not
23.8 — an error of about 21%. If the next step is a journey time
calculation, a speed limit compliance assessment or a business case, that
error flows straight into a number somebody signs their name to.

**3. The warning was on the screen the whole time.** Look again at the lazy
table: `N obs` reads exactly 20 for every link. Real sensor data is never
that tidy. The clue was printed, in a column nobody read.

### The point

The assistant did not malfunction. It did exactly what it was asked to do,
correctly, given what it could see. It had no way of knowing what `-1`
meant, and it did not tell you it was assuming.

**Noticing that is your job now.** This will keep happening, with every tool
and every dataset, because every dataset carries a convention that lives in
somebody's head rather than in the file: a code for missing data, a unit, a
time zone, a site that was renamed halfway through. The assistant cannot see
those. You can — but only if you look.

You will meet exactly this class of problem in this week's task, and again
in the project.

> `failure_demo/README.md` holds the same demonstration in the folder
> itself, for when you are working there.

## Part 3 — The task

[`task.md`](task.md) — build a journey time tool, with AI assistance, against
data that has real problems in it. You do it in class, with the instructor
and the TA circulating; it is the first time this course asks you to use an
assistant, a specification, and the checklist together.

You end up with three things: the code, the prompts you used, and **evidence
that the code is correct**. None of it is collected or graded — you keep it.
The evidence matters because it is the part the assistant cannot do for you,
and because the project weeks ask you to repeat exactly this pattern, at
volume, on your own work.

## What you are allowed to use

Anything — including pandas, a library you have not been taught. Working out
how to use an unfamiliar library safely, with the assistant's help and your
own checks, is precisely this week's skill.

"Anything" includes your choice of assistant. The demonstrations use the
university's licensed one, but the method is identical with any capable
service — including Chinese assistants such as DeepSeek or Kimi, and
prompting in Chinese. See
[`setup/chinese-services.md`](../setup/chinese-services.md). The one thing
that never changes, whichever you use, is the checklist.
