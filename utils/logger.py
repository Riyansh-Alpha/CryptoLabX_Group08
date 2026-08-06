import os
from datetime import datetime

LOG_DIR = "outputs"
LOG_FILE = os.path.join(LOG_DIR, "execution.log")


def log_menu(option):
    """
    Log the selected menu option with current date and time.

    Records every menu interaction to outputs/execution.log in the format:
        [YYYY-MM-DD HH:MM:SS] Menu Option Selected: <option>

    Args:
        option (str): The name of the menu option selected by the user.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] Menu Option Selected: {option}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(entry)
