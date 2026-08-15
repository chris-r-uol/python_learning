# UK open data — the catalogue

The sources behind the atlas chapters. All are free and need no account. All
were checked on **10 August 2026**.

If a source is down, use the cached copy in `data/external/` and record the
date you used it.

`starter/fetch_external.py` is a finished fetcher for the first source. Read
it before you build the others. The pattern is the same every time.

---

## Read this first

Three chapters need an **area code** before they return anything. NaPTAN
needs an ATCO area code. The PCT needs a region folder name. The Census
needs a local-authority code.

None of these can be guessed, and all of them look as if they can. An
assistant will give you a confident wrong answer.

Do not guess. Do not ask. Each one has a known source:

| You need | Where it comes from |
|---|---|
| ATCO area code (chapter 1) | `data/external/atco_area_codes.csv` in this repository — all 150, by name |
| PCT region name (chapter 5) | the list in the PCT entry below — they are historic counties, so Bristol is `avon` |
| Local-authority code (chapter 4) | the deprivation file itself, which carries district names beside their codes |
| The ONS boundary service address (chapter 3) | copy it from the ONS entry below — do not let an assistant reconstruct it from memory |

The last row matters most. That address is long and contains a service
identifier nobody could work out. Copy it. Do not retype it and do not ask
for it.

The other three chapters need only your bounding box. Once chapter 1 sets
your patch, they work straight away.

This page is a list of the things an assistant will invent. In real work
nobody gives you one. You write it yourself before you start. See
[`agent_guide.md`](agent_guide.md).

## The scope rule

Real geospatial analysis is a term's work. The atlas uses three operations,
and everything on this page can be reached with them:

| Operation | Example |
|---|---|
| **Key join** | LSOA code → deprivation decile |
| **Bounding-box filter** | keep rows whose lat/lon fall in your study area |
| **Distance** | how far is this casualty from the nearest stop |

**Out of scope:** polygons, coordinate-system transforms, GDAL, R, PostGIS.

If your assistant suggests `geopandas`, `shapely`, `pyproj`, `ogr2ogr` or an
`EPSG:27700` conversion, the problem has grown too large. Ask for the
bounding-box or distance version instead.

These tools are not bad. But you cannot check what you cannot read, and a
projection error produces a map that looks correct.

---

## Tier 1 — a CSV at a URL

`pandas.read_csv(url)` and you are done. Start here.

### STATS19 — road casualties
Every reported injury collision in Great Britain, with coordinates.

- **Gives you:** where people walking and cycling get hurt in your patch.
- **How:** `https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-collision-2023.csv` (and `-casualty-2023.csv`), joined on `collision_index`.
- **Worked example:** `starter/fetch_external.py`.
- **The trap:** `casualty_type` and `collision_severity` are numbers. Their
  meanings are in a separate document. `0` is a pedestrian, `1` a cyclist.
  Severity `1` means *fatal*, not slight. An assistant will guess these, and
  the guess will look reasonable.
- **Licence:** OGL v3, © Crown copyright.

### Index of Multiple Deprivation 2019
The standard English measure of relative deprivation, by small area (LSOA).

- **Gives you:** how your patch sits in England's deprivation distribution.
- **How:** [File 7 (all scores, ranks, deciles)](https://assets.publishing.service.gov.uk/media/5dc407b440f0b6379a7acc8d/File_7_-_All_IoD2019_Scores__Ranks__Deciles_and_Population_Denominators_3.csv) — 32,844 rows, one per LSOA.
- **The main trap:** IMD 2019 uses **2011** LSOA codes. The boundary service
  in tier 2 returns **2021** codes. Most codes are the same in both, so the
  join appears to work. It drops the areas whose codes changed. Count your
  rows before and after.
- **Second trap:** decile **1 is the most deprived**, not the least. Many
  published charts get this backwards. Check yours twice.
- **Useful:** every row has both the *name* and the *code* of its local
  authority district. So you can cut this file by name, such as `"Leeds"` or
  `"York"`, without knowing any code. The code in those same rows
  (`E08000035` for Leeds) is the one the Census chapter needs.
- **Licence:** OGL v3.

### DfT road traffic counts (AADF)
Annual average daily flows on the road network, by local authority.

- **Gives you:** what the traffic in your patch's local authority is doing,
  and whether it is growing.
- **How:** `https://storage.googleapis.com/dft-statistics/road-traffic/downloads/data-gov-uk/local_authority_traffic.csv`
- **The trap:** these are *annual average daily* flows. You cannot get a
  peak hour from them.
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
- **The trap:** **you must use POST.** A GET with the same query returns an
  HTML error page. `response.json()` then fails with an error that looks
  like a parsing problem. Also, schools are often mapped as areas rather
  than points. Use `out center;` or you get no coordinates.
- **Be polite.** This is a free service on donated hardware. Set a real
  `User-Agent`, send one query at a time, and save the result to disk at
  once.
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
- **Why copy it.** The address contains a service identifier
  (`ESMARspQHYMw9BZ9`) that nobody can work out. Ask an assistant for it and
  you get the right shape with the wrong identifier.
- **The trap:** longitude comes **first**. Swap them and you get a silent
  `NO MATCH` for every point, or worse, a match somewhere in the North Sea.
- **Licence:** OGL v3, © Crown copyright and database right.

### NaPTAN — the real bus stop register
Every public transport access point in Great Britain. Chapter 1's source.

- **Gives you:** real stop names, locations and codes for your patch.
- **How:** `https://naptan.api.dft.gov.uk/v1/access-nodes?dataFormat=csv&atcoAreaCodes=450`
  — where `450` is the ATCO area code for the region your patch sits in
  (450 is West Yorkshire, the Leeds demonstrator's area).
- **Finding your area code:** `data/external/atco_area_codes.csv` lists all
  150, by name. Look yours up there. Do not guess and do not ask the
  assistant. The codes look guessable and are not: West Yorkshire is `450`,
  York is `329`, Bristol is `010`.
- **The trap:** the code must be **three digits**. Keep the leading zero on
  codes like `010`. The API says the format is wrong but not which code you
  wanted.
- **Check it worked:** tens of thousands of stops come back. Filter to your
  bounding box and count them. If you get **zero**, the area code is wrong.
  Check the lookup table again before changing anything else. Also remove
  the stops marked inactive.
- **Licence:** OGL v3.

### Propensity to Cycle Tool — cycling potential
DfT-funded model of how much cycling each road segment could carry.

- **Gives you:** where cycling *would* happen under a given scenario,
  against what happens now.
- **How:** `https://media.githubusercontent.com/media/npct/pct-outputs-regional-notR/master/commute/lsoa/west-yorkshire/rnet_full.geojson`
  — swap `west-yorkshire` for the region containing your patch.
- **The trap:** the regions are **historic counties, not cities**. Bristol
  is `avon`. Manchester is `greater-manchester`. Newcastle is `north-east`.
  Hull is `humberside`. There are forty-five:

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

  A wrong name gives a 404 rather than a wrong answer.
- **The trap:** it models **2011 Census commuting only**. No shopping, no
  school, no leisure. The baseline is fifteen years old. It is a model of a
  scenario, not a measurement, and your sentences must say so. In some
  cities it does not match observed cycling at all.
- **Licence:** OGL / CC-BY. See [pct.bike](https://www.pct.bike/).

### open-meteo — historical weather
Hourly weather for any coordinates, back decades. Chapter 7's source.

- **Gives you:** a year of rain and temperature for your patch, as JSON.
- **How:** `https://archive-api.open-meteo.com/v1/archive?latitude=53.80&longitude=-1.55&start_date=2025-01-01&end_date=2025-12-31&hourly=precipitation,temperature_2m`
  — no key, no account. Point the coordinates at the centre of your patch.
- **The trap:** the response is JSON containing parallel lists. One list of
  timestamps, one list per variable, matched by position. Describe the table
  shape you want, then check the first and last rows against the website's
  own charts.
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

Record these for every source you use:

1. **Where it came from** — the URL, and the date you pulled it.
2. **The licence line** — OGL v3, ODbL, and CC-BY all require attribution.
3. **Row counts** — national, after your patch filter, after every merge.
4. **The approximation you accepted.** A nearest centroid instead of true
   containment. A rectangle instead of a boundary. 2011 codes joined to 2021
   codes. All of these are acceptable if you say you made them.

---

## Real places

Everything in your atlas is real: real casualties, real deprivation, real
streets where people live.

Two rules follow.

State what each dataset is and when you fetched it, so a figure cannot be
mistaken for something else.

Keep description separate from judgement. "This area is in England's most
deprived tenth" is data. Conclusions about the people who live there are not
yours to draw.
