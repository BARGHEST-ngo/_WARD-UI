import re

# Packages that often do location work legitimately
TRUSTED_PREFIXES = (
    "com.google.android.gms",
    "com.google.android.as",
    "android",
    "com.android.location",
)

# Threshold to report
SCORE_THRESHOLD = 2.5

def run(data):

    location_data = data.get("location", {})
    lines = location_data.get("raw", [])

    suspicious = []
    score = 0

    for line in lines:
        line = line.strip()

        if "Request[" not in line and "ProviderRequest" not in line:
            continue

        reasons = []
        line_score = 0

        # Extract UID/package string like "1010254/com.google.android.gms"
        match_package = re.search(r'(\d+)/([a-zA-Z0-9_.]+)', line)
        uid = match_package.group(1) if match_package else None
        package = match_package.group(2) if match_package else None

        is_trusted = any(package.startswith(pfx) for pfx in TRUSTED_PREFIXES) if package else False

        # minUpdateInterval
        match_interval = re.search(r'minUpdateInterval=(\+?)(\d+)', line)
        if match_interval:
            interval = int(match_interval.group(2))
            if interval == 0:
                reasons.append("zero interval")
                line_score += 1.5
            elif interval < 5000:
                reasons.append(f"short interval ({interval}ms)")
                line_score += 1.0

        # Passive + background
        if "PASSIVE" in line and "minUpdateInterval=0" in line:
            reasons.append("passive+zero interval")
            line_score += 1.0

        if "{bg}" in line:
            reasons.append("background")
            line_score += 0.5

        # Hidden from AppOps
        if "hiddenFromAppOps" in line:
            reasons.append("hiddenFromAppOps")
            line_score += 1.5

        # WorkSource delegation
        sources = re.findall(r'WorkSource\{([^\}]+)\}', line)
        if sources:
            total_sources = sum(len(s.split()) for s in sources)
            if total_sources > 2:
                reasons.append(f"multi WorkSource ({total_sources})")
                line_score += 0.5

        # If trusted system component, reduce score weight
        if is_trusted:
            line_score *= 0.5  # Reduce total score weight

        # Only report if final score is high enough
        if line_score >= SCORE_THRESHOLD:
            trust_note = " [trusted]" if is_trusted else ""
            suspicious.append(f"Suspicious location request: {line}{trust_note} | Reasons: {', '.join(reasons)}")
            score += line_score

    return {
        "name": "location_misuse",
        "suspicious": suspicious,
        "score": round(score, 1)
    }
