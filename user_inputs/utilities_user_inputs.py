def input_choice(subject: str, action: str, choices: list = None, notes = None):
    choices_text = f"\n{', '.join(choices)}" if choices else ""
    if not notes:
        notes = ""
    else:
        notes = f"\n{notes}"
    input_message = input(f"\n{'-' * 100}\nFor which {subject} do you want to {action} data?:{choices_text}{notes}\n> ")
    return input_message
    

def print_retry_message(subject: str):
    retry_message = print(f"You've entered an invalid {subject}, try again")
    return retry_message
    

def is_valid_input(choice: str, choices: list):
    return choice in choices or choice.lower() == "all"


def load_commands(subject):
    commands = [
        f"∙ [enter {subject} here]",
        f"∙ [enter 1st {subject} here], [enter 2nd {subject} here], ...,",
        f"∙ ALL",
        f"∙ ALL BUT [enter {subject}(s) here]",
        f"∙ ALL FROM [first {subject}] TO [last {subject}] (order both {subject}s alphabetically)",
        f"∙ ALL STARTING FROM [enter {subject} here]"
    ]
    return commands


def write_start_message(action, year, chamber, state, district, candidate = None):
    state_str = ", ".join(state)
    if len(chamber) > 1:
        district_str = "all"
    elif len(district) > 1:
        if district[-1] >= "99":
            district_str = "all"
        else:
            first_district = district[0]
            last_district = district[-1]
            district_str = f"{first_district}, ..., {last_district}"
    else:
        district_str = district[0]
    if candidate:
        print(f'\n\nStarting to {action} for:\nYear: {year}\nChamber: {chamber}\nState(s): {state_str}\nDistrict(s): {district_str}\nCandidate(s): {candidate}')
    else:
        print(f'\n\nStarting to {action} for:\nYear: {year}\nChamber: {chamber}\nState(s): {state_str}\nDistrict(s): {district_str}\n')