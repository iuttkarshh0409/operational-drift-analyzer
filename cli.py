# cli.py
import argparse

from app import run_analysis
from db.repositories.drift_repo import fetch_latest_snapshot


def show_latest():
    snapshot = fetch_latest_snapshot()

    if not snapshot:
        print("No drift analysis found.")
        return

    print("\nOperational Drift — Summary")
    print("-" * 50)

    print(f"Window                : {snapshot['window_days']} days")
    print(f"Analyzed at           : {snapshot['analyzed_at']}")

    # --------------------------------------------------
    # Retry Behavior
    # --------------------------------------------------
    print("\nRetry Behavior")
    print("-" * 50)

    print(f"Primary signal        : {snapshot['primary_signal']}")

    if snapshot.get("secondary_signal"):
        print(f"Secondary signal      : {snapshot['secondary_signal']}")

    # --------------------------------------------------
    # Dead Events
    # --------------------------------------------------
    print("\nDead Events")
    print("-" * 50)

    # IMPORTANT:
    # None = not enough data
    # 0.0   = valid computed value
    if snapshot["dead_event_ratio"] is None:
        print("Dead event ratio      : Not enough data")
    else:
        print(f"Dead event ratio      : {snapshot['dead_event_ratio']}")
        print(f"Dead confidence       : {snapshot['dead_event_confidence']}")

    # --------------------------------------------------
    # Assessment
    # --------------------------------------------------
    print("\nAssessment")
    print("-" * 50)

    print(f"Risk level            : {snapshot['risk_level']}")
    print(f"Confidence            : {snapshot['confidence']}")

    # --------------------------------------------------
    # Interpretation
    # --------------------------------------------------
    print("\nInterpretation")
    print("-" * 50)
    print(snapshot["explanation"])


def main():
    parser = argparse.ArgumentParser(
        description="Operational Drift Analyzer CLI"
    )

    parser.add_argument(
        "--drift",
        action="store_true",
        help="Run drift analysis now"
    )

    parser.add_argument(
        "--latest",
        action="store_true",
        help="Show latest drift snapshot"
    )

    args = parser.parse_args()

    if args.drift:
        run_analysis()

    if args.latest:
        show_latest()

    if not args.drift and not args.latest:
        parser.print_help()


if __name__ == "__main__":
    main()
