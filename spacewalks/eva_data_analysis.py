import json
import csv
import datetime as dt

import matplotlib.pyplot as plt

# it can be good practice to have a new line to seperate python plugins from the imported packages, commonly python ones go first

# https://data.nasa.gov/resource/eva.json (with modifications)

# 1: vars defined for locations of where data is opened from, col names,
# which had typos, and data which had unrequired absolute locations

input_file = open("eva-data.json", "r", encoding="ascii")
output_file = open("eva-data.csv", "w", encoding="utf-8")


graph_file = "cumulative_eva_graph.png"

fieldnames = ("EVA", "Country", "Crew", "Vehicle", "Date", "Duration", "Purpose")

data = []

# a list of 375 values for each row is created, command line is initialized to readline() from each line of the JSON
for i in range(375):
    line = input_file.readline()
    print(line)
    data.append(json.loads(line[1:-1]))
# data.pop(0)
## Comment out this bit if you don't want the spreadsheet

# Write the data which has been collected to a CSV file called data.csv which was opened at the beginning in write only mode
output_writer = csv.writer(output_file)
# note that the csv is not saved after writing


time = []
date = []

j = 0
for i in data:
    print(data[j])
    # and this bit
    output_writer.writerow(data[j].values())
    if "duration" in data[j].keys():
        duration_string = data[j]["duration"]
        if duration_string == "":
            pass
        else:
            duration_dt = dt.datetime.strptime(duration_string, "%H:%M")
            duration_hours = dt.timedelta(
                hours=duration_dt.hour, minutes=duration_dt.minute, seconds=duration_dt.second
            ).total_seconds() / (60 * 60)
            print(duration_dt, duration_hours)
            time.append(duration_hours)

            if "date" in data[j].keys():
                date.append(dt.datetime.strptime(data[j]["date"][0:10], "%Y-%m-%d"))
                # date.append(data[j]['date'][0:10])

            else:
                time.pop(0)
    j += 1

duration_dt = [0]
for i in time:
    duration_dt.append(duration_dt[-1] + i)

date, time = zip(*sorted(zip(date, time)))


plt.plot(date, duration_dt[1:], "ko-")
plt.xlabel("Year")
plt.ylabel("Total time spent in space to date (hours)")
plt.tight_layout()
plt.savefig(graph_file)
plt.show()
