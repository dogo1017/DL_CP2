# time_handler.py
# Handles getting and formatting the current date and time
# Kept in its own file so the time logic is separate from everything else
import datetime

# Gets the current date and time from the system and formats it as YYYY-MM-DD HH:MM:SS
# Returns it as a string so it can be written directly into the document
def get_current_timestamp():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time