#!/usr/bin/env python3
"""
Select top 1-2 models per provider based on version numbers and quality tiers.

This script analyzes available models and selects the latest/best models from each provider.
"""
import re
import json
import httpx
from collections import defaultdict


def extract_version_number(model_id: str) -> tuple:
    """
    Extract version number from model ID for sorting.

    Examples:
        gpt-5-mini -> (5, 0, 0)
        claude-sonnet-4.5 -> (4, 5, 0)
        gemini-2.5-pro -> (2, 5, 0)
        grok-4-128k -> (4, 0, 0)
    """
    # Find all numbers in the model ID
    numbers = re.findall(r'\d+\.?\d*', model_id)

    # Convert to tuple of floats for comparison
    version_parts = []
    for num_str in numbers:
        if '.' in num_str:
            version_parts.append(float(num_str))
        else:
            version_parts.append(float(num_str))

    # Pad with zeros to ensure comparison works
    while len(version_parts) < 3:
        version_parts.append(0.0)

    return tuple(version_parts[:3])


def get_model_tier(model_id: str) -> int:
    """
    Determine model tier/quality level.
    Higher number = higher tier.

    Tiers:
    - 4: flagship/pro (opus, pro, gpt-5)
    - 3: premium (sonnet, gpt-4.5, o3)
    - 2: standard (haiku, mini, flash)
    - 1: lite/nano (nano, lite, micro)
    """
    model_lower = model_id.lower()

    # Flagship tier
    if any(x in model_lower for x in ['opus', 'pro', 'gpt-5', 'premier', 'o4', 'grok-4']):
        # But not mini/nano/lite versions
        if not any(x in model_lower for x in ['mini', 'nano', 'lite', 'micro']):
            return 4

    # Premium tier
    if any(x in model_lower for x in ['sonnet', 'gpt-4.5', 'o3', 'large']):
        if not any(x in model_lower for x in ['mini', 'nano', 'lite', 'micro']):
            return 3

    # Standard tier (mini, haiku, flash)
    if any(x in model_lower for x in ['haiku', 'mini', 'flash', 'small', 'medium', 'grok-3']):
        if not any(x in model_lower for x in ['nano', 'lite', 'micro']):
            return 2

    # Lite tier
    if any(x in model_lower for x in ['nano', 'lite', 'micro', '8b', '7b']):
        return 1

    # Default to standard tier
    return 2


def select_top_models_per_provider(prices_data: dict, max_per_provider: int = 2) -> dict:
    """
    Select top N models per provider based on version and tier.

    Args:
        prices_data: Pricing data from llm-prices API
        max_per_provider: Maximum models to select per provider

    Returns:
        Dict mapping provider to list of selected model IDs
    """
    # Group models by vendor
    by_vendor = defaultdict(list)
    for model in prices_data['prices']:
        vendor = model['vendor']
        model_id = model['id']
        by_vendor[vendor].append(model_id)

    # Select top models per vendor
    selected = {}
    for vendor, models in by_vendor.items():
        # Score each model: (tier, version_tuple)
        scored_models = []
        for model_id in models:
            tier = get_model_tier(model_id)
            version = extract_version_number(model_id)
            scored_models.append((tier, version, model_id))

        # Sort by tier (desc) then version (desc)
        scored_models.sort(key=lambda x: (x[0], x[1]), reverse=True)

        # Select top N unique tiers
        selected_models = []
        seen_tiers = set()

        for tier, version, model_id in scored_models:
            # Skip if we already have a model from this tier and have enough models
            if tier in seen_tiers and len(selected_models) >= max_per_provider:
                continue

            # Skip special variants (128k, 200k, etc.) if we have the base model
            base_id = re.sub(r'-\d+k$', '', model_id)
            if any(base_id == re.sub(r'-\d+k$', '', m) for m in selected_models):
                continue

            selected_models.append(model_id)
            seen_tiers.add(tier)

            if len(selected_models) >= max_per_provider:
                break

        selected[vendor] = selected_models

    return selected


def main():
    # Fetch current prices
    print("Fetching current model pricing...")
    response = httpx.get("https://www.llm-prices.com/current-v1.json", timeout=30.0)
    prices_data = response.json()

    print(f"\nTotal models available: {len(prices_data['prices'])}\n")

    # Select top models per provider
    top_models = select_top_models_per_provider(prices_data, max_per_provider=2)

    # Display results
    print("=" * 80)
    print("TOP MODELS PER PROVIDER")
    print("=" * 80)
    print()

    for vendor in sorted(top_models.keys()):
        print(f"{vendor.upper()}:")
        for model_id in top_models[vendor]:
            tier = get_model_tier(model_id)
            version = extract_version_number(model_id)
            tier_name = {4: "flagship", 3: "premium", 2: "standard", 1: "lite"}[tier]
            print(f"  - {model_id:<40} (tier: {tier_name}, version: {version})")
        print()

    # Show recommended default set (major providers)
    print("=" * 80)
    print("RECOMMENDED DEFAULT SET (Major Providers)")
    print("=" * 80)
    print()

    major_providers = ['anthropic', 'openai', 'google', 'xai']
    default_models = []

    for vendor in major_providers:
        if vendor in top_models:
            # Take the first (highest tier) model from each provider
            default_models.append(top_models[vendor][0])

    print("For high-tier comparison:")
    print(json.dumps(default_models, indent=2))
    print()

    # Budget-friendly set
    budget_models = []
    for vendor in major_providers:
        if vendor in top_models and len(top_models[vendor]) > 1:
            # Take the second model (usually cheaper)
            budget_models.append(top_models[vendor][1])
        elif vendor in top_models:
            budget_models.append(top_models[vendor][0])

    print("For budget-friendly comparison:")
    print(json.dumps(budget_models, indent=2))


if __name__ == "__main__":
    main()
