import re
from datetime import datetime, timedelta

def WAscore(file_path):
    with open(file_path, encoding="utf-8") as f:
        data = f.read()

    rx = "\d\d?/\d\d?/\d\d"
    dates = re.findall(rx, data)
    dates.sort(key=lambda date: datetime.strptime(date, "%d/%m/%y"))

    for i in dates:
        if datetime.strptime(i,"%d/%m/%y") < datetime.now() - timedelta(days=90):
            dates.remove(i)

    return len(dates)/30
