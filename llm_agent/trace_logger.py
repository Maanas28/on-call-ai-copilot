import json
import sys
from datetime import datetime


def log_step(step: str, message: str, data=None):
    timestamp = datetime.now().strftime("%H:%M:%S")

    print("\n" + "=" * 80, file=sys.stderr)
    print(f"[{timestamp}] {step}", file=sys.stderr)
    print("-" * 80, file=sys.stderr)
    print(message, file=sys.stderr)

    if data is not None:
        print("\nData:", file=sys.stderr)
        print(json.dumps(data, indent=2, default=str), file=sys.stderr)

    print("=" * 80, file=sys.stderr)