#!/usr/bin/env python
"""
Run all pipeline scripts in order. Used when notebooks are not available.
This is the fallback path — attendees who don't use Jupyter can run:

    make test
    # or
    uv run python scripts/run_all.py

Each script is self-contained and can be run independently.
"""
import subprocess
import sys
from pathlib import Path

SCRIPTS = [
    "scripts/01_ingestion.py",
    "scripts/02_retrieval.py",
    "scripts/03_generation.py",
    "scripts/04_evaluation.py",
    "scripts/05_advanced.py",
]


def run_script(path: str) -> bool:
    print(f"\n{'=' * 60}")
    print(f"  Running: {path}")
    print(f"{'=' * 60}")
    result = subprocess.run(
        [sys.executable, path],
        capture_output=False,
        text=True,
    )
    if result.returncode != 0:
        print(f"\n[FAIL] {path}")
        return False
    print(f"\n[OK] PASSED: {path}")
    return True


if __name__ == "__main__":
    results = []
    for script in SCRIPTS:
        if not Path(script).exists():
            print(f"  Skipping {script} (not found)")
            continue
        results.append(run_script(script))

    print(f"\n{'=' * 60}")
    passed = sum(results)
    total = len(results)
    print(f"  Results: {passed}/{total} scripts passed")
    if passed == total:
        print("  [OK] All scripts passed!")
    else:
        print("  [FAIL] Some scripts failed. Check output above.")
    sys.exit(0 if passed == total else 1)
