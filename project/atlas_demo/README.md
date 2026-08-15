# The worked atlas

A complete transport atlas of Leeds city centre, planned and built by an AI
assistant, published at
[the course site](https://chris-r-uol.github.io/python_learning/atlas/).

    python atlas.py

Seven national datasets, cut to the patch, counted, drawn, checked, and
written out as the markdown pages of a website.

| File | What it is |
|---|---|
| `PLAN.md` | The plan, written before any code existed |
| `BUILD_YOUR_OWN.md` | Two lines to change to make it yours |
| `atlas.py` | The one command |
| `atlaslib.py` | Cache and provenance, counted filters, distances, figure style, check register, page writer |
| `pages.py` | Chapter objects to website markdown |
| `chapters/` | One module per chapter, each exporting `build(ctx)` |
| `build/` | Generated: `provenance.json` and `checks.json` |

Output lands in `site_src/atlas/` — the pages and the figures — because the
website is the atlas's output format, not a separate project.

    python atlas.py --offline     use the cached copies, fetch nothing
    python atlas.py --only 3      build one chapter

This is a demonstration, not a model answer to copy. Your project is your own
patch and your own questions.
