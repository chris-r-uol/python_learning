"""
Your first script.

Run it:

    python first_script.py

It reads two days of hourly traffic counts and reports which hours were busy.

The comments explain every step. Read from top to bottom. That is the order
Python reads it in.
"""

# ---------------------------------------------------------------------------
# 1. Settings. The values to change.
# ---------------------------------------------------------------------------

DATA_FILE = "data/site_counts_small.csv"

# An hour is "busy" if more vehicles than this pass in that hour.
# CHANGE THIS NUMBER and run the script again. That is the exercise.
BUSY_THRESHOLD = 900

DIRECTION = "northbound"


# ---------------------------------------------------------------------------
# 2. Read the file.
# ---------------------------------------------------------------------------

# `open` opens the file. `readlines` returns a list, one string per line.
file_handle = open(DATA_FILE)
lines = file_handle.readlines()
file_handle.close()

# `lines` is a list, so items come out by position.
# Positions start at zero. lines[0] is the FIRST line: the header row, which
# names the columns: date,hour,direction,count
header = lines[0]

# lines[1:] means "from position 1 to the end" - everything except the
# header. That is the actual data.
data_lines = lines[1:]

# An f-string: put `f` before the quotes. Anything inside {curly braces} is
# worked out and placed into the text.
print(f"Read {len(data_lines)} rows from {DATA_FILE}")
print(f"Columns are: {header.strip()}")
print()


# ---------------------------------------------------------------------------
# 3. Go through the rows one at a time.
# ---------------------------------------------------------------------------

# Start with an empty list and a total of zero. The loop fills them.
busy_hours = []
total_vehicles = 0

# A `for` loop runs everything indented below once for each line in the
# file. On each pass, `line` holds one line.
for line in data_lines:
    # Each line is one string, like "2026-03-02,8,northbound,1703\n"
    # `strip` removes the newline character at the end.
    # `split` cuts the text at every comma, giving a list of four strings.
    parts = line.strip().split(",")

    # Take the four values out of the list by position, counting from zero.
    # Note the int(). Everything read from a file arrives as TEXT. Values used
    # in arithmetic must be converted to numbers first.
    date = parts[0]               # position 0 - text is fine here
    hour = int(parts[1])          # position 1 - int() makes "8" into 8
    direction = parts[2]          # position 2
    count = int(parts[3])         # position 3 - this gets added up, so it
                                  #              must be a number, not text

    # An `if` runs its indented block only when the condition is true.
    # `continue` means "skip the rest of this pass, start the next line".
    if direction != DIRECTION:
        continue

    # Add this row's count to the running total. The right-hand side is
    # worked out first, then stored under the same name.
    total_vehicles = total_vehicles + count

    # If this hour is busy, add it to the list.
    if count > BUSY_THRESHOLD:
        busy_hours.append((date, hour, count))


# ---------------------------------------------------------------------------
# 4. Report the results.
# ---------------------------------------------------------------------------

print(f"Direction:        {DIRECTION}")
print(f"Busy threshold:   {BUSY_THRESHOLD} vehicles/hour")
print(f"Total vehicles:   {total_vehicles}")
print(f"Busy hours found: {len(busy_hours)}")
print()

if len(busy_hours) == 0:
    print("No hours were above the threshold. Try lowering BUSY_THRESHOLD.")
else:
    # The part after the colon controls the layout. <12 means "pad to 12
    # characters, left-aligned". >5 means "pad to 5, right-aligned". This is
    # what lines the columns up.
    print(f"{'Date':<12} {'Hour':>5} {'Count':>8}")
    for date, hour, count in busy_hours:
        print(f"{date:<12} {hour:>5} {count:>8}")


# ---------------------------------------------------------------------------
# Things to try
# ---------------------------------------------------------------------------
#
# 1. Change BUSY_THRESHOLD to 500 and run the script again. What happens to
#    the table?
#
# 2. Change DIRECTION to "southbound". Does the busiest hour move?
#
# 3. Break it on purpose:
#      - change DATA_FILE to "data/does_not_exist.csv"   -> what error do you get?
#      - change int(parts[3]) to int(parts[9])           -> what error now?
#      - delete a closing bracket somewhere               -> and now?
#    Each mistake produces a different traceback. Read the LAST line first.
#    It says what went wrong. The line number says where. Put the code back
#    as it was afterwards.
