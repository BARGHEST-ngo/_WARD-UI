from importlib import import_module

HEURISTICS = [
    'barghest_ward.heuristics.battery_drain',
]

def run_all_heuristics(data):
    results = []
    for h_path in HEURISTICS:
        mod = import_module(h_path)
        results.append(mod.run(data))
    return results
