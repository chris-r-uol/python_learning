"""
Chapter 7 — A year of weather.

Question: what weather does all of this happen in?

A full year of hourly rainfall and temperature at the centre of the patch,
from the open-meteo historical archive. Free, no key, and the only source in
the atlas that returns its answer as parallel arrays rather than as rows.

This chapter matters because every mode in the atlas except the car is
exposed to it.
"""

import numpy as np

import atlaslib as al

YEAR = 2025
ARCHIVE = (
    "https://archive-api.open-meteo.com/v1/archive"
    "?latitude={lat:.4f}&longitude={lon:.4f}"
    "&start_date={year}-01-01&end_date={year}-12-31"
    "&hourly=precipitation,temperature_2m&timezone=GMT"
)

# Met Office 1991-2020 averaging period, for the area around Leeds. This is
# the anchor: a published figure from outside anything computed here.
LONG_RUN_RAINFALL_MM = 660.0

WET_MM = 0.2                      # an hour with more than this is "wet"
COMMUTE_HOURS = list(range(7, 10)) + list(range(16, 19))

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

LEAD = """
Everyone in chapters 1, 4, 5 and 6 is outside. Waiting at a stop, walking to
one, cycling a corridor — every mode in this atlas except the car happens in
the weather.

open-meteo publishes hourly reanalysis data for any coordinate on earth, free
and without a key. A year at one point is about 8,760 hours of rainfall and
temperature, which is enough to answer a question no monthly average can:
**how often is it actually raining when people are travelling?**
""".strip()


def _parse_archive(text):
    """Parse either the JSON API response or the cached CSV.

    The API returns parallel arrays: hourly.time[i] belongs with
    hourly.precipitation[i]. There is no row anywhere in the response. Reading
    it as records is the mistake this parser exists to prevent.
    """
    stripped = text.lstrip()
    if stripped.startswith("{"):
        import json
        data = json.loads(text)
        hourly = data["hourly"]
        times = hourly["time"]
        rain = [al.to_float(v, 0.0) for v in hourly["precipitation"]]
        temp = [al.to_float(v, float("nan")) for v in hourly["temperature_2m"]]
        return {"time": times, "rain": rain, "temp": temp}, len(times)

    # The cached CSV carries a metadata block, a blank line, then the hourly
    # header. Splitting on the blank line is the whole of the difference.
    blocks = text.replace("\r\n", "\n").split("\n\n")
    hourly_block = blocks[-1] if len(blocks) > 1 else text
    rows, _ = al.parse_csv(hourly_block.strip())
    times, rain, temp = [], [], []
    for row in rows:
        time_value = row.get("time")
        if not time_value:
            continue
        times.append(time_value)
        rain_key = next((k for k in row if k.startswith("precipitation")), None)
        temp_key = next((k for k in row if k.startswith("temperature")), None)
        rain.append(al.to_float(row.get(rain_key), 0.0))
        temp.append(al.to_float(row.get(temp_key), float("nan")))
    return {"time": times, "rain": rain, "temp": temp}, len(times)


def build(ctx):
    chapter = al.Chapter(
        number=7,
        slug="chapter-07",
        title="A year of weather",
        question="What weather does all of this happen in?",
        lead=LEAD,
    )

    lon, lat = ctx.centre
    data = ctx.fetch(
        key="open_meteo",
        name="open-meteo historical archive, hourly, {0}".format(YEAR),
        url=ARCHIVE.format(lat=lat, lon=lon, year=YEAR),
        licence="CC-BY 4.0 — attribution required",
        cache_file="weather_2025.csv",
        parse=_parse_archive,
    )

    times = np.array(data["time"])
    rain = np.array(data["rain"], dtype=float)
    temp = np.array(data["temp"], dtype=float)
    ctx.counted(chapter, "Hourly observations returned", len(times), len(times))

    if len(times) == 0:
        raise SystemExit("Chapter 7: no observations returned.")

    # The arrays must stay in step. Reading them as records would not fail
    # here; it would quietly pair the wrong rain with the wrong hour.
    aligned = len(times) == len(rain) == len(temp)

    months = np.array([int(t[5:7]) for t in times])
    hours = np.array([int(t[11:13]) for t in times])

    monthly_rain = np.array([rain[months == m].sum() for m in range(1, 13)])
    monthly_temp = np.array([np.nanmean(temp[months == m]) for m in range(1, 13)])
    annual_rain = float(rain.sum())

    wet = rain > WET_MM
    wet_hours = int(wet.sum())
    wet_share = 100.0 * wet_hours / len(rain)

    commute_mask = np.isin(hours, COMMUTE_HOURS)
    commute_wet = int((wet & commute_mask).sum())
    commute_total = int(commute_mask.sum())
    commute_wet_share = 100.0 * commute_wet / commute_total
    ctx.counted(chapter, "Commuting hours (07–09, 16–18) that were wet",
                commute_total, commute_wet)

    by_hour = np.array([100.0 * wet[hours == h].mean() for h in range(24)])

    chapter.numbers = {
        "hours": len(times),
        "annual_rain": annual_rain,
        "long_run": LONG_RUN_RAINFALL_MM,
        "wet_share": wet_share,
        "commute_wet_share": commute_wet_share,
        "mean_temp": float(np.nanmean(temp)),
        "wettest_month": MONTHS[int(monthly_rain.argmax())],
        "driest_month": MONTHS[int(monthly_rain.argmin())],
    }

    # -- figures -----------------------------------------------------------

    figure, ax = al.axes(figsize=(9.0, 4.8))
    bars = ax.bar(MONTHS, monthly_rain, color=al.BLUE, width=0.66,
                  label="Rainfall (mm)")
    ax.bar_label(bars, fmt="%.0f", fontsize=8, padding=2)
    ax.set_ylabel("Rainfall (mm per month)", color=al.BLUE)
    ax.set_xlabel("Month of {0}".format(YEAR))
    ax.set_ylim(0, monthly_rain.max() * 1.25)
    twin = ax.twinx()
    twin.plot(MONTHS, monthly_temp, color=al.ORANGE, linewidth=2.4,
              marker="o", markersize=5, label="Mean temperature (°C)")
    twin.set_ylabel("Mean temperature (°C)", color=al.ORANGE)
    twin.spines["top"].set_visible(False)
    twin.set_ylim(0, max(monthly_temp) * 1.5)
    ax.set_title("A year of weather at the centre of the patch\n{0}, {1}. "
                 "Total rainfall {2:.0f} mm".format(ctx.place_name, YEAR, annual_rain),
                 fontsize=11)
    lines = [bars, twin.lines[0]]
    ax.legend(lines, ["Rainfall (mm)", "Mean temperature (°C)"],
              frameon=False, fontsize=9, loc="upper left")
    chapter.figures.append(al.Figure(
        al.save(figure, "ch07_year.png"),
        "Monthly rainfall and mean temperature. Two scales on one figure, "
        "which is only acceptable because both axes are labelled and coloured "
        "to match their series.",
        "Bar and line chart of monthly rainfall and temperature",
    ))

    figure, ax = al.axes(figsize=(9.0, 4.4))
    colours = [al.ORANGE if h in COMMUTE_HOURS else al.BLUE for h in range(24)]
    bars = ax.bar(range(24), by_hour, color=colours, width=0.74)
    ax.axhline(wet_share, color=al.INK, linestyle="--", linewidth=1.2)
    ax.annotate("All hours: {0:.1f}%".format(wet_share),
                xy=(0.2, wet_share), xytext=(0.2, wet_share + by_hour.max() * 0.09),
                fontsize=8.5, color=al.INK)
    ax.set_xticks(range(0, 24, 2))
    ax.set_xlabel("Hour of day (GMT)")
    ax.set_ylabel("Hours with rain above {0} mm (% of that hour's days)".format(WET_MM))
    ax.set_ylim(0, by_hour.max() * 1.28)
    ax.set_title("How often it is raining, by time of day\n{0}, {1}. "
                 "Commuting hours in orange".format(ctx.place_name, YEAR),
                 fontsize=11)
    chapter.figures.append(al.Figure(
        al.save(figure, "ch07_hourly.png"),
        "The share of days on which each hour was wet. The flatness is the "
        "finding: rain does not avoid the commute, and it does not target it "
        "either.",
        "Bar chart of the share of wet hours by hour of day",
    ))

    # -- hand-checks -------------------------------------------------------

    ratio = annual_rain / LONG_RUN_RAINFALL_MM
    ctx.check(
        chapter,
        claim="Annual rainfall is credible for this part of England",
        against="Met Office 1991–2020 average near Leeds, about {0:.0f} mm"
                .format(LONG_RUN_RAINFALL_MM),
        anchored=True,
        passed=0.6 <= ratio <= 1.6,
        detail=(
            "{0:.0f} mm in {1}, against a long-run average of about "
            "{2:.0f} mm — **{3:.0f}%** of normal. This is the check that would "
            "catch a units error: the same figure in inches would read about "
            "{4:.0f}, and in metres about {5:.2f}."
            .format(annual_rain, YEAR, LONG_RUN_RAINFALL_MM, 100 * ratio,
                    annual_rain / 25.4, annual_rain / 1000)
        ),
    )

    expected_hours = 8760 + (24 if YEAR % 4 == 0 else 0)
    ctx.check(
        chapter,
        claim="The year is complete and hourly",
        against="{0} hours in a {1}-day year".format(expected_hours, expected_hours // 24),
        anchored=True,
        passed=abs(len(times) - expected_hours) <= 24,
        detail="{0:,} observations returned, against {1:,} hours in {2}."
               .format(len(times), expected_hours, YEAR),
    )

    ctx.check(
        chapter,
        claim="The parallel arrays are still in step",
        against="The lengths of time, precipitation and temperature",
        anchored=False,
        passed=aligned,
        detail=(
            "time {0:,}, precipitation {1:,}, temperature {2:,}. open-meteo "
            "returns arrays, not records: if these ever differed, every hour "
            "after the gap would carry the wrong weather and nothing would "
            "raise an error."
            .format(len(times), len(rain), len(temp))
        ),
    )

    # -- narrative ---------------------------------------------------------

    chapter.sections = [
        ("A response with no rows in it", """
Every other source in this atlas returns records: one row per stop, per
casualty, per neighbourhood. open-meteo does not. It returns **parallel
arrays**:

```json
"hourly": {
  "time":          ["2025-01-01T00:00", "2025-01-01T01:00", ...],
  "precipitation": [2.70,               3.10,               ...],
  "temperature_2m":[9.5,                9.1,                ...]
}
```

The hour at position *i* belongs with the rainfall at position *i*. That
relationship is held by **position alone**. Nothing in the response ties them
together, and nothing checks it.

If one array were shorter than the others — a gap in the record, a truncated
response — everything after the gap would pair the wrong rainfall with the
wrong hour. Every total would still compute. Every figure would still draw.
Hand-check 22 compares the three lengths for exactly this reason.
"""),

        ("The year", """
**{rain:.0f} mm of rain** fell at the centre of the patch in {year}, against a
long-run average of about **{long_run:.0f} mm** — {pct:.0f}% of normal. The
wettest month was **{wettest}**; the driest was **{driest}**. Mean temperature
across the year was **{temp:.1f} °C**.

Monthly totals are the conventional way to show this and they answer the wrong
question for a transport atlas. Nobody travels in a month. The second figure
asks the question that matters to someone waiting at a stop: **how often is it
actually raining at this time of day?**

Across the whole year, **{wet:.1f}% of hours** had more than {threshold} mm of
rain. During commuting hours — 07:00 to 09:00 and 16:00 to 18:00 — the figure
is **{commute:.1f}%**.

Those two numbers being close together is the finding. Rain in this part of
England is close to uniform across the day. It does not spare the commute and
it does not concentrate on it: roughly **one commuting hour in
{one_in:.0f}** is wet, every day, all year.
""".format(rain=annual_rain, year=YEAR, long_run=LONG_RUN_RAINFALL_MM,
           pct=100 * ratio, wettest=chapter.numbers["wettest_month"],
           driest=chapter.numbers["driest_month"],
           temp=chapter.numbers["mean_temp"], wet=wet_share,
           threshold=WET_MM, commute=commute_wet_share,
           one_in=100.0 / commute_wet_share if commute_wet_share else float("nan"))),

        ("Why this belongs in a transport atlas", """
It is easy to treat weather as background. For everyone in chapter 4 without a
car it is not background, it is the condition of every journey.

The number worth carrying out of this chapter is **{commute:.1f}%**. That is
the share of commuting hours in which someone walking to a stop, waiting at
one, or cycling a corridor from chapter 5 is doing it in the rain.

It is also a number that cuts against an easy conclusion. "It rains too much
here to cycle" is a common claim, and {commute:.0f}% of commuting hours is not
a lot of rain. The obstacle in chapter 5 is not the weather.
""".format(commute=commute_wet_share)),
    ]

    chapter.findings = [
        "**{0:.0f} mm of rain** fell in {1}, about {2:.0f}% of the long-run "
        "average, with a mean temperature of {3:.1f} °C."
        .format(annual_rain, YEAR, 100 * ratio, chapter.numbers["mean_temp"]),
        "**{0:.1f}% of all hours were wet**, and **{1:.1f}% of commuting "
        "hours** — rain here is close to uniform across the day."
        .format(wet_share, commute_wet_share),
        "About **one commuting hour in {0:.0f}** is wet, which is a weaker "
        "argument against cycling than it is usually made to be."
        .format(100.0 / commute_wet_share if commute_wet_share else float("nan")),
    ]

    chapter.caveats = [
        "One point, not the patch. The archive is queried at the centre of the "
        "box; rainfall varies across 76 km², though far less than temperature "
        "varies with altitude.",
        "Reanalysis, not a rain gauge. open-meteo interpolates a model onto a "
        "grid. It is very good and it is not a measurement at that spot.",
        "One year is not a climate. {0} may have been unusual; the comparison "
        "with the long-run average is the only thing here that guards against "
        "that.".format(YEAR),
        "Wet is defined as more than {0} mm in the hour. Move the threshold "
        "and every percentage on this page moves with it.".format(WET_MM),
    ]

    chapter.plan_notes.append(
        """**Prediction P7 said {0} rainfall would be within 20% of the
{1:.0f} mm long-run average. It came in at {2:.0f} mm, which is {3:.0f}% of
normal.**

{4}""".format(YEAR, LONG_RUN_RAINFALL_MM, annual_rain, 100 * ratio,
              "Correct." if 0.8 <= ratio <= 1.2 else
              "Wrong. A single year varies more than I allowed for, which is "
              "the point of comparing against a thirty-year average rather "
              "than against another single year.")
    )

    return chapter
