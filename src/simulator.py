"""
Main simulation orchestrator.
"""
import json
from pathlib import Path
from typing import Optional
from .models import Scenario, SimulationResult
from .price_fetcher import PriceFetcher
from .calculator import CostCalculator


class Simulator:
    """Orchestrates LLM pricing simulations."""

    def __init__(self, cache_dir: Optional[Path] = None):
        self.price_fetcher = PriceFetcher(cache_dir)
        self.prices = None
        self.calculator = None

    def load_prices(self, force_refresh: bool = False) -> None:
        """
        Load price data from remote/cache.

        Args:
            force_refresh: Force fetch from remote
        """
        self.prices = self.price_fetcher.fetch_prices(force_refresh)
        self.calculator = CostCalculator(self.prices)
        print(f"Loaded prices for {len(self.prices)} models")

    def load_scenario(self, scenario_path: Path) -> Scenario:
        """
        Load scenario from JSON file.

        Args:
            scenario_path: Path to scenario JSON file

        Returns:
            Loaded scenario
        """
        with open(scenario_path) as f:
            data = json.load(f)

        return Scenario(**data)

    def run_scenario(self, scenario: Scenario) -> SimulationResult:
        """
        Run a simulation for a scenario.

        Args:
            scenario: The scenario to simulate

        Returns:
            Simulation results
        """
        if self.calculator is None:
            raise RuntimeError("Must call load_prices() before running scenarios")

        print(f"\nRunning scenario: {scenario.name}")
        print(f"Models: {', '.join(scenario.models)}")
        print(f"Intent groups: {len(scenario.intent_groups)}")

        result = self.calculator.calculate_scenario(scenario)

        return result

    def run_scenario_file(self, scenario_path: Path, force_refresh: bool = False) -> SimulationResult:
        """
        Convenience method to load prices, load scenario, and run simulation.

        Args:
            scenario_path: Path to scenario JSON
            force_refresh: Force refresh price data

        Returns:
            Simulation results
        """
        # Load prices if not already loaded
        if self.prices is None or force_refresh:
            self.load_prices(force_refresh)

        # Load and run scenario
        scenario = self.load_scenario(scenario_path)
        return self.run_scenario(scenario)

    def compare_scenarios(self, scenario_paths: list[Path]) -> list[tuple[str, SimulationResult]]:
        """
        Run multiple scenarios and return results for comparison.

        Args:
            scenario_paths: List of scenario file paths

        Returns:
            List of (scenario_name, result) tuples
        """
        if self.prices is None:
            self.load_prices()

        results = []
        for path in scenario_paths:
            scenario = self.load_scenario(path)
            result = self.run_scenario(scenario)
            results.append((scenario.name, result))

        return results
