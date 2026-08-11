# Your Patch — build a transport atlas

**Weeks 4 and 5. This is your own project — no groups, and nothing here is
graded.** This module is for learning; the skills are assessed elsewhere.
What you take away is the thing you build, and the experience of building
something far larger than you could have written alone.

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

## The chapters

Every chapter has the same shape, and the shape is the method:

> **Fetch** (record the source and the date) → **cut to your patch** (count
> what you cut) → **clean** (count again) → **figure** (labelled axes, units,
> a title with the place name in it) → **three sentences** in your own words
> about what it shows → **one hand-check** against the raw data.

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

## The finish line

There are no marks. The finish line is a fact, not a judgement:

**`python atlas.py` builds your whole atlas from scratch — every fetch, every
figure, the report — on a machine that is not yours.**

That single sentence contains most of what this course has taught: paths that
are not hardcoded, dependencies written down, sources recorded, steps that
run in order without you nursing them. Test it the way week 5 tests it: fresh
folder, clean copy, one command.

## The gallery

Week 5 ends with thirty seconds per person: one page of your atlas on the
screen. Say what the place is and what surprised you. That is all — no
presentation, no questions, no judging. The point is a room full of real
places, analysed by people who could not program five weeks ago.

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
