# Python for Transport & Civil Engineering

This course runs for five weeks. By the end of it you will be able to take a
messy transport dataset, clean it, analyse it, and produce a figure that
supports an argument. You will also be able to work out what has gone wrong
when your code does not run — which matters just as much.

## Start here

**Before week 1**, complete the setup. It takes about an hour, and it is not
optional: the first session builds on it.

1. Follow the setup guide for your machine:
   - Windows → [`setup/windows.md`](setup/windows.md)
   - macOS → [`setup/macos.md`](setup/macos.md)
   - Work laptop with no admin rights → [`setup/locked-down-laptop.md`](setup/locked-down-laptop.md)
   - **Installation not working, or you would rather skip it entirely** →
     [`setup/codespaces.md`](setup/codespaces.md). GitHub runs a machine for
     you with everything already installed; you need only a browser and a
     free GitHub account.
   - No GitHub account possible → [`setup/colab-fallback.md`](setup/colab-fallback.md)

   If you prefer Chinese services — Baidu, DeepSeek, WeChat sign-in, Chinese
   documentation — read [`setup/chinese-services.md`](setup/chinese-services.md)
   as well. Everything in this course works with them.

2. At the end of the guide you will run the setup check. From this folder, with
   your virtual environment active:

   ```
   python check_setup.py
   ```

3. Copy everything it prints and send it to us.

### What counts as a pass

The check ends with one of three verdicts:

| Verdict | Meaning |
|---|---|
| **ALL CHECKS PASSED** | Everything is installed and configured. Nothing to do. |
| **READY, WITH NOTES** | **This is also a pass.** Everything the course needs works. The notes are things to be aware of — and some of them, such as "no virtual environment" on Colab or a missing one on the day you install, are entirely normal. Read them, then carry on. |
| **NOT READY YET** | Something genuinely blocks you: Python is too old, the wrong Python is being used, or the packages are not installed. Send us the output and we will fix it with you. |

**Send us the output whichever verdict you get.** To be clear about what
this is: it is a report on *your machine*, not on you, and it is the only
thing all term that we ask you to send. A "not ready" result is just as
useful to us as a pass — it tells us what to fix before the session, so that
nobody spends class time watching an installer.

## What is in this folder

| Folder | Contents |
|---|---|
| `setup/` | Installation guides, one for each situation |
| `week1_setup/` | Your first scripts, and the traceback exercises |
| `week2_programming/` | The worked example and the practice drills |
| `week3_ai/` | The verification checklist and the AI-assisted task |
| `project/` | Your Patch — the individual transport atlas, and the data source catalogue |
| `instructor/` | Teaching notes **and the worked solutions to weeks 1 and 2** |
| `docs/` | How the course was designed, if you are curious |

**Yes, the answers are in there.** `instructor/solutions/` holds the fixed
versions of the week 1 exercises and all twelve week 2 drills. That is
deliberate: nothing on this course is graded, so the only person you can
cheat is yourself, and having the answers available means you can check your
own work the way you would use the answers in the back of a textbook. Use
them after a real attempt, or when you have genuinely run out of ideas.
Reading one first costs you the practice, which is the only thing the task
was ever going to give you.

## Three rules that apply all course

- **A figure with an unlabelled axis is not finished.** Every chart you produce
  needs labelled axes with units, and a title a stranger could understand.
- **Code that works but that you cannot explain is not finished either.** From
  week 3 onwards you will be asked how you know your answer is right.
- **Getting stuck is a normal part of this work, not a sign you are failing.**
  When it happens, bring the error message. The error message is where the
  answer starts.
