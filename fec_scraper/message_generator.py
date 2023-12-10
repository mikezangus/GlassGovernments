def generate_message(action: str, subject: str = None, attempt = None, max_attempts = None, exception: str = None, notes = None):

    if subject is not None:
        subject_message = f" for {subject}"
    else:
        subject_message = ""

    if attempt is not None and max_attempts is not None:
        attempt_message = f" on attempt {attempt}/{max_attempts}"
        if attempt < max_attempts:
            next_action_message = ", retrying."
        else:
            next_action_message = ", moving on."
    else:
        attempt_message = ""
        next_action_message = "."

    if exception is not None:
        exception_message = f" Excepton: {exception}"
    else:
        exception_message = ""

    if notes is not None:
        notes_message = f"\nNotes: {notes}"
    else:
        notes_message = ""

    message = f"Failed to {action}{subject_message}{attempt_message}{next_action_message}{exception_message}{notes_message}"
    return message
