# Instructor materials

> **Status (11 August 2026):** the course is an ungraded learning module,
> and weeks 4–5 are the individual transport atlas
> (`docs/ATLAS_PROJECT_DESIGN.md`). The corridor dataset and its solutions
> below now support the **week 3 task only**; the marking rubric is retired;
> `hidden_check.py` survives as an optional self-check on the week 3 data.
>
> **This folder ships in the student repository, deliberately.** Nothing is
> graded, so open solutions cost nothing and give students a way to check
> themselves — the week 1 and week 2 task notes point at them explicitly,
> framed as the answers in the back of the textbook. Do not treat anything
> in here as secret, and do not add anything that would need to be.

| Path | What it is |
|---|---|
| `run_sheets/delivery_notes.md` | What to say, what goes wrong, what to cut when running late |
| `marking/rubric.md` | Full rubric, all components |
| `marking/hidden_check.py` | Ground truth + automated check of a group's cleaned data |
| `solutions/week1/` | Fixed versions of the six traceback exercises |
| `solutions/week2/drills_solutions.py` | All twelve drills solved |
| `solutions/week2/make_target_figure.py` | Regenerates the task 2 target figure + marking key |
| `solutions/project/reference_solution.py` | Worked core requirements, recovers the planted bottleneck |
| `data_generator.py` | Seeded generator for every dataset in the course |

## Regenerating the data

```
python instructor/data_generator.py
```

Change `SEED` for a new cohort. The planted defects move, so last year's answers
do not transfer. **Re-run `reference_solution.py` afterwards and update the
ground-truth numbers in `marking/hidden_check.py` and `marking/rubric.md`** —
they are hardcoded to the current seed.

## The planted defects

| Defect | Lesson |
|---|---|
| 2,400 exact duplicate rows (depot logged 8 April twice) | Count rows before and after every operation |
| Stop S009 renamed part-way through the period | Group by id, never by name |
| 71 negative dwell times, all on BUS_2837 | Sanity-check ranges before trusting a mean |
| BUS_2841 stops reporting for 3 days | Absence is not zero |
| Times past midnight recorded with hour 24 (e.g. 24:06:52) | Sorting text is not sorting time; naive parsers reject hour 24 |

## Ground truth (current seed: 20260810)

- Raw arrivals: **97,278** rows → **94,878** after de-duplication
- Worst segment: **SEG06** (Hollow Lane approach), **16:00–18:00**, **outbound**
- Running **~160%** above its own off-peak baseline
- Peak headway CV **0.40–0.44** vs **0.16–0.20** off-peak — real bunching

```
python instructor/marking/hidden_check.py           # prints ground truth
python instructor/marking/hidden_check.py their.csv # checks a group's export
```
