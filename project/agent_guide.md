# Directing an agent

Week 3 taught you to work with an assistant one function at a time. The
atlas is a different problem: seven pipelines, several hundred lines, more
than you can read as carefully at the end as you did at the start. You are
no longer supervising a helper. You are directing production.

This page is about the part that does not scale by itself — quality
control — and it exists because we ran this project with a very capable AI
assistant and watched exactly where its self-checking held up and where it
quietly became decoration.

---

## 1. Before you delegate, write down what it will get wrong

The single most useful document in this project is
[`data_sources.md`](data_sources.md). Look at what it actually is: a
pre-loaded list of the things an assistant will confidently invent. That
severity `1` means fatal. That `avon` is the PCT region for Bristol. That
the ATCO code is not the number you would guess. That longitude comes
first.

When we ran this project with an assistant, that document was what made
delegating safe — not skill, and not care. Because the list existed, the
assistant never guessed the ATCO code, never invented the severity mapping,
never tried `bristol` as a region name. Take the document away and the same
process produces seven plausible, wrong chapters, all of which run.

**In real work nobody hands you that document.** You write it, before you
start, from whatever you can find out: the data guide, the column headers,
a colleague, the publisher's website. It does not need to be long. It needs
to name the conventions that are true but not visible in the file.

So the transferable move, and the one worth practising here, is this:
*before you delegate volume, write down what your assistant is likely to
invent.* For the atlas that list is given to you. For your eighth chapter,
your dissertation, and your first job, it is not.

---

## 2. Ask for the plan before the code

The second pre-delegation move, and the one that costs the least for what it
returns: **before an assistant writes a chapter, make it tell you how it
intends to write it.**

The arithmetic is simple. You can read a ten-line plan properly in about a
minute. You cannot read three hundred lines of generated code properly in
anything like that, and at seven chapters you will not try. A plan is the
last point where the work is small enough to review honestly.

You do not need a special tool for this. Ask, in words:

> Before writing any code, give me your plan for this chapter as numbered
> steps: which file you will create, which function does what, which source
> you will fetch and from which address, and where you will print row
> counts. Do not write any code yet.

**What you are looking for in the answer.** This is where the list from
section 1 earns its keep — a plan is short enough that you can actually
check it against what you know:

- Has it named the **right source and address**, or invented one? "I will
  look up the ATCO code for the area" is the sound of a plan about to guess.
- Has it silently changed the **question**? A plan to average what you asked
  it to count is easier to catch here than in the output.
- Does it say **where the row counts go**? If not, say so now rather than
  reading them into the code afterwards.
- Is it **one chapter**, or has it quietly scoped seven? Scope creep is
  visible in a plan and invisible in a diff.

Then do one of three things: approve it, correct the step that is wrong, or
send it back with a narrower scope. Only then let it build.

**Built-in plan modes.** Several assistants can do this as a formal step
rather than a typed request — GitHub Copilot in VS Code has a plan mode, and
other assistants have their own equivalents under various names. They are
worth trying: a plan you can approve step by step is easier to review than a
paragraph of prose.

Two honest caveats. First, these features differ in what they are allowed to
do — some produce a plan and then write files directly, others are more
restricted, and the details change from release to release. If yours will not
write into your project folder, that is a limitation of the tool and not a
problem with the approach: the typed request above does the same job in any
assistant, including the Chinese services in `setup/chinese-services.md`.
Second, **a plan mode does not review the plan for you.** It makes the plan
easy to see. Reading it is still the job, and approving a plan you did not
read is the same mistake as accepting code you did not read, one step
earlier.

## 3. Three layers of quality control

They behave completely differently, and only one of them is yours.

### Layer 1 — the agent catches it on its own

Tracebacks. A wrong column name, a file that is not there, a type error.
The agent sees the error and fixes it without being asked, and in a typical
build this accounts for most corrections.

This layer is free. You will get it whether you ask for it or not, and it
is not evidence of anything.

### Layer 2 — the agent will do it, but only if you ask

Row counts before and after every filter and join. Small tests for the
arithmetic. Rebuilding from a clean folder to prove nothing depends on the
mess in your working directory.

All of this is fully delegable and all of it is invisible unless you ask
for it. The difference between

> build chapter 3

and

> build chapter 3, printing the row count before and after every filter and
> every join, each with a label

is one clause. It is also the difference between a black box and a pipeline
that checks itself in front of you. **If you take one habit from this page,
take that clause.**

### Layer 3 — irreducibly yours

Checking that the answer is true of the world.

An agent can compute a number, and it can compare that number to an
expectation. What it cannot do is know whether the expectation was right,
because it wrote that too. This is where quality control stops being
delegable, and it is the whole of the next section.

---

## 4. QC theatre, and how to avoid producing it

Here is what happened when a very capable assistant built this atlas.

It produced **twenty hand-checks**, and a display reading *"20 of 20
pass"*. It looked like thorough verification. It mostly was not, for one
reason: the assistant wrote both the expectation and the answer. That is
marking your own homework with a nice interface on top. Two of the twenty
were literal tautologies — comparing a number to itself — and that only came
to light when an unrelated string-comparison bug made them fail.

Of the twenty, about **four** were worth anything. Those four had one
property in common: each was anchored to something **outside the dataset**.

- Leeds City Bus Station is on Dyer Street — checkable on a map.
- The 1991–2020 average annual rainfall near Leeds is about 660 mm —
  checkable against the Met Office.
- Both Leeds universities must appear in the amenities layer, or the query
  is wrong — checkable because you know they exist.

An agent cannot generate those, because they come from the world rather
than from the file. It can, however, generate things that *look* exactly
like them — which is why "20 of 20 pass" is not a quality signal, and why
the number to be proud of is not how many checks you have but how many are
anchored outside the data.

**A check that only compares the code to itself proves the code is
consistent. It says nothing about whether it is true.**

---

## 5. A contract to give your agent

Paste this, adapt it, and then hold the agent to it:

> For every chapter:
> - print the row count before and after each filter and each join, each
>   with a label saying what it is;
> - state every approximation you accepted;
> - record the source URL, the licence, and the date I fetched it;
> - **do not invent a hand-check.** Where a hand-check belongs, leave
>   `TODO: hand-check` and tell me exactly what I would need to verify, and
>   where I could verify it.

The last clause is the important one, and it inverts the usual behaviour.
Left alone, an agent produces checks that pass. Under this contract it
produces a **shortlist of things you must go and confirm** — one per
chapter, against a map, a published statistic, or somewhere you have
actually stood.

Seven external anchors across the project is achievable inside a studio
session, and it is real quality control rather than the appearance of it.

---

## 6. Look at your output

Every data bug in that build failed loudly. Every *presentation* bug failed
silently and looked confident: a map two zoom levels too far out, a cycling
network saturated to a single colour, a legend that had quietly lost its
units.

No row count catches any of those. Nothing in layer 1 or layer 2 catches
them. The only thing that caught them was somebody looking at the picture.

So add one step to every chapter: **open the figure and look at it.** Not
"did the script exit without error" — look at the image. Can you read the
axis labels? Is the map showing your patch or half the county? Does the
colour scale distinguish anything, or has it collapsed? Would a stranger
know what they were looking at?

This matters more if you build the optional web app. A front end makes the
project more impressive and much easier to be quietly wrong in, because
every failure it introduces is a visual one. If you go that far, build in
the habit of screenshotting each view and looking at it as deliberately as
you read your row counts.

---

## 7. Keep your own score

At the end of each chapter, write two numbers at the top of it:

> *Eighteen hand-checks. Four verified against something outside the data —
> the bus station address, the rainfall average, the two universities, and
> the casualty total against the published figure.*

Nobody will ask you for those numbers. There is no submission, no
presentation, and nobody reviewing your atlas. That is precisely what makes
them worth keeping accurately.

The assistant in our trial would have had to write *four*, next to a display
saying *20 of 20 pass*. Writing the honest second number is what stops you
believing your own interface — and it is a habit you will need most in the
situations this course cannot simulate, where the work matters, the deadline
is real, and nobody is looking over your shoulder.

Be the person who knows which four they are.
