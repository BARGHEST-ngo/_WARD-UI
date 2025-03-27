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
            except ValueError:
                usage = 0.0
            battery_usage[app] = battery_usage.get(app, 0) + usage
            try:
                fg = float(row.get("fg", 0))
            except ValueError:
                fg = 0.0
            app_fg_usage[app] = app_fg_usage.get(app, 0) + fg

        elif line_type == "wr":
            try:
                count = int(row.get("count", 1))
            except ValueError:
                count = 1
            wakeups_count += count

        elif line_type == "kwl":
            try:
                count = int(row.get("count", 1))
            except ValueError:
                count = 1
            wakelocks_count += count

        elif line_type == "uid":
            uid_val = row.get("uid", "")
            pkg = row.get("pkg", "unknown")
            uid_to_pkg[uid_val] = pkg

    uid_keys = [key for key in battery_usage if key.startswith("uid_")]
    for uid_key in uid_keys:
        total_usage = battery_usage.pop(uid_key)
        uid_val = uid_key[len("uid_"):]
        packages = [pkg for (uid_map, pkg) in uid_to_pkg.items() if uid_map == uid_val and pkg.startswith("com.")]
        if packages:
            distributed = total_usage / len(packages)
            for pkg in packages:
                battery_usage[pkg] = battery_usage.get(pkg, 0) + distributed
                if pkg not in app_fg_usage:
                    app_fg_usage[pkg] = 0.0

    suspicious_details = []
    system_threshold_usage = 50.0
    tp_threshold_usage = 20.0
    threshold_ratio = 0.1

    for app, usage in battery_usage.items():
        fg = app_fg_usage.get(app, 0)
        ratio = (fg / usage) if usage > 0 else 0
        if app.startswith("com."):
            current_threshold = tp_threshold_usage
        else:
            if app in SYSTEM_WHITELIST:
                continue
            current_threshold = system_threshold_usage

        if usage > current_threshold and ratio < threshold_ratio:
            suspicion_score = (usage - current_threshold) * (threshold_ratio - ratio)
            is_system = is_system_app(app)
            reason = (f"Battery usage {usage:.2f} exceeds threshold {current_threshold:.2f} by {usage - current_threshold:.2f}; "
                      f"foreground ratio {ratio:.2f} is below threshold {threshold_ratio:.2f}")
            if is_system:
                reason += " (possibly a system process)"
            suspicious_details.append(f"{app}: {reason}")

    score = len(suspicious_details) * 10 + (wakeups_count + wakelocks_count) / 100.0

    return {
        "name": "Battery Drain Heuristic",
        "suspicious": suspicious_details,
        "score": score
    }
