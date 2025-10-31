"""
Domain models for LLM pricing simulation.
"""
from datetime import datetime
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field


class ModelPrice(BaseModel):
    """Price data from simonw/llm-prices."""
    id: str
    vendor: str
    name: str
    input_per_million: float
    output_per_million: float
    input_cached_per_million: Optional[float] = None
    updated_at: datetime


class LLMModel(BaseModel):
    """Internal representation of an LLM model."""
    internal_id: str
    price_ref: str  # Points to ModelPrice.id
    max_context_tokens: Optional[int] = None
    default_prompt_tokens: int = 150
    default_output_tokens: int = 500
    supports_tools: bool = False


class IntentType(str, Enum):
    """Types of prompt intents."""
    EVALUATIVE = "evaluative"
    EXPLAINER = "explainer"
    PROBLEM = "problem"
    BRAND = "brand"


class PromptIntent(BaseModel):
    """A prompt intent we want to track."""
    id: str
    label: str
    type: IntentType
    base_prompt: str


class PromptVariant(BaseModel):
    """A variant of a prompt intent."""
    id: str
    intent_id: str
    text: str
    estimated_input_tokens: int
    multiplier: float = 1.0  # For token estimation adjustments


class TokenStrategy(str, Enum):
    """How to calculate input tokens for a flow step."""
    FROM_PROMPT = "from_prompt"
    FIXED = "fixed"
    FROM_PREVIOUS_OUTPUT = "from_previous_output"
    PERCENT_OF_PREVIOUS_OUTPUT = "percent_of_previous_output"


class FlowStep(BaseModel):
    """A processing step in the LLM flow."""
    name: str
    uses_model: str  # Reference to LLMModel.internal_id
    input_tokens_strategy: TokenStrategy
    fixed_input_tokens: Optional[int] = None
    percent_of_previous: Optional[float] = None  # For PERCENT_OF_PREVIOUS_OUTPUT
    expected_output_tokens: int
    runs_per_prompt: int = 1
    use_cached_input: bool = False  # If true, use cached input pricing when available


class Frequency(str, Enum):
    """How often to run the simulation."""
    HOURLY = "hourly"
    TWO_HOURLY = "2_hourly"
    FOUR_HOURLY = "4_hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    CUSTOM = "custom"


class IntentGroup(BaseModel):
    """A group of intents with specific settings."""
    name: str
    intents_count: int
    variants_per_intent: int
    frequency: Frequency
    flow_steps: list[FlowStep]
    custom_runs_per_month: Optional[int] = None  # For CUSTOM frequency


class Scenario(BaseModel):
    """Complete simulation scenario."""
    id: str
    name: str
    models: list[str]  # List of LLMModel.internal_id
    intent_groups: list[IntentGroup]
    days_per_month: int = 30
    price_overrides: dict[str, dict[str, float]] = Field(default_factory=dict)


class SimulationResult(BaseModel):
    """Results of a simulation run."""
    total_monthly_cost_usd: float
    by_model: list[dict[str, Any]]
    by_intent_group: list[dict[str, Any]]
    by_step: list[dict[str, Any]]
    total_calls_per_month: int
    total_input_tokens_per_month: int
    total_output_tokens_per_month: int
    meta: dict[str, str]
