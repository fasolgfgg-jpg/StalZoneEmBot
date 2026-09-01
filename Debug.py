from datetime import datetime

def NewFileLogs(name):
    file = open(f"name.nlf", "w")
    file.write(name)
def WriteLine(type, message):
    name = open(f"name.nlf", "r")
    time = datetime.now()
    ftime = time.strftime("%H:%M:%S")
    file = open(f"Logs/{name.read()}.log", "a")
    name.close()
    if type == "Error":
        print(f"\033[0;32m[{ftime}]\033[91m[Error]: \033[0;0m{message}")
        file.write(f"[{ftime}][Error]: {message}\n")
    elif type == "Warn":
        print(f"\033[0;32m[{ftime}]\033[1;33m[Warn]: \033[0;0m{message}")
        file.write(f"[{ftime}][Warn]: {message}\n")
    else:
        print(f"\033[0;32m[{ftime}]\033[0;32m[Info]: \033[0;0m{message}")
        file.write(f"[{ftime}][Info]: {message}\n")
    file.close()
#WriteLine("Warn", "End the message")