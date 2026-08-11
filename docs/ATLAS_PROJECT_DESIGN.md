# Your Patch — the individual transport atlas

Design note, 10 August 2026. Replaces the group corridor project in weeks 4–5,
and supersedes both the corridor sections of `COURSE_DESIGN.md` and the whole
of `WEEKS_4_5_DESIGN.md`.

## The constraints this design answers

1. **No group work.** Every student builds their own project.
2. **No grading, anywhere in the course.** This is a learning module; the
   skills are assessed elsewhere. Nothing in the student material may read as
   marks, weights, or rubrics.
3. **The point is volume through AI.** The task must be so bulky that a
   student at this level could not reasonably write it by hand in the time —
   because the skill being practised is *directing* production: running the
   specify → generate → verify loop many times, quickly, on real material.
4. **Not a corridor study.** A corridor-reliability commission resembles
   another module we teach; weeks 4–5 must not.

## The concept

Every student chooses **a patch**: a British town or city district. The
cohort is substantially international, so the framing is deliberately *not*
"your home town" — the data is GB-only, and personal geography would exclude
exactly the students it was meant to motivate. Instead: **Leeds is the
default and always fine** (it is where they are, and it is the demonstrator),
and anywhere else in Great Britain is open to anyone curious about it — a
city they have heard of, a club they follow, somewhere they mean to visit.
London is excluded: it is the reflex choice, the file sizes are hostile, and
"which London?" burns studio time. Duplicate patches are acceptable —
thirty Leeds atlases would still differ in box, figures, and findings —
though the brief nudges toward variety because the gallery is better for it.

They then build **a transport atlas of their patch**: a pipeline that fetches
seven national open datasets, cleans each one, draws its figures, and
assembles the whole thing into a multi-page report that rebuilds from scratch
with one command. Chapter by chapter: the bus stops that serve the patch, its
road casualty record, its deprivation profile, who has no car, its modelled
cycling potential, what OpenStreetMap knows is there, and a year of its
weather. Each chapter ends with three sentences the student writes
themselves: what the data shows about *their* place.

The instructor's demonstrator is the same atlas built live for **Leeds** —
which keeps Leeds as the home city of the course, gives every chapter a
worked reference, and gives anyone who takes Leeds as their own patch a
scaffold they can check themselves against at every step.

## Why this satisfies the constraints

**Individual by construction.** Every student runs their own pipeline end to
end — there is nothing to divide up and nobody to hide behind, even when two
students share a city, because the box, the figures, and the sentences are
theirs. An atlas of a place you chose because you were curious about it is
yours in a way no shared corridor ever is.

**Bulky by construction.** Seven chapters, each needing a fetcher, a cleaning
step, one or two figures, and report assembly — roughly 600–1,000 lines of
working code plus an HTML builder. At this cohort's level that is weeks of
unassisted work; with an assistant and the week 3 method it is two studio
sessions plus the week between. That gap *is* the lesson. Nobody experiences
what AI acceleration means from a 40-line exercise; they experience it by
shipping something they know they could not have typed.

**Ungraded without going soft.** The motivation structure replaces marks with
three things: ownership (it is their town), a visible finish line (the atlas
builds from scratch with one command), and an audience (the week 5 gallery,
where everyone shows one page). The verification habits from week 3 continue
as *practice* — each chapter includes one hand-check against the raw data —
because the habit is the point, not evidence for a marker.

**Nothing like a corridor commission.** No AVL, no reliability metrics, no
worst segment, no intervention argument, no stakeholder brief. The synthetic
corridor dataset survives only as the week 3 task material, where its planted
defects still teach verification.

## The chapters

Core — all seven, in any order after chapter 1:

| # | Chapter | Source | Verified |
|---|---|---|---|
| 1 | The patch and its stops | NaPTAN | yes |
| 2 | Road safety | STATS19, two years | yes |
| 3 | Deprivation | IMD 2019 + ONS boundary lookup | yes |
| 4 | Who has no car | Census 2021 via Nomis | yes |
| 5 | Cycling potential | PCT regional route network | yes |
| 6 | What is there | OpenStreetMap via Overpass | yes |
| 7 | A year of weather | open-meteo archive | yes |

Stretch — any, none required: an eighth chapter of the student's own
devising; a comparison chapter (your patch against the Leeds demonstrator); a
Streamlit version of the atlas; rail (ORR station usage, manual download).

Every chapter has the same internal shape, taught once in the studio and then
repeated: *fetch (state the source and date) → cut to the patch (count what
you cut) → clean (count again) → figure (labelled, titled) → three sentences
→ one hand-check.* The repetition is deliberate: by chapter three the student
has a working rhythm with the assistant; by chapter seven the rhythm is the
skill.

## Week structure

**Week 4 — foundations (studio).** Short teach: the chapter shape, and
choosing a workable patch (Leeds by default; any GB town they fancy
otherwise; a bounding box they can defend). Patches go on the board — not to
enforce uniqueness, but because seeing others' choices is itself an
advertisement for variety. Demonstrator: the instructor builds Leeds
chapters 1 and 2 live, with
the assistant, thinking aloud — including at least one wrong generation
caught by a row count. Then studio: every student gets chapter 1 working on
their own patch before the session ends. That single working chapter is the
week's finish line; it proves their loop runs end to end.

**Between weeks.** Chapters at their own pace. The cache-first fallback data
committed in the repo means nobody is blocked by an API outage.

**Week 5 — volume (studio).** The whole session is production. The TA and
instructor circulate on unblocking, not checking. Last twenty minutes: the
gallery — every student puts one page of their atlas on the screen for thirty
seconds. No presentations, no questions required, no judgement; the point is
thirty-one different places, all real, all built by people who could not
program five weeks ago.

## What must change elsewhere (course-wide de-grading)

The no-grading rule reaches back into weeks 1–3, which currently carry
marking language. Required edits, all small: the week 2 "pass" phrasing
becomes a suggestion of scope; the week 3 task loses its marking table and
weights (the evidence-first framing survives as professional practice, not as
scoring); the verification checklist's "this is what is marked" closing
becomes "this is what you keep"; the instructor rubric is retired with a
notice; the delivery notes and design docs get aligned.

## Delivery preparation — status

- **Cached fallbacks: done (10 August 2026).** All seven sources committed
  in `project/data/external/`, Leeds-sized, with a provenance manifest
  (`SOURCES.md`): STATS19 (729 casualties), NaPTAN (1,324 stops), IMD (482
  Leeds LSOAs), Census TS045 (2,440 rows), PCT (3,552 segments), OSM (290
  amenities), open-meteo (a year of hourly weather). Regenerate per cohort
  with `instructor/demonstrator/fetch_fallbacks.py`.
- **The Leeds demonstrator: done, all seven chapters.**
  `instructor/demonstrator/leeds_atlas.py` builds seven figures and
  `output/index.html` from the fallbacks, offline. Chapters 1–2 are still
  built live in session; the committed output is the safety net and the
  reference for Leeds-patch students. See `instructor/demonstrator/README.md`.
- **Still open:** instructor materials referencing the corridor as "the
  project" (reference solution, hidden check, delivery notes weeks 4–5) are
  annotated as week 3 support material but could be tidied further.

## Risks

| Risk | Mitigation |
|---|---|
| Thirty students hitting the same APIs individually | cache-first: instructor-fetched fallback files committed for every source, Leeds-sized; students on a dead API use the fallback and note it |
| A student picks a data-poor patch (a hamlet, a moor) | patch guidance in the brief: somewhere with a few thousand people; the patch board and the week 4 circulation catch the rest |
| A student insists on London | excluded in the brief, with the practical reasons stated; offer a single borough as the compromise if someone has a genuine attachment |
| Volume without understanding — pure paste-and-hope | the chapter shape embeds one hand-check per chapter; the week 3 failure demo is recent memory; no marks means no incentive to fake it |
| A student finishes early | stretch chapters are open-ended; the Streamlit atlas absorbs any amount of energy |
| Sensitive findings about real places (deprivation, casualties) | the brief keeps the disclosure discipline: describe what the data says, source and date it, and write about places with the respect you would want for your own street |
