# barghest_ward/core/collect.py

import os
import subprocess
import sys

ADB_COMMANDS = {
    "batterystats.txt": "adb shell dumpsys batterystats",
    "batterystats-checkin.txt": "adb shell dumpsys batterystats --checkin",
    "logcat.txt": "adb logcat -v threadtime -d",
    "services.txt": "adb shell dumpsys activity services",
    "power.txt": "adb shell dumpsys power",
    "alarm.txt": "adb shell dumpsys alarm",
    "idle.txt": "adb shell dumpsys deviceidle",
    "connectivity.txt": "adb shell dumpsys connectivity",
    "netstats.txt": "adb shell dumpsys netstats",
    "network_policy.txt": "adb shell dumpsys network_policy",
    "location.txt": "adb shell dumpsys location",
    "usagestats.txt": "adb shell dumpsys usagestats",
    "usage-events.txt": "adb shell cmd usagestats query events",
    "prop.txt": "adb shell getprop",
    "full-dumpsys.txt": "adb shell dumpsys"
}


def collect_adb_data(output_dir: str):
    """
    Run the specified ADB commands and save results into output_dir.
    Creates directory if it doesn't exist.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename, cmd in ADB_COMMANDS.items():
        filepath = os.path.join(output_dir, filename)
        print(f"[+] Collecting {filename} via: {cmd}")
        with open(filepath, 'wb') as f:
            proc = subprocess.run(cmd.split(), stdout=f, stderr=subprocess.PIPE)
            if proc.returncode != 0:
                print(f"    [!] Command failed for {filename}: {proc.stderr.decode('utf-8', 'replace')}")
            else:
                print(f"    [✓] Saved -> {filepath}")
