---
title: Setting up
---

# Setting up

Pick the guide that matches your situation. All of them end in the same
place: a working Python, a virtual environment, the course packages, and a
setup check that tells you whether it worked.

**Budget about 45 minutes, and watch the clock.** If a step fails, that is
the first genuine piece of practice this course offers — read the error,
check the "If this fails" notes under the step, and paste the exact message
into an AI assistant if it is still opaque. But if half an hour disappears
into fighting your own machine, stop and use
[Codespaces](codespaces.md) instead. Knowing when to change approach is a
professional judgement, not a concession.

<div class="grid cards" markdown>

-   :material-microsoft-windows: **[Windows](windows.md)**

    ---

    Tick **Add python.exe to PATH** on the first installer screen. That one
    checkbox causes most week 1 failures.

-   :material-apple: **[macOS](macos.md)**

    ---

    Install from python.org, not the Python already on your Mac. Type
    `python3`, not `python`, until your environment is active.

-   :material-github: **[GitHub Codespaces](codespaces.md)**

    ---

    Nothing to install: a browser and a free GitHub account. A real terminal
    and a real virtual environment, so no part of the course is lost.

-   :material-lock-outline: **[Locked-down laptop](locked-down-laptop.md)**

    ---

    No admin rights, blocked installers, or a network that interferes.
    Options in order, with a thirty-minute limit before you switch.

-   :material-google: **[Google Colab](colab-fallback.md)**

    ---

    If a GitHub account is not possible for you. Everything can be done
    there; the differences are listed honestly.

-   :material-translate: **[Using Chinese services](chinese-services.md)**

    ---

    DeepSeek, Kimi, Qwen and the rest are fully supported choices, and
    prompting in Chinese is encouraged. Also covers working from China.

</div>

## What the check tells you

Running `python check_setup.py` ends in one of three verdicts.

| Verdict | What it means |
|---|---|
| **ALL CHECKS PASSED** | Nothing to do. |
| **READY, WITH NOTES** | **Also a pass.** Everything the course needs works. Some notes are entirely normal — "no virtual environment" is expected on Colab. |
| **NOT READY YET** | Something genuinely blocks you: Python too old, the wrong Python, or packages missing. The check names each problem and its fix, in order. |

Nothing is collected — the check is for you. Work through whatever it
reports, and if the obvious fix does not land, the
[start-here page](../index.md) has a short section on getting yourself
unstuck.
