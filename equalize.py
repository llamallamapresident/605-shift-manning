import math

# Swaps duties around to distribute hours more equally
def equalize(duties, names, max_time):

    # Get average hours rounded up
    total_hours_combined = 0
    total_people = 0
    for name in names.values():
        total_people += 1
        total_hours_combined += int(name["total_hours"])
    average_hours = math.ceil(total_hours_combined / total_people)

    # Get the duration of the shortest possible duty
    durations_list = []
    for duty in duties.items():
        if int(duty[1]["duration"]) not in durations_list:
            durations_list.append(int(duty[1]["duration"]))
    shortest_duty_hours = min(durations_list)
    durations_list_length = len(durations_list)

    # Get the shortest possible change in hours from a 1-1 duty swap, returning 0 if there is only 1 duration
    if durations_list_length >= 2:
        shortest_swap_change = abs(durations_list[0] - durations_list[1])
        for i in range(durations_list_length):
            for j in range(durations_list_length - i):
                k = durations_list_length - j - 1
                if i != k:
                    if abs(durations_list[i] - durations_list[k]) < shortest_swap_change:
                        shortest_swap_change = abs(durations_list[i] - durations_list[k])
    else:
        shortest_swap_change = 0
    
    give_and_swap(duties, names, average_hours, total_people, shortest_duty_hours, shortest_swap_change, max_time)
    return duties, names


def give_and_swap(duties, names, average_hours, total_people, shortest_duty_hours, shortest_swap_change, max_time):
    changes_made = False

    # Attempt swapping duties if duty hours are not all the same
    if shortest_swap_change != 0:
        changes_made = swap(duties, names, average_hours, total_people, shortest_swap_change, max_time)
    
    # Use recursion if changes are made
    if changes_made == True:
        give_and_swap(duties, names, average_hours, total_people, shortest_duty_hours, shortest_swap_change, max_time)
    
    # Attempt giving duties if duty hours are not all the same
    changes_made = give(duties, names, average_hours, total_people, shortest_duty_hours, max_time)

    # Use recursion if changes are made
    if changes_made == True:
        give_and_swap(duties, names, average_hours, total_people, shortest_duty_hours, shortest_swap_change, max_time)
    
    return


def give(duties, names, average_hours, total_people, shortest_duty_hours, max_time):

    # Get list of people with more and less than the average hours +- 1
    too_little_hours_namelist = order_by_least_hours(names, average_hours, total_people)
    too_many_hours_namelist = order_by_most_hours(names, average_hours, total_people)

    # Attempt to give duties by looping through the namelists, using recursion if a swap is made

    for name_more in too_many_hours_namelist:
        for name_little in too_little_hours_namelist:
            difference_in_hours = int(names[name_more]["total_hours"]) - int(names[name_little]["total_hours"])
            if difference_in_hours > shortest_duty_hours:

                # If a duty has been given try equalizing again
                if attempt_give_duty(duties, names, name_more, name_little, difference_in_hours, max_time) == True:
                    return True
    return False


def order_by_least_hours(names, average_hours, total_people):
    tmp_names = names.copy()
    too_little_hours_namelist = []
    for i in range(total_people):
        name = least_hours(tmp_names)
        if int(tmp_names[name]["total_hours"]) >= average_hours:
            break
        too_little_hours_namelist.append(name)
        tmp_names.pop(name)
    return too_little_hours_namelist


def least_hours(tmp_names):
    chosen_name = list(tmp_names.keys())[0]
    for name in tmp_names.items():
        if int(name[1]["total_hours"]) < int(tmp_names[chosen_name]["total_hours"]):
            chosen_name = name[0]
    return chosen_name


def order_by_most_hours(names, average_hours, total_people):
    tmp_names = names.copy()
    too_many_hours_namelist = []
    for i in range(total_people):
        name = most_hours(tmp_names)
        if int(tmp_names[name]["total_hours"]) <= average_hours:
            break
        too_many_hours_namelist.append(name)
        tmp_names.pop(name)
    return too_many_hours_namelist


def most_hours(tmp_names):
    chosen_name = list(tmp_names.keys())[0]
    for name in tmp_names.items():
        if int(name[1]["total_hours"]) > int(tmp_names[chosen_name]["total_hours"]):
            chosen_name = name[0]
    return chosen_name


# If any duty can be given from name_more to name_little, updates duties and names and returns True
def attempt_give_duty(duties, names, name_more, name_little, difference_in_hours, max_time):
    name_more_dutylist = get_dutylist(name_more, names, max_time)
    for more_duty_id in name_more_dutylist:
        
        # Check if giving the duty will result in a more equal hours distribution
        if int(duties[more_duty_id]["duration"]) < difference_in_hours:

            # Check if name_little can take the duty
            total_duty_time = int(duties[more_duty_id]["duration"]) + int(int(duties[more_duty_id]["rest"]))
            if give_duty_check(names, duties, name_little, more_duty_id, total_duty_time) == True:

                # Update duties with new person
                duties[more_duty_id]["person"] = name_little

                # Update timings and total_hours in names for name_more and name_little
                names[name_more]["total_hours"] -= int(duties[more_duty_id]["duration"])
                names[name_little]["total_hours"] += int(duties[more_duty_id]["duration"])

                for i in range(total_duty_time):
                    time = i + int(duties[more_duty_id]["start_time"])
                    names[name_more]["timings"][time]["id"] = None
                    names[name_more]["timings"][time]["location"] = "none"
                    names[name_little]["timings"][time]["id"] = more_duty_id
                
                for i in range(int(duties[more_duty_id]["duration"])):
                    time = i + int(duties[more_duty_id]["start_time"])
                    names[name_little]["timings"][time]["location"] = duties[more_duty_id]["location"]

                for i in range(int(duties[more_duty_id]["rest"])):
                    time = i + int(duties[more_duty_id]["start_time"]) + int(duties[more_duty_id]["duration"])
                    names[name_little]["timings"][time]["location"] = duties[more_duty_id]["location"] + "(resting)"
                return True
    return False


# Returns all duties a person has
def get_dutylist(name, names, max_time):
    tmp_dutylist = []
    for i in range(max_time):
        id = names[name]["timings"][i]["id"]
        if id != None and id not in tmp_dutylist:
            tmp_dutylist.append(id)
    return tmp_dutylist


def give_duty_check(names, duties, name_little, more_duty_id, total_duty_time):
    for i in range(total_duty_time):

        # Returns False if name_little is busy during any of the timings
        time = i + int(duties[more_duty_id]["start_time"])
        if names[name_little]["timings"][time]["id"] != None:
            return False
    return True


def swap(duties, names, average_hours, total_people, shortest_swap_change, max_time):
    
    # Get list of people with more and less than the average hours +- 1
    too_little_hours_namelist = order_by_least_hours(names, average_hours, total_people)
    too_many_hours_namelist = order_by_most_hours(names, average_hours, total_people)
    
    # Attempt to swap duties by looping through the namelists, using recursion if a swap is made
    for name_more in too_many_hours_namelist:
        for name_little in too_little_hours_namelist:
            difference_in_hours = int(names[name_more]["total_hours"]) - int(names[name_little]["total_hours"])
            if difference_in_hours > shortest_swap_change:

                # If a swap has been made try equalizing again
                if attempt_swap_duty(duties, names, name_more, name_little, difference_in_hours, max_time) == True:
                    return True
    return False

def attempt_swap_duty(duties, names, name_more, name_little, difference_in_hours, max_time):
    name_more_dutylist = get_dutylist(name_more, names, max_time)
    name_little_dutylist = get_dutylist(name_little, names, max_time)
    for more_duty_id in name_more_dutylist:
        for little_duty_id in name_little_dutylist:

            # Check if swapping duties will result in more equal hours distribution
            hours_change_from_swap = int(duties[more_duty_id]["duration"]) - int(duties[little_duty_id]["duration"])
            if hours_change_from_swap < difference_in_hours and hours_change_from_swap > 0:

                # Check if both people can accept the swap
                if swap_duty_check(duties, names, name_more, name_little, more_duty_id, little_duty_id) == True:

                    # Update duties with new people
                    duties[more_duty_id]["person"] = name_little
                    duties[little_duty_id]["person"] = name_more

                    # Update total_hours in names for name_more and name_little
                    names[name_more]["total_hours"] -= hours_change_from_swap
                    names[name_little]["total_hours"] += hours_change_from_swap

                    # Reset and update timings in names for name_more and name_little
                    for i in range(int(duties[more_duty_id]["duration"]) + int(duties[more_duty_id]["rest"])):
                        time = int(duties[more_duty_id]["start_time"]) + i
                        names[name_more]["timings"][time]["id"] = None
                        names[name_more]["timings"][time]["location"] = "none"

                    for i in range(int(duties[little_duty_id]["duration"]) + int(duties[little_duty_id]["rest"])):
                        time = int(duties[little_duty_id]["start_time"]) + i
                        names[name_little]["timings"][time]["id"] = None
                        names[name_little]["timings"][time]["location"] = "none"

                    for i in range(int(duties[little_duty_id]["duration"])):
                        time = int(duties[little_duty_id]["start_time"]) + i
                        names[name_more]["timings"][time]["id"] = little_duty_id
                        names[name_more]["timings"][time]["location"] = duties[little_duty_id]["location"]

                    for i in range(int(duties[little_duty_id]["rest"])):
                        time = int(duties[little_duty_id]["start_time"]) + int(duties[little_duty_id]["duration"]) + i
                        names[name_more]["timings"][time]["id"] = little_duty_id
                        names[name_more]["timings"][time]["location"] = duties[little_duty_id]["location"] + "(resting)"

                    for i in range(int(duties[more_duty_id]["duration"])):
                        time = int(duties[more_duty_id]["start_time"]) + i
                        names[name_little]["timings"][time]["id"] = more_duty_id
                        names[name_little]["timings"][time]["location"] = duties[more_duty_id]["location"]

                    for i in range(int(duties[more_duty_id]["rest"])):
                        time = int(duties[more_duty_id]["start_time"]) + int(duties[more_duty_id]["duration"]) + i
                        names[name_little]["timings"][time]["id"] = more_duty_id
                        names[name_little]["timings"][time]["location"] = duties[more_duty_id]["location"] + "(resting)"

                    return True
    return False


def swap_duty_check(duties, names, name_more, name_little, more_duty_id, little_duty_id):

    # Check if name_more is able to swap
    for i in range(int(duties[little_duty_id]["duration"]) + int(duties[little_duty_id]["rest"])):
        time = i + int(duties[little_duty_id]["start_time"])
        if names[name_more]["timings"][time]["id"] != None and names[name_more]["timings"][time]["id"] != more_duty_id:
            return False

    # Check if name_little is able to swap
    for i in range(int(duties[more_duty_id]["duration"]) + int(duties[more_duty_id]["rest"])):
        time = i + int(duties[more_duty_id]["start_time"])
        if names[name_little]["timings"][time]["id"] != None and names[name_little]["timings"][time]["id"] != little_duty_id:
            return False
    
    return True