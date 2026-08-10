# Marking rubric

| Component | Weight | Where |
|---|---|---|
| Week 1 setup checkpoint | pass/fail gate | `check_setup.py` output submitted |
| Week 2 drill set | 10% | `week2_programming/drills/` |
| Week 3 AI tool + verification | 20% | `week3_ai/task.md` |
| Project — code & reproducibility | 30% | group repo |
| Project — brief & presentation | 25% | group |
| Individual reflection | 15% | individual |

---

## Week 2 drills — 10%

Mechanical. Run their `drills.py`.

| | |
|---|---|
| 12/12 | 100% |
| 9–11/12 (all core) | 85% |
| 6–8 | 60% |
| below 6 | 30%, and flag for support before week 4 |

Also require the reproduced target figure. Pass if the two curves are right and
the axes are labelled with units. The exact styling does not matter; the
**weekday peak of ~2,856 veh/h at 08:00 and weekend peak of ~2,279 at 13:00**
do. A student whose weekend curve is flat has not worked out how to get the day
of the week from the date, which is the point of the exercise.

---

## Week 3 task — 20%

**The weighting inside this component is 60/20/20 on evidence / prompts / tool.**
Apply it strictly on the first submission or the message does not land.

### Verification evidence (60%)

| Band | What it looks like |
|---|---|
| **Excellent (85–100)** | Hand-worked case with the actual timestamps and arithmetic shown, and the tool's answer beside it. All five edge cases addressed with observed behaviour, not speculation. At least one case where they found their tool was wrong and said so. |
| **Good (65–84)** | Hand-worked case present and correct. Most edge cases tested. Some "this should handle X" without showing it. |
| **Weak (40–64)** | A hand-worked case that is really just re-running the tool. Edge cases listed but not tested. |
| **Fail (0–39)** | "I tested it and it worked." No numbers. |

**The mark that teaches:** a student whose tool handles three of five edge cases
and documents the other two honestly scores higher than one who claims all five
and shows nothing. Say so in the feedback, explicitly, or they will read the
mark as arbitrary.

### Prompt record (20%)
Looking for genuine iteration — a prompt that failed, a diagnosis, a rewrite.
A single prompt with a perfect result scores mid-band at best: either they got
lucky or they edited the history.

### The tool (20%)
Runs. Produces mean/median/p90. Reports what it dropped. That is all.

---

## Project — code & reproducibility (30%)

### Reproducibility (10 of the 30)
Clone into a clean directory. Follow their README. Run it.

| | |
|---|---|
| Runs first time | full marks |
| Runs after one obvious fix (missing `pip install`) | 70% |
| Needs a path edited | 40% |
| Cannot be made to run | 0 — and tell them, this is the most fixable thing on the list |

### Cleaning (10 of the 30)
Run `hidden_check.py` against their cleaned export.

Scored on defects **found and justified**, not on matching the reference. A group
that keeps the negative dwell rows and argues the arrival time is still valid has
made a better decision than one that silently drops them.

| Defects identified | Mark |
|---|---|
| 4–5 with reasoning | 85–100 |
| 3 with reasoning | 65–84 |
| 2 | 45–64 |
| 0–1 | below 45 |

BUS_2841 is the hard one — finding it is a distinction marker, missing it is not
a penalty.

### Analysis (10 of the 30)
- Requirement 2 shows a distribution, not just a mean → the difference between a
  pass and a good mark
- Requirement 3 headway calculation sorted correctly and not differenced across
  days or directions
- Requirement 4 uses a **relative** baseline. A group that names the longest
  segment rather than the worst-performing one has answered a different question
- Extension attempted and completed

Ground truth for requirement 4: **SEG06, 16:00–18:00, outbound**, running ~160%
above its own off-peak baseline. A group naming a different segment needs a very
good argument; a group naming SEG06 with no evidence gets no credit for it.

---

## Project — brief & presentation (25%)

**The brief (15).** Two pages. Written for a non-technical reader. Marked on:
does it state the finding in the first paragraph; is the recommendation
actionable; is uncertainty acknowledged; would a councillor understand it.

Deduct for: code in the brief, unexplained jargon (*headway*, *p90*, *CV*),
"further work is needed" as a substitute for a conclusion, going over two pages.

**The figure (5).** Labelled axes with units. A title stating the finding, not
describing the chart. Readable in greyscale or with a legend that does not rely
on colour alone.

**The presentation (5).** Five minutes. First sentence is the answer. Marked on
whether a non-technical audience could act on it.

---

## Individual reflection — 15%

*What did you verify, and how do you know your answer is right?*

| Band | What it looks like |
|---|---|
| **Excellent (85–100)** | Names a specific thing they checked, what they expected, what they got, what they did about the gap. Describes a moment they were wrong. |
| **Good (65–84)** | Specific verification described, but everything worked first time — plausible, but less evidence of real engagement. |
| **Weak (40–64)** | General account of the group's process. "We checked our results carefully." |
| **Fail (0–39)** | A description of what the group did, with no verification content at all. |

This component exists to catch passengers. Cross-reference against the
cross-group review in week 5 — the student who could not explain their group's
code should not be writing a confident reflection about verifying it. Where
those two disagree, ask.
