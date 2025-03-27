# barghest_ward/heuristics/battery_drain.py

import re

SYSTEM_WHITELIST = {
    "scrn", "cpu", "blue", "camera", "video", "cell",
    "wifi", "memory", "phone", "ambi", "idle",
    "audio", "flashlight", "sensors", "???"
}

def is_system_app(package):
    if package in SYSTEM_WHITELIST:
        return True
    system_prefixes = ("com.android.", "android.", "com.samsung.", "com.sec.")
    return package.startswith(system_prefixes)

def run(data):
    # data is expected to have a 'parsed' list of dictionaries
    rows = data.get("parsed", [])
    battery_usage = {}
    app_fg_usage = {}
    wakeups_count = 0
    wakelocks_count = 0
    uid_to_pkg = {}

    for row in rows:
        line_type = row.get("line_type", "")
        if line_type == "pwi":
            # battery usage lines
            app = row.get("app", "unknown")
            try:
                usage = float(row.get("usage", 0))
            except ValueError:
                usage = 0.0
            battery_usage[app] = battery_usage.get(app, 0) + usage

            try:
                fg = float(row.get("fg", 0))
            except ValueError:
                fg = 0.0
            app_fg_usage[app] = app_fg_usage.get(app, 0) + fg

        elif line_type == "wr":
            # wakeup lines
            try:
                count = int(row.get("count", 1))
            except ValueError:
                count = 1
            wakeups_count += count

        elif line_type == "kwl":
            # wakelock lines
            try:
                count = int(row.get("count", 1))
            except ValueError:
                count = 1
            wakelocks_count += count

        elif line_type == "uid":
            # map numeric uid -> package name
            uid_val = row.get("uid", "")
            pkg = row.get("pkg", "unknown")
            uid_to_pkg[uid_val] = pkg

    # If usage is recorded under "uid_XXX", distribute to com.X packages
    uid_keys = [key for key in battery_usage if key.startswith("uid_")]
    for uid_key in uid_keys:
        total_usage = battery_usage.pop(uid_key)
        uid_val = uid_key[len("uid_") :]
        # find packages matching this numeric uid that start with com.
        packages = [pkg for (uval, pkg) in uid_to_pkg.items()
                    if uval == uid_val and pkg.startswith("com.")]
        if packages:
            dist_usage = total_usage / len(packages)
            for pkg in packages:
                battery_usage[pkg] = battery_usage.get(pkg, 0) + dist_usage
                if pkg not in app_fg_usage:
                    app_fg_usage[pkg] = 0.0

    suspicious_details = []
    system_threshold_usage = 50.0
    tp_threshold_usage = 20.0
    threshold_ratio = 0.1

    # basic detection: usage vs. threshold, no advanced sensor detection here..
    for app, usage in battery_usage.items():
        fg = app_fg_usage.get(app, 0)
        ratio = (fg / usage) if usage > 0 else 0

        # if it's not com.* and is in the whitelist, skip entirely -- need to consider this maybe not best strategy checkin later TODO
        if app in SYSTEM_WHITELIST:
            continue

        # choose threshold based on type
        if app.startswith("com."):
            current_threshold = tp_threshold_usage
        else:
            # if it's not recognized as an android.* etc., but also not whitelisted
            current_threshold = system_threshold_usage

        if usage > current_threshold and ratio < 0.1:
            is_sys = is_system_app(app)
            diff = usage - current_threshold
            reason = (f"Battery usage {usage:.2f} exceeds threshold {current_threshold:.2f} by {diff:.2f}; "
                      f"foreground ratio {ratio:.2f} < {threshold_ratio}")
            if is_sys:
                reason += " (possibly a system process)"
            suspicious_details.append(f"{app}: {reason}")

    # final score includes wakelock/wakeup
    score = len(suspicious_details) * 10 + (wakeups_count + wakelocks_count) / 100.0

    return {
        "name": "Battery Drain Heuristic",
        "suspicious": suspicious_details,
        "score": score
    }
