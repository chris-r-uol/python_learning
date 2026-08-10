# Corridor reliability — project brief

**Weeks 4 and 5. Groups of 3–4.**

---

## The commission

You are analysts working for a transport authority. The 47 corridor runs from
Cathedral Square in the city centre to Longmoor Terminus, eighteen stops, both
directions, roughly every 8 minutes in the peaks.

Complaints about the 47 have gone up. The operator says the service is running to
timetable. Passengers say it is unreliable. Both can be true, and the authority
needs to know which.

They have given you four weeks of automatic vehicle location data and asked three
questions:

1. **Where and when is the corridor failing?**
2. **How badly, in terms a passenger would recognise?**
3. **What would one intervention be worth?**

You have two studio sessions and the week in between.

---

## The data

In `data/`. It is real-world shaped, which means it is not clean. Nobody has
written you a note explaining its quirks, because in practice nobody ever does.

| File | Rows | Contents |
|---|---|---|
| `arrivals.csv` | ~97,000 | `trip_id`, `stop_id`, `stop_name`, `direction`, `service_date`, `scheduled_time`, `actual_time`, `dwell_s`, `vehicle_id` |
| `stops.csv` | 18 | `stop_id`, `stop_name`, `lat`, `lon`, `sequence` |
| `segments.csv` | 17 | `segment_id`, `from_stop`, `to_stop`, `length_m` |
| `boardings.csv` | ~9,600 | `service_date`, `stop_id`, `hour`, `boardings` |

Times are `HH:MM:SS`. Distances are metres. Dwell is seconds.

**A warning, and it is the only one you get.** There are at least five things
wrong with `arrivals.csv`. Some of them will make your code crash, which is the
easy kind. Some of them will not — they will quietly give you a wrong answer that
looks completely reasonable. You saw exactly this in week 3.

Before you analyse anything, find out what is wrong with it. Count your rows
before and after every operation.

---

## Core requirements — every group

**1. Load and clean.**
Document every cleaning decision and why you made it. "Dropped 2,400 rows"
is not a decision; "dropped 2,400 exact duplicate rows, all from 8 April,
which appears to have been logged twice by the depot" is.

**2. Journey time distribution by time of day.**
Not just the mean. A mean journey time of 45 minutes tells the authority nothing
about whether to expect 40 or 60. Show the spread and say what it means.

**3. Headway regularity.**
Are buses bunching? Where, and when? A corridor running every 8 minutes on paper
where the gaps are 2, 3 and 19 minutes is not running every 8 minutes.

**4. The worst segment and time period.**
Identify it, with evidence. Be careful: a long segment takes longer than a short
one, and that is not a problem. You are looking for segments that perform badly
*relative to their own normal*.

**5. One figure.**
A figure a councillor could read. Labelled axes, units, and a title that states
the finding rather than describing the chart.

---

## Extension — pick exactly one

**A. Scenario.** A bus lane on the worst segment gives an estimated 30% run time
reduction in the peak. What is that worth across the corridor — in minutes, and
in whatever unit you think makes the case?

**B. Metric comparison.** Compute excess wait time alongside a simple punctuality
measure (% of trips within 5 minutes of schedule). They will disagree. Argue
which better represents what passengers experience, and show a case where
choosing the wrong one leads to the wrong intervention.

**C. Passenger-weighted delay.** Use `boardings.csv` to weight delay by the
number of people who actually experience it. This usually reorders the priority
list. If it does, say so — that is the finding.

**D. Your own.** Approved in writing by the end of week 4.

---

## Deliverables

**1. A repo that runs from a clean clone.**
Someone else will download your code onto a different machine and run it. If it
needs a file that only exists on your laptop, or a library you never wrote down,
it fails. You will test this on each other in week 5.

**2. A two-page brief for the authority.**
Written for someone who does not code and will not read your code. What did you
find, how confident are you, what should they do. Two pages means two pages.

**3. The figure.**

**4. A five-minute presentation.**
Finding, evidence, recommendation. Five minutes is short — the first sentence
should be the answer, not the background.

**5. An individual reflection (each person, ~400 words).**
*What did you verify, and how do you know your answer is right?* Specific. Name
the thing you checked, what you expected, what you got.

---

## Marking

| | Weight |
|---|---|
| Code correctness & reproducibility | 30% |
| Cleaning decisions — found and justified | included above |
| Brief & presentation | 25% |
| Individual reflection | 15% |
| *(plus weeks 2 and 3 coursework)* | 30% |

There is a hidden check. Your cleaned dataset and your requirement 4 answer will
be compared against ground truth. You are not told the answer in advance,
and neither is the authority in real life.

---

## How to work

**Rotate roles.** Data, analysis, visualisation, writing. Swap at least once. The
week 5 cross-group review will find out who understands the code.

**Commit early and often.** A commit that works is a place you can get back to.

**Do the boring thing first.** Every group that skips the data reconnaissance
loses more time later than they saved.

**Ask.** Two studio sessions with someone in the room is the most support you will
ever get. Use it.
