# Corridor reliability — project brief

**Weeks 4 and 5. Groups of 3 or 4.**

---

## The commission

You are analysts working for a transport authority. The 47 corridor runs from
Cathedral Square in the city centre to Longmoor Terminus: eighteen stops, both
directions, a bus roughly every 8 minutes in the peaks.

Complaints about the 47 have risen. The operator says the service runs to
timetable. Passengers say it is unreliable. Both can be true at once, and the
authority needs to know which is closer to the truth.

You have been given four weeks of automatic vehicle location data and three
questions:

1. **Where and when is the corridor failing?**
2. **How badly, in terms a passenger would recognise?**
3. **What would one intervention be worth?**

You have two studio sessions and the week in between.

---

## The data

In `data/`. It is shaped like real-world data, which means it is not clean.
Nobody has written you a note explaining its quirks, because in practice
nobody ever does.

| File | Rows | Contents |
|---|---|---|
| `arrivals.csv` | ~97,000 | `trip_id`, `stop_id`, `stop_name`, `direction`, `service_date`, `scheduled_time`, `actual_time`, `dwell_s`, `vehicle_id` |
| `stops.csv` | 18 | `stop_id`, `stop_name`, `lat`, `lon`, `sequence` |
| `segments.csv` | 17 | `segment_id`, `from_stop`, `to_stop`, `length_m` |
| `boardings.csv` | ~9,600 | `service_date`, `stop_id`, `hour`, `boardings` |

Times are `HH:MM:SS`. Distances are in metres. Dwell times are in seconds.

**One warning, and it is the only one you get.** There are at least five
things wrong with `arrivals.csv`. Some of them will make your code crash,
which is the easy kind of problem. Some of them will not — they will quietly
give you a wrong answer that looks entirely reasonable. You saw exactly this
in week 3.

Before you analyse anything, find out what is wrong with the data. Count your
rows before and after every operation.

One fact about the setting, which you must also state in your brief: **the 47
is a synthetic bus service, but the geography underneath it is real.** The
stop coordinates trace a real line through a real city, which is what makes
the external datasets in week 5 join to it meaningfully. It also means your
findings are findings about an invented service, and must never be presented
as conclusions about the real city's bus network.

---

## Core requirements — every group

**1. Load and clean.**
Document every cleaning decision and the reason for it. "Dropped 2,400 rows"
is not a decision. "Dropped 2,400 exact duplicate rows, all from 8 April,
which appears to have been logged twice by the depot" is.

**2. Journey time distribution by time of day.**
Not only the mean. A mean journey time of 45 minutes tells the authority
nothing about whether to expect 40 or 60. Show the spread, and say what it
means for a passenger.

**3. Headway regularity.**
Are buses bunching? Where, and when? A corridor that runs every 8 minutes on
paper, but where the real gaps are 2, 3, and 19 minutes, is not running every
8 minutes.

**4. The worst segment and time period.**
Identify it, with evidence. Be careful: a long segment takes longer to drive
than a short one, and that is not a problem. You are looking for the segment
that performs badly *relative to its own normal*.

**5. One figure.**
A figure a councillor could read. Labelled axes, units, and a title that
states the finding rather than describing the chart.

---

## Extension — pick exactly one

Name your choice, in writing, by the end of the week 4 session.

Extensions E1 to E5 use real national datasets. The catalogue, with working
addresses, known traps, and licence terms, is in
[`data_sources.md`](data_sources.md) — read its scope rule before you begin.
`starter/fetch_external.py` is a complete worked example of the pattern.

| | Extension | Data | The question it answers |
|---|---|---|---|
| **E0** | Bus lane scenario | corridor data only | A bus lane cuts run time on the worst segment by 30% in the peak. What is that worth across the corridor? |
| **E1** | Equity | Index of Multiple Deprivation | Whose delay is it? Weight the delay by the deprivation of the areas that bear it. |
| **E2** | Safety | STATS19 casualties | Where people walking and cycling are hurt along the corridor, set against where the bus is slowest. |
| **E3** | Latent demand | Propensity to Cycle Tool | Where cycling could relieve the corridor, and what the model behind that claim does not know. |
| **E4** | Access | OpenStreetMap | Which schools and other destinations depend on which stops — and therefore which failures matter most. |
| **E5** | Captive passengers | Census 2021 car availability | How many households near each stop have no car, and no alternative when the bus fails. |
| **E6** | Your own proposal | — | Approved in writing by the end of week 4. |

E0 needs no internet access and no new dataset. It is a full-credit choice,
not a lesser one — the scenario argument is the hardest to make well.

---

## Deliverables

**1. A repository that runs from a clean clone.**
Someone else will download your code onto a different machine and run it. If
it depends on a file that exists only on your laptop, or on a library you
never wrote down, it fails. You will test this on each other in week 5.

**2. A two-page brief for the authority.**
Written for a reader who does not code and will not read your code. What you
found, how confident you are, and what they should do. Two pages means two
pages.

**3. The figure.**

**4. A data provenance record** *(if your extension used external data)*.
For every external dataset: the address it came from and the date you
retrieved it; the licence line; your row counts at each stage — as downloaded,
after your area filter, after every merge; and the approximation you accepted,
stated plainly. Every approximation is defensible. None of them is defensible
silently.

**5. A five-minute presentation.**
Finding, evidence, recommendation. Five minutes is short: the first sentence
should be the answer, not the background.

**6. An individual reflection (each person, about 400 words).**
*What did you verify, and how do you know your answer is right?* Be specific.
Name the thing you checked, what you expected, and what you found.

---

## Marking

| | Weight |
|---|---|
| Code correctness and reproducibility (cleaning decisions included) | 25% |
| External data: integration, provenance, stated approximations | 15% |
| Brief and presentation | 20% |
| Individual reflection | 15% |
| *(weeks 2 and 3 coursework)* | *(25%)* |

A group that takes E0 is marked out of the same total: the 15% external-data
component is assessed on the scenario's assumptions and their justification,
which is the equivalent discipline.

There is a hidden check. Your cleaned dataset and your requirement 4 answer
will be compared against ground truth. You are not told the answer in
advance — and neither is the authority, in real life.

---

## How to work

**Rotate the roles.** Data, analysis, visualisation, writing. Swap at least
once. The week 5 cross-group review will reveal who understands the code.

**Commit early and often.** A commit that works is a place you can always get
back to.

**Do the unglamorous work first.** Every group that skips the data
reconnaissance loses more time later than the reconnaissance would have cost.

**Ask.** Two studio sessions with someone in the room is the most support you
will ever get on a piece of analysis. Use it.
