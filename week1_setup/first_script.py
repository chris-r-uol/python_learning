"""
Your first script.

Run it:

    python first_script.py

It reads two days of hourly traffic counts and reports which hours were busy.

Everything below is spelled out in more detail than real code would be. That
is deliberate. Read it from top to bottom - that is the order Python reads it
in too.
"""

# ---------------------------------------------------------------------------
# 1. Settings. These are the things we might want to change.
# ---------------------------------------------------------------------------

DATA_FILE = "data/site_counts_small.csv"

# An hour is "busy" if more vehicles than this pass in that hour.
# CHANGE THIS NUMBER and run the script again. That is the exercise.
BUSY_THRESHOLD = 900

DIRECTION = "northbound"


# ---------------------------------------------------------------------------
# 2. Read the file.
# ---------------------------------------------------------------------------

# `open` gives us the file. `readlines` gives us a list - one string per line.
file_handle = open(DATA_FILE)
lines = file_handle.readlines()
file_handle.close()

# `lines` is now a list, so we can pick items out of it by position.
# Positions start at zero, so lines[0] is the FIRST line - the header row,
# which names the columns: date,hour,direction,count
header = lines[0]

# lines[1:] means "from position 1 to the end" - everything except the
# header. That is the actual data.
data_lines = lines[1:]

print("Read {} rows from {}".format(len(data_lines), DATA_FILE))
print("Columns are: {}".format(header.strip()))
print()


# ---------------------------------------------------------------------------
# 3. Go through the rows one at a time.
# ---------------------------------------------------------------------------

# Start with an empty list and a total of zero. The loop below fills them.
busy_hours = []
total_vehicles = 0

# A `for` loop: run everything indented below, once for each line in the
# file. On each pass, `line` holds one line of the file.
for line in data_lines:
    # Each line is one string, like "2026-03-02,8,northbound,1703\n"
    # `strip` removes the invisible newline character at the end.
    # `split` cuts the text at every comma, giving a list of four strings.
    parts = line.strip().split(",")

    # Pull the four values out of the list by position, counting from zero.
    # Note the int(): everything read from a file arrives as TEXT, so the
    # values we want to do arithmetic on have to be converted to numbers.
    date = parts[0]               # position 0 - text, and text is fine here
    hour = int(parts[1])          # position 1 - int() makes "8" into 8
    direction = parts[2]          # position 2
    count = int(parts[3])         # position 3 - we add this up, so it must
                                  #              be a number, not text

    # An `if`: only do something when the condition is true. `continue`
    # means "skip the rest of this pass and start the next line".
    if direction != DIRECTION:
        continue

    # Add this row's count onto the running total. The right-hand side is
    # worked out first, then stored back under the same name.
    total_vehicles = total_vehicles + count

    # If this hour is busy, remember it by adding it to our list.
    if count > BUSY_THRESHOLD:
        busy_hours.append((date, hour, count))


# ---------------------------------------------------------------------------
# 4. Report what we found.
# ---------------------------------------------------------------------------

print("Direction:        {}".format(DIRECTION))
print("Busy threshold:   {} vehicles/hour".format(BUSY_THRESHOLD))
print("Total vehicles:   {}".format(total_vehicles))
print("Busy hours found: {}".format(len(busy_hours)))
print()

if len(busy_hours) == 0:
    print("No hours were above the threshold. Try lowering BUSY_THRESHOLD.")
else:
    print("{:<12} {:>5} {:>8}".format("Date", "Hour", "Count"))
    for date, hour, count in busy_hours:
        print("{:<12} {:>5} {:>8}".format(date, hour, count))


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
#    Each mistake produces a different traceback. Read the LAST line first: it
#    says what went wrong. Then find the line number: it says where. Put the
#    code back as it was afterwards.
