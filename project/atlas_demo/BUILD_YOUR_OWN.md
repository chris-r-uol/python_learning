# Build your own

Everything in this section — seven chapters, eighteen figures, the scorecard,
this website — is produced by one command from a repository you can clone.

The website is not a separate project. It is the *output format*. There is no
Streamlit server, no Svelte build, no JavaScript, and nothing to deploy by
hand. The atlas writes markdown; MkDocs renders it; GitHub Pages serves it.

If you want your own atlas of your own patch as its own website, the whole
change is **two lines**.

---

## The two lines

Open `project/atlas_demo/atlas.py`. Near the top:

```python
PLACE_NAME = "Leeds city centre"
BBOX = (53.75, -1.62, 53.83, -1.49)     # south, west, north, east
```

Change them to your patch. Then:

```bash
cd project/atlas_demo
python atlas.py
```

Every chapter refetches, refilters, redraws and rewrites itself for your
place. Nothing else in the project needs to know where you moved to.

!!! warning "Two things that will bite you"

    **The ATCO area code.** Chapter 1 has `BUS_AREA = "450"`, which is West
    Yorkshire. Yours is different, it is not guessable, and the list of all
    150 is in `project/data/external/atco_area_codes.csv`. A wrong code
    returns a valid, empty answer.

    **The PCT region.** Chapter 5 has `PCT_REGION = "west-yorkshire"`. PCT
    regions are *historic counties*, so Bristol is `avon`. Also a valid,
    empty answer when wrong.

    Everything else — the census, deprivation, weather, OpenStreetMap and
    STATS19 — follows the bounding box on its own.

    The cached fallback copies in `project/data/external/` were cut to the
    **Leeds** box. If a live source fails while you are building another
    patch, the fallback is the wrong shape for you, and the provenance table
    on each page will say so.

---

## How the website part works

This is the piece worth stealing even if you never build a transport atlas.

### 1. The build writes markdown, not HTML

`pages.py` turns each finished chapter into a markdown file:

```python
def write_chapter(chapter, ctx):
    return al.write_page(chapter.slug + ".md", al.render_chapter(chapter, ctx))
```

`render_chapter` in `atlaslib.py` lays out the page: the question, the
narrative, the figures, the row counts, the hand-checks, the caveats, the
provenance. It knows nothing about transport. Hand it any `Chapter` object
and it produces a page in the same shape.

The figures are saved straight into `site_src/atlas/figures/`, so the page can
reference them with an ordinary relative link.

### 2. The prose is written by hand; the numbers are not

This is the part that matters, and it is the reason the atlas cannot quietly
go stale.

Each chapter's narrative lives in the chapter module as a template:

```python
("What the patch actually contains", """
With area 910 added, the patch holds **{stops:,} access points**: {bus:,} bus
stops and {rail} rail stations.
""".format(stops=len(stops), bus=len(bus_stops), rail=len(rail_stops))),
```

The words are mine. **Every number is injected from the computation.** If the
data changes, the sentence changes with it. There is no way to write "1,328
stops" into a page and have it still say that after the network grows,
because that string does not exist anywhere in the source.

If you take one idea from this section into your own work, take this one. A
report with hand-typed numbers in it is correct exactly once.

### 3. MkDocs renders it

`mkdocs.yml` already lists these pages in its navigation. Building the site is:

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

Then open the address it prints. Edit a chapter, rerun `python atlas.py`, and
the page reloads.

### 4. GitHub Pages publishes it

`.github/workflows/pages.yml` builds the site on every push to `main` and
deploys it. To publish your own:

1. Fork or push the repository to your own GitHub account.
2. In your repository, open **Settings → Pages** and set the source to
   **GitHub Actions**.
3. Push. The site appears at
   `https://<your-username>.github.io/<your-repo>/`.

The generated pages and figures are committed to the repository, which is
deliberate: the Actions runner does not have to fetch seven government
datasets in order to publish a page.

---

## If you would rather use Streamlit or Svelte

Nothing here stops you. The chapters produce plain Python objects, and
`pages.py` is only one consumer of them.

Swap `pages.py` for a module that writes whatever you want and the seven
chapters are unchanged. The separation is deliberate: **fetching, checking and
drawing know nothing about the output format.**

The reasons to use this approach instead:

| | This | Streamlit / Svelte |
|---|---|---|
| Dependencies | MkDocs, already in the repository | A framework, a server, a build step |
| Hosting | GitHub Pages, free, static | Somewhere that runs a process |
| Works offline | Yes, it is HTML | Needs the server |
| Rebuild cost | One command | One command, plus a deployment |
| Interactive | No | Yes |

If you want sliders and dropdowns, use Streamlit — that is what
`requirements-stretch.txt` is for. If you want a document that loads
instantly, works on a phone, and is still there in three years, this is the
cheaper option by a wide margin.

---

## What to copy

The files worth reading, in order of how much they will save you:

| File | Why |
|---|---|
| `atlaslib.py` | The counted filter, the check register, the provenance ledger, the distance function. About 200 lines and it is most of the quality control. |
| `PLAN.md` | The plan written before the code. The invention list in §1 is the single highest-value page in this section. |
| `chapters/ch01_stops.py` | One complete chapter: fetch, cut, count, draw, check, narrate. |
| `pages.py` | Chapter objects to website. Reusable unchanged. |
| `atlas.py` | The orchestrator. Sixty lines. |

The rest is transport.
