import subprocess
import sys

scripts = ["save_prices.py", "get_inventory.py", "analyze_prices.py", "generate_report.py"]
for script in scripts:
    print(f"\n=== Running {script} ===")
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"ERROR in {script}:")
        print(result.stderr)
        break