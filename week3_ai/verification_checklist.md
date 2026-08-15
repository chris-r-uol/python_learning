# Verification checklist

Use this whenever you accept code you did not write: from an AI assistant,
from a website, from a colleague.

Print it. Keep it beside you.

Code that runs is not the same as code that is right. Most errors in
AI-assisted work are silent. The script finishes, the number looks
reasonable, and the number is wrong.

---

## The four checks

### 1. Does it run?

Run it. If it fails, read the traceback from the bottom up.

### 2. Does it give the right answer on a case you already know?

Take five rows of the data. Work out the answer yourself, with a pen or a
spreadsheet. Then run the code on those five rows. Compare.

Most people skip this check. It is the one that finds real errors.

Work out the answer **separately** from the code. Comparing the code with
itself proves nothing.

If you cannot build a case where you know the answer, stop. You do not
understand the problem well enough yet to judge code that claims to solve
it.

### 3. What does it do with the awkward cases?

Test each one that applies to your data:

- [ ] **A missing value.** Is it dropped, or treated as zero? Those give
      different answers.
- [ ] **A duplicate row.** Is it counted twice?
- [ ] **A zero.** Does anything divide by it?
- [ ] **An empty input.** Does the code fail clearly, or return something
      that looks fine?
- [ ] **The full dataset**, not the sample. Does it still finish? Does the
      answer still make sense?

### 4. Can you explain every line?

Read the code line by line. Say what each line does.

A line you cannot explain is a line you cannot defend. You can always ask
what a line does. Keep asking until you understand it.

---

## Warning signs

- **Rows disappearing.** Compare the row count before and after every
  filter, merge and cleaning step. If the count changed, know why.
- **Numbers stored as text.** Values read from a file are text until
  something converts them. Text sorts alphabetically, so "10:00" comes
  before "9:00".
- **Invented column names.** Code that uses columns your data does not have.
  Worse: columns it does have, which mean something else.
- **Hidden assumptions.** The assistant does not know that your buses run
  every 8 minutes, or that your data crosses midnight. It will assume
  something and not tell you.
- **The wrong statistic.** A mean where a median was needed. An average of
  averages. These give numbers of about the right size, which makes them
  hard to notice.

---

## How to work

Small steps. Run the code after each one. Save a copy whenever something
works.

The pattern to avoid: ask for 200 lines, receive 200 lines, and have no idea
which one is wrong. Ask for one function. Check it. Then ask for the next.

---

## What you keep

For the week 3 task, and for every chapter of the project, keep three things
together:

1. The code.
2. The prompts you used.
3. **Evidence that the code is correct**: your hand-worked case, and what
   happened on each awkward case.

The evidence is the part with lasting value. A partial solution with proof
is worth more than a complete solution without it.
