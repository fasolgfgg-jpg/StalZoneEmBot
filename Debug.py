import os
from datetime import datetime
from pathlib import Path

#LOGS_DIR = "Logs"
BASE_DIR = Path(__file__).resolve().parent

LOGS_DIR = BASE_DIR / "data" / "logs"
NAME_FILE = LOGS_DIR / "name.nlf"

def NewFileLogs(name):
    os.makedirs(LOGS_DIR, exist_ok=True)
    with open(NAME_FILE, "w", encoding="utf-8") as file:
        file.write(name)


def WriteLine(type, message):
    os.makedirs(LOGS_DIR, exist_ok=True)
    try:
        with open(NAME_FILE, "r", encoding="utf-8") as name:
            log_name = name.read().strip()
    except FileNotFoundError:
        log_name = datetime.now().strftime("%Y.%m.%d")

    time = datetime.now()
    ftime = time.strftime("%H:%M:%S")
    with open(f"{LOGS_DIR}/{log_name}.log", "a", encoding="utf-8") as file:
        if type == "Error":
            print(f"\033[0;32m[{ftime}]\033[91m[Error]: \033[0;0m{message}", flush=True,)
            file.write(f"[{ftime}][Error]: {message}\n")
        elif type == "Warn":
            print(f"\033[0;32m[{ftime}]\033[1;33m[Warn]: \033[0;0m{message}", flush=True,)
            file.write(f"[{ftime}][Warn]: {message}\n")
        else:
            print(f"\033[0;32m[{ftime}]\033[0;32m[Info]: \033[0;0m{message}", flush=True,)
            file.write(f"[{ftime}][Info]: {message}\n")
