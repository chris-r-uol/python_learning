# Your Patch — build a transport atlas

**Weeks 4 and 5. This is your own project.**

There are no groups. Nothing here is graded, collected, submitted,
presented or reviewed by anyone. The assessment of these skills happens
elsewhere in your programme.

What you take away is the thing you build. Ask for help whenever you want
it. Nobody will look at your work unless you invite them.

---

## The idea

Choose **a patch**: a British town or city district that interests you.

**Leeds is the default and a good choice.** You are studying here, and the
instructor builds the Leeds atlas chapter by chapter. You always have a
worked example. Several people choosing Leeds is fine. Your bounding box,
your figures and your sentences are still your own.

The data covers all of Great Britain, so choose anywhere that interests you.
A city you want to understand: Manchester, York, Newcastle, Glasgow,
Bristol. A seaside town. The home of a football club you follow. Somewhere
you plan to visit. Pick a place you are curious about.

**Do not choose London.** London-sized cuts of these national files are very
large, and deciding what counts as London wastes your time.

You will build a **transport atlas** of your patch. It is a program that
fetches seven national open datasets, cuts each one down to your patch,
cleans it, draws its figures, and builds a report. It rebuilds everything
from nothing with one command.

By the end of week 5 you will have several hundred lines of working code and
a document about a real place. Five weeks ago you had not written a line of
Python.

## Why the task is this big

You could not write this atlas by hand in the time. Seven data pipelines and
a report builder is weeks of work at your stage.

With an AI assistant it is two studio sessions and the week between,
provided you work the way week 3 taught you: describe the task precisely,
generate one piece at a time, check each piece before the next.

The skill this builds is **directing volume**: running that loop quickly and
repeatedly without losing control of whether the answers are right.

**Read [`agent_guide.md`](agent_guide.md) before you build anything.** Two
of its habits belong at the start. Write down what your assistant is likely
to invent. And **ask for the plan before the code**: a ten-line plan takes a
minute to read, three hundred lines of code does not.

## The chapters

Every chapter has the same shape:

> **Fetch** (record the source and the date) → **cut to your patch** (count
> what you cut) → **clean** (count again) → **figure** (labelled axes,
> units, place name in the title) → **look at the figure** → **three
> sentences** about what it shows → **one hand-check against something
> outside the data**.

Two steps are easy to skip and both catch real errors.

**Look at the figure** means open the image. Not check that the script
finished. Data errors stop the program. Presentation errors do not: a map at
the wrong zoom, a colour scale with everything one colour.

**A hand-check outside the data** means checked against a map, a published
figure, or somewhere you have stood. Not against a number your own code
produced. [`agent_guide.md`](agent_guide.md) explains why this matters.

The seven chapters. Full details, addresses and known problems are in
[`data_sources.md`](data_sources.md):

| # | Chapter | What it answers | Source |
|---|---|---|---|
| 1 | **The patch and its stops** | Where is public transport, and where is it not? | NaPTAN |
| 2 | **Road safety** | Where have people walking and cycling been hurt in two years? | STATS19 |
| 3 | **Deprivation** | Where does your patch sit in England's range? | IMD 2019 + ONS |
| 4 | **Who has no car** | How many households depend on walking, cycling and the bus? | Census 2021 |
| 5 | **Cycling potential** | What does the national model say cycling here could be? | PCT |
| 6 | **What is there** | Schools, surgeries, supermarkets. What do the stops serve? | OpenStreetMap |
| 7 | **A year of weather** | What does a year of rain and temperature look like? | open-meteo |

Do chapter 1 first. It sets your bounding box, which every other chapter
uses. After that, any order.

**Optional extras.** None of these are expected:

- an eighth chapter of your own;
- a comparison of your patch with the Leeds example;
- the whole atlas as a Streamlit app (`requirements-stretch.txt`);
- rail, using the ORR station usage file.

## Choosing a workable patch

You need a **bounding box**: south, west, north and east. Draw it on a map
before you write code.

Keep it small. A town centre and its surroundings, or one district of a
larger city. Not a whole conurbation.

Choose somewhere with at least a few thousand people. A small village makes
the chapters empty.

If your box turns out to be dull or too big, change it. It is one line, and
nothing else in the atlas needs to know.

## Saving your progress with Git

You are about to write several hundred lines quickly. Some experiments will
not work.

**Git** keeps saved versions of your work, so any version that once worked
is one you can return to. You installed it during setup. The whole method is
one habit and five commands.

**The habit:** every time a chapter runs and its checks pass, save a
version.

**Once, at the start.** In a terminal, in your course folder:

```
git init
```

This turns the folder into a *repository*, which is a folder whose history
is recorded. Skip this in a Codespace. It is already one.

**After each chapter starts working:**

```
git status
```

shows what has changed since your last saved version.

```
git add .
```

marks everything to be saved.

```
git commit -m "chapter 2 fetches and passes its row counts"
```

saves it, with a message in your own words. Write messages you will
understand later.

**Looking back.**

```
git log --oneline
```

lists every version you saved.

```
git restore atlas.py
```

puts one file back to how it was at your last save. This is why the habit is
worth having. You can let the assistant try something ambitious, because
going back costs one line.

**A copy online, if you want one.** In VS Code, open the Source Control
panel and use **Publish to GitHub**. It creates a private repository under
your account. After that, `git push` sends each new version up.

In a Codespace there is one difference. You started it from the course
repository, which you cannot write to. The first time you push, GitHub
offers to create a **fork**, which is your own copy. Accept it.

## The finish line

You can check this yourself:

**`python atlas.py` rebuilds your whole atlas from nothing.** Every fetch,
every figure, the report. In a folder where nothing was set up by hand.

That one sentence covers most of this course: paths that are not fixed to
your machine, dependencies written down, sources recorded, steps that run in
order.

Test it. Copy your project to a new folder, delete anything the script
should create, and run the one command.

## Two numbers worth keeping

Keep a count of two things, for yourself:

1. **How many hand-checks you have.**
2. **How many of those you checked against something outside the data**: a
   map, a published statistic, somewhere you have stood.

The second number is the one that means something.

An assistant will produce twenty checks that all pass and prove nothing,
because it wrote both the question and the answer. Only the checks against
the outside world tell you your atlas is true.

Nobody will ask you for these numbers. Keep them honestly anyway.

## Working with real places

Your atlas contains real casualties, real deprivation, real streets where
people live.

Two rules:

- **State what each dataset is and when you fetched it.** A figure without
  that can be mistaken for something it is not.
- **Keep description separate from judgement.** "This area is in England's
  most deprived tenth" is data. Conclusions about the people who live there
  are not yours to draw.

## Where the help is

The studio sessions are for this work. The instructor and the TA are there.
The ten-minute rule from week 1 applies.

The assistant is your main tool. Use any capable one, in any language you
prefer. See [`setup/chinese-services.md`](../setup/chinese-services.md).

[`data_sources.md`](data_sources.md) lists the problems we already know
about.

If a data source is down, the repository has a cached copy of every source
in `data/external/`. Use it and note the date.
