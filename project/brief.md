# Your Patch — build a transport atlas

**Weeks 4 and 5. This is your own project, and it is yours alone.** There
are no groups. Nothing here is graded, collected, submitted, presented, or
reviewed by anybody — not by the instructor, not by the TA, not by other
students. This module exists so that you learn to do this; the assessment
of these skills happens elsewhere in your programme, not here.

What you take away is the thing you build, and the experience of building
something far larger than you could have written alone. Ask for help as
often as you like — that is what the studio sessions are for — but nobody
is going to look over your shoulder unless you invite them.

---

## The idea

Choose **a patch**: a British town or city district that interests you.

**Leeds is the default, and a perfectly good choice** — it is the city you
are studying in, and the instructor's demonstrator builds the Leeds atlas
chapter by chapter, so you will always have a worked reference. If several
people take Leeds, that is fine: your bounding box, your figures, and your
sentences will still be your own.

But the datasets cover all of Great Britain, so if anywhere else appeals,
take it. A city you have heard of and want to understand — Manchester, York,
Newcastle, Glasgow, Bristol. A seaside town. The home of a football club you
follow. Somewhere you are thinking of visiting while you are in the UK. The
atlas is more interesting when you are curious about the answer, and that is
the whole selection criterion.

One exclusion: **not London.** Partly because it is what everyone reaches
for, but mainly because it is a practical trap — London-sized cuts of these
national files are enormous, and its geography needs decisions (which
borough? what is "London"?) that eat your studio time without teaching you
anything new.

You will build **a transport atlas of your patch**: a program that fetches
seven national open datasets, cuts each one down to your patch, cleans it,
draws its figures, and assembles everything into a report — and that rebuilds
the whole thing from nothing with one command.

By the end of week 5 you will have several hundred lines of working code and
a document about a real place, built by you. Five weeks ago you had not
written a line of Python. That distance is the point of the module.

## Why the task is deliberately too big

Be clear about what is being practised. You could not write this atlas by
hand in the time available — at your stage, seven data pipelines and a report
builder is weeks of work. That is intentional. Working with an AI assistant,
it is two studio sessions and the week between, *provided* you work the way
week 3 taught you: specify precisely, generate one piece at a time, verify
each piece before the next.

The skill this project builds is **directing volume**: running that loop
quickly and repeatedly without losing control of correctness. It is the
single most transferable thing this course teaches, and the only way to
learn it is on a task too big to do any other way.

**Read [`agent_guide.md`](agent_guide.md) before you build anything.** Two
of its habits belong at the very start rather than partway through: writing
down what your assistant is likely to invent, and **asking for the plan
before the code**. That second one is the cheapest quality control
available — a ten-line plan takes a minute to read, and three hundred lines
of generated code does not, so the plan is the last point where reviewing
the work honestly is realistic. Some assistants offer this as a built-in
plan mode; asking for it in words works everywhere.

## The chapters

Every chapter has the same shape, and the shape is the method:

> **Fetch** (record the source and the date) → **cut to your patch** (count
> what you cut) → **clean** (count again) → **figure** (labelled axes, units,
> a title with the place name in it) → **look at the figure** → **three
> sentences** in your own words about what it shows → **one hand-check
> anchored outside the data**.

Two of those steps are easy to skip and are the ones that catch real
errors. **Look at the figure** means open the image, not check that the
script finished — data errors fail loudly, but presentation errors fail
silently and look confident. And a hand-check **anchored outside the data**
means checked against a map, a published statistic, or somewhere you have
stood — not against a number your own code produced.
[`agent_guide.md`](agent_guide.md) explains why that distinction is the
whole of quality control here.

The seven core chapters, with sources — all details, working addresses, and
known traps are in [`data_sources.md`](data_sources.md):

| # | Chapter | What it answers | Source |
|---|---|---|---|
| 1 | **The patch and its stops** | Where is public transport, and where is it not? | NaPTAN |
| 2 | **Road safety** | Where have people walking and cycling been hurt, in the last two years? | STATS19 |
| 3 | **Deprivation** | How does your patch sit in England's deprivation distribution? | IMD 2019 + ONS lookup |
| 4 | **Who has no car** | How many households depend entirely on walking, cycling, and the bus? | Census 2021 (Nomis) |
| 5 | **Cycling potential** | What does the national model think cycling here could be? | PCT |
| 6 | **What is there** | Schools, surgeries, supermarkets — what do the stops actually serve? | OpenStreetMap |
| 7 | **A year of weather** | What does a year of rain and temperature look like here? | open-meteo |

Do chapter 1 first — it defines your patch's bounding box, which every other
chapter reuses. After that, any order.

**Stretch, if you have appetite** (none of this is expected): an eighth
chapter of your own devising; a comparison chapter — your patch against the
Leeds demonstrator; the whole atlas as a Streamlit app
(`requirements-stretch.txt`); rail, using the ORR station usage file.

## Making the patch workable

Whatever place you choose, the working unit is a **bounding box** — south,
west, north, east — that you can defend as "my patch". Draw it on a map
before you write any code, and keep it modest: a town centre and its
surroundings, or one district of a bigger city, not a whole conurbation.
Somewhere with at least a few thousand people in it; an isolated hamlet will
make the chapters feel empty. If your first box turns out dull or unwieldy,
changing it is one line — nothing else in the atlas needs to know.

## Saving your progress with Git

You are about to produce several hundred lines of code at speed, and some of
your experiments will not work. The professional answer to that is **Git**:
a tool that keeps named snapshots of your work, so that any version that
ever worked is a version you can get back. You installed it in setup week;
this is the moment it starts earning its place. The whole working method is
one habit and four commands.

**The habit:** every time a chapter runs and its checks pass, take a
snapshot. A known-good version you can return to turns every failed
experiment from a crisis into a shrug.

**One-time start.** In a terminal, standing in your course folder:

```
git init
```

That turns the folder into a *repository* — a folder whose history is
recorded. (If you work in a Codespace, skip this: it is already one.)

**The snapshot loop** — after each chapter starts working:

```
git status
```

shows what has changed since your last snapshot. Then:

```
git add .
```

stages everything, and:

```
git commit -m "chapter 2 fetches and passes its row counts"
```

records the snapshot, with a message in your own words saying what state
this is. Write messages your future self can read — "fixed stuff" helps
nobody, including you.

**Looking back, and getting things back.**

```
git log --oneline
```

lists every snapshot you have taken. And if an experiment has made a mess of
one file, this restores it to how it was at your last commit:

```
git restore atlas.py
```

That command is the whole reason the habit pays: it means you can let the
assistant try something ambitious, knowing the way back costs one line.

**An off-machine copy (optional but sensible).** If you would like your
atlas backed up to your own GitHub account, the easiest route is VS Code's
Source Control panel — the **Publish to GitHub** button creates a private
repository under your account and pushes to it in one step. After that,
`git push` sends each new snapshot up. In a Codespace there is one wrinkle:
you launched it from the course repository, which is not yours to push to —
the first time you push, GitHub will offer to create a **fork** under your
own account. Accept, and everything works from then on.

That is the entire toolkit: `init` once, then `status`, `add`, `commit` as
a rhythm, `log` and `restore` when you need history, `push` if you want a
copy in the cloud. Ask the assistant about anything beyond this — branches,
undoing commits — if and when you ever need it, which in this project you
probably will not.

## The finish line

The finish line is a fact you can check for yourself, not a judgement
anybody makes about you:

**`python atlas.py` builds your whole atlas from scratch — every fetch, every
figure, the report — in a folder where nothing has been set up by hand.**

That single sentence contains most of what this course has taught: paths that
are not hardcoded, dependencies written down, sources recorded, steps that
run in order without you nursing them. Test it: copy your project to a fresh
folder, delete anything the script should be creating, and run the one
command. Either it rebuilds or it does not, and you will know which.

## The two numbers worth knowing

Keep a running count of two things, for yourself:

1. **How many hand-checks you have.**
2. **How many of those you verified against something outside the data** — a
   map, a published statistic, somewhere you have actually stood.

The second number is the one that means anything, and it is easy to fool
yourself about. An assistant will cheerfully produce twenty checks that all
pass and prove nothing, because it wrote both the question and the answer.
Only the externally anchored ones tell you your atlas is true rather than
merely self-consistent. [`agent_guide.md`](agent_guide.md) explains the
difference and how to get more of them.

Nobody is going to ask you for these numbers. That is exactly why they are
worth keeping honestly — the habit of knowing how much of your own work you
have actually confirmed is the thing you are here to build, and it only ever
gets used when nobody is checking.

## Working honestly with real places

Your atlas will contain real casualties, real deprivation, real streets where
real people live. Two disciplines, kept from week 3: state what the data is
and when you fetched it, so your figures cannot be mistaken for something
they are not; and write about your patch with the respect you would want for
your own street. "This LSOA is in England's most deprived decile" is data.
Conclusions about the people who live there are not yours to draw.

## Where the help is

The studio sessions exist for exactly this work — the instructor and the TA
are there to unblock you, and the ten-minute rule from week 1 still applies.
The assistant is your production tool — any capable one, in any language you
prefer (see [`setup/chinese-services.md`](../setup/chinese-services.md));
`data_sources.md` lists every trap we already know about; and if an API is
down, the repository carries cached fallback copies of every source — use
them and note the date.
