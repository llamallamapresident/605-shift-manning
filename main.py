import csv
from assign import assign
from equalize import equalize
import os

script_dir = os.getcwd()

def main(input_namelist_path, input_dutylist_path, output_namelist_name, output_dutylist_name):

    # Extract names and duties from csv file in the form of dictionaries
    max_time = get_max_time(input_dutylist_path)
    names = extract_names(input_namelist_path, max_time)
    duties = extract_duties(input_dutylist_path)

    # Assign people to duties without overlap
    duties, names = assign(duties, names, max_time)

    # Equalize working hours via swapping duties
    duties, names = equalize(duties, names, max_time)

    # Output a csv of duties with people assigned and a csv of people and their respective duties
    output_names(names, max_time, output_namelist_name)
    output_duties(duties, output_dutylist_name)


# Returns the last time unit of the cycle
def get_max_time(input_dutylist_path):
    max_time = 0
    with open(input_dutylist_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (int(row["start_time"]) + int(row["duration"])) > max_time:
                max_time = int(row["start_time"]) + int(row["duration"])
    return max_time


# Extracts a dictionary of names paired to duty timings and total hours
def extract_names(input_namelist_path, max_time):
    names = {}
    with open(input_namelist_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            timings = {}
            for time in range(max_time):
                tmp = {
                    "location": "none",
                    "id": None
                }
                timings.update({time: tmp})

            person_info = {
                "timings": timings,
                "total_hours": 0
            }

            names.update({row["name"]: person_info})
    return names


# Extracts a dictionary of duties paired to the duty infomation and the person doing it
def extract_duties(input_dutylist_path):
    duties = {}
    with open(input_dutylist_path, "r") as file:
        reader = csv.DictReader(file)
        i = 0
        for row in reader:
            duty_info = {
                "location": row["location"],
                "start_time": row["start_time"],
                "duration": row["duration"],
                "rest": row["rest"],
                "person": "unassgined"
            }
            duties.update({i: duty_info})
            i += 1
    return duties


def output_names(names, max_time, output_namelist_name):
    with open(os.path.join(script_dir, 'output/', output_namelist_name), 'w', newline='') as csvfile:
        fieldnames = ['name', 'timings', "total_hours"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for name in names.items():
            tmp = {}
            for time in range(max_time):
                tmp.update({time: name[1]["timings"][time]["location"]})
            writer.writerow({"name": name[0], "timings": tmp, "total_hours": name[1]["total_hours"]})
    return


def output_duties(duties, output_dutylist_name):
    with open(os.path.join(script_dir, 'output/', output_dutylist_name), 'w', newline='') as csvfile:
        fieldnames = ['location', 'start_time', "duration", "rest", "person"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for duty in duties.values():
            writer.writerow({
                "location": duty["location"], 
                "start_time": duty["start_time"], 
                "duration": duty["duration"],
                "rest": duty["rest"],
                "person": duty["person"]
            })
    return