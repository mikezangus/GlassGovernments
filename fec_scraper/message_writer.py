def write_base_message(context: str, action: str, subject: str = None, attempt = None, max_attempts = None, exception: str = None, notes = None):
    
    if subject:
        subject_message = f" for {subject}"
    else:
        subject_message = ""

    if attempt and max_attempts:
        attempt_message = f" on attempt {attempt}/{max_attempts}"
        if attempt < max_attempts:
            next_action_message = ", retrying."
        else:
            next_action_message = ", moving on."
    else:
        attempt_message = ""
        next_action_message = "."

    if exception:
        exception_message = f" Excepton: {exception}"
    else:
        exception_message = ""

    if notes:
        notes_message = f"\nNotes: {notes}"
    else:
        notes_message = ""

    message = f"{context.capitalize()} to {action}{subject_message}{attempt_message}{next_action_message}{exception_message}{notes_message}"
    return message


def write_start_message(action: str, subject: str = None, notes = None):
    context = "starting"
    start_message = write_base_message(context = context, action = action, subject = subject, notes = notes)
    return start_message


def write_failure_message(action: str, subject: str = None, attempt = None, max_attempts = None, exception: str = None, notes = None):
    context = "failed"
    failure_message = write_base_message(context = context, action = action, subject = subject, attempt = attempt, max_attempts = max_attempts, exception = exception, notes = notes)
    return failure_message

