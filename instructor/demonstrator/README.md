# The Leeds demonstrator

The instructor's own atlas for the Your Patch project — the same seven
chapters the students build, done for the default patch (Leeds city centre,
the bounding box in `project/starter/atlas.py`).

| File | What it is |
|---|---|
| `fetch_fallbacks.py` | Fetches every atlas source live, cuts it to the Leeds patch, and writes the cached fallbacks to `project/data/external/` plus their provenance manifest (`SOURCES.md`) |
| `leeds_atlas.py` | All seven chapters, built from those fallbacks: seven figures and `output/index.html` |
| `output/` | The built atlas — the committed copy is the reference |

## How it is used

**Before each delivery:** run `fetch_fallbacks.py`, then `leeds_atlas.py`,
and skim the figures. This refreshes the fallback data (STATS19 years, the
weather year, and OSM all move), confirms every endpoint is still alive, and
regenerates the reference atlas. Update the year constants when a new
STATS19 release lands.

**In the week 4 session:** chapters 1 and 2 are built *live*, with the
assistant, thinking aloud — including at least one wrong generation caught
by a row count. The committed `output/` is the safety net if the live build
goes wrong: switch to it, keep talking, nothing is lost.

**For students whose patch is Leeds:** the built atlas is the reference
implementation they can check themselves against. Share figures from
`output/` as each chapter becomes relevant rather than handing over the
whole report on day one — the volume is theirs to produce; the reference
exists so they can tell whether they produced it correctly.

`leeds_atlas.py` deliberately reads the cached fallbacks rather than
fetching, so it runs offline — it is the safety net, and safety nets do not
get to depend on the conference wifi. The fetching pattern the students copy
is `project/starter/fetch_external.py`, and `fetch_fallbacks.py` shows the
same pattern applied across all six remaining sources.
