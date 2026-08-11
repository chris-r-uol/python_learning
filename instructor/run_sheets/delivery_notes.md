# Delivery notes

The timed run sheets are in `docs/COURSE_DESIGN.md`. This file is the other
half: what to actually say, what goes wrong, and what to cut when you are
running late.

---

## Before week 1

**Send the pre-work 10 days out, not 3.** You need time to triage.

**Triage the `check_setup.py` submissions the day before.** Sort them into:

- *passed* — nothing to do
- *no venv* — fine, that's expected, we cover it in the session
- *wrong Python* (system Python, Store Python, 3.9) — email the specific fix
- *nothing at all* — phone call, or put them straight on Colab

Walk into week 1 knowing which category every student is in. The 10-minute
triage slot at the start is for the ones who ignored the email, and there will
be some.

---

## Week 1

**Say this early:** *"Everyone in this room will spend the next five weeks
getting error messages. That is not you failing at programming. That is
programming."* Some of them are technically confident people who are about to be
bad at something for the first time in a while, and they need permission.

**The single most valuable ten minutes** is the traceback anatomy at 80–90. If
you are running late, cut the environments section down to two sentences and
protect this. Environments they can pick up from the guide. Reading a traceback
they cannot.

**Live-code the modification.** Do not show finished code. Type it, get it
wrong, read the error out loud, fix it. Watching an expert recover from an error
is the thing they cannot get from a textbook.

**Common in the room:**

- Running `python first_script.py` from the wrong folder. Good — that's the
  lesson. Make them fix it with `cd` rather than doing it for them.
- `python` vs `python3` on macOS. Say it three times.
- Someone will have a file called `first_script.py.txt`. Windows hides
  extensions by default; show them how to turn that off.

---

## Week 2

**This session will overrun. Plan the cut in advance.**

Priority order if you lose time:

1. Protect the figure (stage 6). It is what makes them want to carry on.
2. Protect the function (stage 4). It is the hardest idea and the most reusable.
3. Cut the NumPy rewrite (stage 5) to a two-minute "here is what this becomes,
   the drills will walk you through it." It reads well cold.
4. Never cut stage 3. The verbose loop is the load-bearing wall.

**Type stage 3 slowly and out loud.** Nested loops are where people fall off.
Narrate the indices: *"we are now on hour eight; we are about to look at every
row in the file and ask whether it is hour eight."*

**When you get to stage 5**, do not just show the NumPy version — show them the
line count. Stage 3 is 15 lines. Stage 5 is 3. Then say the important part:
*"you could not have understood those 3 lines an hour ago."*

**The assert at the end of stage 4 is deliberate.** Point at it. *"I checked my
new version against my old one. That is the entire idea of week 3, three weeks
early."*

**The drills are ungraded** — the marker in the file is self-checking, not
assessment. Encourage at least the nine unstarred; the three starred ones
identify who will move fastest in the project weeks and can absorb stretch
chapters.

---

## Week 3

**Do the failure demo cold, before any framing.** If you explain what is about
to happen first, it does not land. The choreography (the student-facing
`week3_ai/failure_demo/README.md` is now a post-session recap and no longer
contains it):

1. Say the task out loud, then type the lazy prompt in front of them exactly
   as written: *"analyse this traffic data and tell me the average speed on
   each link"*, attaching `data/link_speeds.csv`. Whatever assistant you are
   licensed for will produce something close to `lazy_analysis.py`; if it does
   something better, run the saved file instead and say so — the point
   survives either way.
2. Run it. **Stop. Ask the room: is this right?** Let the silence run — it
   looks right, and that is the lesson arriving.
3. Open the CSV, point at the `-1` values, run `correct_analysis.py`.
4. Draw out the three things in order: the ranking survived; the magnitudes
   are ~21% wrong; the tell (`N obs` = 20 everywhere) was printed all along.
5. Close with the line the rest of the course hangs on: the assistant did not
   make a mistake — it had no way to know what `-1` meant, and it did not say
   it was guessing. That is their job now.
6. Rewrite the prompt together until it names the columns, the types, what
   `-1` means, and the expected output. Re-run. Compare.

**Re-run the demo live on whatever assistant your students are licensed for, the
week before you teach it.** These tools change. If it now handles the sentinel
correctly, you need a harder example — the pattern to reach for is a convention
that lives outside the file. The renamed stop in the project data works, or feed
it distances in metres and ask for a speed in kph.

**Expect a substantial part of the cohort on Chinese assistants** — DeepSeek
and Kimi above all (see `setup/chinese-services.md`, which sanctions them).
The failure demo reproduces on them just as reliably, and it is worth
re-running it on DeepSeek too before the session so you can say so from
experience. Students prompting in Chinese is fine and explicitly allowed;
what you circulate to check is the same as for everyone — the row counts and
the hand-worked case, not the language of the prompt.

**Say the grading rule out loud, twice.** "The evidence is what is marked." Some
of them will not believe you until they see the first mark come back.

**Expect pushback**, usually one of:

- *"Why did we spend two weeks on loops if the AI writes them?"* — Because you
  just watched it write something wrong, and everyone in the room who could read
  code spotted it. That is the answer, and the demo has already made it for you.
- *"This is just how I already use it."* — Good. Then the verification section
  will be easy marks. It will not be.

**The hands-on block will fragment.** Different setups, different licences,
different speeds. Keep the objective narrow: one working function that loads the
project data. Not a finished tool.

---

## Weeks 4–5

> **Superseded:** the notes below describe the retired group corridor studio.
> Weeks 4–5 are now the individual transport atlas — structure and studio
> flow in `docs/ATLAS_PROJECT_DESIGN.md`.

**Form the groups yourself.** Do not let them self-select — you will get one
group of four strong students and one group of four who are all hoping someone
else does it. Use the week 2 drill scores: one 12/12, one who got 9, two in
between.

**The data reconnaissance slot (15–35 in week 4) is the highest-value 20 minutes
of the whole project.** Every group reports three things they noticed. Write them
on the board. Between them the room will find four of the five defects. Do not
tell them the fifth — let it bite someone, then let them tell the room in
week 5.

**Ground truth is in `instructor/marking/hidden_check.py`.** Do not open it in
front of them.

**The five defects, and roughly when each surfaces:**

| Defect | Usually found | If nobody finds it |
|---|---|---|
| 2,400 duplicate rows | reconnaissance, if they count rows | Ask the room: "has anyone checked for duplicates?" |
| Stop S009 renamed | when a group-by gives 19 stops | Ask: "how many stops are on this corridor?" |
| Negative dwell times | when someone plots a distribution | Ask: "what is the minimum dwell time?" |
| BUS_2841 missing 3 days | rarely — this is the hard one | Leave it. It barely affects the answer, and that is itself worth saying. |
| Times past midnight (24:06) | when a naive parse crashes | It will crash. They will find it. |

**Circulating: ask, don't fix.** The three questions that unstick almost
everything:

1. "How many rows did you have before that, and how many after?"
2. "What would you expect that number to be?"
3. "Show me the five rows that produced that."

**The cross-group review in week 5 is not a formality.** Give it the full 15
minutes and make them actually clone and run. Roughly half will fail — hardcoded
absolute paths, an uncommitted data file, a library nobody wrote down. Let them
feel it. It is the single most transferable lesson in the two weeks and it
cannot be taught by telling.

**Presentations: enforce the first sentence.** If a group opens with "so, we were
given a dataset of bus arrivals…", stop them and ask for the finding. Five
minutes is not long enough for background.

---

## What to fix for next time

Keep a note during delivery of:

- Which pre-work setup failures you saw, and whether the guides covered them
- Where week 2 actually ran out of time
- Whether the failure demo still failed
- Which project defect nobody found
- Any group whose repo would not run, and why

Reroll `SEED` in `instructor/data_generator.py` before the next cohort so the
defects move and last year's answers do not transfer.
