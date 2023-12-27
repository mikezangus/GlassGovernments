def write_base_message(context, action, subject = None, attempt = None, max_attempts = None, exception = None, notes = None):
    
    if subject:
        subject_message = f" for {subject}"
    else:
        subject_message = ""

    if attempt and max_attempts:
        attempt_message = f" on attempt {attempt}/{max_attempts}"
        if attempt < max_attempts and context == "failed":
            next_action_message = ", retrying."
        elif attempt == max_attempts and context == "failed":
            next_action_message = ", moving on."
        else:
            next_action_message = "."
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


def write_start_message(action, subject = None, notes = None):
    context = "starting"
    start_message = write_base_message(context = context, action = action, subject = subject, notes = notes)
    return start_message


def write_success_message(action, subject = None, attempt = None, max_attempts = None, notes = None):
    context = "succeeded"
    success_message = write_base_message(context = context, action = action, subject = subject, attempt = attempt, max_attempts = max_attempts, notes = notes)
    return success_message


def write_failure_message(action, subject = None, attempt = None, max_attempts = None, exception = None, notes = None):
    context = "failed"
    failure_message = write_base_message(context = context, action = action, subject = subject, attempt = attempt, max_attempts = max_attempts, exception = exception, notes = notes)
    return failure_message

