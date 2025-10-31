"""
Report generation for simulation results.
"""
import json
from typing import Literal
from .models import SimulationResult


class Reporter:
    """Generates reports from simulation results."""

    def generate_report(
        self,
        result: SimulationResult,
        format: Literal["text", "json", "markdown"] = "text"
    ) -> str:
        """
        Generate a report from simulation results.

        Args:
            result: Simulation results
            format: Output format

        Returns:
            Formatted report string
        """
        if format == "json":
            return self._format_json(result)
        elif format == "markdown":
            return self._format_markdown(result)
        else:
            return self._format_text(result)

    def generate_comparison(
        self,
        results: list[tuple[str, SimulationResult]],
        format: Literal["text", "json", "markdown"] = "text"
    ) -> str:
        """
        Generate a comparison report for multiple scenarios.

        Args:
            results: List of (scenario_name, result) tuples
            format: Output format

        Returns:
            Formatted comparison report
        """
        if format == "json":
            return self._format_comparison_json(results)
        elif format == "markdown":
            return self._format_comparison_markdown(results)
        else:
            return self._format_comparison_text(results)

    def _format_text(self, result: SimulationResult) -> str:
        """Format results as plain text."""
        lines = [
            "=" * 80,
            "LLM PRICING SIMULATION RESULTS",
            "=" * 80,
            "",
            f"Total Monthly Cost: ${result.total_monthly_cost_usd:,.2f}",
            f"Total API Calls: {result.total_calls_per_month:,}",
            f"Total Input Tokens: {result.total_input_tokens_per_month:,}",
            f"Total Output Tokens: {result.total_output_tokens_per_month:,}",
            "",
            "Cost Breakdown by Model:",
            "-" * 80,
        ]

        for item in sorted(result.by_model, key=lambda x: x["cost_usd"], reverse=True):
            lines.append(f"  {item['model']:<40} ${item['cost_usd']:>10,.2f}")

        lines.extend([
            "",
            "Cost Breakdown by Intent Group:",
            "-" * 80,
        ])

        for item in sorted(result.by_intent_group, key=lambda x: x["cost_usd"], reverse=True):
            lines.append(f"  {item['name']:<40} ${item['cost_usd']:>10,.2f}")
            if "calls" in item:
                lines.append(f"    Calls: {item['calls']:,}")

        lines.extend([
            "",
            "Cost Breakdown by Step:",
            "-" * 80,
        ])

        for item in sorted(result.by_step, key=lambda x: x["cost_usd"], reverse=True):
            lines.append(f"  {item['step']:<40} ${item['cost_usd']:>10,.2f}")

        lines.extend([
            "",
            "Metadata:",
            "-" * 80,
        ])

        for key, value in result.meta.items():
            lines.append(f"  {key}: {value}")

        lines.append("=" * 80)

        return "\n".join(lines)

    def _format_json(self, result: SimulationResult) -> str:
        """Format results as JSON."""
        return json.dumps(result.model_dump(), indent=2)

    def _format_markdown(self, result: SimulationResult) -> str:
        """Format results as Markdown."""
        lines = [
            "# LLM Pricing Simulation Results",
            "",
            "## Summary",
            "",
            f"- **Total Monthly Cost**: ${result.total_monthly_cost_usd:,.2f}",
            f"- **Total API Calls**: {result.total_calls_per_month:,}",
            f"- **Total Input Tokens**: {result.total_input_tokens_per_month:,}",
            f"- **Total Output Tokens**: {result.total_output_tokens_per_month:,}",
            "",
            "## Cost by Model",
            "",
            "| Model | Cost (USD) |",
            "|-------|------------|",
        ]

        for item in sorted(result.by_model, key=lambda x: x["cost_usd"], reverse=True):
            lines.append(f"| {item['model']} | ${item['cost_usd']:,.2f} |")

        lines.extend([
            "",
            "## Cost by Intent Group",
            "",
            "| Intent Group | Cost (USD) | Calls |",
            "|--------------|------------|-------|",
        ])

        for item in sorted(result.by_intent_group, key=lambda x: x["cost_usd"], reverse=True):
            calls = item.get("calls", "N/A")
            lines.append(f"| {item['name']} | ${item['cost_usd']:,.2f} | {calls:,} |")

        lines.extend([
            "",
            "## Cost by Step",
            "",
            "| Step | Cost (USD) |",
            "|------|------------|",
        ])

        for item in sorted(result.by_step, key=lambda x: x["cost_usd"], reverse=True):
            lines.append(f"| {item['step']} | ${item['cost_usd']:,.2f} |")

        lines.extend([
            "",
            "## Metadata",
            "",
        ])

        for key, value in result.meta.items():
            lines.append(f"- **{key}**: {value}")

        return "\n".join(lines)

    def _format_comparison_text(self, results: list[tuple[str, SimulationResult]]) -> str:
        """Format comparison as plain text."""
        lines = [
            "=" * 80,
            "SCENARIO COMPARISON",
            "=" * 80,
            "",
        ]

        # Summary table
        lines.append(f"{'Scenario':<45} {'Monthly Cost':>15} {'Calls':>15}")
        lines.append("-" * 80)

        for name, result in sorted(results, key=lambda x: x[1].total_monthly_cost_usd, reverse=True):
            lines.append(
                f"{name:<45} ${result.total_monthly_cost_usd:>14,.2f} {result.total_calls_per_month:>15,}"
            )

        lines.extend(["", "=" * 80, ""])

        # Individual scenario details
        for name, result in results:
            lines.extend([
                f"\n{name}",
                "-" * len(name),
                self._format_text(result),
                ""
            ])

        return "\n".join(lines)

    def _format_comparison_json(self, results: list[tuple[str, SimulationResult]]) -> str:
        """Format comparison as JSON."""
        comparison = {
            "scenarios": [
                {
                    "name": name,
                    "results": result.model_dump()
                }
                for name, result in results
            ]
        }
        return json.dumps(comparison, indent=2)

    def _format_comparison_markdown(self, results: list[tuple[str, SimulationResult]]) -> str:
        """Format comparison as Markdown."""
        lines = [
            "# Scenario Comparison",
            "",
            "## Summary",
            "",
            "| Scenario | Monthly Cost | Calls/Month |",
            "|----------|--------------|-------------|",
        ]

        for name, result in sorted(results, key=lambda x: x[1].total_monthly_cost_usd, reverse=True):
            lines.append(
                f"| {name} | ${result.total_monthly_cost_usd:,.2f} | {result.total_calls_per_month:,} |"
            )

        lines.append("")

        # Individual details
        for name, result in results:
            lines.extend([
                f"## {name}",
                "",
                self._format_markdown(result),
                ""
            ])

        return "\n".join(lines)
