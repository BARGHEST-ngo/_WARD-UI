import re
from collections import defaultdict

def parse_time(raw):
    match = re.search(r"(\d+h)?\s*(\d+m)?\s*(\d+s)?", raw)
    if not match:
        return 0
    hours = int(match.group(1)[:-1]) if match.group(1) else 0
    minutes = int(match.group(2)[:-1]) if match.group(2) else 0
    seconds = int(match.group(3)[:-1]) if match.group(3) else 0
    return hours * 3600 + minutes * 60 + seconds


def run(data):
    lines = data.get("raw", [])
    service_times = defaultdict(lambda: {"fg_service": 0, "fg_activity": 0, "top_time": 0})

    current_app = None

    for line in lines:
        if "Proc " in line:
            match = re.search(r"Proc (\S+):", line)
            if match:
                current_app = match.group(1)

        if current_app:
            fg_service_match = re.search(r"Foreground services:\s*(.+?)\srealtime", line)
            fg_activity_match = re.search(r"Foreground activities:\s*(.+?)\srealtime", line)
            top_match = re.search(r"Top for:\s*(.+?)\s", line)

            if fg_service_match:
                service_times[current_app]["fg_service"] += parse_time(fg_service_match.group(1))
            if fg_activity_match:
                service_times[current_app]["fg_activity"] += parse_time(fg_activity_match.group(1))
            if top_match:
                service_times[current_app]["top_time"] += parse_time(top_match.group(1))

    suspicious = []
    for app, t in service_times.items():
        if t["fg_service"] > t["fg_activity"] + 60:
            suspicious.append(f"{app} - fg_service:{t['fg_service']}s vs fg_activity:{t['fg_activity']}s")

    score = len(suspicious) * 5

    return {
        "name": "Foreground Service Mismatch Heuristic",
        "suspicious": suspicious,
        "score": score
    }
