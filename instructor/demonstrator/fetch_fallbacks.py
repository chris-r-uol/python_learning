"""
Instructor tool: fetch every atlas source live, cut it to the Leeds
demonstrator patch, and write the cached fallback files that ship in
project/data/external/.

    python instructor/demonstrator/fetch_fallbacks.py

Run before each delivery. STATS19 is fetched by the student-facing worked
example (project/starter/fetch_external.py) and is not repeated here.

Every file this writes is recorded, with source, date, licence, and row
counts, in project/data/external/SOURCES.md - the same provenance habit the
course asks of students, applied to our own data.
"""

import datetime
import json
import os

import pandas as pd
import requests

# The demonstrator patch - keep identical to the default in
# project/starter/atlas.py so the demonstrator and the starter agree.
PLACE_NAME = "Leeds city centre"
BBOX = (53.75, -1.62, 53.83, -1.49)          # south, west, north, east
S, W, N, E = BBOX

HERE = os.path.dirname(os.path.abspath(__file__))
EXTERNAL = os.path.join(HERE, "..", "..", "project", "data", "external")

HEADERS = {"User-Agent": "python-learning-course/1.0 (teaching; instructor prefetch)"}

TODAY = datetime.date.today().isoformat()
manifest = []


def record(filename, source, licence, note):
    manifest.append((filename, source, licence, note))
    print("  -> {0}   {1}".format(filename, note))
    print()


def in_bbox(lon, lat):
    return W <= lon <= E and S <= lat <= N


# ---------------------------------------------------------------------------

def fetch_naptan():
    """Chapter 1: bus stops. NaPTAN, ATCO area 450 (West Yorkshire)."""
    print("NaPTAN (area 450)")
    url = "https://naptan.api.dft.gov.uk/v1/access-nodes?dataFormat=csv&atcoAreaCodes=450"
    stops = pd.read_csv(url, low_memory=False)
    print("  West Yorkshire stops downloaded  {0:>7}".format(len(stops)))

    stops = stops[stops["Status"] == "active"]
    print("  active                           {0:>7}".format(len(stops)))

    stops = stops[stops["Latitude"].between(S, N) & stops["Longitude"].between(W, E)]
    print("  inside the patch                 {0:>7}".format(len(stops)))

    keep = ["ATCOCode", "CommonName", "LocalityName", "StopType",
            "Longitude", "Latitude"]
    out = os.path.join(EXTERNAL, "naptan_stops.csv")
    stops[keep].to_csv(out, index=False)
    record("naptan_stops.csv",
           "NaPTAN API, atcoAreaCodes=450 (West Yorkshire)",
           "OGL v3, (c) Crown copyright",
           "{0} active stops in the patch".format(len(stops)))


def fetch_imd():
    """Chapter 3: deprivation. IMD 2019 File 7, cut to the Leeds district."""
    print("IMD 2019 (File 7)")
    url = ("https://assets.publishing.service.gov.uk/media/5dc407b440f0b6379a7acc8d/"
           "File_7_-_All_IoD2019_Scores__Ranks__Deciles_and_Population_Denominators_3.csv")
    imd = pd.read_csv(url)
    print("  England LSOAs downloaded         {0:>7}".format(len(imd)))

    lad_col = "Local Authority District code (2019)"
    leeds = imd[imd[lad_col] == "E08000035"]
    print("  Leeds district LSOAs             {0:>7}".format(len(leeds)))

    keep = [c for c in imd.columns if c.startswith(("LSOA", "Local Authority"))
            or "Index of Multiple Deprivation" in c]
    out = os.path.join(EXTERNAL, "imd2019_leeds.csv")
    leeds[keep].to_csv(out, index=False)
    record("imd2019_leeds.csv",
           "MHCLG, English Indices of Deprivation 2019, File 7",
           "OGL v3",
           "{0} LSOAs (Leeds district; 2011 LSOA codes)".format(len(leeds)))


def fetch_census():
    """Chapter 4: car availability. Census 2021 TS045 via Nomis, Leeds LSOAs."""
    print("Census 2021 TS045 via Nomis")
    url = ("https://www.nomisweb.co.uk/api/v01/dataset/NM_2063_1.data.csv"
           "?date=latest&geography=E08000035TYPE151&measures=20100")
    census = pd.read_csv(url)
    print("  rows downloaded (Leeds LSOAs)    {0:>7}".format(len(census)))

    keep = ["GEOGRAPHY_CODE", "GEOGRAPHY_NAME", "C2021_CARS_5_NAME", "OBS_VALUE"]
    out = os.path.join(EXTERNAL, "census_car_availability.csv")
    census[keep].to_csv(out, index=False)
    record("census_car_availability.csv",
           "ONS Census 2021 table TS045 via the Nomis API (dataset NM_2063_1)",
           "OGL v3",
           "{0} rows; 2021 LSOA codes; households by cars available".format(len(census)))


def fetch_pct():
    """Chapter 5: cycling potential. PCT West Yorkshire route network."""
    print("PCT route network (west-yorkshire)")
    url = ("https://media.githubusercontent.com/media/npct/pct-outputs-regional-notR/"
           "master/commute/lsoa/west-yorkshire/rnet_full.geojson")
    response = requests.get(url, headers=HEADERS, timeout=300)
    response.raise_for_status()
    network = response.json()
    print("  West Yorkshire segments          {0:>7}".format(len(network["features"])))

    fields = ["bicycle", "govtarget_slc", "dutch_slc"]
    kept = []
    for feature in network["features"]:
        coords = feature["geometry"]["coordinates"]
        if feature["geometry"]["type"] == "LineString":
            lines = [coords]
        else:
            lines = coords
        if any(in_bbox(lon, lat) for line in lines for lon, lat in line):
            kept.append({
                "type": "Feature",
                "geometry": {
                    "type": feature["geometry"]["type"],
                    "coordinates": [[[round(lon, 5), round(lat, 5)]
                                     for lon, lat in line] for line in lines]
                    if feature["geometry"]["type"] != "LineString"
                    else [[round(lon, 5), round(lat, 5)] for lon, lat in coords],
                },
                "properties": {f: feature["properties"].get(f) for f in fields},
            })
    print("  segments touching the patch      {0:>7}".format(len(kept)))

    out = os.path.join(EXTERNAL, "pct_rnet.geojson")
    with open(out, "w") as handle:
        json.dump({"type": "FeatureCollection",
                   "place": PLACE_NAME,
                   "source": "PCT (pct.bike), commute rnet, west-yorkshire",
                   "features": kept}, handle)
    record("pct_rnet.geojson",
           "Propensity to Cycle Tool, commute route network, west-yorkshire",
           "OGL / CC-BY (see pct.bike)",
           "{0} segments touching the patch".format(len(kept)))


def fetch_osm():
    """Chapter 6: what is there. Overpass, six amenity types, POST only."""
    print("OpenStreetMap via Overpass")
    query = """
[out:json][timeout:120];
(
  nwr["amenity"="school"]({s},{w},{n},{e});
  nwr["amenity"="college"]({s},{w},{n},{e});
  nwr["amenity"="university"]({s},{w},{n},{e});
  nwr["amenity"="hospital"]({s},{w},{n},{e});
  nwr["amenity"="pharmacy"]({s},{w},{n},{e});
  nwr["shop"="supermarket"]({s},{w},{n},{e});
);
out center tags;
""".format(s=S, w=W, n=N, e=E)
    response = requests.post("https://overpass-api.de/api/interpreter",
                             data={"data": query}, headers=HEADERS, timeout=180)
    response.raise_for_status()
    elements = response.json()["elements"]
    print("  elements returned                {0:>7}".format(len(elements)))

    features = []
    for element in elements:
        if "lat" in element:
            lon, lat = element["lon"], element["lat"]
        elif "center" in element:
            lon, lat = element["center"]["lon"], element["center"]["lat"]
        else:
            continue
        tags = element.get("tags", {})
        category = tags.get("amenity") or ("supermarket" if tags.get("shop") == "supermarket" else None)
        if category is None:
            continue
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point",
                         "coordinates": [round(lon, 6), round(lat, 6)]},
            "properties": {"category": category, "name": tags.get("name", "")},
        })
    print("  usable point features            {0:>7}".format(len(features)))

    out = os.path.join(EXTERNAL, "osm_amenities.geojson")
    with open(out, "w") as handle:
        json.dump({"type": "FeatureCollection",
                   "place": PLACE_NAME,
                   "source": "OpenStreetMap via Overpass API",
                   "features": features}, handle)
    record("osm_amenities.geojson",
           "OpenStreetMap contributors, via the Overpass API",
           "ODbL - attribution required",
           "{0} amenities in six categories".format(len(features)))


def fetch_weather():
    """Chapter 7: a year of weather. open-meteo archive, 2025, hourly."""
    print("open-meteo archive (2025)")
    url = ("https://archive-api.open-meteo.com/v1/archive"
           "?latitude={0}&longitude={1}"
           "&start_date=2025-01-01&end_date=2025-12-31"
           "&hourly=precipitation,temperature_2m&format=csv").format(
               round((S + N) / 2, 3), round((W + E) / 2, 3))
    response = requests.get(url, headers=HEADERS, timeout=120)
    response.raise_for_status()
    out = os.path.join(EXTERNAL, "weather_2025.csv")
    with open(out, "w") as handle:
        handle.write(response.text)
    rows = response.text.count("\n")
    print("  lines written                    {0:>7}".format(rows))
    record("weather_2025.csv",
           "open-meteo.com historical archive, hourly, centre of the patch",
           "CC-BY 4.0 - attribution required",
           "hourly precipitation and temperature for 2025 (~{0} lines)".format(rows))


def write_manifest():
    lines = [
        "# Cached fallback data - sources",
        "",
        "Fetched by `instructor/demonstrator/fetch_fallbacks.py` on **{0}**,".format(TODAY),
        "cut to the demonstrator patch ({0}, bounding box".format(PLACE_NAME),
        "S {0}, W {1}, N {2}, E {3}).".format(S, W, N, E),
        "",
        "These files exist so that a dead API never blocks a studio session. If",
        "you use one instead of fetching live, say so in your own provenance",
        "record, with the date above.",
        "",
        "`casualties.geojson` (STATS19) is produced by the student-facing worked",
        "example, `project/starter/fetch_external.py`, run on the same patch.",
        "",
        "| File | Source | Licence | Contents |",
        "|---|---|---|---|",
    ]
    lines.append("| casualties.geojson | DfT STATS19 collision + casualty files, 2022-23 "
                 "| OGL v3 | active-mode casualties in the patch |")
    for filename, source, licence, note in manifest:
        lines.append("| {0} | {1} | {2} | {3} |".format(filename, source, licence, note))
    lines.append("")
    with open(os.path.join(EXTERNAL, "SOURCES.md"), "w") as handle:
        handle.write("\n".join(lines))
    print("Manifest written to SOURCES.md")


def main():
    os.makedirs(EXTERNAL, exist_ok=True)
    fetch_naptan()
    fetch_imd()
    fetch_census()
    fetch_pct()
    fetch_osm()
    fetch_weather()
    write_manifest()
    print()
    print("All fallbacks written to {0}".format(os.path.relpath(EXTERNAL, HERE)))


if __name__ == "__main__":
    main()
