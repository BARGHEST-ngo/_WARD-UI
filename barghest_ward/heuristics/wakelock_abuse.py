import re
from collections import defaultdict

SENSITIVE_WAKELOCKS = {
    "*alarm*", "*location*", "AudioMix", "*launch*", "*job*/", "*sync*"
}

SERVICE_WHITELIST = {
    "com.google.android.apps.turbo",           # Device Health Services
    "com.google.android.gms",                  # Google Play Services
    "com.android.vending",                     # Google Play Store
    "com.google.android.partnersetup",         # Google Setup
    "com.google.android.as",                   # Android Services Intelligence
    "com.google.android.apps.restore",         # Restore service
    "com.google.android.apps.tachyon",         # Google Meet
    "com.google.android.calendar",             # Google Calendar
    "com.google.android.apps.maps",            # Google Maps
    "com.google.android.youtube",              # YouTube
    "com.google.android.adservices.api",       # AdServices API
    "com.google.android.cellbroadcastreceiver",# Emergency Alerts
    "com.google.android.videos",               # Google TV/Play Movies
    "com.android.chrome",                      # Chrome
    "com.samsung.android.vtcamerasettings",
    "com.sec.phone",
    "media.extractor",
    "gpuservice",
    "adbd",
    "com.samsung.android.beaconmanager",
    "com.sec.hearingadjust",
    "com.sec.android.provider.badge",
    "com.samsung.android.bixby.agent",
    "com.samsung.android.game.gos",
    "com.microsoft.skydrive",
    "com.android.providers.calendar",
    "com.sec.android.app.camera",
    "com.samsung.android.scs",
    "com.osp.app.signin",
    "com.samsung.android.app.contacts",
    "com.samsung.android.mcfserver",
    "com.samsung.android.samsungpass",
    "com.samsung.android.smartcallprovider",
    "com.sec.android.app.soundalive",
    "com.sec.android.app.launcher",
    "com.microsoft.appmanager",
    "com.sec.android.easyonehand",
    "com.sec.android.app.clockpackage",
    "com.samsung.android.fast",
    "com.samsung.android.calendar",
    "com.samsung.android.app.reminder",
    "com.samsung.android.oneconnect",
    "com.samsung.cmh",
    "com.samsung.android.ce",
    "com.samsung.android.smartsuggestions"
}


KERNEL_LEVEL_APPS = {"unknown"}
KERNEL_PREFIXES = ("kworker/",)


def is_kernel_level(app_name):
    return app_name in KERNEL_LEVEL_APPS or any(app_name.startswith(pfx) for pfx in KERNEL_PREFIXES)


def simplify_tag(tag):
    if "*job*/" in tag or "JobService" in tag:
        return "JobScheduler"
    elif "*sync*" in tag:
        return "*sync*"
    elif "*alarm*" in tag:
        return "*alarm*"
    elif "*location*" in tag:
        return "*location*"
    elif "*launch*" in tag:
        return "*launch*"
    elif "AudioMix" in tag:
        return "AudioMix"
    else:
        return None  # Filter out noise


def run(data):
    batterystats = data.get("batterystats", {})
    lines = batterystats.get("raw", [])

    wakelock_counts = defaultdict(int)
    sensitive_triggers = defaultdict(set)
    current_app = None

    for line in lines:
        app_match = re.match(r"\s*(Apk|Proc)\s+([^\s:]+):", line)
        if app_match:
            current_app = app_match.group(2)
            continue

        if "Wake lock" in line:
            match = re.search(r"Wake lock\s+([^:]+)", line)
            if match:
                wakelock_name = match.group(1).strip()
                app_name = current_app or "unknown"
                wakelock_counts[app_name] += 1

                for tag in SENSITIVE_WAKELOCKS:
                    if tag in wakelock_name:
                        sensitive_triggers[app_name].add(wakelock_name)

    suspicious_apps = []
    for app, count in wakelock_counts.items():
        if app in STATIC_WHITELIST:
            continue

        has_sensitive = bool(sensitive_triggers[app])
        tags = sorted(sensitive_triggers[app])
        summarized_tags = ", ".join(tags[:3]) + (f" (+{len(tags) - 3} more)" if len(tags) > 3 else "") if tags else "None"

        if count >= 3 or (count <= 2 and has_sensitive):
            entry = f"- App: {app} ({count} wakelocks)\n  Tags: {summarized_tags}"
            if app == "unknown" or app.startswith("kworker/"):
                entry += "\n  [!] Likely system/kernel process — further analysis may be needed."
            suspicious_apps.append(entry)

    score = len(suspicious_apps) * 5

    return {
        "name": "Wakelock Abuse Heuristic",
        "suspicious": suspicious_apps,
        "score": score
    }
