# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based cost estimation tool for LLM competitive intelligence products. It simulates monthly API costs by running "prompt batteries" (collections of questions/concepts) across multiple LLM providers to understand unit economics.

**Key concept**: Each scenario runs ALL prompts through ALL specified models. For example, 50 questions × 3 models × 30 days = 4,500 calls per model (13,500 total). This simulates asking the same questions to different LLMs to compare their responses.

## Core Commands

```bash
# Setup
uv sync

# Run simulations (use 'uv run' for all Python commands)
uv run python run_simulation.py scenarios/jtbd_1_brand_category.json
uv run python run_simulation.py --all
uv run python run_simulation.py --compare scenarios/jtbd_*.json

# Output formats
uv run python run_simulation.py --all --output markdown --save results/report.md
uv run python run_simulation.py scenarios/jtbd_1.json --output json

# Force refresh pricing data
uv run python run_simulation.py scenarios/jtbd_1.json --refresh
```

## Architecture

### Data Flow

1. **PriceFetcher** → Fetches real-time pricing from simonw/llm-prices API
   - Caches to `data/price_cache.json` (24hr TTL)
   - Applies manual overrides from `data/overrides.json`
   - Returns `dict[model_id, ModelPrice]`

2. **Simulator** → Orchestrates the simulation
   - Loads scenario JSON files
   - Initializes CostCalculator with price data
   - Runs scenarios through calculator

3. **CostCalculator** → Core calculation engine
   - For each intent group: calculates `prompts × models × frequency × steps`
   - Multiplies by token counts and prices per million tokens
   - Returns breakdown by model, intent group, and flow step

4. **Reporter** → Generates output
   - Formats results as text, JSON, or Markdown
   - Creates comparison reports for multiple scenarios

### Critical Calculation Logic

**Multi-model multiplication** happens in `calculator.py:_calculate_flow_step()`:
```python
# This is the key: EACH model processes ALL prompts
total_prompts = intents_count × variants_per_intent
for model_id in models:  # Multiplies cost across all models
    cost = calculate_single_call(...)
    total_cost = cost × total_prompts × runs_per_month × runs_per_prompt
```

**Token strategies** determine input token counts:
- `fixed`: Uses `fixed_input_tokens` value
- `from_previous_output`: Chains flow steps (extraction uses answer's output tokens)
- `percent_of_previous_output`: Takes percentage of previous step's output

**Frequency mapping** in `calculator.py:_get_runs_per_month()`:
- `hourly`: 24 × days_per_month
- `2_hourly`: 12 × days_per_month
- `daily`: days_per_month
- `weekly`: days_per_month ÷ 7

### Model IDs

Model IDs in scenarios must match simonw/llm-prices exactly:
- ✅ `"gpt-4o"` (correct)
- ❌ `"openai-gpt-4o"` (wrong - adds vendor prefix)
- ✅ `"claude-3.7-sonnet"` (correct)
- ✅ `"gemini-2.5-flash"` (correct)

Check current IDs: `curl -s https://www.llm-prices.com/current-v1.json | jq '.prices[].id'`

## Scenario Structure

Scenarios are JSON files in `scenarios/`. Use `template.json` as starting point.

**Key fields:**
- `models`: Array of model IDs - ALL prompts run through ALL models
- `intent_groups`: Can have multiple groups with different frequencies
- `flow_steps`: Processing pipeline (answer → extract → judge, etc.)
- `price_overrides`: Per-model price adjustments for "what-if" analysis

**Token strategies:**
- Use `from_previous_output` for extraction/judge steps that process previous LLM output
- Use `fixed` with `fixed_input_tokens` for initial answer steps
- Use `percent_of_previous_output` with `percent_of_previous` for partial processing

## Common Modifications

### Adding a new scenario
1. Copy `scenarios/template.json`
2. Update model IDs (must match simonw/llm-prices)
3. Set `intents_count` and `variants_per_intent` (multiplied together)
4. Choose frequency: `hourly`, `2_hourly`, `4_hourly`, `daily`, `weekly`
5. Define flow steps with token strategies

### Adding price overrides
Edit `data/overrides.json`:
```json
{
  "gpt-4o": {
    "input_per_million": 5.0,
    "output_per_million": 15.0
  }
}
```

### Adding new frequency patterns
1. Add enum to `src/models.py:Frequency`
2. Add case to `src/calculator.py:_get_runs_per_month()`

### Adding new token strategies
1. Add enum to `src/models.py:TokenStrategy`
2. Add logic to `src/calculator.py:_calculate_input_tokens()`

## Data Sources

- **Price data**: https://www.llm-prices.com/current-v1.json (78+ models)
- **API structure**: `{"updated_at": "...", "prices": [{"id": "...", "vendor": "...", "input": float, "output": float, ...}]}`
- **Cache location**: `data/price_cache.json` (auto-generated)
- **Historical data**: https://www.llm-prices.com/historical-v1.json (not yet implemented)

## Known Limitations

- Token counts are estimated via `fixed_input_tokens`, not actual (tiktoken integration needed)
- Cached input pricing is modeled but not fully utilized (would need variant-aware caching)
- No support for image/audio/batch pricing
- Provider-specific features (committed use discounts, tiering) not modeled
