# UK open data — the catalogue

For the week 5 extension. Every source here is free, needs no account, and was
checked working on **10 August 2026**. If one is unavailable on the day, record
that and use another. Public data services go down from time to time; working
around it is part of the job, not a reason to stop.

`starter/fetch_external.py` is a complete worked fetcher for the first one. Read
it before you build any of the others. The pattern never changes.

---

## The scope rule

You have three weeks of Python. Real geospatial analysis is a term's work on its
own, so this project draws a hard line:

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

- **Gives you:** where people walking and cycling get hurt near your corridor.
- **How:** `https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-collision-2023.csv` (and `-casualty-2023.csv`), joined on `collision_index`.
- **Worked example:** `starter/fetch_external.py`.
- **The trap:** `casualty_type` and `collision_severity` are integer codes whose
  meanings are in a separate guidance document. `0` is a pedestrian, `1` a
  cyclist, severity `1` is *fatal*, not slight. An assistant will guess, and it
  will guess plausibly.
- **Licence:** OGL v3, © Crown copyright.

### Index of Multiple Deprivation 2019
The standard English measure of relative deprivation, by small area (LSOA).

- **Gives you:** the equity argument. Who is bearing the unreliability.
- **How:** [File 7 (all scores, ranks, deciles)](https://assets.publishing.service.gov.uk/media/5dc407b440f0b6379a7acc8d/File_7_-_All_IoD2019_Scores__Ranks__Deciles_and_Population_Denominators_3.csv) — 32,844 rows, one per LSOA.
- **The trap, and it is the instructive one:** IMD 2019 uses **2011** LSOA
  codes. The boundary service in tier 2 returns **2021** codes. Most codes are
  identical between the two vintages, so a merge will appear to work — and
  quietly drop the areas whose codes changed. Count your rows before and
  after. This is the whole course in one join.
- **Second trap:** decile **1 is the most deprived**, not the least. Published
  charts regularly get this backwards; check yours twice.
- **Licence:** OGL v3.

### DfT road traffic counts (AADF)
Annual average daily flows on the road network, by local authority.

- **Gives you:** what the traffic on the corridor's parallel road is doing, and
  whether it is growing.
- **How:** `https://storage.googleapis.com/dft-statistics/road-traffic/downloads/data-gov-uk/local_authority_traffic.csv`
- **The trap:** it is *annual average daily* — you cannot get a peak hour out of
  it, and any argument you build about the peak from this number is invented.
- **Licence:** OGL v3.

### Census 2021 via Nomis
Households, car availability, method of travel to work, by small area.

- **Gives you:** how many people near each stop have no car — i.e. who has no
  alternative when the bus fails.
- **How:** the Nomis API returns CSV directly, e.g.
  `https://www.nomisweb.co.uk/api/v01/dataset/NM_2062_1.data.csv?geography=...&measures=20100`
- **The trap:** finding the right dataset id and geography code is most of the
  work. Ask the assistant, then check the row count and one value against the
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

- **Gives you:** the LSOA code for each stop, which unlocks IMD and Census.
- **How:** a GET to the LSOA boundary FeatureServer with
  `geometry=<lon>,<lat>&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=LSOA21CD,LSOA21NM&returnGeometry=false&f=json`
- **Verified:** stop S001 returns `E01033620` (Birmingham 138A).
- **The trap:** longitude comes **first**. Swap them and you get a silent
  `NO MATCH` for every stop, or worse, a match somewhere in the North Sea.
- **Licence:** OGL v3, © Crown copyright and database right.

### NaPTAN — the real bus stop register
Every public transport access point in Great Britain.

- **Gives you:** real stop names, locations and codes — useful if you want to
  anchor the fictional corridor to real infrastructure.
- **How:** `https://naptan.api.dft.gov.uk/v1/access-nodes?dataFormat=csv&atcoAreaCodes=430`
- **The trap:** the area code must be **three digits**, and the West Midlands
  is **430**, not `043`. Assistants reliably suggest `043`. The API's error
  message tells you the format is wrong, but not which code you wanted. Around
  15,500 stops come back for 430 — filter them to your bounding box.
- **Licence:** OGL v3.

### Propensity to Cycle Tool — cycling potential
DfT-funded model of how much cycling each road segment could carry.

- **Gives you:** the latent-demand argument — where cycling *would* happen under
  a given scenario, against what happens now.
- **How:** `https://media.githubusercontent.com/media/npct/pct-outputs-regional-notR/master/commute/lsoa/west-midlands/rnet_full.geojson`
- **The trap:** it models **2011 Census commuting only**. No shopping, no
  school, no leisure, and the baseline is fifteen years old. It is a scenario
  model, not an observation, and every sentence you write about it needs to say
  so. In Coventry its correlation with observed cycling is roughly *negative* —
  a good model can still be the wrong model for your place.
- **Licence:** OGL / CC-BY. See [pct.bike](https://www.pct.bike/).

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

## What you must record for every source you use

Non-negotiable, and it is marked:

1. **Where it came from** — the URL, and the date you pulled it.
2. **The licence line** — OGL v3 and ODbL both require attribution.
3. **Row counts** — national, after your area filter, after every merge.
4. **The approximation you made** — nearest-centroid instead of true
   containment, bounding box instead of corridor, 2011 codes joined to 2021
   codes. Every one of these is defensible. None of them is defensible silently.

---

## A word about the corridor

The 47 and its eighteen stops are **synthetic**. The geography underneath them
is **real** — the coordinates in `stops.csv` run north through Birmingham, so
real casualties, real deprivation and real schools genuinely do fall along it.

That is what makes the joins work, and it is also a trap. You are practising
on a real place with an invented bus service. **Do not present your findings
as conclusions about the real city's bus network** — not in your brief, not in
your presentation, and not anywhere your work could be forwarded. State what
the data is. That sentence costs you nothing, and it is the difference between
an analyst and a liability.
