# Weeks 4–5 — Project studio, redesigned

> **SUPERSEDED (10 August 2026).** The group corridor studio described below
> was replaced by the individual, ungraded transport atlas — see
> [`ATLAS_PROJECT_DESIGN.md`](ATLAS_PROJECT_DESIGN.md). Kept for the record;
> do not deliver from this document.

Supersedes the weeks 4–5 section of [`COURSE_DESIGN.md`](COURSE_DESIGN.md). Two
changes: the sessions grow from 105 minutes to **3 hours each**, and week 5
becomes an exercise in **AI-accelerated access to real national datasets**.

Total contact time goes from 8h to 11h.

---

## 1. The design problem

Week 3 hands them an assistant and a verification checklist. The risk is that
weeks 4–5 then become a project they could have done without either — the
corridor data is supplied, clean-ish, and small enough to brute-force. The
assistant ends up as a faster way to type pandas, and the verification checklist
ends up in a drawer.

Real national data fixes this, because it makes the assistant **necessary rather
than convenient**. Nobody can teach STATS19's casualty codes, Overpass QL, the
Nomis dataset ids and the ONS boundary API inside a course this length. The only
route through is to specify what you want, get help, and check the result — which
is precisely the capability week 3 claims to build.

It also scales the week 3 lesson up. The failure demo turned on a convention that
lived outside the file: `-1` meant "no observation". Every dataset in
[`project/data_sources.md`](../project/data_sources.md) has one of those, and
they are no longer planted by me:

- STATS19 severity `1` is **fatal**, not slight.
- IMD decile `1` is the **most deprived**.
- IMD 2019 carries **2011** LSOA codes; the ONS boundary service returns **2021**
  codes. The merge appears to work and quietly drops the changed ones.
- Overpass rejects GET and returns an HTML page that breaks `.json()`.
- West Midlands is ATCO **430**. Assistants say `043`.

I did not invent one of those. That is the argument for using real data.

### The load-bearing choice

**Week 4 is the scaffolded problem with a known answer. Week 5 is the open one
with no answer at all.**

Week 4's corridor has ground truth — `instructor/marking/hidden_check.py` knows
the bottleneck is SEG06, outbound, 16:00–18:00. That is what makes week 4 a
calibration exercise: they find out whether their verification habits actually
work, against a fact.

Week 5 has no ground truth, because nobody has done the analysis. That is the
right order. Verification you have never tested against a known answer is a
ritual, not a skill.

---

## 2. Week 4 — Studio I: the corridor (180 min)

Unchanged in substance from the existing design, with the extra 75 minutes spent
on reconnaissance, a proper aggregation teach, and a guided first contact with
external data.

| Time | Activity |
|---|---|
| 0–15 | **Brief.** Groups of 3–4 formed. Roles assigned — data, analysis, visualisation, writing — rotating, not fixed. |
| 15–45 | **Data reconnaissance.** Every group loads `arrivals.csv` and reports **three things they noticed**. Round-robin on the board. The five planted defects surface as a room-wide discovery rather than a scavenger hunt. Do not confirm or deny during the round — collect first, then adjudicate. |
| 45–70 | **Mini-teach: aggregation.** Group, summarise, compare. The one technique they still need and the only real teaching block in week 4. |
| 70–80 | Break. |
| 80–150 | **Studio.** Core requirements 1–4. You circulate. |
| 150–170 | **Guided external fetch.** Everyone runs `starter/fetch_external.py` at the same time and reads the output together. Not a demo — they run it. See the warning in §6 about doing this from one campus IP. |
| 170–180 | **Standup.** Each group: what we have, what is blocking us. Blockers heard twice become the week 5 mini-teach. |

**Why reconnaissance gets 30 minutes.** It is the highest-value half hour in the
project and every group that skips it loses more time later than it saved. Thirty
minutes is enough for the slower groups to find the duplicates without being told.

**The guided fetch is the de-risking step.** Its only job is that no group starts
week 5 having never made a successful HTTP request. It runs in about a minute and
prints its own row counts, so the lesson — national file, area filter, count what
you cut — lands without a lecture.

**Between weeks (~3h).** Finish core requirements 1–4. Push code. Submit **one
paragraph** naming the external dataset they will use and the question it
answers that `arrivals.csv` cannot. That paragraph is the scope control; without
it, week 5 becomes four groups discovering Overpass simultaneously at 14:05.

---

## 3. Week 5 — Studio II: integrate, extend, communicate (180 min)

| Time | Activity |
|---|---|
| 0–10 | **Mini-teach on the most common week 4 blocker.** Decided on the night, from the standup. |
| 10–35 | **The integration clinic.** The three joins (§4) and the row-count discipline. Live, on the projector, with a deliberate broken merge. |
| 35–95 | **Studio.** Extension work. |
| 95–105 | Break. |
| 105–130 | **Cross-group review.** Groups swap repos and run each other's code from a clean clone. About half will fail — hardcoded paths, uncommitted data, an undeclared dependency. That is the lesson and it is better learned here. |
| 130–165 | **Presentations.** Five minutes per group. Finding, figure, recommendation. Non-technical framing enforced. |
| 165–180 | **Close.** What they can now do; what to learn next. |

**The integration clinic should include a failure.** Do a merge that silently
drops a third of the rows — the 2011/2021 LSOA vintage mismatch is the honest
one and it is sitting right there in the data. Show the merge succeeding, show
the row count, let them sit with it. This is the week 3 failure demo's sequel and
it should be run the same way: consequence first, explanation second.

**Presentation timing.** Five minutes × groups. Six groups fits; nine does not.
If the cohort is large, run presentations in two parallel rooms and accept that
you only see half — or cut the cross-group review to 15 minutes, never the
presentations.

---

## 4. The three joins

This is the entire technical content of week 5, and it is deliberately small.

| Join | Looks like | Where it bites |
|---|---|---|
| **Key join** | LSOA code → IMD decile | Different code vintages. Different string case. Whitespace. Count rows before and after, every time. |
| **Bounding box** | keep rows inside lat/lon limits | A box is not a corridor. A 12 × 4 km box around an 11 km line is ~50 km² of city. |
| **Distance** | casualty → nearest stop | Degrees are not metres, and a degree of longitude is not a degree of latitude at 52° N. |

Everything in the catalogue is reachable with those three. Anything that is not
is out of scope — see the scope rule in `data_sources.md`. **The rule exists so
that when an assistant proposes `geopandas` and `EPSG:27700`, the group has a
sanctioned way to say no** rather than spending forty minutes installing GDAL.

---

## 5. The extension menu

Exactly one per group, named in writing at the end of week 4.

| | Extension | Source | The argument it makes |
|---|---|---|---|
| **E0** | Bus lane scenario | none — corridor data only | 30% run time reduction on the worst segment: what is it worth corridor-wide? |
| **E1** | Equity | IMD 2019 | Delay weighted by deprivation. Who is bearing the unreliability. |
| **E2** | Safety | STATS19 | Casualty burden along the corridor, against where the bus is slowest. |
| **E3** | Latent demand | PCT | Where cycling could take pressure off, and what the model does not know. |
| **E4** | Access | OSM / Overpass | Schools and trip generators near stops; which failing stops matter most. |
| **E5** | Car-free households | Census 2021 / Nomis | Who has no alternative when the bus fails. |
| **E6** | Own proposal | approved in writing | — |

**Keep E0.** It needs no external data and no network. It is the safety valve for
a group that lost week 4 to a broken laptop, and offering it openly stops a
struggling group from failing at two things at once.

**E1 is the strongest teaching option** and the one to steer undecided groups
toward: it needs all three joins, it contains the vintage-mismatch trap, and it
usually reorders the priority list — which is the finding.

---

## 6. Stretch: a small web app

**Streamlit, one file, not marked.**

```
streamlit run app.py
```

Why Streamlit and not the obvious alternatives: no JavaScript, no build step, no
HTML, no deployment. A student who can write a function and a matplotlib figure
can have a working interactive app in about forty lines — a dropdown for the
stop, a slider for the time band, the figure underneath.

**It carries no marks, and say so out loud.** If it is marked, every group builds
one and the analysis suffers. It exists because a working app is the thing they
show someone, and that is what makes people carry on after week 5 — which the
risk register lists as the highest-likelihood failure of the whole course.

It also needs a separate install (`requirements-stretch.txt`) so the core
environment does not grow for the groups who never touch it.

---

## 7. Assessment

Weeks 4–5 grew from 3.5 to 6 contact hours; the weighting should follow, and
provenance needs to be worth marks or it will not happen.

| Component | Was | Now |
|---|---|---|
| Week 1 setup checkpoint | pass/fail | pass/fail |
| Week 2 drill set | 10% | 10% |
| Week 3 AI tool + verification | 20% | 15% |
| Project — code correctness & reproducibility | 30% | 25% |
| **Project — external data: integration, provenance, stated approximations** | — | **15%** |
| Project — brief & presentation | 25% | 20% |
| Individual reflection | 15% | 15% |

The new 15% is marked on the record, not the result: the URL and retrieval date,
the licence line, row counts at every stage, and a written statement of the
approximation made. A group that joins one dataset correctly and documents it
fully scores better than a group that joins three and documents none. Same
asymmetry as week 3, applied to data rather than code.

---

## 8. Risks this adds

| Risk | Likelihood | Mitigation |
|---|---|---|
| **Thirty students hit Overpass from one campus IP and get rate-limited** | **High** | Pre-fetch the OSM extract centrally, commit it to the repo, and have groups use the local copy. Only groups working outside session time query Overpass live. This one will bite in the guided-fetch block if you let it. |
| Campus firewall blocks a government endpoint | Medium | Run every fetcher yourself the week before, from the teaching network. Commit the small outputs as a fallback so a blocked group can continue on cached data. |
| Assistant proposes a geospatial stack and a group loses the session to installing GDAL | **High** | The scope rule, stated in `data_sources.md` and repeated in the clinic. Groups need explicit permission to refuse the assistant's suggestion. |
| Groups present findings about Birmingham as if the bus service were real | Medium | Stated in `data_sources.md` and enforced in the presentation. The corridor is synthetic; the geography is real. Both sentences have to appear in the brief. |
| Scope explosion — three datasets, none finished | **High** | Exactly one extension, named in writing at the end of week 4. |
| External data becomes the project and the corridor analysis is thin | Medium | Core requirements 1–4 are still marked and still checked against ground truth. The extension cannot rescue a missing core. |

---

## 9. What this requires elsewhere in the repo

Done:

- `project/data_sources.md` — the catalogue, all endpoints verified 10 Aug 2026.
- `project/starter/fetch_external.py` — one complete worked fetcher (STATS19),
  run against the live DfT endpoint and verified: 356 pedestrian and cyclist
  casualties in the corridor box across 2022–23.
- `project/data/external/casualties.geojson` — that fetcher's output, committed
  as the cached fallback for a blocked or offline group (96 KB).
- `requirements.txt` — adds `requests`.
- `requirements-stretch.txt` — Streamlit and Plotly, for the web app only.

Still needed:

- **`project/brief.md`** — replace extensions A–D with the E0–E6 menu, and add
  the provenance requirement to the deliverables list.
- **A pre-fetched OSM extract** committed to `project/data/external/`, per the
  rate-limit risk above. This is the one that will bite hardest if skipped.
- **`instructor/marking/rubric.md`** — the new 15% component and its criteria.
- **A worked E1 reference** (IMD equity) for the instructor, in the same spirit
  as `reference_solution.py`. Without one you are marking a join you have not
  done, and the vintage mismatch is easy to miss from the front of the room.

---

## 10. Decisions to check

1. **Six hours of studio with two teaching blocks totalling 55 minutes.** That is
   deliberate — weeks 4–5 are for doing, not covering. If your validation needs
   more visible instruction, the integration clinic is the block to grow.
2. **One external dataset, not two.** Two is where the marks look better and the
   learning gets worse.
3. **The web app is unmarked.** Marking it would be popular and would cost the
   analysis. I would hold the line.
4. **Real data means a live dependency on services you do not control.** The
   cached-fallback work in §9 is not optional; it is what stops a DfT outage from
   taking the session with it.
