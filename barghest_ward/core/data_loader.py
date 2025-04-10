import os
from barghest_ward.core.parse import parse_batterystats_file

PARSERS = {
    "batterystats-checkin": parse_batterystats_file,
    # Add more parsers as needed
}

def load_collected_logs(log_dir):
    data = {}
    loaded_files = []

    for filename in os.listdir(log_dir):
        if not filename.endswith(".txt"):
            continue

        name = filename.removesuffix(".txt")
        path = os.path.join(log_dir, filename)

        try:
            if name in PARSERS:
                data[name] = PARSERS[name](path)
            else:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    data[name] = {"raw": f.readlines()}
            loaded_files.append(filename)
        except Exception:
            data[name] = {"raw": []}

    print(f"[✓] Loaded {len(loaded_files)} logs from '{log_dir}'")
    return data
