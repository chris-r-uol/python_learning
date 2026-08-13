---
title: Setting up
---

# Setting up

Pick the guide that matches your situation. All of them end in the same
place: a working Python, a virtual environment, the course packages, and a
setup check you send us.

**Budget about 45 minutes, and stop if it fights you.** If a step fails, copy
the error, note which step you were on, and send us that instead. We would
rather fix it before the first session than watch you fix it during.

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
| **NOT READY YET** | Something genuinely blocks you: Python too old, the wrong Python, or packages missing. Send it and we will fix it with you. |

Send the output whichever verdict you get. It is a report on your machine,
not on you, and it is the only thing all term that we ask you to send.
