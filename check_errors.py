import csv
import sys

def check_error_rate(jtl_file, threshold=2.0):
    total = 0
    errors = 0

    with open(jtl_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            if row.get('success', 'true').strip().lower() == 'false':
                errors += 1

    if total == 0:
        print("0.00")
        return 0.0

    error_rate = (errors / total) * 100
    print(f"{error_rate:.2f}")

    if error_rate > threshold:
        sys.exit(1)

    return error_rate

if __name__ == "__main__":
    jtl_path  = sys.argv[1] if len(sys.argv) > 1 else "results\\results.jtl"
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    check_error_rate(jtl_path, threshold)