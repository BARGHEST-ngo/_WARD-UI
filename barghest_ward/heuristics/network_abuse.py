def run(data):
    netstats_text = data.get("netstats.txt", "")
    suspicious = []

    uid_to_pkg = {}
    current_section = None

    for line in netstats_text.splitlines():
        line = line.strip()

        # Track section
        if "mAppUidStatsMap" in line:
            current_section = "app_stats"
            continue
        if line.startswith("UID to package mapping"):
            current_section = "uid_map"
            continue

        if current_section == "uid_map":
            if "uid=" in line and "->" in line:
                parts = line.split("->")
                uid = parts[0].split("=")[-1].strip()
                pkg = parts[1].strip()
                uid_to_pkg[uid] = pkg

        elif current_section == "app_stats":
            if line and line[0].isdigit():
                parts = line.split()
                if len(parts) >= 5:
                    uid = parts[0]
                    try:
                        rx = int(parts[1])
                        tx = int(parts[3])
                        total_bytes = rx + tx
                        if total_bytes > 1_000_000_000:  # 1 GB threshold
                            pkg = uid_to_pkg.get(uid, f"uid_{uid}")
                            suspicious.append(
                                f"{pkg} (UID {uid}) used {total_bytes / 1e6:.2f}MB of network traffic"
                            )
                    except ValueError:
                        continue

    score = len(suspicious) * 10
    return {
        "name": "network_abuse",
        "suspicious": suspicious,
        "score": score
    }
