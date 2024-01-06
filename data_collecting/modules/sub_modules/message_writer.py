def write_base_message(context, action, subject = None, attempt = None, max_attempts = None, exception = None, notes = None, time = None):
    
    if subject:
        subject_message = f"{subject} | "
    else:
        subject_message = ""

    if attempt and max_attempts:
        attempt = attempt + 1
        attempt_message = f" on attempt {attempt}/{max_attempts}"
        if attempt < max_attempts and context == "failed":
            next_action_message = ", retrying"
        elif attempt == max_attempts and context == "failed":
            next_action_message = ", moving on"
        else:
            next_action_message = ""
    else:
        attempt_message = ""
        next_action_message = ""

    if exception:
        exception_message = f" Excepton: {exception}"
    else:
        exception_message = ""

    if notes:
        notes_message = f"\nNotes: {notes}"
    else:
        notes_message = ""

    if time:
        time_message = f" at {time}"
    else:
        time_message = ""

    message = f"{subject_message}{context.capitalize()} to {action}{attempt_message}{next_action_message}{exception_message}{time_message}{notes_message}"


    return message


def write_start_message(action, subject = None, attempt = None, max_attempts = None, notes = None, time = None):
    context = "starting"
    start_message = write_base_message(context, action, subject, attempt, max_attempts, None, notes, time)
    return start_message


def write_success_message(action, subject = None, attempt = None, max_attempts = None, notes = None, time = None):
    context = "succeeded"
    success_message = write_base_message(context, action, subject, attempt, max_attempts, notes = notes, time = time)
    return success_message


def write_failure_message(action, subject = None, attempt = None, max_attempts = None, exception = None, notes = None, time = None):
    context = "failed"
    failure_message = write_base_message(context, action, subject, attempt, max_attempts, exception, notes, time)
    return failure_message