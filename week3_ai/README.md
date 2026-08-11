# Week 3 — AI acceleration

**By the end of this week you can:** describe a task precisely enough that an
AI assistant produces correct code, check that code against a case you can
work out by hand, and build things in small steps that you verify as you go.

The session has three parts. First a demonstration — deliberately before any
teaching, for reasons that will be obvious once you have seen it. Then the
ideas. Then one substantial task, done in class under supervision, which uses
everything from the first three weeks at once.

---

## Part 1 — Demonstration: the failure

We begin in `failure_demo/`: a reasonable-sounding request typed into an AI
assistant, a professional-looking answer, and an error of about 21% that
nothing on the screen would warn you about.

```
cd week3_ai/failure_demo
python lazy_analysis.py
python correct_analysis.py
```

If you missed the session, `failure_demo/README.md` records what happened and
why it matters. If you have not seen the session yet, know that the
demonstration lands harder live — the folder will still be there afterwards.

## Part 2 — The ideas

### 1. You have been promoted

Until this week, you wrote every line yourself. From today, an assistant can
write most of the lines — which changes your job rather than removing it.
You are now the person who **specifies** the work and the person who **signs
it off**.

Engineering already has this role, and you know how seriously it is taken. A
senior engineer signs drawings they did not draft. The signature does not
mean "someone competent probably did this"; it means *I checked this, and I
answer for it*. The checking is the qualification. Nobody is impressed that
the drawings were produced quickly.

The same logic governs assistants. An assistant makes you faster at exactly
the rate at which you can check its output — that is the whole equation. A
person who cannot check the output is not being made faster. They are
producing unverified answers sooner, with better formatting, and the
formatting makes it worse, because polished output disarms suspicion. The
two skills this week teaches — specifying and verifying — are the two halves
of being the signature rather than the drafter. Both depend on your being
able to read code, which is what the last two weeks bought you.

### 2. Specifying

The demonstration fails because the request leaves everything important
unsaid. Look at the difference concretely, using the week 2 data you already
know. Here is the request most people type:

> Analyse traffic_counts.csv and tell me the daily pattern.

And here is the same request as a specification:

> The file `traffic_counts.csv` has four columns: `date` (text, YYYY-MM-DD),
> `hour` (integer, 0–23), `direction` (text, either "northbound" or
> "southbound"), and `count` (integer, vehicles counted in that hour). There
> are two rows per hour per date, one per direction — I want them combined
> into a two-way total before averaging. Produce the average two-way count
> for each hour of the day, as 24 values in vehicles per hour. Peak values
> should land somewhere near 2,000–3,000; single figures or hundreds of
> thousands mean something is wrong. If any hour is missing for some date,
> report it — do not silently treat it as zero.

Every sentence in the second version closes a door through which a wrong
answer could walk. That is the entire craft, and it has four parts:

- **The shape of the input.** Columns, types, units. The specification above
  settles that `count` is vehicles per hour, not per day — without that, an
  assistant guesses, and either guess produces plausible output.
- **The conventions that live outside the file.** Nothing inside the CSV
  says there are two rows per hour. You know it; the assistant cannot. Every
  dataset has knowledge like this — a code for missing data, a unit, a
  renamed site — and it exists only in heads and documentation, never in the
  file itself. The demonstration you just watched turned entirely on one
  such convention.
- **The output you expect** — shape, units, and *rough size*. Saying "peaks
  near 2,000–3,000" costs one clause and buys you both a sanity check and a
  shared definition of nonsense.
- **The awkward cases.** Missing hours, duplicates, empty results. For each
  one, say what should happen. Any case you leave unspecified, the assistant
  will decide for you — silently, and with confidence.

Writing this down feels slow, and the feeling is misleading. Every item you
leave out becomes a guess; every guess is a place the code can be
confidently wrong; and finding a confident wrong answer later costs far more
than the specification would have. You have written specifications before —
a design brief, a lab protocol, a survey instruction sheet. This is that
skill, pointed at code.

### 3. Verifying

The full method is [`verification_checklist.md`](verification_checklist.md) —
print it and keep it beside you; it is written to remain useful long after
this course. Its heart is four checks, applied to any code you did not write
yourself.

1. **Does it run?** The lowest bar, and still worth stating, because a
   traceback read bottom-up (week 1) is the fastest possible feedback.
2. **Does it give the right answer on a case you already know?** This is the
   one people skip, so slow down on it. Take five rows of the real data.
   Compute the answer for those five rows *without the code* — by hand, or
   in a spreadsheet, which you can drive expertly. Then run the code on the
   same five rows and compare. The independence is the point: the check must
   not reuse the thing being checked, which is also why "the code agrees
   with itself" is not evidence. You saw this check in miniature in week 2 —
   the `assert` line comparing stage 4 against stage 3. If you cannot
   construct a case where you know the answer, stop: you do not yet
   understand the problem well enough to judge code that claims to solve
   it — and discovering that now is cheap.
3. **What does it do with the awkward cases?** Missing values, duplicates,
   zeros, empty inputs, the full file rather than the sample. Feed each one
   in deliberately and watch. Code that has only ever seen clean data has
   not been tested; it has been rehearsed.
4. **Can you explain every line?** Go through the code and narrate it. A
   line you cannot explain is a line you cannot defend in front of the
   person who asks — and in week 4, someone asks. Asking the assistant what
   a line does is always allowed, and asking until you actually understand
   is the skill. Skipping the line is the only wrong move.

### 4. Working in the loop

The failure pattern has a shape: ask for everything at once, receive two
hundred lines, discover the output is wrong, and have no idea which of the
two hundred lines to distrust. At that point your options are to debug
unfamiliar code — slow, miserable — or to start again — demoralising, and no
more likely to work the second time.

The alternative is to move in small, verified steps. Ask for one function —
*read the file, return the rows*. Run it. Check something about the result:
print the row count, print the first row, compare against what you know.
Only then ask for the next function. Each step is small enough that when
something breaks, the suspect list has one name on it — the piece that
changed since everything last worked.

And keep hold of that "last worked" state deliberately: save a copy, or make
a commit, every time the code reaches a state that runs and checks out. A
known-good version you can return to converts every failed experiment from a
crisis into a shrug. Small steps feel slower than the two-hundred-line leap.
Measure to the point where the answer is *verified*, rather than merely
generated, and they are much faster — this is the same edit → run → look
loop from week 1, with generation added.

### 5. Where this breaks

Honest limits, each with the form it actually takes:

- **Invisible domain assumptions.** The assistant assumes metres where the
  data is in kilometres, or that a day ends at midnight when your service
  runs past it — states the result confidently, and mentions the assumption
  nowhere.
- **Silent data loss.** A filter that drops rows with missing values when
  the missing rows were the finding; a merge that quietly discards
  everything without a match. The row count falls and nothing announces it —
  which is why the checklist has you compare counts at every step.
- **Plausible statistics.** A mean where the distribution is skewed and a
  median was needed; an average of averages that weights nothing correctly.
  The result is wrong by a factor small enough to look right — the hardest
  kind of wrong to catch, and check 2 is the tool that catches it.
- **The sample-versus-full-file gap.** Code rehearsed on a hundred clean
  rows meets the real file, which contains a duplicate day and one renamed
  site — and either crashes, or worse, does not.

Every one of these is caught by the four checks. None of them is caught by
reading the output and finding it believable — believable output is exactly
what the demonstration produced while being 21% wrong.

---

## Part 3 — The task

[`task.md`](task.md) — build a journey time tool, with AI assistance, against
the project's real data. You do it in class, with the instructor and the TA
circulating; it is the first time this course asks you to use an assistant,
a specification, and the checklist together on data that has real problems
in it.

You submit three things: the code, the prompts you used, and **evidence that
the code is correct**. The evidence carries 60% of the mark. A partial tool
with thorough verification scores higher than a complete tool with none —
that weighting is deliberate, and it is how the project weeks are marked too.

## What you are allowed to use

Anything — including pandas, a library you have not been taught. Working out
how to use an unfamiliar library safely, with the assistant's help and your
own checks, is precisely this week's skill.
