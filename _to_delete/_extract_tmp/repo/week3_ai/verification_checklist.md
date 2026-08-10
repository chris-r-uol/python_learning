# Verification checklist

Use this every time you accept code you did not write yourself — from an AI
assistant, from Stack Overflow, from a colleague. Print it. Keep it next to you.

Code that runs is not code that is right. Almost everything that goes wrong with
AI-generated analysis goes wrong *silently* — the script completes, the number
looks plausible, and it is wrong.

---

## The four checks

### 1. Does it run?
The lowest bar. Run it. If it errors, read the traceback bottom-up before doing
anything else.

### 2. Does it give the right answer on a case you already know?
Take five rows. Work out the answer with a pencil or a spreadsheet. Run the code
on those five rows. Do the numbers match?

**This is the check people skip, and it is the one that catches real errors.**
If you cannot construct a case you know the answer to, you do not understand the
problem well enough to be checking the code yet.

### 3. What does it do with the awkward cases?
Test each one that applies:

- [ ] A missing value — is it dropped, or treated as zero? Those are different answers.
- [ ] A duplicate row — counted twice?
- [ ] A zero — does anything divide by it?
- [ ] An empty input — does it crash or return something misleading?
- [ ] The full dataset, not just the sample — does it still finish, and still make sense?

### 4. Can you explain every line?
Go line by line. Any line you cannot explain is a line you cannot defend.
Ask what it does — you are allowed to ask, you are not allowed to skip.

---

## Warning signs in generated code

- **Rows disappearing.** Compare the row count before and after every filter,
  merge, or clean. If the number dropped, know exactly why.
- **Silent type coercion.** Times read as text, numbers read as text. Sorting
  "10:00" before "9:00" is a classic and it looks fine until it doesn't.
- **Invented column names.** Confident code referring to columns your data
  doesn't have — or worse, that it does have but that mean something else.
- **Domain assumptions.** An assistant does not know your headways are 8 minutes
  or that your data crosses midnight. It will assume something reasonable and
  not tell you.
- **Plausible statistics.** A mean where a median was needed, an unweighted
  average of averages. These produce numbers that are wrong by the right order
  of magnitude, which is the hardest kind of wrong to spot.

---

## Working method

Small steps. Run after every one. Commit whenever something works.

The failure mode is asking for 200 lines, getting 200 lines, and having no idea
which of them broke. Ask for one function. Check it. Then ask for the next.

---

## What you submit

For the week 3 homework, and for the project, you submit:

1. The code.
2. The prompts you used.
3. **Evidence it is correct** — your hand-worked case, and what happened on the
   awkward cases above.

The evidence is what is marked. A partial solution with proof scores higher than
a complete solution without it.
