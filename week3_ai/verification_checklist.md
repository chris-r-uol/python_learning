# Verification checklist

Use this checklist every time you accept code you did not write yourself —
from an AI assistant, from a website, from a colleague. Print it. Keep it next
to you.

Code that runs is not the same as code that is right. Almost everything that
goes wrong in AI-assisted analysis goes wrong *silently*: the script finishes
without an error, the number looks plausible, and the number is wrong.

---

## The four checks

### 1. Does it run?

The lowest bar. Run it. If it produces an error, read the traceback from the
bottom up before doing anything else.

### 2. Does it give the right answer on a case you already know?

Take five rows of the data. Work out the answer with a pencil or a
spreadsheet. Run the code on those same five rows. Do the numbers match?

**This is the check that people skip, and it is the one that catches real
errors.** If you cannot construct a case where you know the answer, you do not
yet understand the problem well enough to be checking the code — which is
worth knowing in itself.

### 3. What does it do with the awkward cases?

Test each one that applies to your data:

- [ ] A missing value — is it dropped, or treated as zero? Those give
      different answers.
- [ ] A duplicate row — is it counted twice?
- [ ] A zero — does anything divide by it?
- [ ] An empty input — does the code fail loudly, or return something
      misleading?
- [ ] The full dataset, not just the sample — does it still finish, and does
      the answer still make sense?

### 4. Can you explain every line?

Go through the code line by line. Any line you cannot explain is a line you
cannot defend. You are always allowed to ask what a line does. You are not
allowed to skip it.

---

## Warning signs in generated code

- **Rows disappearing.** Compare the row count before and after every filter,
  merge, and cleaning step. If the count dropped, know exactly why.
- **Numbers stored as text.** Times and counts read from a file arrive as
  text unless something converts them. Text sorts alphabetically, so "10:00"
  sorts before "9:00" — and everything looks fine until it is not.
- **Invented column names.** Confident code that refers to columns your data
  does not have — or, worse, columns it does have that mean something else.
- **Hidden domain assumptions.** An assistant does not know that your buses
  run every 8 minutes, or that your data crosses midnight. It will assume
  something reasonable, and it will not tell you it assumed it.
- **Plausible statistics.** A mean where a median was needed; an unweighted
  average of averages. These errors produce numbers of the right general size,
  which makes them the hardest kind to notice.

---

## Working method

Small steps. Run the code after every step. Commit, or save a copy, whenever
something works.

The failure pattern to avoid: asking for 200 lines, receiving 200 lines, and
having no idea which of them is broken. Ask for one function. Check it. Then
ask for the next one.

---

## What you keep

For the week 3 task, and again for every chapter of the project, keep three
things together:

1. The code.
2. The prompts you used.
3. **Evidence that the code is correct** — your hand-worked case, and what
   happened on each of the awkward cases above.

The evidence is the part with lasting value. A partial solution with proof is
worth more than a complete solution without it — in this course, where nobody
is grading either, and afterwards, where nobody is checking either.
