"""
The Leeds demonstrator atlas - all seven chapters, built on the cached
fallback files in project/data/external/.

    python instructor/demonstrator/leeds_atlas.py

Two jobs. In the week 4 session, chapters 1 and 2 are built live with the
assistant; this file is the safety net if the live build goes sideways, and
the worked reference for every later chapter. It reads the cached fallbacks
rather than fetching, so it runs offline - the fetching pattern is
demonstrated separately by project/starter/fetch_external.py and rehearsed
in instructor/demonstrator/fetch_fallbacks.py.

Output: instructor/demonstrator/output/ - seven figures and index.html.
"""

import csv
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PLACE_NAME = "Leeds city centre"
BBOX = (53.75, -1.62, 53.83, -1.49)

HERE = os.path.dirname(os.path.abspath(__file__))
EXTERNAL = os.path.join(HERE, "..", "..", "project", "data", "external")
OUTPUT = os.path.join(HERE, "output")

BLUE = "#2a78d6"
ORANGE = "#eb6834"
GREY = "#8a8a8a"


def styled_axes(figsize=(9, 5)):
    figure, axes = plt.subplots(figsize=figsize)
    axes.grid(axis="y", alpha=0.25)
    axes.spines["top"].set_visible(False)
    axes.spines["right"].set_visible(False)
    return figure, axes


def save(figure, name):
    path = os.path.join(OUTPUT, name)
    figure.tight_layout()
    figure.savefig(path, dpi=150)
    plt.close(figure)
    return name


# ---------------------------------------------------------------------------

def chapter_1_stops():
    stops = pd.read_csv(os.path.join(EXTERNAL, "naptan_stops.csv"))

    figure, axes = plt.subplots(figsize=(8, 8))
    axes.scatter(stops["Longitude"], stops["Latitude"],
                 s=8, color=BLUE, alpha=0.55, linewidths=0)
    # One degree of longitude is shorter than one of latitude at 53.8 N;
    # without this correction the map is squashed east-west.
    axes.set_aspect(1.0 / np.cos(np.radians(53.79)))
    axes.set_xlabel("Longitude (degrees)")
    axes.set_ylabel("Latitude (degrees)")
    axes.set_title("{0} active public transport stops\n{1}, NaPTAN".format(
        len(stops), PLACE_NAME))
    axes.spines["top"].set_visible(False)
    axes.spines["right"].set_visible(False)
    name = save(figure, "chapter1_stops.png")

    busiest = stops.groupby("LocalityName").size().sort_values(ascending=False)
    text = (
        "The patch contains {0} active public transport stops. "
        "The densest locality is {1}, with {2} stops - the city-centre "
        "interchange effect is visible before any service data is added. "
        "Stop positions alone already sketch the road network."
    ).format(len(stops), busiest.index[0], busiest.iloc[0])
    return "The patch and its stops", name, text


def chapter_2_safety():
    with open(os.path.join(EXTERNAL, "casualties.geojson")) as handle:
        collection = json.load(handle)
    casualties = pd.DataFrame([f["properties"] for f in collection["features"]])

    counts = casualties.groupby(["severity", "mode"]).size().unstack(fill_value=0)
    order = ["slight", "serious", "fatal"]
    counts = counts.reindex(order)

    figure, axes = styled_axes()
    x = np.arange(len(order))
    width = 0.38
    axes.bar(x - width / 2, counts["pedestrian"], width, color=BLUE, label="Pedestrian")
    axes.bar(x + width / 2, counts["cyclist"], width, color=ORANGE, label="Cyclist")
    axes.set_xticks(x)
    axes.set_xticklabels([s.capitalize() for s in order])
    axes.set_xlabel("Casualty severity")
    axes.set_ylabel("Casualties (people, 2022-23)")
    total = len(casualties)
    fatal = int((casualties["severity"] == "fatal").sum())
    axes.set_title("{0} people walking or cycling were hurt in two years\n"
                   "{1}, STATS19 2022-23".format(total, PLACE_NAME))
    axes.legend(frameon=False)
    name = save(figure, "chapter2_safety.png")

    serious = int((casualties["severity"] == "serious").sum())
    pedestrians = int((casualties["mode"] == "pedestrian").sum())
    text = (
        "STATS19 records {0} pedestrian and cyclist casualties in the patch "
        "across 2022-23, of whom {1} were seriously hurt and {2} killed. "
        "Pedestrians account for {3} of the {0}. Every one of these points "
        "has a location, so the natural next question - where, exactly - is "
        "answerable with the distance technique from the studio."
    ).format(total, serious, fatal, pedestrians)
    return "Road safety", name, text


def chapter_3_deprivation():
    imd = pd.read_csv(os.path.join(EXTERNAL, "imd2019_leeds.csv"))
    decile_col = [c for c in imd.columns if "Decile" in c][0]

    deciles = imd.groupby(decile_col).size().reindex(range(1, 11), fill_value=0)

    figure, axes = styled_axes()
    colors = [ORANGE if d == 1 else BLUE for d in deciles.index]
    axes.bar(deciles.index, deciles.values, color=colors)
    axes.set_xticks(range(1, 11))
    axes.set_xlabel("IMD 2019 decile (1 = most deprived tenth of England)")
    axes.set_ylabel("Neighbourhoods (LSOAs)")
    most = int(deciles.loc[1])
    share = 100.0 * most / len(imd)
    axes.set_title("{0:.0f}% of Leeds neighbourhoods are in England's most "
                   "deprived decile\nLeeds district, IMD 2019".format(share))
    name = save(figure, "chapter3_deprivation.png")

    least = int(deciles.loc[10])
    text = (
        "Across the Leeds district's {0} neighbourhoods, {1} ({2:.0f}%) fall "
        "in England's most deprived decile, against {3} in the least deprived "
        "- the city holds both extremes at once. This chapter is drawn at "
        "district level; cutting it to the patch needs the ONS point-in-LSOA "
        "lookup, which is a worthwhile refinement for a student atlas. Note "
        "the codes: IMD 2019 uses 2011 LSOA boundaries."
    ).format(len(imd), most, share, least)
    return "Deprivation", name, text


def chapter_4_car_free():
    census = pd.read_csv(os.path.join(EXTERNAL, "census_car_availability.csv"))

    categories = ["No cars or vans in household", "1 car or van in household",
                  "2 cars or vans in household", "3 or more cars or vans in household"]
    totals = census[census["C2021_CARS_5_NAME"].isin(categories)]
    by_category = totals.groupby("C2021_CARS_5_NAME")["OBS_VALUE"].sum().reindex(categories)
    all_households = int(by_category.sum())
    shares = 100.0 * by_category / all_households

    figure, axes = styled_axes()
    labels = ["No car", "1 car", "2 cars", "3 or more"]
    colors = [ORANGE, BLUE, BLUE, BLUE]
    axes.bar(labels, shares.values, color=colors)
    for i, value in enumerate(shares.values):
        axes.annotate("{0:.0f}%".format(value), (i, value),
                      ha="center", va="bottom", fontsize=10)
    axes.set_xlabel("Cars or vans available to the household")
    axes.set_ylabel("Share of households (%)")
    axes.set_title("{0:.0f}% of Leeds households have no car\n"
                   "Leeds district, Census 2021 (TS045)".format(shares.iloc[0]))
    name = save(figure, "chapter4_car_free.png")

    no_car = int(by_category.iloc[0])

    # The LSOA where car-free living is most common - a groupby, a join of
    # two slices, and a division: the studio's key-join pattern in miniature.
    per_area = census.pivot_table(index="GEOGRAPHY_NAME",
                                  columns="C2021_CARS_5_NAME",
                                  values="OBS_VALUE", aggfunc="sum")
    per_area["no_car_share"] = (per_area["No cars or vans in household"]
                                / per_area["Total: All households"])
    top = per_area["no_car_share"].sort_values(ascending=False)
    text = (
        "Of the district's {0:,} households, {1:,} ({2:.0f}%) have no car or "
        "van - for them, walking, cycling, and public transport are the whole "
        "transport system. The neighbourhood where car-free households are "
        "most common is {3}, at {4:.0f}%. Census codes here are 2021 LSOAs; "
        "joining them to the 2019 deprivation file is the vintage trap from "
        "the catalogue."
    ).format(all_households, no_car, shares.iloc[0], top.index[0], 100 * top.iloc[0])
    return "Who has no car", name, text


def chapter_5_cycling_potential():
    with open(os.path.join(EXTERNAL, "pct_rnet.geojson")) as handle:
        network = json.load(handle)
    segments = pd.DataFrame([f["properties"] for f in network["features"]])

    scenarios = {"bicycle": "Census 2011\nbaseline",
                 "govtarget_slc": "Government\ntarget",
                 "dutch_slc": "Go Dutch"}
    sums = [segments[k].sum() for k in scenarios]

    figure, axes = styled_axes()
    axes.bar(list(scenarios.values()), sums, color=[GREY, BLUE, ORANGE])
    axes.set_ylabel("Modelled commuter cyclists (segment-sum, indicative)")
    multiple = sums[2] / sums[0]
    axes.set_title("The Go Dutch scenario is {0:.1f}x the observed baseline\n"
                   "{1}, PCT commute model".format(multiple, PLACE_NAME))
    name = save(figure, "chapter5_cycling.png")

    text = (
        "Across the {0} network segments touching the patch, the PCT's Go "
        "Dutch scenario models roughly {1:.1f} times the cycling of its 2011 "
        "observed baseline. Two honesty notes belong in any use of this "
        "chart: the sums count each cyclist on every segment they cross, so "
        "the scale is indicative rather than a count of people; and the model "
        "covers 2011 commuting only - no leisure, shopping, or study trips, "
        "and a baseline now well over a decade old."
    ).format(len(segments), multiple)
    return "Cycling potential", name, text


def chapter_6_what_is_there():
    with open(os.path.join(EXTERNAL, "osm_amenities.geojson")) as handle:
        collection = json.load(handle)
    amenities = pd.DataFrame([f["properties"] for f in collection["features"]])

    counts = amenities.groupby("category").size().sort_values()

    figure, axes = styled_axes(figsize=(9, 4.5))
    axes.barh(counts.index.str.capitalize(), counts.values, color=BLUE)
    axes.grid(axis="x", alpha=0.25)
    axes.grid(axis="y", alpha=0)
    axes.set_xlabel("Mapped locations in the patch")
    axes.set_title("What the stops serve: {0} everyday destinations\n"
                   "{1}, OpenStreetMap".format(len(amenities), PLACE_NAME))
    name = save(figure, "chapter6_amenities.png")

    schools = int(counts.get("school", 0))
    pharmacies = int(counts.get("pharmacy", 0))
    supermarkets = int(counts.get("supermarket", 0))
    text = (
        "OpenStreetMap places {0} everyday destinations in the patch across "
        "six categories, including {1} schools, {2} pharmacies, and {3} "
        "supermarkets. These are the places transport exists to reach, which "
        "makes this layer the natural companion to chapter 1: a stop matters "
        "in proportion to what is near it. Coverage is community-mapped, so "
        "treat absence as unmapped, never as proven absent."
    ).format(len(amenities), schools, pharmacies, supermarkets)
    return "What is there", name, text


def chapter_7_weather():
    weather = pd.read_csv(os.path.join(EXTERNAL, "weather_2025.csv"), skiprows=3)
    weather.columns = ["time", "rain_mm", "temp_c"]
    weather["month"] = pd.to_datetime(weather["time"]).dt.month

    rain = weather.groupby("month")["rain_mm"].sum()
    temperature = weather.groupby("month")["temp_c"].mean()
    months = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]

    figure, (top, bottom) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    top.bar(rain.index, rain.values, color=BLUE)
    top.set_ylabel("Rainfall (mm/month)")
    wettest = int(rain.idxmax())
    top.set_title("A year outdoors in Leeds: {0:.0f} mm of rain, "
                  "wettest in {1}\n{2}, open-meteo 2025".format(
                      rain.sum(),
                      ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November",
                       "December"][wettest - 1],
                      PLACE_NAME))
    bottom.plot(temperature.index, temperature.values, color=ORANGE, linewidth=2)
    bottom.set_ylabel("Mean temperature (deg C)")
    bottom.set_xlabel("Month")
    bottom.set_xticks(range(1, 13))
    bottom.set_xticklabels(months)
    for axes in (top, bottom):
        axes.grid(axis="y", alpha=0.25)
        axes.spines["top"].set_visible(False)
        axes.spines["right"].set_visible(False)
    name = save(figure, "chapter7_weather.png")

    rainy_hours = int((weather["rain_mm"] > 0.2).sum())
    share = 100.0 * rainy_hours / len(weather)
    text = (
        "In 2025 the patch received {0:.0f} mm of rain, and rain heavier than "
        "drizzle fell in {1:,} hours - {2:.0f}% of the year. Monthly mean "
        "temperatures ran from {3:.1f} to {4:.1f} deg C. For anyone walking, "
        "cycling, or waiting at one of chapter 1's stops, this is the "
        "operating environment; joining it to demand or reliability data is a "
        "natural stretch chapter."
    ).format(rain.sum(), rainy_hours, share, temperature.min(), temperature.max())
    return "A year of weather", name, text


# ---------------------------------------------------------------------------

def build_report(chapters):
    parts = [
        "<!DOCTYPE html><html><head><meta charset='utf-8'>",
        "<title>The {0} transport atlas</title>".format(PLACE_NAME),
        "<style>body{font-family:Georgia,serif;max-width:860px;margin:2em auto;"
        "padding:0 1em;color:#222;line-height:1.55}img{max-width:100%;border:1px "
        "solid #ddd}h1{font-size:1.7em}h2{margin-top:2.2em}p.meta{color:#666;"
        "font-size:0.9em}</style></head><body>",
        "<h1>The {0} transport atlas</h1>".format(PLACE_NAME),
        "<p class='meta'>The instructor's demonstrator for the Your Patch "
        "project. Built entirely from the cached open-data fallbacks in "
        "<code>project/data/external/</code> &mdash; sources, dates, and "
        "licences in <code>SOURCES.md</code> there. Contains OS, DfT, ONS, "
        "MHCLG and open-meteo data (OGL v3 / CC-BY) and OpenStreetMap data "
        "(ODbL, &copy; OpenStreetMap contributors).</p>",
    ]
    for number, (title, figure_name, text) in enumerate(chapters, start=1):
        parts.append("<h2>Chapter {0} &mdash; {1}</h2>".format(number, title))
        parts.append("<img src='{0}' alt='{1}'>".format(figure_name, title))
        parts.append("<p>{0}</p>".format(text))
    parts.append("</body></html>")

    path = os.path.join(OUTPUT, "index.html")
    with open(path, "w") as handle:
        handle.write("\n".join(parts))
    return path


def main():
    os.makedirs(OUTPUT, exist_ok=True)
    chapters = [
        chapter_1_stops(),
        chapter_2_safety(),
        chapter_3_deprivation(),
        chapter_4_car_free(),
        chapter_5_cycling_potential(),
        chapter_6_what_is_there(),
        chapter_7_weather(),
    ]
    report = build_report(chapters)
    print("Atlas of {0}: {1} chapters".format(PLACE_NAME, len(chapters)))
    for number, (title, figure_name, _) in enumerate(chapters, start=1):
        print("  {0}. {1:<24} {2}".format(number, title, figure_name))
    print("Report:", os.path.relpath(report, HERE))


if __name__ == "__main__":
    main()
