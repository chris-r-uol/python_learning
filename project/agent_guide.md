# Directing an agent

Week 3 taught you to work with an assistant one function at a time.

The atlas is different: seven pipelines and several hundred lines. You
cannot read all of it as carefully at the end as you did at the start.

This page is about quality control, which is the part that does not scale by
itself.

---

## 1. Write down what it will get wrong, before you delegate

Look at what [`data_sources.md`](data_sources.md) is. It is a list of the
things an assistant will invent: that severity `1` means fatal, that `avon`
is the region name for Bristol, that the ATCO code is not the number you
would guess, that longitude comes first.

When this project was built with an assistant, that list is what made it
safe. Because the list existed, the assistant never guessed the ATCO code,
never invented the severity mapping, never tried `bristol` as a region name.
Without the list, the same process gives you seven wrong chapters that all
run.

**In real work nobody gives you that list.** You write it before you start,
from the data guide, the column headers, a colleague, or the publisher's
website. It does not need to be long. It needs to name the facts that are
true but not visible in the file.

So: **before you delegate a large job, write down what your assistant is
likely to invent.** For this atlas the list is given to you. For your next
project it will not be.

## 2. Ask for the plan before the code

Before an assistant writes a chapter, make it tell you how it intends to
write it.

You can read a ten-line plan in a minute. You cannot read three hundred
lines of generated code in a minute, and across seven chapters you will not
try. The plan is the last point where checking the work is quick.

Ask for it in words:

> Before writing any code, give me your plan for this chapter as numbered
> steps: which file you will create, which function does what, which source
> you will fetch and from which address, and where you will print row
> counts. Do not write any code yet.

**What to look for in the answer:**

- **Is the source and address right, or invented?** "I will look up the ATCO
  code for the area" means it is about to guess.
- **Has the question changed?** A plan to average what you asked it to count
  is easier to see here than in the output.
- **Does it say where the row counts go?** If not, say so now.
- **Is it one chapter, or seven?** Scope creep is visible in a plan and
  invisible in code.

Then approve it, correct the step that is wrong, or ask for a smaller scope.
Only then let it build.

**Built-in plan modes.** Some assistants can do this as a formal step
instead of a typed request. GitHub Copilot in VS Code has one, and other
assistants have their own. They are worth trying.

Two things to know. These features differ in what they are allowed to write
to your folder, and they change between releases. If yours cannot write
files, the typed request above does the same job in any assistant. And a
plan mode does not read the plan for you. Approving a plan you did not read
is the same mistake as accepting code you did not read, one step earlier.

## 3. Three layers of quality control

They behave differently, and only one of them is yours.

### Layer 1 — the agent finds it alone

Tracebacks. A wrong column name, a missing file, a type error. The agent
sees the error and fixes it without being asked. In a normal build this is
most of the corrections.

This layer is free. You get it whether you ask or not.

### Layer 2 — the agent does it, if you ask

Row counts before and after every filter and join. Small tests for the
arithmetic. Rebuilding from a clean folder.

All of this is easy to delegate, and none of it happens unless you ask. The
difference between

> build chapter 3

and

> build chapter 3, printing the row count before and after every filter and
> every join, each with a label

is one clause. **If you take one habit from this page, take that clause.**

### Layer 3 — only you can do it

Checking that the answer is true.

An agent can calculate a number and compare it with an expectation. It
cannot know whether the expectation was right, because it wrote that too.

## 4. Checks that prove nothing

Here is what happened when a capable assistant built this atlas.

It produced **twenty hand-checks** and a display reading *"20 of 20 pass"*.
It looked thorough. It mostly was not, because the assistant wrote both the
expectation and the answer. Two of the twenty compared a number with itself.
That only came to light when an unrelated bug made them fail.

About **four** of the twenty were worth anything. All four were checked
against something **outside the dataset**:

- Leeds City Bus Station is on Dyer Street. You can check that on a map.
- The 1991-2020 average annual rainfall near Leeds is about 660 mm. You can
  check that against the Met Office.
- Both Leeds universities must appear in the amenities layer, or the query
  is wrong.

An agent cannot produce those, because they come from the world rather than
from the file. It can produce things that look like them.

So "20 of 20 pass" is not a sign of quality. The number that matters is how
many checks are anchored outside the data.

**A check that compares the code with itself proves the code is consistent.
It says nothing about whether the code is right.**

## 5. A contract for your agent

Paste this, adjust it, and hold the agent to it:

> For every chapter:
>
> - print the row count before and after each filter and each join, each
>   with a label saying what it is;
> - state every approximation you made;
> - record the source URL, the licence, and the date I fetched it;
> - **do not invent a hand-check.** Where a hand-check belongs, write
>   `TODO: hand-check` and tell me exactly what I would need to verify, and
>   where.

The last point changes the usual behaviour. Left alone, an agent produces
checks that pass. Under this contract it produces a **list of things you
must go and confirm**: one per chapter, against a map, a published
statistic, or somewhere you have been.

Seven checks against the outside world is achievable in a studio session.

## 6. Look at your output

Every data error in that build stopped the program. Every presentation error
did not. A map two zoom levels too far out. A cycling network where
everything came out one colour. A legend that had lost its units.

No row count finds those. Layers 1 and 2 do not find them. Somebody looking
at the picture finds them.

So add one step to every chapter: **open the figure and look at it.** Not
"did the script finish". Look at the image:

- Can you read the axis labels?
- Is the map showing your patch, or half the county?
- Does the colour scale separate anything?
- Would a stranger know what they are looking at?

This matters more if you build the web app. A front end makes the project
more impressive and easier to be wrong in, because its errors are visual.
Screenshot each view and look at it as carefully as you read your row
counts.

## 7. Keep your own score

At the end of each chapter, write two numbers at the top of it:

> Eighteen hand-checks. Four checked against something outside the data: the
> bus station address, the rainfall average, the two universities, and the
> casualty total against the published figure.

Nobody will ask for those numbers. There is no submission and nobody
reviewing your atlas.

The assistant in our test would have had to write *four*, next to a display
saying *20 of 20 pass*. Writing the honest second number is what stops you
believing your own interface.
