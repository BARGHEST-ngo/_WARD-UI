import argparse
from barghest_ward.core.analyzer import run_all_heuristics
from barghest_ward.core.parser import parse_input_file
from barghest_ward.core.report import print_report

def main():
    parser = argparse.ArgumentParser(description="Barghest Ward - Android ADB Forensics Engine")
    parser.add_argument("--input", required=True, help="Path to the input dumpsys/checkin file")
    args = parser.parse_args()

    data = parse_input_file(args.input)
    results = run_all_heuristics(data)
    print_report(results)
