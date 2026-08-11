# UK open data — the catalogue

The sources behind the atlas chapters. Every source here is free, needs no
account, and was checked working on **10 August 2026**. If one is unavailable
on the day, use the cached fallback copy in `data/external/` and record the
date. Public data services go down from time to time; working around it is
part of the job, not a reason to stop.

`starter/fetch_external.py` is a complete worked fetcher for the first one.
Read it before you build any of the others. The pattern never changes.

---

## First, the thing that wastes the most time

Three of the seven chapters need an **area identifier** before they will
give you anything: NaPTAN wants an ATCO area code, the PCT wants a region
folder name, and the Census wants a local-authority code. None of these is
guessable, all of them look guessable, and asking an assistant produces
confident wrong answers — this is exactly the week 3 lesson wearing a
different hat.

So do not guess, and do not ask. Each one has a known route:

| You need | Where it comes from |
|---|---|
| ATCO area code (chapter 1) | `data/external/atco_area_codes.csv` in this repository — all 150, by name |
| PCT region name (chapter 5) | the list in the PCT entry below — they are historic counties, so Bristol is `avon` |
| Local-authority code (chapter 4) | the deprivation file itself, which carries district names beside their codes |
| The ONS boundary service address (chapter 3) | copy it from the ONS entry below — do not let an assistant reconstruct it from memory |

That last row deserves its own warning, because it is the one place in the
catalogue where an assistant will fill a gap with something that looks
right. The address is long, it contains a service identifier nobody could
derive, and a wrong one returns an error rather than a wrong answer *only
if you are lucky*. Copy it. Do not retype it, and do not ask for it.

The three chapters not in that table — safety, amenities and weather — need
only your bounding box, so once chapter 1 has defined your patch they will
work straight away.

**One more thing about this page, and it is the point of it.** What you are
looking at is a list of the things an assistant will confidently invent.
Nobody will hand you one of these in real work; you write it yourself,
before you start. See [`agent_guide.md`](agent_guide.md).

## The scope rule

You have three weeks of Python. Real geospatial analysis is a term's work on
its own, so the atlas draws a hard line:

**In scope** — three operations, and everything on this page is reachable with them:

| Operation | Example |
|---|---|
| **Key join** | LSOA code → deprivation decile |
| **Bounding-box filter** | keep rows whose lat/lon fall in your study area |
| **Distance** | how far is this casualty from the nearest stop |

**Out of scope** — polygons, coordinate-system transforms, GDAL, R, PostGIS. If
your assistant proposes `geopandas`, `shapely`, `pyproj`, `ogr2ogr` or an
`EPSG:27700` conversion, you have been handed a problem one size too big. Stop
and ask for the bounding-box or distance version instead.

That rule is not because the real tools are bad. It is because you cannot verify
what you cannot read, and a projection bug produces a map that looks fine.

---

## Tier 1 — a CSV at a URL

`pandas.read_csv(url)` and you are done. Start here.

### STATS19 — road casualties
Every reported injury collision in Great Britain, with coordinates.

- **Gives you:** where people walking and cycling get hurt in your patch.
- **How:** `https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-collision-2023.csv` (and `-casualty-2023.csv`), joined on `collision_index`.
- **Worked example:** `starter/fetch_external.py`.
- **The trap:** `casualty_type` and `collision_severity` are integer codes whose
  meanings are in a separate guidance document. `0` is a pedestrian, `1` a
  cyclist, severity `1` is *fatal*, not slight. An assistant will guess, and it
  will guess plausibly.
- **Licence:** OGL v3, © Crown copyright.

### Index of Multiple Deprivation 2019
The standard English measure of relative deprivation, by small area (LSOA).

- **Gives you:** how your patch sits in England's deprivation distribution.
- **How:** [File 7 (all scores, ranks, deciles)](https://assets.publishing.service.gov.uk/media/5dc407b440f0b6379a7acc8d/File_7_-_All_IoD2019_Scores__Ranks__Deciles_and_Population_Denominators_3.csv) — 32,844 rows, one per LSOA.
- **The trap, and it is the instructive one:** IMD 2019 uses **2011** LSOA
  codes. The boundary service in tier 2 returns **2021** codes. Most codes are
  identical between the two vintages, so a merge will appear to work — and
  quietly drop the areas whose codes changed. Count your rows before and
  after. This is the whole course in one join.
- **Second trap:** decile **1 is the most deprived**, not the least. Published
  charts regularly get this backwards; check yours twice.
- **A useful side effect.** Every row carries both the *name* and the
  *code* of its local authority district. So you can cut this file down by
  name — `"Leeds"`, `"York"` — without needing to know any code, and the
  code you get back in the same rows (`E08000035` for Leeds) is exactly the
  one the Census chapter needs. Two chapters, one lookup, and the lookup is
  a word you already know.
- **Licence:** OGL v3.

### DfT road traffic counts (AADF)
Annual average daily flows on the road network, by local authority.

- **Gives you:** what the traffic in your patch's local authority is doing,
  and whether it is growing.
- **How:** `https://storage.googleapis.com/dft-statistics/road-traffic/downloads/data-gov-uk/local_authority_traffic.csv`
- **The trap:** it is *annual average daily* — you cannot get a peak hour out of
  it, and any argument you build about the peak from this number is invented.
- **Licence:** OGL v3.

### Census 2021 via Nomis
Households, car availability, method of travel to work, by small area.

- **Gives you:** how many households in your patch have no car — the people
  for whom walking, cycling, and the bus are the whole transport system.
- **How:** the Nomis API returns CSV directly, e.g.
  `https://www.nomisweb.co.uk/api/v01/dataset/NM_2062_1.data.csv?geography=...&measures=20100`
- **The trap:** finding the right dataset id and geography code is most of
  the work. The car-availability table (TS045) is dataset `NM_2063_1`, and
  a district's small areas are requested as
  `geography=<district code>TYPE151` — for example
  `E08000035TYPE151` for every LSOA in Leeds. **You do not need to hunt for
  that district code:** it comes free with the deprivation file above.
- **Verify it:** check the row count and one value against the
  [Nomis web interface](https://www.nomisweb.co.uk/) by hand.
- **Licence:** OGL v3.

---

## Tier 2 — an API, shaped with the assistant

More capable, more ways to be silently wrong. Do these second.

### OpenStreetMap via Overpass
Schools, shops, crossings, cycle lanes, anything mapped.

- **Gives you:** what is actually near the stops — trip generators, severance,
  the cycle infrastructure that does or does not exist.
- **How:** POST an Overpass QL query to `https://overpass-api.de/api/interpreter`
  (mirror: `https://overpass.kumi.systems/api/interpreter`).
- **The trap:** **it must be POST.** A GET with the same query returns an HTML
  error page, and `response.json()` then fails with something that looks like a
  parsing bug rather than a method bug. Also: schools are often mapped as areas,
  not points — use `out center;` or you will get no coordinates at all.
- **Be polite:** it is a free service run on donated hardware. Set a real
  `User-Agent`, one query at a time, and cache the result to disk immediately.
- **Licence:** ODbL, © OpenStreetMap contributors. Attribution is required.

### ONS Open Geography — which LSOA is this point in?
Point-in-polygon, done on their server, so you never touch a polygon.

- **Gives you:** the LSOA code for any point in your patch, which unlocks
  IMD and Census.
- **The address — copy this, do not retype it and do not ask for it:**

  ```
  https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Lower_layer_Super_Output_Areas_December_2021_Boundaries_EW_BSC_V4/FeatureServer/0/query
  ```

  with these parameters:

  ```
  geometry=<lon>,<lat>
  geometryType=esriGeometryPoint
  inSR=4326
  spatialRel=esriSpatialRelIntersects
  outFields=LSOA21CD,LSOA21NM
  returnGeometry=false
  f=json
  ```

  Verified working: the point `-1.5491, 53.7965` returns `E01033016`
  (Leeds 111E). Use that as your first test — if you get that answer back,
  your request is correctly formed and you can move on to your own points.
- **Why the emphasis on copying.** That address contains a service
  identifier (`ESMARspQHYMw9BZ9`) that nobody could derive and no assistant
  can remember. Asked for it, an assistant will produce something with the
  right shape and the wrong identifier, delivered with complete confidence.
  This is the single most likely place in the whole atlas to lose an hour,
  and it is in the chapter about not letting that happen.
- **The trap:** longitude comes **first**. Swap them and you get a silent
  `NO MATCH` for every point, or worse, a match somewhere in the North Sea.
- **Licence:** OGL v3, © Crown copyright and database right.

### NaPTAN — the real bus stop register
Every public transport access point in Great Britain. Chapter 1's source.

- **Gives you:** real stop names, locations and codes for your patch.
- **How:** `https://naptan.api.dft.gov.uk/v1/access-nodes?dataFormat=csv&atcoAreaCodes=450`
  — where `450` is the ATCO area code for the region your patch sits in
  (450 is West Yorkshire, the Leeds demonstrator's area).
- **Finding your area code:** `data/external/atco_area_codes.csv` in this
  repository lists all 150 of them, area name against code. Look yours up
  there. Do **not** ask the assistant for it and do not guess: the codes
  look guessable and are not (West Yorkshire is `450`, but York is `329`
  and Bristol is `010`), and the only official source is an XML file that
  is more trouble than it is worth for one number.
- **The trap:** the code must be **three digits**, so keep the leading zero
  on codes such as `010`. The API's error message tells you the format is
  wrong but not which code you wanted, so a mistake here looks like a
  format problem when it is really a lookup problem.
- **Verify it worked:** tens of thousands of stops come back per area.
  Filter to your bounding box and count. If you get **zero**, you almost
  certainly have the wrong area — check the lookup table again before
  changing anything else. Also drop the stops marked inactive.
- **Licence:** OGL v3.

### Propensity to Cycle Tool — cycling potential
DfT-funded model of how much cycling each road segment could carry.

- **Gives you:** where cycling *would* happen under a given scenario,
  against what happens now.
- **How:** `https://media.githubusercontent.com/media/npct/pct-outputs-regional-notR/master/commute/lsoa/west-yorkshire/rnet_full.geojson`
  — swap `west-yorkshire` for the region containing your patch.
- **The trap, and it will catch you:** the regions are **historic counties,
  not cities**, so the name you want is often not the name you expect.
  Bristol is under `avon`. Manchester is `greater-manchester`. Newcastle is
  `north-east`. Hull is `humberside`. There are forty-five in all:

  ```
  avon, bedfordshire, berkshire, buckinghamshire, cambridgeshire, cheshire,
  cornwall-and-isles-of-scilly, cumbria, derbyshire, devon, dorset,
  east-sussex, essex, gloucestershire, greater-manchester, hampshire,
  hereford-and-worcester, hertfordshire, humberside, isle-of-wight, kent,
  lancashire, leicestershire, lincolnshire, liverpool-city-region, london,
  norfolk, north-east, north-yorkshire, northamptonshire, northumberland,
  nottinghamshire, oxfordshire, shropshire, somerset, south-yorkshire,
  staffordshire, suffolk, surrey, wales, warwickshire, west-midlands,
  west-sussex, west-yorkshire, wiltshire
  ```

  A wrong name gives you a 404 rather than a wrong answer, which is the
  kindest way for this to fail.
- **The trap:** it models **2011 Census commuting only**. No shopping, no
  school, no leisure, and the baseline is fifteen years old. It is a scenario
  model, not an observation, and every sentence you write about it needs to say
  so. In some cities its correlation with observed cycling is roughly
  *negative* — a good model can still be the wrong model for your place.
- **Licence:** OGL / CC-BY. See [pct.bike](https://www.pct.bike/).

### open-meteo — historical weather
Hourly weather for any coordinates, back decades. Chapter 7's source.

- **Gives you:** a year of rain and temperature for your patch, as JSON.
- **How:** `https://archive-api.open-meteo.com/v1/archive?latitude=53.80&longitude=-1.55&start_date=2025-01-01&end_date=2025-12-31&hourly=precipitation,temperature_2m`
  — no key, no account. Point the coordinates at the centre of your patch.
- **The trap:** the response is JSON with parallel lists — one list of
  timestamps, one list per variable, matched by position. Turning that into
  a table is a small, precise specification exercise: say the shape you
  want, and check the first and last rows against the website's own charts.
- **Licence:** CC-BY 4.0, attribution required. See
  [open-meteo.com](https://open-meteo.com/).

---

## Tier 3 — real, and out of scope here

Named so you know they exist and know why you are not using them this term.

| Source | Why not |
|---|---|
| OS Open Roads | ~1 GB GeoPackage, needs GDAL. The right tool for road classification, wrong tool for a 3-hour studio. |
| Cycle infrastructure Level of Service (`osmactive`) | Needs an R toolchain. This is how the Coventry work classified cycle provision — ask if you want to see it. |
| Bus Open Data Service (live/GTFS-RT feeds) | Needs an API key and a feed parser. This is where real AVL data comes from. |
| EPC register | Bulk download sits behind a sign-in. |
| OS Open UPRN / Code-Point Open | Useful for address-level work, needs projection handling. |

---

## What to record for every source you use

This is the professional habit the atlas exists to build. Nobody is marking
it — which is exactly why doing it anyway is the habit worth having:

1. **Where it came from** — the URL, and the date you pulled it.
2. **The licence line** — OGL v3, ODbL, and CC-BY all require attribution.
3. **Row counts** — national, after your patch filter, after every merge.
4. **The approximation you accepted** — nearest-centroid instead of true
   containment, a rectangle instead of a boundary, 2011 codes joined to 2021
   codes. Every one of these is defensible. None of them is defensible
   silently.

---

## A word about real places

Everything in your atlas is real: real casualties, real deprivation, real
streets where real people live — quite possibly including you. Two
disciplines follow. State what each dataset is and when you fetched it, so a
figure can never be mistaken for something it is not. And keep description
separate from judgement: "this area is in England's most deprived decile" is
data; conclusions about the people who live there are not yours to draw. Write
about every patch with the respect you would want for your own street.
