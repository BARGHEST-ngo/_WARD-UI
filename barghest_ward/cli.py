import os
import click
from barghest_ward.core.analyzer import run_all_heuristics
from barghest_ward.core.data_loader import load_collected_logs
from barghest_ward.core.report import print_report

DEFAULT_LOG_DIR = "adb-logs"

@click.group()
def cli():
    """Barghest Ward - Mobile Spyware Forensics Toolkit"""
    pass

@cli.command()
@click.argument("log_dir", required=False, default=DEFAULT_LOG_DIR)
@click.option("--json", "json_out", type=click.Path(), help="Export findings to a JSON file.")
def analyze(log_dir, json_out):
    """Analyze logs in the specified directory."""
    if not os.path.exists(log_dir):
        print(f"[!] Log directory '{log_dir}' not found.")
        return

    print(f"[+] Analyzing logs in '{log_dir}' ...")

    try:
        data = load_collected_logs(log_dir)
        results = run_all_heuristics(data)

        print_report(results)

        if json_out:
            import json
            with open(json_out, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
            print(f"[✓] Results exported to {json_out}")

    except Exception as e:
        print(f"[!] Analysis error: {e}")

@cli.command()
@click.argument("output_dir", required=False, default=DEFAULT_LOG_DIR)
def collect(output_dir):
    """Collect ADB logs into the specified directory."""
    from barghest_ward.core.collect import collect_adb_data
    print(f"[+] Collecting logs to '{output_dir}'")
    collect_adb_data(output_dir)
    print("[✓] Collection complete.")

def main():
    cli()

if __name__ == "__main__":
    main()
