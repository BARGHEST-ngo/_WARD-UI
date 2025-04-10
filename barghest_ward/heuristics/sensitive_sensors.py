import re
from collections import defaultdict

SENSITIVE_TAGS = {"+camera", "+audio", "+sensor"}

def run(data):
    batterystats = data.get("batterystats", {})
    lines = batterystats.get("raw", [])
    current_top_app = None
    app_usage = defaultdict(lambda: {"camera": 0, "audio": 0, "sensor": 0})

    for line in lines:
        line = line.strip()

        # Update current top or foreground app
        if "+top=" in line or "+fg=" in line:
            match = re.search(r"[+:\s](?:top|fg)=[^:\s]+:?(\S+)", line)
            if match:
                current_top_app = match.group(1).strip().strip('"')

        # Track sensitive tag usage
        for tag in SENSITIVE_TAGS:
            if tag in line and current_top_app:
                component = tag.lstrip("+")
                app_usage[current_top_app][component] += 1

    suspicious_apps = []
    for app, stats in app_usage.items():
        cam, aud, sens = stats["camera"], stats["audio"], stats["sensor"]
        if cam > 0 or aud > 2 or sens > 3:
            suspicious_apps.append(
                f"{app} - camera:{cam}, audio:{aud}, sensor:{sens}"
            )

    return {
        "name": "sensitive_sensor_usage",
        "suspicious": suspicious_apps,
        "score": len(suspicious_apps) * 10
    }
