# Python for Transport & Civil Engineering — Course Design

**Cohort:** transport / civil engineering students. Technically literate (spreadsheets, CAD, maybe some MATLAB exposure), little to no programming.
**Shape:** 5 weeks · 8h contact total · ~2–3h homework per week (~20h total commitment).
**Environment:** local VS Code + venv, Google Colab as a no-questions-asked fallback.

> **Delivery model update (August 2026).** The course now runs fully
> supervised: each week is structured as *teaching → instructor-led
> demonstration → tasks done in class*, with a TA circulating. The
> "homework" framing below is retired — what the run sheets call homework is
> now in-session task time, and the student-facing week READMEs carry the
> teaching content in written form (concepts first, then the demonstration,
> then the tasks). Contact time grows accordingly; weeks 4–5 are 3h each
> (see `WEEKS_4_5_DESIGN.md`). The task content, marking, and weights are
> unchanged. The timed run sheets below predate this change and need
> rebalancing before delivery.

---

## 1. What "competent" means here — and what it doesn't

Eight contact hours will not produce software engineers. Pretending otherwise is how these courses fail: the syllabus promises breadth, the students end week 5 having seen everything and retained nothing, and six months later nobody has opened VS Code again.

So the target is deliberately narrow and behavioural. By week 5 a student can:

1. **Open a project and run it.** Clone or download a repo, activate an environment, run a script, and know what to do when it doesn't work.
2. **Read code before writing it.** Look at 30 lines of someone else's Python and say what it does, where the data goes, and what would happen if an input changed.
3. **Modify and extend.** Change parameters, add a filter, add a column, add a chart — working from an existing script rather than a blank file.
4. **Get a dataset from raw to figure.** Load a CSV, clean the obvious problems, aggregate it, plot it, and explain the plot.
5. **Debug from a traceback.** Read the error, find the line, form a hypothesis, test it. Not "ask someone".
6. **Direct and verify AI-generated code.** Specify a task precisely, and check the output is right rather than merely plausible.

Explicitly **not** in scope: object-oriented design, testing frameworks, packaging, async, web, databases, git branching/merging beyond clone-and-commit.

The one-line version for students: *"You will finish able to do useful analysis in Python and get yourself unstuck. You will not finish able to build an app."*

### The load-bearing design choice

Weeks 1–2 teach the minimum needed to *supervise* code. Week 3 hands them a force multiplier that only works if that supervision is real. Weeks 4–5 make them use it on a problem large enough that unsupervised AI output will visibly break.

That ordering is the whole course. AI acceleration before verification skills produces students who can generate 200 lines they can't evaluate — confident, fast, and wrong. Put it after, and week 3 is the payoff for weeks 1–2 rather than a replacement for them.

---

## 2. Contact-time budget

| Week | Theme | Contact |
|---|---|---|
| 1 | Getting Python working | 1h 30m |
| 2 | Actually programming | 1h 30m |
| 3 | AI acceleration | 1h 30m |
| 4 | Project studio I | 1h 45m |
| 5 | Project studio II | 1h 45m |
| | **Total** | **8h 00m** |

---

## 3. Week-by-week

### Week 1 — Getting Python working

**Outcomes.** By the end, a student can explain what a program is, navigate to a folder in a terminal, run a `.py` file, say what a virtual environment is for, and change a value in a script and see the effect.

**The problem with week 1** is that installation eats it. Thirty students, five OS/version combinations, one corporate laptop with no admin rights — and 90 minutes is gone before anyone writes a line. So installation is pre-work, not session time.

**Pre-work (60–90 min, due 48h before session 1).**
- Install VS Code and Python 3.11+ (separate OS-specific guides: Windows, macOS, managed/locked-down laptop).
- Download the course repo.
- Run `python check_setup.py` and submit the output it prints.
- Anyone who can't: submit the error text. They get triaged before the session, not during it.

The submitted output is a *diagnostic*, not a formality. It tells you before the room fills up how many people are broken and how.

**Session run sheet (90 min).**

| Time | Activity |
|---|---|
| 0–10 | Setup triage. Broken students paired with working ones or moved to Colab. Nobody spends the session watching an installer. |
| 10–25 | **What a program actually is.** A file of instructions, read top to bottom, by an interpreter. Live: a 6-line script, run it, change a number, run it again. The point is the loop of edit → run → look. |
| 25–45 | **Where things live.** Files, folders, paths, working directory. Terminal: `cd`, `ls`/`dir`, `python script.py`. Why "file not found" is almost always a working-directory problem. |
| 45–60 | **Environments.** Framed by the failure it prevents: two projects, two versions of a library, one machine. One command to create, one to activate, one to install. Not a lecture on packaging. |
| 60–80 | **Guided modification.** Supplied script reads a small traffic count file and prints a summary. They change the threshold, change the file, break it on purpose, read the traceback. |
| 80–90 | **Traceback anatomy.** How to read one: bottom line first, then the file and line number. This is the single highest-leverage 10 minutes of the week. |

**Homework (~2h).**
- *Traceback safari*: six deliberately broken scripts. For each, name the error, find the line, fix it. Auto-checked.
- *Parameter sweep*: run the supplied script across five input values, record results in a table, write two sentences on the pattern.

**Common failure & mitigation.** PATH problems on Windows and the macOS system-Python trap are the two big ones. The OS-specific setup guides address each directly, and `check_setup.py` detects both by name and prints the fix.

---

### Week 2 — Actually programming

**Outcomes.** A student can use variables and lists, write a loop with a conditional inside it, package repeated work into a function, do arithmetic on a NumPy array, and produce a labelled matplotlib figure.

**The problem with week 2** is that the topic list — variables, lists, loops, conditionals, functions, NumPy, visualisation — is a semester of material compressed into 90 minutes. Teaching each as its own unit guarantees a tour rather than a skill.

So: one worked problem, end to end, live, with the concepts introduced as they become necessary. The problem is a real one from their domain — an hourly traffic count file, producing a peak-period profile.

**Session run sheet (90 min).**

| Time | Activity |
|---|---|
| 0–5 | Homework debrief — the two errors most people hit. |
| 5–20 | **Store and decide.** Variables and types, then `if`. Introduced as: the script needs to remember a count, and treat weekends differently. |
| 20–40 | **Repeat.** Lists, then `for`. Build the hourly aggregation by hand with a loop. Deliberately verbose — they need to see the machinery before it's hidden. |
| 40–55 | **Package.** The same block appears three times, so turn it into a function. Arguments and return introduced as the answer to duplication, not as syntax to memorise. |
| 55–70 | **NumPy as the punchline.** Rewrite the loop as one line of array arithmetic. Framed as: *this is the same thing, faster and shorter, and now you know what it's doing underneath.* Vectorisation lands because they just wrote the loop. |
| 70–88 | **First figure.** Plot the peak profile. Axis labels, title, units, saving to file. One rule enforced from here on: a figure with an unlabelled axis is not finished. |
| 88–90 | Homework brief. |

**Homework (~3h).**
- *Drill set*: 12 short exercises with `assert`-based self-checks — they run a script and it tells them pass/fail. Covers each construct in isolation.
- *Reproduce the figure*: given a target image and a dataset, produce a matching plot. Harder than it sounds and a genuinely good test of whether week 2 landed.

**A decision you need to make: pandas.** Your outline says NumPy, and NumPy is the right thing to teach *here* because it makes the loop lesson pay off. But for the transport data in weeks 4–5, pandas is what a practitioner would actually reach for. Two options:

- **(a) Introduce pandas in week 3** as the first AI-assisted task — "here is a library you haven't been taught; use AI to help you use it, and verify the result." Elegant, because it makes week 3 about a real capability gain rather than a demo. Riskier.
- **(b) Give them a pre-written loader** in week 4 that hands back clean NumPy arrays, and never mention pandas. Safer, but leaves them unable to handle their own data afterwards.

I'd take (a). It's the option where week 3 does real work. But it depends on your cohort's appetite — flag which you want and I'll build to it.

---

### Week 3 — AI acceleration

**Outcomes.** A student can write a specification precise enough to get correct code out of an AI assistant, verify that output against a case they can check by hand, and work in small verify-as-you-go increments rather than accepting a large block on trust.

**The problem with week 3** is obvious: hand agentic tooling to people who have been programming for two weeks and you can produce students who ship 200 lines they cannot evaluate. The session has to be built around that risk, not around the tooling.

The framing: **you have been promoted.** You are no longer the person writing every line — you are the person who specifies the work and signs off on it. Both of those jobs require you to be able to read code, which is what the last two weeks bought you.

**Session run sheet (90 min).**

| Time | Activity |
|---|---|
| 0–15 | **The failure demo — do this first.** Live, with a lazy prompt: *"analyse this traffic data"*. Get back something that runs, looks professional, and is wrong — wrong aggregation, or silently dropping the rows with missing values. Let the room sit with it. Everything after this lands better. |
| 15–35 | **Specifying.** What a usable prompt contains: the shape of the input (columns, types, units), the expected output, the edge cases, the constraint. Rewrite the lazy prompt together and re-run it. |
| 35–55 | **Verifying.** Four checks, every time: does it run; does it give the right answer on a small case you worked out by hand; what does it do with a missing value / a zero / a duplicate; can you explain every line. They get this as a printed checklist and use it for the rest of the course. |
| 55–80 | **Working in the loop.** Hands-on in VS Code with the assistant. Small steps, run after each, commit when something works. Build one real thing: a function that reads the messy project data and returns something clean. |
| 80–90 | **Where this breaks.** Honest limits: confidently wrong domain assumptions, silent data loss, plausible-looking statistics, code that works on the sample and fails on the full file. |

**Homework (~2h).** Build a small tool with AI assistance — and submit three things: the code, the prompts used, and evidence of correctness (the hand-worked case and what happened on the edge cases). **The evidence is what's marked.** Code that works but comes with no verification scores lower than a partial solution that comes with proof.

That grading asymmetry is deliberate and should be stated to students on day one of week 3. It's the only mechanism that reliably stops paste-and-hope.

**Tooling note.** Pick one assistant and standardise — whatever your institution licenses. Mixed tooling turns the hands-on block into support triage.

---

### Weeks 4–5 — Project studio: corridor reliability

**The problem.** Groups of 3–4 act as analysts for a transport authority. They are given four weeks of stop-level bus arrival data for a single urban corridor — scheduled vs actual — plus stop locations and segment definitions. The authority wants to know where and when the corridor is failing, and what one intervention would be worth.

**Why this problem.** It has genuinely messy data, so cleaning is unavoidable rather than an exercise. It needs grouping and aggregation, which is the core analytical move. It contains a real judgement call — *which* reliability metric — so two competent groups can reach different defensible answers. It produces a figure that carries an argument. And it's recognisably their profession.

**The data (supplied, synthetic but realistic).**
- `arrivals.csv` — ~180k rows: trip id, stop id, scheduled time, actual time, vehicle id, date.
- `stops.csv` — stop id, name, lat/lon, sequence.
- `segments.csv` — segment id, from/to stop, length.
- `boardings.csv` — stop-level passenger counts by hour, for the passenger-weighted extension.

Deliberately included defects, each teaching something: missing pings for one vehicle over three days; duplicate rows from a double-logged depot; one stop renamed mid-period (so a naive group-by silently splits it); a handful of negative dwell times; timestamps crossing midnight.

**Core requirements — every group.**
1. Load and clean, with cleaning decisions documented and justified.
2. Journey time distribution by time of day — not just the mean.
3. Headway regularity: are buses bunching, and where.
4. Identify the worst segment/time-period combination, with evidence.
5. One figure that makes the case to a non-technical reader.

**Extension — pick one.**
- **Scenario:** apply a bus-lane speed uplift to the worst segment and quantify the corridor-level benefit.
- **Metric comparison:** compute excess wait time alongside a simple punctuality measure and argue which better represents passenger experience.
- **Passenger-weighted delay:** use `boardings.csv` to weight delay by who actually experiences it — usually reorders the priorities, which is the point.
- **Own proposal:** subject to approval in week 4.

**Week 4 run sheet (105 min).**

| Time | Activity |
|---|---|
| 0–15 | Brief. Groups formed. Roles assigned — data, analysis, visualisation, writing — rotating, not fixed, so nobody hides. |
| 15–35 | **Data reconnaissance.** Every group loads the data and reports three things they notice. Surfaces the planted defects as a room-wide discovery rather than a scavenger hunt. |
| 35–50 | Mini-teach: aggregation patterns — group, summarise, compare. The one technique they still need. |
| 50–95 | **Studio.** Working time. You circulate. |
| 95–105 | Standup: each group states what they have and what's blocking them. Blockers you hear twice become the week 5 mini-teach. |

**Between weeks (~3h).** Complete the core requirements. Push code. Submit a one-paragraph statement of intended extension and the argument they expect to make.

**Week 5 run sheet (105 min).**

| Time | Activity |
|---|---|
| 0–10 | Mini-teach on the most common blocker from week 4. |
| 10–55 | **Studio.** Extension work and integration. |
| 55–70 | **Cross-group review.** Groups swap code and try to run each other's from a clean clone. Roughly half will fail — hardcoded paths, missing files, undeclared dependencies. That's the lesson, and it's better learned here than in an assessment. |
| 70–95 | **Presentations.** Five minutes per group: the finding, the figure, the recommendation. Non-technical framing enforced. |
| 95–105 | Course close: what they can now do, and what to learn next. |

**Deliverables.** A repo that runs from a clean clone; a two-page brief for the authority; the figure; a five-minute presentation; and an individual reflection — *what did you verify, and how do you know your answer is right?*

**Assessment weighting.**

| Component | Weight |
|---|---|
| Week 1 setup checkpoint | pass/fail gate |
| Week 2 drill set | 10% |
| Week 3 AI tool + verification evidence | 20% |
| Group project — code correctness & reproducibility | 30% |
| Group project — brief & presentation | 25% |
| Individual reflection | 15% |

Reproducibility carries real weight because it's the difference between analysis and a one-off. And the individual reflection exists so a group can't carry a passenger.

---

## 4. Risk register

| Risk | Likelihood | Mitigation |
|---|---|---|
| Setup failures consume week 1 | **High** | Pre-work with `check_setup.py`; triage before the session; Colab fallback with the same repo, no penalty for using it. |
| Week 2 overruns and visualisation gets cut | **High** | Single worked problem, not seven topics. If time is lost, cut the NumPy rewrite — not the figure. The figure is what motivates them. |
| Week 3 produces paste-and-hope | **High** | Failure demo first; verification checklist; grading weighted onto evidence rather than output. |
| Groups where one person does everything | Medium | Rotating roles; individual reflection at 15%; cross-group review exposes who understands the code. |
| Project scope creep | Medium | Core requirements fixed and small; exactly one extension; extension approved in writing. |
| Wide ability spread | Medium | Drill set has starred stretch items; project extensions vary in difficulty; strong students used as paired triage in week 1. |
| Nobody opens Python again after week 5 | **High** | Final 10 minutes is a concrete next-step path, and the project repo is theirs — a working template for their own data. |

---

## 5. Repo structure

```
python_learning/
├── README.md                   # student entry point — start here
├── check_setup.py              # week 1 diagnostic
├── requirements.txt
├── setup/
│   ├── windows.md
│   ├── macos.md
│   ├── locked-down-laptop.md
│   └── colab-fallback.md
├── week1_setup/
│   ├── first_script.py
│   ├── exercises/              # traceback safari
│   └── README.md
├── week2_programming/
│   ├── worked_example.py       # the live-coded peak profile
│   ├── drills/                 # 12 assert-checked exercises
│   └── README.md
├── week3_ai/
│   ├── verification_checklist.md
│   ├── failure_demo/           # the lazy-prompt demo, preserved
│   └── README.md
├── project/
│   ├── brief.md
│   ├── data/                   # arrivals, stops, segments, boardings
│   ├── starter/                # skeleton with function stubs
│   └── README.md
├── instructor/
│   ├── run_sheets/
│   ├── solutions/
│   ├── data_generator.py       # regenerates project data with new seeds
│   └── marking/
└── docs/
    └── COURSE_DESIGN.md        # this file
```

---

## 6. Decisions I made that you should check

1. **Setup is pre-work, not session time.** Costs you a pre-session admin round; buys back most of week 1.
2. **Week 2 is one worked problem, not a topic tour.** Fewer things covered, more things retained. If your validation requires topic coverage on paper, the homework drills provide the audit trail.
3. **AI comes after fundamentals, and week 3 opens with a failure.** The alternative ordering is faster and produces students who can't tell good output from bad.
4. **Week 3 marks the verification evidence, not the code.** This is the mechanism that makes the framing real. Without it the framing is a speech.
5. **Project data is synthetic with planted defects.** Real GTFS/AVL data is more authentic but you lose control of difficulty and can't guarantee the teaching moments. The generator is seeded, so you can reroll for a new cohort.
6. **One corridor, one dataset, all groups.** Makes cross-group comparison possible in week 5 and keeps your support load sane.

## 7. Open questions for you

- **pandas in week 3, or NumPy-only throughout?** (See week 2. My recommendation: pandas, introduced as the first AI-assisted task.)
- **Which AI assistant is licensed** for your students? Determines the week 3 hands-on entirely.
- **Group size and cohort size** — affects studio circulation and whether week 5 presentations fit in 25 minutes.
- **Is the pass/fail setup gate enforceable**, or do you need a path for students who arrive at week 1 with nothing installed?
- **Assessment constraints** from your institution that the weighting above needs to fit.
