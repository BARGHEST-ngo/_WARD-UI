import importlib

HEURISTICS = [
    'barghest_ward.heuristics.battery_drain',
    'barghest_ward.heuristics.network_abuse',
    'barghest_ward.heuristics.location_misuse',
    'barghest_ward.heuristics.sensitive_sensor_usage',
    'barghest_ward.heuristics.wakelock_abuse'
]

def run_all_heuristics(data):
    results = []
    for h_path in HEURISTICS:
        try:
            mod = importlib.import_module(h_path)
            result = mod.run(data)
            results.append(result)
        except Exception as e:
            results.append({
                "name": h_path.split('.')[-1],
                "error": str(e),
                "suspicious": [],
                "score": 0,
            })
    return results
