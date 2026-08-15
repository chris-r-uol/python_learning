---
title: Setting up
---

# Setting up

Choose the guide that matches your situation. All of them end the same way:
a working Python, a virtual environment, the course packages, and a check
that tells you whether it worked.

**Allow about 45 minutes.** If a step fails, read the error and the "If this
fails" notes under that step. If 30 minutes pass and it is still broken, use
[Codespaces](codespaces.md) instead.

<div class="grid cards" markdown>

-   :material-microsoft-windows: **[Windows](windows.md)**

    ---

    Tick "Add python.exe to PATH" on the first installer screen. That
    checkbox causes most week 1 problems.

-   :material-apple: **[macOS](macos.md)**

    ---

    Install from python.org, not the Python already on your Mac. Type
    `python3` until your environment is active.

-   :material-github: **[GitHub Codespaces](codespaces.md)**

    ---

    Nothing to install. A browser and a free GitHub account. You get a real
    terminal and a real virtual environment.

-   :material-lock-outline: **[Locked-down laptop](locked-down-laptop.md)**

    ---

    No admin rights, blocked installers, or a network that interferes.
    Options in order.

-   :material-google: **[Google Colab](colab-fallback.md)**

    ---

    Use this if you cannot have a GitHub account. The differences are listed
    at the end of the guide.

-   :material-translate: **[Using Chinese services](chinese-services.md)**

    ---

    DeepSeek, Kimi, Qwen and others are supported. Prompting in Chinese is
    fine. Also covers working from China.

</div>

## What the check tells you

`python check_setup.py` gives one of three results.

| Result | Meaning |
|---|---|
| **ALL CHECKS PASSED** | Nothing to do. |
| **READY, WITH NOTES** | Also a pass. Everything needed works. Some notes are normal, such as "no virtual environment" on Colab. |
| **NOT READY YET** | Something is missing or wrong. The check names each problem and its fix. |

Nothing is collected. The check is for you. If the fix it names does not
work, the [start page](../index.md) lists what to try next.
