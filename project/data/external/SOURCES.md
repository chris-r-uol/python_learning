# Cached fallback data - sources

Fetched by `instructor/demonstrator/fetch_fallbacks.py` on **2026-08-10**,
cut to the demonstrator patch (Leeds city centre, bounding box
S 53.75, W -1.62, N 53.83, E -1.49).

These files exist so that a dead API never blocks a studio session. If
you use one instead of fetching live, say so in your own provenance
record, with the date above.

`casualties.geojson` (STATS19) is produced by the student-facing worked
example, `project/starter/fetch_external.py`, run on the same patch.

The last three files were added for the worked atlas in
`project/atlas_demo/`. The two centroid files are separate on purpose: IMD
2019 uses 2011 LSOA codes and Census 2021 uses 2021 codes, and joining across
them returns a smaller table rather than an error.

| File | Source | Licence | Contents |
|---|---|---|---|
| casualties.geojson | DfT STATS19 collision + casualty files, 2022-23 | OGL v3 | active-mode casualties in the patch |
| atco_area_codes.csv | NPTG gazetteer via the NaPTAN API (flattened from XML) | OGL v3 | 150 areas, code against name — the chapter 1 lookup, and **not** patch-specific: it covers all of Great Britain |
| naptan_stops.csv | NaPTAN API, atcoAreaCodes=450 (West Yorkshire) | OGL v3, (c) Crown copyright | 1324 active stops in the patch |
| imd2019_leeds.csv | MHCLG, English Indices of Deprivation 2019, File 7 | OGL v3 | 482 LSOAs (Leeds district; 2011 LSOA codes) |
| census_car_availability.csv | ONS Census 2021 table TS045 via the Nomis API (dataset NM_2063_1) | OGL v3 | 2440 rows; 2021 LSOA codes; households by cars available |
| pct_rnet.geojson | Propensity to Cycle Tool, commute route network, west-yorkshire | OGL / CC-BY (see pct.bike) | 3552 segments touching the patch |
| osm_amenities.geojson | OpenStreetMap contributors, via the Overpass API | ODbL - attribution required | 290 amenities in six categories |
| weather_2025.csv | open-meteo.com historical archive, hourly, centre of the patch | CC-BY 4.0 - attribution required | hourly precipitation and temperature for 2025 (~8764 lines) |
| naptan_rail.csv | NaPTAN API, atcoAreaCodes=910 (national rail) | OGL v3, (c) Crown copyright | 4 rail stations in the patch. Rail is **not** in area 450 |
| lsoa_2011_centroids.geojson | ONS LSOA Dec 2011 population-weighted centroids | OGL v3, (c) Crown copyright and database right | 174 centroids touching the patch. **2011** codes, to match IMD 2019 |
| lsoa_2021_centroids.geojson | ONS LSOA 2021 population-weighted centroids | OGL v3, (c) Crown copyright and database right | 177 centroids touching the patch. **2021** codes, to match Census 2021 |
