def print_report(results):
    print("\n===== Barghest Ward Report =====")
    for result in results:
        print(f"\n[+] {result['name']}")
        if result['suspicious']:
            for item in result['suspicious']:
                print(f" - Suspicious: {item}")
        else:
            print(" - No suspicious findings.")
