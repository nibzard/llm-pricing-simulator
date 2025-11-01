# LLM Pricing Simulator - Project Summary

## What This Is

A Python-based research tool to estimate monthly API costs for running an LLM-powered competitive intelligence/brand monitoring product. It models different usage patterns (JTBDs) across multiple providers and provides detailed cost breakdowns.

## What's Built

### Core Components

1. **Price Fetcher** (`src/price_fetcher.py`)
   - Fetches real-time pricing from simonw/llm-prices API
   - Caches data locally (24hr TTL)
   - Supports manual price overrides

2. **Cost Calculator** (`src/calculator.py`)
   - Token-based cost calculation
   - Multi-pass flow support (answer → extract → judge)
   - Handles different frequency patterns (hourly → weekly)

3. **Simulator** (`src/simulator.py`)
   - Orchestrates simulations
   - Loads scenarios from JSON
   - Runs multi-scenario comparisons

4. **Reporter** (`src/reporter.py`)
   - Text, JSON, and Markdown output
   - Cost breakdowns by model, intent group, and step
   - Comparison reports across scenarios

5. **Dashboard** (`dashboard.py`)
   - Interactive Streamlit web interface
   - Real-time scenario builder
   - Visual cost analysis with Plotly charts
   - Pricing strategy calculator
   - Multi-scenario comparison views

### Scenarios

4 pre-built JTBD scenarios:
- **JTBD 1**: Brand/category monitoring (30 intents, daily, $58/mo)
- **JTBD 2**: Ranking alerts (50 intents, mixed freq, $1,046/mo)
- **JTBD 3**: Model comparison (80 intents, 2-hourly, $3,891/mo)
- **JTBD 4**: Competitor discovery (40 intents, daily, $176/mo)

## Quick Start

```bash
# Setup
uv sync

# Interactive dashboard (recommended)
uv run streamlit run dashboard.py

# CLI: Run single scenario
uv run python run_simulation.py scenarios/jtbd_1_brand_category.json

# CLI: Run all scenarios
uv run python run_simulation.py --all

# CLI: Save comparison report
uv run python run_simulation.py --all --output markdown --save results/report.md
```

## Key Results

See `results/KEY_INSIGHTS.md` for detailed analysis.

**TL;DR**:
- Monthly costs range from $58 (light use) to $3,891 (heavy use)
- Frequency is the biggest cost driver (hourly = 15x daily)
- Gemini is 20-40x cheaper than Claude Sonnet
- Unit economics are viable with 3-5x markup

## What You Can Do With This

### Research Tasks

✅ **Cost estimation**: Model different usage patterns
✅ **Sensitivity analysis**: Test "what if" scenarios
✅ **Model comparison**: Find cheapest option for each task
✅ **Pricing strategy**: Calculate unit costs for SaaS tiers
✅ **Historical analysis**: Compare costs over time (add historical data)

### Customization

1. **New scenarios**: Copy `scenarios/template.json`
2. **Price overrides**: Edit `data/overrides.json`
3. **Token estimates**: Update `fixed_input_tokens` values
4. **Frequencies**: Add new patterns in `models.py`

## Project Structure

```
llm-pricing-simulator/
├── src/
│   ├── models.py           # Pydantic models
│   ├── price_fetcher.py    # Fetch/cache pricing
│   ├── calculator.py       # Cost calculations
│   ├── simulator.py        # Simulation orchestration
│   └── reporter.py         # Report generation
├── scenarios/              # JTBD scenarios (JSON)
├── data/
│   ├── overrides.json      # Manual price overrides
│   └── price_cache.json    # Cached pricing (auto)
├── results/                # Generated reports (auto)
├── dashboard.py            # Streamlit web dashboard
├── run_simulation.py       # CLI tool
└── README.md               # Documentation
```

## Tech Stack

- **Python 3.12+** via uv
- **httpx**: API requests
- **pydantic**: Data validation
- **python-dateutil**: Date handling
- **streamlit**: Interactive web dashboard
- **plotly**: Interactive data visualizations
- **pandas**: Data manipulation and analysis

## Limitations & TODOs

**Current Limitations**:
- ❌ Token counts are estimated, not actual (need tiktoken integration)
- ❌ No support for image/audio pricing
- ❌ Provider-specific features (tiers, committed use) not modeled
- ❌ Cached input pricing modeled but not fully utilized

**Future Enhancements**:
- [ ] Add tiktoken for real token counting
- [ ] Historical price volatility analysis
- [ ] Export to CSV for spreadsheet analysis
- [ ] Support for batch API pricing
- [ ] Integration with real LLM APIs for quality testing

## Who Should Use This

- **Product managers**: Validate unit economics before building
- **Engineers**: Understand infrastructure costs
- **Finance**: Model different pricing strategies
- **Researchers**: Analyze LLM cost trends

## License

MIT - This is an internal research tool
