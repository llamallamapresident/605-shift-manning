from tkinter import messagebox

def assign(duties, names, max_time):
    
    # Assign duties first by their start time from earliest to latest, then longest to shortest
    ordered_duties = order(duties)

    for id in ordered_duties:
        duration = int(duties[id]["duration"])
        rest = int(duties[id]["rest"])
        start_time = int(duties[id]["start_time"])
        person = assign_person(start_time, names)

        # Update duties with person
        duties[id]["person"] = person

        # Update names with new timings and total hours
        names[person]["total_hours"] += duration

        for time_passed in range(duration):
            time = start_time + time_passed
            if time < max_time:
                names[person]["timings"][time]["location"] = duties[id]["location"]
                names[person]["timings"][time]["id"] = id
        
        for time_passed in range(rest):
            time = start_time + duration + time_passed
            if time < max_time:
                names[person]["timings"][time]["location"] = duties[id]["location"] + "(resting)"
                names[person]["timings"][time]["id"] = id
                
    return duties, names


# Returns a list of duty ids in order
def order(duties):
    tmp_duties = duties.copy()
    ordered_duties = []
    for i in range(len(duties)):
        id = earliest(tmp_duties)
        ordered_duties.append(id)
        tmp_duties.pop(id)
    return ordered_duties


# Returns the duty id that is the earliest and longest
def earliest(duties):
    id = list(duties.keys())[0]

    for duty in duties.items():

        # Choose the earliest start time
        if int(duty[1]["start_time"]) < int(duties[id]["start_time"]):
            id = duty[0]

        # If start time is the same choose the longest duty (including rest time)
        elif int(duty[1]["start_time"]) == int(duties[id]["start_time"]):
            if (int(duty[1]["duration"]) + int(duty[1]["rest"])) > (int(duties[id]["duration"]) + int(duties[id]["rest"])):
                id = duty[0]
    
    return id


# Returns the person doing the duty
def assign_person(start_time, names):

    # Get list of people avaliable at the start_time
    avaliable = []
    for name in names.items():
        if name[1]["timings"][start_time]["location"] == "none":
            avaliable.append(name[0])
    
    # Exit if there are no avaliable people
    if avaliable == []:
        messagebox.showerror("error", "Insufficient people to assign (try lowering the minimum rest time or requesting more manpower)")
        exit(1)
    
    # Get the person with the least hours
    person = avaliable[0]
    for name in avaliable:
        if names[name]["total_hours"] < names[person]["total_hours"]:
            person = name

    return person