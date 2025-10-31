#!/usr/bin/env python3
"""
CLI tool to run LLM pricing simulations.

Usage:
    python run_simulation.py scenarios/jtbd_1_brand_category.json
    python run_simulation.py --all
    python run_simulation.py --compare scenarios/*.json
"""
import argparse
import sys
from pathlib import Path
from src.simulator import Simulator
from src.reporter import Reporter


def main():
    parser = argparse.ArgumentParser(description="Run LLM pricing simulations")
    parser.add_argument(
        "scenario",
        nargs="?",
        help="Path to scenario JSON file"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all scenarios in scenarios/ directory"
    )
    parser.add_argument(
        "--compare",
        nargs="+",
        help="Compare multiple scenarios"
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Force refresh price data from remote"
    )
    parser.add_argument(
        "--output",
        choices=["text", "json", "markdown"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--save",
        help="Save results to file"
    )

    args = parser.parse_args()

    # Validate arguments
    if not any([args.scenario, args.all, args.compare]):
        parser.print_help()
        sys.exit(1)

    # Initialize simulator and reporter
    simulator = Simulator()
    reporter = Reporter()

    try:
        # Handle different modes
        if args.all:
            # Run all scenarios
            scenario_dir = Path("scenarios")
            scenario_files = [f for f in scenario_dir.glob("*.json") if f.name != "template.json"]

            if not scenario_files:
                print("No scenario files found in scenarios/")
                sys.exit(1)

            print(f"Running {len(scenario_files)} scenarios...\n")
            results = simulator.compare_scenarios(scenario_files)

            # Generate comparison report
            output = reporter.generate_comparison(results, format=args.output)

        elif args.compare:
            # Compare specific scenarios
            scenario_files = [Path(p) for p in args.compare]

            # Validate files exist
            for f in scenario_files:
                if not f.exists():
                    print(f"Error: Scenario file not found: {f}")
                    sys.exit(1)

            results = simulator.compare_scenarios(scenario_files)
            output = reporter.generate_comparison(results, format=args.output)

        else:
            # Run single scenario
            scenario_path = Path(args.scenario)

            if not scenario_path.exists():
                print(f"Error: Scenario file not found: {scenario_path}")
                sys.exit(1)

            result = simulator.run_scenario_file(scenario_path, force_refresh=args.refresh)
            output = reporter.generate_report(result, format=args.output)

        # Output results
        print(output)

        # Save to file if requested
        if args.save:
            save_path = Path(args.save)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, "w") as f:
                f.write(output)
            print(f"\nResults saved to {save_path}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
