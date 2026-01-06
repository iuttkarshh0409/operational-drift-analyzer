# cli.py
import argparse

from app import run_analysis
from db.repositories.drift_repo import fetch_latest_snapshot


def show_latest():
    snapshot = fetch_latest_snapshot()

    if not snapshot:
        print("No drift analysis found.")
        return

    print("\nOperational Drift Snapshot")
    print("-" * 30)

    print(f"Analyzed at : {snapshot['analyzed_at']}")
    print(f"Window     : {snapshot['window_days']} days")
    print(f"Risk level : {snapshot['risk_level']}")
    print(f"Confidence : {snapshot['confidence']}")
    print(f"Signal     : {snapshot['primary_signal']}")

    if snapshot.get("secondary_signal"):
        print(f"Secondary  : {snapshot['secondary_signal']}")

    # ---------- NEW: Dead Event Ratio visibility ----------
    dead_ratio = snapshot.get("dead_event_ratio")
    dead_conf = snapshot.get("dead_event_confidence")

    if dead_ratio is None:
        print("Dead Event Ratio : UNKNOWN (insufficient data)")
    else:
        print(
            f"Dead Event Ratio : {round(dead_ratio * 100, 2)}% "
            f"(confidence: {dead_conf})"
        )

    print(f"\nExplanation:\n{snapshot['explanation']}")


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
