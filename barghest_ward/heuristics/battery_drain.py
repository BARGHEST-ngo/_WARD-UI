# barghest_ward/heuristics/battery_drain.py

import re

SYSTEM_WHITELIST = {
    "scrn", "cpu", "blue", "camera", "video", "cell",
    "wifi", "memory", "phone", "ambi", "idle",
    "audio", "flashlight", "sensors", "???"
}

def is_system_app(package: str) -> bool:
    if package in SYSTEM_WHITELIST:
        return True
    return package.startswith(("com.android.", "android.", "com.samsung.", "com.sec."))

def run(data):
    rows = data.get("parsed", [])

    battery_usage = {}
    app_fg_usage = {}
    wakeups_count = 0
    wakelocks_count = 0
    uid_to_pkg = {}

    for row in rows:
        line_type = row.get("line_type", "")
        if line_type == "pwi":
            app = row.get("app", "unknown")
            try:
                usage = float(row.get("usage", 0))
                fg = float(row.get("fg", 0))
            except ValueError:
                usage, fg = 0.0, 0.0
            battery_usage[app] = battery_usage.get(app, 0.0) + usage
            app_fg_usage[app] = app_fg_usage.get(app, 0.0) + fg

        elif line_type == "wr":
            try:
                wakeups_count += int(row.get("count", 1) or 1)
            except ValueError:
                wakeups_count += 1

        elif line_type == "kwl":
            try:
                wakelocks_count += int(row.get("count", 1) or 1)
            except ValueError:
                wakelocks_count += 1

        elif line_type == "uid":
            uid_val = row.get("uid", "")
            pkg = row.get("pkg", "unknown")
            uid_to_pkg.setdefault(uid_val, pkg)

    # Remap uid_XXX entries to actual package names
    for key in [k for k in battery_usage if k.startswith("uid_")]:
        usage = battery_usage.pop(key)
        fg_val = app_fg_usage.pop(key, 0.0)
        uid_val = key.split("_", 1)[-1]
        matching_pkgs = [pkg for uid, pkg in uid_to_pkg.items()
                         if uid == uid_val and pkg.startswith("com.")]
        if matching_pkgs:
            usage_share = usage / len(matching_pkgs)
            fg_share = fg_val / len(matching_pkgs)
            for pkg in matching_pkgs:
                battery_usage[pkg] = battery_usage.get(pkg, 0.0) + usage_share
                app_fg_usage[pkg] = app_fg_usage.get(pkg, 0.0) + fg_share

    suspicious_details = []

    SYSTEM_THRESHOLD = 50.0
    USERAPP_THRESHOLD = 20.0
    FOREGROUND_RATIO_CUTOFF = 0.1

    for app, usage in battery_usage.items():
        fg = app_fg_usage.get(app, 0.0)
        ratio = (fg / usage) if usage > 0 else 0

        if app in SYSTEM_WHITELIST:
            continue

        threshold = USERAPP_THRESHOLD if app.startswith("com.") else SYSTEM_THRESHOLD

        if usage > threshold and ratio < FOREGROUND_RATIO_CUTOFF:
            reason = (
                f"Battery usage {usage:.2f} > threshold {threshold:.2f}, "
                f"fg ratio {ratio:.2f} < {FOREGROUND_RATIO_CUTOFF}"
            )
            if is_system_app(app):
                reason += " (system app)"
            suspicious_details.append(f"{app}: {reason}")

    score = len(suspicious_details) * 10 + (wakeups_count * 0.05) + (wakelocks_count * 0.1)

    return {
        "name": "battery_drain",
        "suspicious": suspicious_details,
        "score": round(score, 2)
    }
