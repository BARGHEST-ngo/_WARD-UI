# barghest_ward/core/parse.py

def parse_batterystats_file(filepath: str) -> dict:
    data_rows = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) < 4:
                    continue

                line_type = parts[3].strip().lower()
                entry = {"line_type": line_type, "raw": parts}

                if line_type == "pwi":
                    if parts[4] == "uid" and len(parts) >= 8:
                        uid = parts[1].strip()
                        entry["app"] = "uid_" + uid
                        entry["usage"] = parts[5].strip()
                        entry["fg"] = parts[7].strip()  # Index 7 = foreground
                    elif len(parts) >= 6:
                        entry["app"] = parts[4].strip()
                        entry["usage"] = parts[5].strip()
                        entry["fg"] = parts[6].strip() if len(parts) > 6 else "0"

                elif line_type in ("wr", "kwl") and len(parts) >= 5:
                    entry["count"] = parts[4].strip()

                elif line_type == "uid" and len(parts) >= 6:
                    entry["uid"] = parts[4].strip()
                    entry["pkg"] = parts[5].strip()

                data_rows.append(entry)
        return {"parsed": data_rows}

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
