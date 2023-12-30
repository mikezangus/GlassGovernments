def input_choice(subject: str, action: str, choices: list = None, notes = None):
    choices_text = f"\n{', '.join(choices)}" if choices else ""
    notes_text = f"\n{notes}" if notes else ""
    input_message = input(f"\n{'-' * 100}\nFor which {subject} do you want to {action} data?:{choices_text}{notes_text}\n> ")
    return input_message
    

def print_retry_message(subject: str):
    retry_message = print(f"You've entered an invalid {subject}, try again")
    return retry_message
    

def is_valid_input(choice: str, choices: list):
    return choice in choices or choice.lower() == "all"


def load_commands(subject: str):
    commands = [
        f"∙ [enter {subject} here]",
        f"∙ [enter 1st {subject} here], [enter 2nd {subject} here], ...,",
        f"∙ ALL",
        f"∙ ALL BUT [enter {subject}(s) here]",
        f"∙ ALL FROM [first {subject}] TO [last {subject}] (order both {subject}s alphabetically)",
        f"∙ ALL STARTING FROM [enter {subject} here]"
    ]
    return "\n".join(commands)


def write_start_message(action: str, year: str, chamber_list: list, state_list: list, district_list: list, candidate_list: list = None):
    state_str = ", ".join(state_list)
    if len(chamber_list) > 1:
        district_str = "all"
    elif len(district_list) > 1:
        if district_list[-1] >= "99":
            district_str = "all"
        else:
            first_district = district_list[0]
            last_district = district_list[-1]
            district_str = f"{first_district}, ..., {last_district}"
    else:
        district_str = district_list[0]
    if candidate_list:
        if len(candidate_list) > 1:
            last_name_list = [candidate.split("_")[3] for candidate in candidate_list]
            candidate_str = ", ".join(last_name_list)
        else:
            candidate_str = candidate_list[0]
        print(f'\n\nStarting to {action} for:\nYear: {year}\nChamber: {chamber_list}\nState(s): {state_str}\nDistrict(s): {district_str}\nCandidate(s): {candidate_str}')
    else:
        print(f'\n\nStarting to {action} for:\nYear: {year}\nChamber: {chamber_list}\nState(s): {state_str}\nDistrict(s): {district_str}\n')