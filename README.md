# LLM Pricing Simulator

A Python-based tool to estimate and analyze runtime API costs for LLM-based monitoring products. This simulator helps understand unit economics by modeling different usage patterns across multiple LLM providers and models.

## Purpose

This tool is designed to answer questions like:
- "If we track 200 queries across 4 models daily with extraction, what's our monthly bill?"
- "What if we only track 30 high-priority queries every 2 hours on GPT + Claude?"
- "What if OpenAI raises prices by 20%?"
- "Which models give us the best cost/quality ratio?"

## Features

- **Real pricing data**: Fetches current pricing from [simonw/llm-prices](https://www.llm-prices.com)
- **Multi-model support**: Compare costs across OpenAI, Anthropic, Google, and more
- **Multi-pass flows**: Model extraction, comparison, and other post-processing steps
- **Flexible scenarios**: Define different intent groups with varying frequencies
- **Multiple output formats**: Text, JSON, and Markdown reports
- **Price overrides**: Support for custom/enterprise pricing
- **Caching**: Local price caching to reduce API calls

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable Python dependency management.

```bash
# Install dependencies
uv sync
```

## Quick Start

### Run a single scenario

```bash
python run_simulation.py scenarios/jtbd_1_brand_category.json
```

### Run all scenarios

```bash
python run_simulation.py --all
```

### Compare specific scenarios

```bash
python run_simulation.py --compare scenarios/jtbd_1*.json scenarios/jtbd_2*.json
```

## Project Structure

```
llm-pricing-simulator/
├── src/
│   ├── models.py          # Domain models
│   ├── price_fetcher.py   # Fetches LLM pricing data
│   ├── calculator.py      # Cost calculation engine
│   ├── simulator.py       # Orchestrates simulations
│   └── reporter.py        # Report generation
├── scenarios/             # Scenario definitions
│   ├── jtbd_*.json        # JTBD-based scenarios
│   └── template.json      # Template for new scenarios
├── data/
│   ├── overrides.json     # Manual price overrides
│   └── price_cache.json   # Cached pricing (auto-generated)
└── run_simulation.py      # CLI entry point
```

## Data Sources

Primary data: [simonw/llm-prices](https://github.com/simonw/llm-prices)
- Current prices: https://www.llm-prices.com/current-v1.json

Price data is cached locally for 24 hours.
