"""
The machinery every chapter shares.

Section 3 of PLAN.md names four pieces: a cache with provenance, a counting
filter, a figure house style, and a check register. They are all here, plus
the page writer that turns a finished chapter into a page of the website.

No chapter is allowed to fetch, filter, join, draw or claim anything except
through this file. That restriction is the whole quality-control design: if
counting is the only way to filter, nobody forgets to count.
"""

from __future__ import annotations

import io
import json
import os
import time
from dataclasses import dataclass, field

import matplotlib

matplotlib.use("Agg")           # no display in CI, and none needed
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np               # noqa: E402
import requests                  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(HERE, "..", "data", "external")
SITE_DIR = os.path.join(HERE, "..", "..", "site_src", "atlas")
FIGURE_DIR = os.path.join(SITE_DIR, "figures")
BUILD_DIR = os.path.join(HERE, "build")

FETCH_TIMEOUT = 90
RETRIES = 3
RETRY_WAIT = 6

# Identify the client. This is politeness on most services and a hard
# requirement on at least one: Overpass answers the default python-requests
# User-Agent with "406 Not Acceptable", which reads like a broken query rather
# than a rejected client.
USER_AGENT = (
    "python_learning-atlas/1.0 (teaching example; "
    "github.com/chris-r-uol/python_learning)"
)


# ---------------------------------------------------------------------------
# House style. One palette, checked for colourblind separation, used by every
# figure so that the atlas reads as one document rather than seven.
# ---------------------------------------------------------------------------

INK = "#1a1a1a"
MUTED = "#8a8a8a"
BLUE = "#1f6fb4"
ORANGE = "#e2711d"
GREEN = "#2e8b57"
PURPLE = "#7b52ab"
RED = "#c1292e"
SERIES = [BLUE, ORANGE, GREEN, PURPLE, RED, "#5a5a5a"]


def axes(figsize=(9, 5)):
    """Return (figure, axes) in the house style."""
    figure, ax = plt.subplots(figsize=figsize, dpi=140)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors=INK, labelsize=9)
    ax.grid(axis="y", alpha=0.18, linewidth=0.8)
    ax.set_axisbelow(True)
    return figure, ax


def save(figure, name):
    """Save a figure into the website's figure folder. Returns the filename."""
    os.makedirs(FIGURE_DIR, exist_ok=True)
    path = os.path.join(FIGURE_DIR, name)
    figure.tight_layout()
    figure.savefig(path, dpi=140, facecolor="white")
    plt.close(figure)
    return name


# ---------------------------------------------------------------------------
# Distance. Degrees are not metres, and a degree of longitude is not a degree
# of latitude. Both facts are in this one function so that no chapter has to
# remember them, and hand-check 6 tests it against two known points.
# ---------------------------------------------------------------------------

METRES_PER_DEGREE_LAT = 111_132.0


def metres_per_degree_lon(latitude):
    """Metres in one degree of longitude at this latitude."""
    return METRES_PER_DEGREE_LAT * np.cos(np.radians(latitude))


def distance_metres(lon1, lat1, lon2, lat2):
    """Straight-line distance in metres. Works on scalars or arrays.

    An equirectangular approximation, which is accurate to well under a metre
    over the few kilometres an urban patch spans, and is fast enough to run
    against every stop for every casualty.
    """
    mean_lat = (np.asarray(lat1) + np.asarray(lat2)) / 2.0
    dx = (np.asarray(lon2) - np.asarray(lon1)) * metres_per_degree_lon(mean_lat)
    dy = (np.asarray(lat2) - np.asarray(lat1)) * METRES_PER_DEGREE_LAT
    return np.hypot(dx, dy)


def nearest_distance_metres(lons, lats, target_lons, target_lats, block=256):
    """For each point in (lons, lats), the distance to the nearest target.

    Done in blocks so that a few thousand points against a few thousand
    targets does not build one enormous array.
    """
    lons = np.asarray(lons, dtype=float)
    lats = np.asarray(lats, dtype=float)
    tlon = np.asarray(target_lons, dtype=float)
    tlat = np.asarray(target_lats, dtype=float)
    out = np.empty(len(lons), dtype=float)
    for start in range(0, len(lons), block):
        stop = start + block
        d = distance_metres(
            lons[start:stop, None], lats[start:stop, None], tlon[None, :], tlat[None, :]
        )
        out[start:stop] = d.min(axis=1)
    return out


# ---------------------------------------------------------------------------
# The record-keeping types. Each chapter fills these in; the page writer reads
# them. Nothing reaches the website that did not pass through one of them.
# ---------------------------------------------------------------------------

@dataclass
class Count:
    """One row count, before and after one operation."""
    label: str
    before: int
    after: int

    @property
    def kept(self):
        if self.before == 0:
            return 0.0
        return 100.0 * self.after / self.before


@dataclass
class Check:
    """One hand-check.

    `anchored` is the field that matters. True means the claim was compared
    with something outside this dataset: a map, a published statistic, a
    physical fact. False means it only tests that the code agrees with
    itself, which is worth having but proves much less.
    """
    number: int
    claim: str
    against: str
    anchored: bool
    passed: bool
    detail: str = ""


@dataclass
class Source:
    """Where one dataset came from, and whether it came live or from cache."""
    key: str
    name: str
    url: str
    licence: str
    live: bool
    retrieved: str
    rows: int
    note: str = ""


@dataclass
class Figure:
    filename: str
    caption: str
    alt: str


@dataclass
class Chapter:
    number: int
    slug: str
    title: str
    question: str
    lead: str = ""
    sections: list = field(default_factory=list)   # (heading, markdown) pairs
    counts: list = field(default_factory=list)
    figures: list = field(default_factory=list)
    checks: list = field(default_factory=list)
    sources: list = field(default_factory=list)
    findings: list = field(default_factory=list)   # the three sentences
    caveats: list = field(default_factory=list)
    numbers: dict = field(default_factory=dict)
    plan_notes: list = field(default_factory=list)  # where the plan was wrong


# ---------------------------------------------------------------------------
# The build context. Holds the patch, the ledgers, and the only permitted way
# to fetch, filter or join.
# ---------------------------------------------------------------------------

class Context:
    def __init__(self, place_name, bbox, offline=False):
        self.place_name = place_name
        self.bbox = bbox                      # south, west, north, east
        self.offline = offline
        self.sources = []
        self.checks = []
        self.chapters = []
        # What one chapter hands to the next. Chapter 1 puts the stop
        # coordinates here; chapters 2 and 6 measure distance against them.
        self.shared = {}
        self.built_at = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
        self._check_number = 0

    # -- the patch ---------------------------------------------------------

    @property
    def south(self):
        return self.bbox[0]

    @property
    def west(self):
        return self.bbox[1]

    @property
    def north(self):
        return self.bbox[2]

    @property
    def east(self):
        return self.bbox[3]

    @property
    def centre(self):
        return ((self.west + self.east) / 2.0, (self.south + self.north) / 2.0)

    @property
    def width_km(self):
        lon_m = metres_per_degree_lon((self.south + self.north) / 2.0)
        return (self.east - self.west) * lon_m / 1000.0

    @property
    def height_km(self):
        return (self.north - self.south) * METRES_PER_DEGREE_LAT / 1000.0

    @property
    def area_km2(self):
        return self.width_km * self.height_km

    def inside(self, lons, lats):
        """Boolean mask: which points fall in the patch."""
        lons = np.asarray(lons, dtype=float)
        lats = np.asarray(lats, dtype=float)
        return (
            (lats >= self.south) & (lats <= self.north)
            & (lons >= self.west) & (lons <= self.east)
        )

    # -- fetching ----------------------------------------------------------

    def fetch(self, key, name, url, licence, cache_file, parse,
              method="GET", body=None, note=""):
        """Fetch one source, or fall back to the cached copy.

        `parse` is given the raw text and returns whatever the chapter wants.
        Whichever path is taken, a Source record is written, so a reader of
        the published page can always see whether a number came off the live
        service or out of a file with a date on it.
        """
        cache_path = os.path.join(CACHE_DIR, cache_file) if cache_file else None
        text = None
        live = False

        if not self.offline:
            headers = {"User-Agent": USER_AGENT}
            last_error = None
            # Two attempts, because a shared public API that answers 429 or
            # 504 is busy rather than broken. Overpass in particular rations
            # by IP, and the second ask usually succeeds.
            for attempt in range(RETRIES):
                try:
                    if method == "POST":
                        response = requests.post(url, data=body, headers=headers,
                                                 timeout=FETCH_TIMEOUT)
                    else:
                        response = requests.get(url, headers=headers,
                                                timeout=FETCH_TIMEOUT)
                    response.raise_for_status()
                    text = response.text
                    live = True
                    break
                except Exception as error:            # noqa: BLE001
                    status = getattr(getattr(error, "response", None),
                                     "status_code", None)
                    last_error = "{0}{1}".format(
                        type(error).__name__,
                        " {0}".format(status) if status else "")
                    if attempt + 1 < RETRIES:
                        time.sleep(RETRY_WAIT)
            if text is None:
                note = (note + " " if note else "") + (
                    "Live fetch failed ({0}) after {1} attempts; used the "
                    "cached copy.".format(last_error, RETRIES)
                )

        if text is None:
            if not cache_path or not os.path.exists(cache_path):
                # RuntimeError, not SystemExit: a chapter may have its own
                # fallback and must be able to catch this.
                raise RuntimeError(
                    "No live data and no cached copy for '{0}'".format(key)
                )
            with open(cache_path, encoding="utf-8") as handle:
                text = handle.read()

        data, rows = parse(text)
        self.sources.append(Source(
            key=key,
            name=name,
            url=url,
            licence=licence,
            live=live,
            retrieved=(self.built_at if live else _cache_date(cache_path)),
            rows=rows,
            note=note.strip(),
        ))
        return data

    # -- counting ----------------------------------------------------------

    def counted(self, chapter, label, before, after):
        """Record one filter or join. Returns the `after` count unchanged."""
        count = Count(label=label, before=int(before), after=int(after))
        chapter.counts.append(count)
        return count.after

    # -- checking ----------------------------------------------------------

    def check(self, chapter, claim, against, anchored, passed, detail=""):
        self._check_number += 1
        check = Check(
            number=self._check_number,
            claim=claim,
            against=against,
            anchored=bool(anchored),
            passed=bool(passed),
            detail=detail,
        )
        chapter.checks.append(check)
        self.checks.append(check)
        return check

    # -- ledgers -----------------------------------------------------------

    def write_ledgers(self):
        os.makedirs(BUILD_DIR, exist_ok=True)
        with open(os.path.join(BUILD_DIR, "provenance.json"), "w") as handle:
            json.dump([s.__dict__ for s in self.sources], handle, indent=1)
        with open(os.path.join(BUILD_DIR, "checks.json"), "w") as handle:
            json.dump([c.__dict__ for c in self.checks], handle, indent=1)


def _cache_date(path):
    if not path or not os.path.exists(path):
        return "unknown"
    return time.strftime("%Y-%m-%d", time.gmtime(os.path.getmtime(path)))


# ---------------------------------------------------------------------------
# Small parsers, so chapters do not each reinvent them.
# ---------------------------------------------------------------------------

def parse_csv(text, delimiter=","):
    """Return (list of dicts, row count)."""
    import csv
    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    rows = list(reader)
    return rows, len(rows)


def parse_geojson(text):
    data = json.loads(text)
    return data, len(data.get("features", []))


def parse_json(text):
    data = json.loads(text)
    return data, 1


def to_float(value, default=float("nan")):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


# ---------------------------------------------------------------------------
# The page writer. Turns a Chapter into markdown for the website.
#
# Every number in a published page arrives through this function from the
# computation, never typed into prose by hand. That is what stops the words
# and the arithmetic from drifting apart.
# ---------------------------------------------------------------------------

BANNER = (
    '!!! quote "Written by an AI assistant"\n\n'
    "    This page was planned, built and written by Claude. The prose is\n"
    "    hand-written; every number in it was injected from the computation\n"
    "    at build time. Rebuilt {built}.\n"
)


def _counts_table(counts):
    if not counts:
        return ""
    lines = [
        "| Operation | Rows before | Rows after | Kept |",
        "|---|---:|---:|---:|",
    ]
    for c in counts:
        lines.append("| {0} | {1:,} | {2:,} | {3:.1f}% |".format(
            c.label, c.before, c.after, c.kept))
    return "\n".join(lines)


def _checks_table(checks):
    if not checks:
        return ""
    lines = [
        "| # | The claim | Checked against | Anchored outside the data | Result |",
        "|---|---|---|:---:|:---:|",
    ]
    for c in checks:
        lines.append("| {0} | {1} | {2} | {3} | {4} |".format(
            c.number, c.claim, c.against,
            "⚓ yes" if c.anchored else "○ no",
            "pass" if c.passed else "**FAIL**"))
    return "\n".join(lines)


def _sources_table(sources):
    if not sources:
        return ""
    lines = ["| Dataset | Retrieved | Rows | Licence |", "|---|---|---:|---|"]
    for s in sources:
        how = "live" if s.live else "cached copy"
        rows = "{0:,}".format(s.rows) if isinstance(s.rows, int) else "—"
        lines.append("| [{0}]({1}) | {2}, {3} | {4} | {5} |".format(
            s.name, s.url, s.retrieved, how, rows, s.licence))
    body = "\n".join(lines)
    notes = [s.note for s in sources if s.note]
    if notes:
        body += "\n\n" + "\n".join("!!! warning\n\n    " + n for n in notes)
    return body


def render_chapter(chapter, ctx):
    """Return the markdown for one chapter page."""
    out = []
    out.append("# Chapter {0} — {1}".format(chapter.number, chapter.title))
    out.append("")
    out.append("*{0}*".format(chapter.question))
    out.append("")
    out.append(BANNER.format(built=ctx.built_at))
    if chapter.lead:
        out.append(chapter.lead.strip())
        out.append("")

    for heading, body in chapter.sections:
        if heading:
            out.append("## " + heading)
            out.append("")
        out.append(body.strip())
        out.append("")

    if chapter.figures:
        out.append("## The figures")
        out.append("")
        for fig in chapter.figures:
            out.append("![{0}](figures/{1})".format(fig.alt, fig.filename))
            out.append("")
            out.append("*{0}*".format(fig.caption))
            out.append("")

    if chapter.findings:
        out.append("## What it shows")
        out.append("")
        for sentence in chapter.findings:
            out.append("- " + sentence)
        out.append("")

    if chapter.counts:
        out.append("## Row counts")
        out.append("")
        out.append(
            "Every filter and every join in this chapter, with the row count "
            "on each side of it. A join that quietly dropped most of the "
            "patch would show up here as a percentage, not as an error."
        )
        out.append("")
        out.append(_counts_table(chapter.counts))
        out.append("")

    if chapter.checks:
        out.append("## Hand-checks")
        out.append("")
        out.append(_checks_table(chapter.checks))
        out.append("")
        for c in chapter.checks:
            if c.detail:
                out.append("**Check {0}.** {1}".format(c.number, c.detail))
                out.append("")

    if chapter.caveats:
        out.append("## What this chapter does not say")
        out.append("")
        for caveat in chapter.caveats:
            out.append("- " + caveat)
        out.append("")

    if chapter.plan_notes:
        out.append("## Where the plan was wrong")
        out.append("")
        for note in chapter.plan_notes:
            out.append('!!! failure "Correction to [the plan](plan.md)"')
            out.append("")
            for line in note.strip().split("\n"):
                out.append("    " + line)
            out.append("")

    if chapter.sources:
        out.append("## Provenance")
        out.append("")
        out.append(_sources_table(chapter.sources))
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def write_page(filename, markdown):
    os.makedirs(SITE_DIR, exist_ok=True)
    path = os.path.join(SITE_DIR, filename)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(markdown)
    return path
