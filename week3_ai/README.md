# Week 3 — AI acceleration

**By the end of this week you can:** describe a task precisely enough that
an AI assistant produces correct code, check that code against a case you
work out by hand, and build in small steps that you check as you go.

The session has three parts. First the ideas. Then a worked demonstration.
Then one task, which you do in class.

> In the session, the demonstration comes first. If you are reading this
> before the session, you can do the same: go to Part 2, work through it,
> then come back here. Either order works. Part 2 asks you to judge the
> answer for yourself before it explains anything.

---

## Part 1 — The ideas

### 1. Your job changes

Until now you wrote every line. From this week an assistant can write most
of them. Your job becomes two things: **describe** the work, and **check**
the result.

Engineering already works this way. A senior engineer signs drawings they
did not draw. The signature means: I checked this, and I am responsible for
it. The checking is the job.

An assistant makes you faster only as fast as you can check its output. If
you cannot check it, you are not working faster. You are producing
unchecked answers more quickly, and they look neat, which makes them harder
to doubt.

Both halves of the job need you to read code. That is what weeks 1 and 2
were for.

### 2. Reading code you did not write

From this week the code in front of you contains things this course never
taught. You need to recognise two constructions.

Reading level means you can look at a line and say what it does. You are not
expected to write them from memory.

#### Dictionaries

The demonstration in Part 2 uses three lines that are hard to read without
this section:

```python
speeds_by_link = defaultdict(list)
reader = csv.DictReader(handle)
speeds_by_link[row["link_id"]].append(float(row["speed_kph"]))
```

A **dictionary** is like a list, but you reach items by a **label** instead
of a position:

```python
counts = [52, 22, 24]          # a list. counts[0] is 52
speeds = {"A101": 12.6,        # a dictionary. speeds["A101"] is 12.6
          "A102": 16.6}
```

The label is the **key**. What it points to is the **value**. Curly brackets
build a dictionary. Square brackets look items up. Assigning to a key adds
or replaces an entry:

```python
speeds["B201"] = 23.8
```

Dictionaries are the tool for **grouping**. "All the speeds on link A101" is
something you want to find by the label `A101`, not by remembering that A101
was the fourth link in the file.

The two unfamiliar names:

- `defaultdict(list)` is a dictionary with one convenience. If you use a key
  that does not exist yet, it creates it with an empty list instead of
  raising an error. The code can add a speed to A101's list without first
  checking whether A101 has been seen.
- `csv.DictReader` reads the file so each row is a dictionary, keyed by the
  column names in the header. That is why the code says `row["speed_kph"]`
  instead of `parts[3]`. It is easier to read, and it still works if someone
  adds a column.

So the third line means: take the speed from this row, convert it from text
to a decimal number, and add it to the list of speeds for this row's link.

Remember that sentence. In Part 2 that line is where the analysis goes
wrong.

#### DataFrames

The task uses `pandas`. Pandas gives you a **DataFrame**: a table with named
columns and numbered rows, like one sheet of a spreadsheet.

```python
import pandas as pd
arrivals = pd.read_csv("arrivals.csv")   # the whole file, as a table
```

Six things cover most of the pandas you will be given:

| You see | It means |
|---|---|
| `len(arrivals)` | how many rows |
| `arrivals["dwell_s"]` | one named column |
| `arrivals[arrivals["stop_id"] == "S001"]` | keep only the rows where this is true |
| `arrivals["dwell_s"].mean()` | one number summarising that column |
| `arrivals.groupby("stop_id")["dwell_s"].mean()` | one number per stop |
| `left.merge(right, on="trip_id")` | join two tables on a shared column |

Read the filter line twice. The inner part,
`arrivals["stop_id"] == "S001"`, asks the question of every row at once and
gives a column of true and false answers. The outer square brackets keep the
rows that answered true. It is the `if` inside a loop from week 2, applied
to a whole table at once.

#### Count your rows

Whenever a line changes a table, ask the same question at once: **how many
rows do I have now, and is that the number I expected?**

```python
print(len(arrivals))          # before
arrivals = arrivals.drop_duplicates()
print(len(arrivals))          # after. What did that remove?
```

A filter that matches nothing gives an empty table. A merge on a key that
repeats **multiplies** your rows. Both produce a neat, wrong answer further
down, and neither announces itself. The row count is how you catch them.

### 3. Describing the task

Most requests fail for one reason: they leave out what matters. Compare
these two, using the week 2 data.

The request most people write:

> Analyse traffic_counts.csv and tell me the daily pattern.

The same request, written properly:

> The file `traffic_counts.csv` has four columns: `date` (text,
> YYYY-MM-DD), `hour` (integer, 0-23), `direction` (text, either
> "northbound" or "southbound"), and `count` (integer, vehicles in that
> hour). There are two rows per hour per date, one per direction. Combine
> them into a two-way total before averaging. Produce the average two-way
> count for each hour of the day, as 24 values in vehicles per hour. Peak
> values should be near 2,000 to 3,000. If any hour is missing for a date,
> report it. Do not treat it as zero.

Every sentence in the second version closes a gap. There are four parts:

- **The shape of the input.** Columns, types, units. The second version says
  `count` is vehicles per hour, not per day. Without that, the assistant
  guesses, and both guesses look reasonable.
- **What the file does not say.** Nothing in the CSV says there are two rows
  per hour. You know it. The assistant cannot. Every dataset has facts like
  this, held in people's heads or in documents, never in the file.
- **The output you expect.** Shape, units and rough size. "Peaks near 2,000
  to 3,000" costs one clause and gives you both a check and a shared idea of
  what is wrong.
- **The awkward cases.** Missing hours, duplicates, empty results. Say what
  should happen. Anything you leave out, the assistant decides for you,
  without telling you.

Writing this takes a few minutes. Finding a wrong answer later takes longer.

You have written specifications before: a design brief, a lab method, survey
instructions. This is the same skill.

### 4. Checking the result

The full method is in
[`verification_checklist.md`](verification_checklist.md). Print it and keep
it beside you.

There are four checks. Apply them to any code you did not write.

1. **Does it run?** Read the traceback from the bottom up.
2. **Does it give the right answer on a case you already know?** Take five
   rows of the data. Work out the answer without the code, by hand or in a
   spreadsheet. Then run the code on those five rows and compare. The check
   only works if you calculate the answer separately. Comparing the code to
   itself proves nothing. You saw a small version of this in week 2: the
   `assert` line comparing stage 4 with stage 3. If you cannot build a case
   where you know the answer, stop. You do not understand the problem well
   enough yet to judge the code.
3. **What does it do with the awkward cases?** Missing values, duplicates,
   zeros, empty inputs, and the full file instead of a sample. Feed each one
   in and watch. Code that has only seen clean data has not been tested.
4. **Can you explain every line?** Read the code and say what each line
   does. A line you cannot explain is a line you cannot defend. You can
   always ask the assistant what a line does. Keep asking until you
   understand it.

### 5. Working in small steps

The pattern to avoid: ask for everything, receive two hundred lines, find
the output is wrong, and have no idea which line to suspect. You are then
left debugging unfamiliar code or starting again.

Instead, move in small steps. Ask for one function: *read the file, return
the rows*. Run it. Check the result: print the row count, print the first
row, compare with what you know. Then ask for the next function.

Each step is small enough that when something breaks, only one thing has
changed.

Keep the working version. Save a copy or make a commit every time the code
runs and checks out. Then a failed experiment costs nothing.

Small steps feel slower. Measured to a checked answer, they are faster.

### 6. Where this fails

Four failures to expect:

- **Hidden assumptions.** The assistant assumes metres where your data is in
  kilometres, or that a day ends at midnight when your service runs past it.
  It states the result confidently and does not mention the assumption.
- **Lost data.** A filter that drops rows with missing values, when those
  rows were the finding. A merge that quietly discards everything without a
  match. The row count falls and nothing says so.
- **The wrong statistic.** A mean where the data is skewed and a median was
  needed. An average of averages. The answer is wrong by an amount too small
  to look wrong.
- **Sample versus full file.** Code that works on a hundred clean rows meets
  the real file, which has a duplicate day and a renamed site.

The four checks catch all of these. Reading the output and finding it
believable catches none of them.

---

## Part 2 — The demonstration

Everything above, happening at once, on half a page of real data.

Work through it slowly. Stop where the text tells you to stop. There is a
point in the middle where you judge an answer for yourself. Do that honestly,
even if you already suspect the outcome.

### The data

A traffic authority has average speeds for four road links, measured at two
times of day over ten days. That is eighty rows in
`failure_demo/data/link_speeds.csv`:

```
date,link_id,hour,speed_kph
2026-04-01,A101,8,12.8
2026-04-02,A101,8,12.0
2026-04-03,A101,8,15.0
```

Four columns: the date, the link, the hour, and the speed in kilometres per
hour.

### The request

This sentence was typed into an AI assistant, with the file attached:

> *analyse this traffic data and tell me the average speed on each link*

It is the kind of request anyone would write. It names the file, the subject
and the calculation.

### What came back

The assistant produced `failure_demo/lazy_analysis.py`. The working part is
four lines: read the file, collect the speeds under each link, print the
average of each.

```python
for row in reader:
    speeds_by_link[row["link_id"]].append(float(row["speed_kph"]))

for link in sorted(speeds_by_link):
    values = speeds_by_link[link]
    print(f"{link:<10} {sum(values) / len(values):>10.1f} {len(values):>10}")
```

Run it:

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

Before reading on, decide: **is this right?**

Look at the table. It is formatted. It has units. The values are a
reasonable size for congested urban roads. The order looks sensible: A103
slowest, B201 fastest. Twenty observations per link, and four links times
twenty is the eighty rows we started with.

Most people say it is fine.

### What was wrong

Open the CSV and look at the `speed_kph` column. Thirteen of the eighty
values are `-1.0`:

```
2026-04-04,A101,17,-1.0
```

`-1` is the sensor's code for *no observation*. It is not a speed. No
vehicle travelled at minus one kilometre per hour.

Nothing in the file says this. There is no note, no extra column, no legend.
You would have to know already, or ask, or read a document nobody sent you.

The assistant could not know. It also did not say it was assuming anything.

So it averaged those thirteen values as if they were measured speeds, and
every average came out too low.

The corrected version removes them and reports how many it removed:

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

### Three things to take from this

**1. The order did not change.** A103 is still slowest, B201 still fastest.
Every quick check a busy person makes still passes.

**2. The numbers are badly wrong.** B201's real average is 30.0 kph, not
23.8. That is an error of about 21%. If the next step is a journey time
calculation or a business case, that error goes into a number somebody
signs.

**3. The warning was on screen.** `N obs` reads exactly 20 for every link.
Real sensor data is never that even. The clue was printed in a column nobody
read.

### The point

The assistant did what it was asked. It had no way to know what `-1` meant,
and it did not say it was assuming.

Noticing that is now your job.

This will keep happening, with every tool and every dataset. Every dataset
carries a fact that lives in someone's head instead of in the file: a code
for missing data, a unit, a time zone, a site renamed halfway through. The
assistant cannot see these. You can, if you look.

> `failure_demo/README.md` describes the same demonstration in that folder.

---

## Part 3 — The task

[`task.md`](task.md) — build a journey time tool with AI assistance, using
data that has real problems in it. You do it in class.

You end with three things: the code, the prompts you used, and **evidence
that the code is correct**. Nothing is collected. The evidence matters
because it is the part the assistant cannot do for you.

## What you may use

Anything, including pandas, which this course has not taught. Working out
how to use an unfamiliar library safely is this week's skill.

That includes your choice of assistant. The demonstrations use the one the
university licenses. The method works with any of them, including DeepSeek
and Kimi, and you can prompt in Chinese. See
[`setup/chinese-services.md`](../setup/chinese-services.md).
