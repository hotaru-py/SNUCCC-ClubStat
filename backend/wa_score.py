import re
from datetime import datetime

def WAscore(file_path):
    with open(file_path, encoding="utf-8") as f:
        data = f.read()
    print(data)

    rx = "\d\d?/\d\d?/\d\d"
    match = re.findall(rx, data)
    dates = list(set(match))
    

    print(dates) 

    return len(match)
