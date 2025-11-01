"""
Cost calculation engine for LLM pricing simulation.
"""
from typing import Optional
from .models import (
    Scenario,
    IntentGroup,
    FlowStep,
    ModelPrice,
    Frequency,
    TokenStrategy,
    SimulationResult
)


class CostCalculator:
    """Calculates costs for LLM usage scenarios."""

    def __init__(self, prices: dict[str, ModelPrice]):
        """
        Initialize calculator with price data.

        Args:
            prices: Dictionary mapping model ID to ModelPrice
        """
        self.prices = prices

    def calculate_scenario(self, scenario: Scenario) -> SimulationResult:
        """
        Calculate costs for a complete scenario.

        Args:
            scenario: The scenario to simulate

        Returns:
            Detailed simulation results
        """
        total_cost = 0.0
        total_calls = 0
        total_input_tokens = 0
        total_output_tokens = 0

        by_model = {model_id: 0.0 for model_id in scenario.models}
        by_intent_group = []
        by_step = {}

        # Process each intent group
        for group in scenario.intent_groups:
            group_cost, group_details = self._calculate_intent_group(
                group, scenario.models, scenario.days_per_month, scenario.price_overrides
            )

            by_intent_group.append({
                "name": group.name,
                "cost_usd": group_cost,
                "calls": group_details["calls"],
                "input_tokens": group_details["input_tokens"],
                "output_tokens": group_details["output_tokens"]
            })

            total_cost += group_cost
            total_calls += group_details["calls"]
            total_input_tokens += group_details["input_tokens"]
            total_output_tokens += group_details["output_tokens"]

            # Accumulate by model and step
            for model_id, cost in group_details["by_model"].items():
                by_model[model_id] = by_model.get(model_id, 0.0) + cost

            for step_name, cost in group_details["by_step"].items():
                by_step[step_name] = by_step.get(step_name, 0.0) + cost

        # Format results
        by_model_list = [{"model": mid, "cost_usd": round(cost, 2)} for mid, cost in by_model.items()]
        by_step_list = [{"step": name, "cost_usd": round(cost, 2)} for name, cost in by_step.items()]

        # Get price metadata
        meta = self._get_price_metadata()

        return SimulationResult(
            total_monthly_cost_usd=round(total_cost, 2),
            by_model=by_model_list,
            by_intent_group=by_intent_group,
            by_step=by_step_list,
            total_calls_per_month=total_calls,
            total_input_tokens_per_month=total_input_tokens,
            total_output_tokens_per_month=total_output_tokens,
            meta=meta
        )

    def _calculate_intent_group(
        self,
        group: IntentGroup,
        models: list[str],
        days_per_month: int,
        price_overrides: dict[str, dict[str, float]]
    ) -> tuple[float, dict]:
        """Calculate costs for a single intent group."""
        total_cost = 0.0
        by_model = {model_id: 0.0 for model_id in models}
        by_step = {}

        # Calculate runs per month based on frequency
        runs_per_month = self._get_runs_per_month(group.frequency, days_per_month, group.custom_runs_per_month)

        # Total prompts = intents * variants
        total_prompts = group.intents_count * group.variants_per_intent

        # Track previous step output for chained calculations
        previous_output_tokens = None

        # Process each flow step
        for step in group.flow_steps:
            step_cost, step_details = self._calculate_flow_step(
                step,
                models,
                total_prompts,
                runs_per_month,
                previous_output_tokens,
                price_overrides
            )

            total_cost += step_cost
            previous_output_tokens = step.expected_output_tokens

            # Accumulate by model
            for model_id, cost in step_details["by_model"].items():
                by_model[model_id] = by_model.get(model_id, 0.0) + cost

            # Accumulate by step
            by_step[step.name] = by_step.get(step.name, 0.0) + step_cost

        details = {
            "calls": sum(len(models) * total_prompts * runs_per_month * step.runs_per_prompt for step in group.flow_steps),
            "input_tokens": 0,  # Would need to track per step
            "output_tokens": 0,  # Would need to track per step
            "by_model": by_model,
            "by_step": by_step
        }

        return total_cost, details

    def _calculate_flow_step(
        self,
        step: FlowStep,
        models: list[str],
        total_prompts: int,
        runs_per_month: int,
        previous_output_tokens: Optional[int],
        price_overrides: dict[str, dict[str, float]]
    ) -> tuple[float, dict]:
        """Calculate costs for a single flow step across all models or a single model."""
        total_cost = 0.0
        by_model = {}

        # Determine input tokens based on strategy
        input_tokens = self._calculate_input_tokens(
            step.input_tokens_strategy,
            step.fixed_input_tokens,
            step.percent_of_previous,
            previous_output_tokens
        )

        output_tokens = step.expected_output_tokens

        # Determine which models to use for this step
        if step.uses_model == "current":
            # Use all models being tested (original behavior)
            models_for_step = models
        else:
            # Use a specific model for this step (e.g., extraction or judge)
            models_for_step = [step.uses_model]
            # Still need to account for processing output from ALL tested models
            # So we multiply total_prompts by the number of models being tested
            total_prompts = total_prompts * len(models)

        # Calculate for each model in this step
        for model_id in models_for_step:
            model_cost = self._calculate_single_call(
                model_id,
                input_tokens,
                output_tokens,
                step.use_cached_input,
                price_overrides.get(model_id, {})
            )

            # Multiply by quantity
            total_model_cost = (
                model_cost
                * total_prompts
                * runs_per_month
                * step.runs_per_prompt
            )

            by_model[model_id] = total_model_cost
            total_cost += total_model_cost

        details = {"by_model": by_model}
        return total_cost, details

    def _calculate_input_tokens(
        self,
        strategy: TokenStrategy,
        fixed_tokens: Optional[int],
        percent: Optional[float],
        previous_output: Optional[int]
    ) -> int:
        """Calculate input tokens based on strategy."""
        if strategy == TokenStrategy.FROM_PROMPT:
            # Would come from actual prompt - using fixed for now
            return fixed_tokens or 150

        elif strategy == TokenStrategy.FIXED:
            return fixed_tokens or 0

        elif strategy == TokenStrategy.FROM_PREVIOUS_OUTPUT:
            if previous_output is None:
                raise ValueError("Cannot use FROM_PREVIOUS_OUTPUT for first step")
            return previous_output

        elif strategy == TokenStrategy.PERCENT_OF_PREVIOUS_OUTPUT:
            if previous_output is None:
                raise ValueError("Cannot use PERCENT_OF_PREVIOUS_OUTPUT for first step")
            if percent is None:
                raise ValueError("percent_of_previous must be set for PERCENT_OF_PREVIOUS_OUTPUT")
            return int(previous_output * percent)

        return 0

    def _calculate_single_call(
        self,
        model_id: str,
        input_tokens: int,
        output_tokens: int,
        use_cached: bool,
        overrides: dict[str, float]
    ) -> float:
        """Calculate cost for a single LLM call."""
        # Get base prices
        if model_id not in self.prices:
            print(f"Warning: Model {model_id} not found in prices, using $0")
            return 0.0

        price = self.prices[model_id]

        # Apply overrides if provided
        input_price = overrides.get("input_per_million", price.input_per_million)
        output_price = overrides.get("output_per_million", price.output_per_million)

        # Use cached price if available and requested
        if use_cached and price.input_cached_per_million is not None:
            input_price = overrides.get("input_cached_per_million", price.input_cached_per_million)

        # Calculate cost
        input_cost = (input_tokens / 1_000_000) * input_price
        output_cost = (output_tokens / 1_000_000) * output_price

        return input_cost + output_cost

    def _get_runs_per_month(
        self,
        frequency: Frequency,
        days_per_month: int,
        custom_runs: Optional[int]
    ) -> int:
        """Calculate runs per month based on frequency."""
        if frequency == Frequency.HOURLY:
            return 24 * days_per_month
        elif frequency == Frequency.TWO_HOURLY:
            return 12 * days_per_month
        elif frequency == Frequency.FOUR_HOURLY:
            return 6 * days_per_month
        elif frequency == Frequency.DAILY:
            return days_per_month
        elif frequency == Frequency.WEEKLY:
            return days_per_month // 7
        elif frequency == Frequency.CUSTOM:
            if custom_runs is None:
                raise ValueError("custom_runs_per_month must be set for CUSTOM frequency")
            return custom_runs

        return days_per_month

    def _get_price_metadata(self) -> dict[str, str]:
        """Get metadata about price data."""
        if not self.prices:
            return {"price_source_updated_at": "unknown"}

        # Get the most recent update time
        latest_update = max(price.updated_at for price in self.prices.values())

        return {
            "price_source_updated_at": latest_update.isoformat(),
            "models_count": str(len(self.prices))
        }
