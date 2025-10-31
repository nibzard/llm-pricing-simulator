"""
Price fetcher for LLM pricing data.
Fetches from simonw/llm-prices and supports local caching and overrides.
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import httpx
from .models import ModelPrice


PRICE_URL = "https://www.llm-prices.com/current-v1.json"
CACHE_FILE = Path("data/price_cache.json")
OVERRIDES_FILE = Path("data/overrides.json")
CACHE_HOURS = 24


class PriceFetcher:
    """Fetches and caches LLM pricing data."""

    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_file = cache_dir / "price_cache.json" if cache_dir else CACHE_FILE
        self.overrides_file = cache_dir / "overrides.json" if cache_dir else OVERRIDES_FILE
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)

    def fetch_prices(self, force_refresh: bool = False) -> dict[str, ModelPrice]:
        """
        Fetch current prices, using cache if available and fresh.

        Args:
            force_refresh: If True, ignore cache and fetch fresh data

        Returns:
            Dictionary mapping model ID to ModelPrice
        """
        # Check cache first
        if not force_refresh and self._is_cache_fresh():
            print("Using cached price data...")
            return self._load_from_cache()

        # Fetch from remote
        print(f"Fetching prices from {PRICE_URL}...")
        try:
            prices = self._fetch_remote()
            self._save_to_cache(prices)
            return prices
        except Exception as e:
            print(f"Error fetching prices: {e}")
            # Fall back to cache if available
            if self.cache_file.exists():
                print("Falling back to cached data...")
                return self._load_from_cache()
            raise

    def _fetch_remote(self) -> dict[str, ModelPrice]:
        """Fetch prices from remote API."""
        response = httpx.get(PRICE_URL, timeout=30.0)
        response.raise_for_status()

        data = response.json()
        prices = {}

        # Parse the top-level updated_at timestamp
        global_updated_at = data.get("updated_at", datetime.now().isoformat())
        if isinstance(global_updated_at, str):
            try:
                global_updated_at = datetime.fromisoformat(global_updated_at)
            except ValueError:
                global_updated_at = datetime.now()

        # Iterate over the prices array
        for item in data.get("prices", []):
            # Parse the model price data
            model_id = item.get("id")
            if not model_id:
                continue

            prices[model_id] = ModelPrice(
                id=model_id,
                vendor=item.get("vendor", "unknown"),
                name=item.get("name", model_id),
                input_per_million=float(item.get("input", 0)),
                output_per_million=float(item.get("output", 0)),
                input_cached_per_million=float(item["input_cached"]) if item.get("input_cached") else None,
                updated_at=global_updated_at
            )

        # Apply local overrides
        prices = self._apply_overrides(prices)

        return prices

    def _apply_overrides(self, prices: dict[str, ModelPrice]) -> dict[str, ModelPrice]:
        """Apply local price overrides from file."""
        if not self.overrides_file.exists():
            return prices

        try:
            with open(self.overrides_file) as f:
                overrides = json.load(f)

            for model_id, override_data in overrides.items():
                if model_id in prices:
                    # Update existing model
                    existing = prices[model_id]
                    prices[model_id] = ModelPrice(
                        id=existing.id,
                        vendor=existing.vendor,
                        name=existing.name,
                        input_per_million=override_data.get("input_per_million", existing.input_per_million),
                        output_per_million=override_data.get("output_per_million", existing.output_per_million),
                        input_cached_per_million=override_data.get("input_cached_per_million", existing.input_cached_per_million),
                        updated_at=datetime.now()
                    )
                else:
                    # Add new model from override
                    prices[model_id] = ModelPrice(
                        id=model_id,
                        vendor=override_data.get("vendor", "custom"),
                        name=override_data.get("name", model_id),
                        input_per_million=override_data["input_per_million"],
                        output_per_million=override_data["output_per_million"],
                        input_cached_per_million=override_data.get("input_cached_per_million"),
                        updated_at=datetime.now()
                    )

            print(f"Applied {len(overrides)} price overrides")
        except Exception as e:
            print(f"Warning: Could not apply overrides: {e}")

        return prices

    def _is_cache_fresh(self) -> bool:
        """Check if cache exists and is fresh enough."""
        if not self.cache_file.exists():
            return False

        cache_age = datetime.now() - datetime.fromtimestamp(self.cache_file.stat().st_mtime)
        return cache_age < timedelta(hours=CACHE_HOURS)

    def _load_from_cache(self) -> dict[str, ModelPrice]:
        """Load prices from cache file."""
        with open(self.cache_file) as f:
            data = json.load(f)

        prices = {}
        for model_id, item in data.items():
            prices[model_id] = ModelPrice(**item)

        return prices

    def _save_to_cache(self, prices: dict[str, ModelPrice]) -> None:
        """Save prices to cache file."""
        cache_data = {}
        for model_id, price in prices.items():
            cache_data[model_id] = price.model_dump(mode="json")

        with open(self.cache_file, "w") as f:
            json.dump(cache_data, f, indent=2, default=str)

        print(f"Cached {len(prices)} model prices")
