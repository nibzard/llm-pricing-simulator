#!/usr/bin/env python3
"""
Streamlit dashboard for LLM pricing simulation.

Run with: streamlit run dashboard.py
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pathlib import Path
import json

from src.price_fetcher import PriceFetcher
from src.calculator import CostCalculator
from src.models import (
    Scenario, IntentGroup, FlowStep, Frequency, TokenStrategy, SimulationResult
)

# Page config
st.set_page_config(
    page_title="LLM Pricing Simulator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'prices' not in st.session_state:
    st.session_state.prices = None
if 'calculator' not in st.session_state:
    st.session_state.calculator = None
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = []


def load_prices(force_refresh=False):
    """Load price data."""
    fetcher = PriceFetcher()
    prices = fetcher.fetch_prices(force_refresh)
    st.session_state.prices = prices
    st.session_state.calculator = CostCalculator(prices)
    return prices


def load_scenario_files():
    """Load all scenario JSON files from scenarios/ directory."""
    scenarios_dir = Path("scenarios")
    scenario_files = {}

    if scenarios_dir.exists():
        for file_path in scenarios_dir.glob("*.json"):
            # Skip template file
            if file_path.name == "template.json":
                continue
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    scenario = Scenario(**data)
                    scenario_files[file_path.stem] = {
                        "path": file_path,
                        "scenario": scenario
                    }
            except Exception as e:
                st.warning(f"Could not load {file_path.name}: {e}")

    return scenario_files


def create_scenario_from_form(name, models, intents, variants, frequency, flow_steps, days=30):
    """Create a scenario from form inputs."""
    return Scenario(
        id=name.lower().replace(" ", "-"),
        name=name,
        models=models,
        intent_groups=[
            IntentGroup(
                name="Main intent group",
                intents_count=intents,
                variants_per_intent=variants,
                frequency=Frequency(frequency),
                flow_steps=flow_steps
            )
        ],
        days_per_month=days
    )


def main():
    st.title("💰 LLM Pricing Simulator Dashboard")
    st.markdown("Estimate and optimize costs for LLM-based competitive intelligence products")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        if st.button("🔄 Refresh Price Data", use_container_width=True):
            with st.spinner("Fetching latest prices..."):
                load_prices(force_refresh=True)
                st.success("Prices updated!")

        # Load prices if not already loaded
        if st.session_state.prices is None:
            with st.spinner("Loading price data..."):
                prices = load_prices()
            st.success(f"Loaded {len(prices)} models")

        st.divider()

        # Quick stats
        if st.session_state.prices:
            st.metric("Available Models", len(st.session_state.prices))

            # Show price date
            if st.session_state.prices:
                first_price = next(iter(st.session_state.prices.values()))
                st.caption(f"Updated: {first_price.updated_at.strftime('%Y-%m-%d')}")

    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Scenario Builder",
        "📊 Cost Analysis",
        "💵 Pricing Strategy",
        "🔄 Comparison",
        "📄 Report Generator"
    ])

    with tab1:
        scenario_builder_tab()

    with tab2:
        cost_analysis_tab()

    with tab3:
        pricing_strategy_tab()

    with tab4:
        comparison_tab()

    with tab5:
        report_generator_tab()


def scenario_builder_tab():
    """Interactive scenario builder."""
    st.header("Build Your Scenario")

    if not st.session_state.prices:
        st.warning("Loading price data...")
        return

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("1️⃣ Basic Configuration")

        scenario_name = st.text_input(
            "Scenario Name",
            value="Custom Scenario",
            help="Give your scenario a descriptive name"
        )

        # Model selection
        available_models = sorted(st.session_state.prices.keys())

        # Group models by vendor for easier selection
        vendors = {}
        for model_id in available_models:
            vendor = st.session_state.prices[model_id].vendor
            if vendor not in vendors:
                vendors[vendor] = []
            vendors[vendor].append(model_id)

        st.markdown("**Select Models to Track:**")
        selected_models = []

        # Show popular models first (latest flagships)
        popular_models = [
            "claude-opus-4", "claude-sonnet-4.5", "claude-4.5-haiku",
            "gpt-5", "gpt-5-mini", "gpt-4.5",
            "gemini-2.5-pro", "gemini-2.5-flash",
            "grok-4", "grok-4-fast"
        ]

        # Default selections
        default_selections = ["claude-sonnet-4.5", "gpt-5", "gemini-2.5-pro"]

        cols = st.columns(3)
        for i, model in enumerate(popular_models):
            if model in available_models:
                if cols[i % 3].checkbox(
                    st.session_state.prices[model].name,
                    value=(model in default_selections),
                    key=f"model_{model}"
                ):
                    selected_models.append(model)

        # Show all models in expander
        with st.expander("📋 See All Available Models"):
            for vendor, models in sorted(vendors.items()):
                st.markdown(f"**{vendor.title()}**")
                vcols = st.columns(3)
                for i, model in enumerate(sorted(models)):
                    if model not in popular_models:
                        if vcols[i % 3].checkbox(
                            st.session_state.prices[model].name,
                            key=f"model_all_{model}"
                        ):
                            selected_models.append(model)

        if not selected_models:
            st.warning("⚠️ Please select at least one model")
            return

        st.success(f"✓ Selected {len(selected_models)} models")

        st.divider()
        st.subheader("2️⃣ Usage Pattern")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            intents_count = st.number_input(
                "Number of Intents/Questions",
                min_value=1,
                max_value=1000,
                value=50,
                help="How many unique concepts/questions to track"
            )

        with col_b:
            variants_per_intent = st.number_input(
                "Variants per Intent",
                min_value=1,
                max_value=20,
                value=3,
                help="Different phrasings of each question"
            )

        with col_c:
            frequency = st.selectbox(
                "Monitoring Frequency",
                options=["hourly", "2_hourly", "4_hourly", "daily", "weekly", "monthly"],
                index=3,
                help="How often to run the queries"
            )

        total_prompts = intents_count * variants_per_intent
        st.info(f"📝 Total prompts per run: **{total_prompts:,}** ({intents_count} × {variants_per_intent})")

        st.divider()
        st.subheader("3️⃣ Processing Pipeline")

        # Flow steps
        num_steps = st.number_input(
            "Number of Processing Steps",
            min_value=1,
            max_value=5,
            value=2,
            help="How many LLM calls per prompt (e.g., answer → extract → judge)"
        )

        flow_steps = []
        for i in range(num_steps):
            with st.expander(f"Step {i+1}: Configure", expanded=(i < 2)):
                step_col1, step_col2 = st.columns(2)

                with step_col1:
                    step_name = st.text_input(
                        "Step Name",
                        value=["main-answer", "extract-entities", "judge", "compare", "cluster"][i],
                        key=f"step_name_{i}"
                    )

                    # Model assignment selection
                    st.markdown("**Model Assignment:**")

                    # Step 1 MUST use all selected models (that's the point of the tool!)
                    if i == 0:
                        st.info(f"✅ Step 1 always uses **all {len(selected_models)} selected models** for comparison")
                        uses_model = "current"
                    else:
                        # Steps 2+ can choose between all models or a specific model
                        model_mode = st.radio(
                            "Which models to use?",
                            options=["All selected models", "Specific model (cost optimization)"],
                            index=1,  # Default to specific model for extraction/judge steps
                            key=f"model_mode_{i}",
                            help="'All selected models' processes with every model. 'Specific model' uses one cheap model for extraction/judge."
                        )

                        # Conditional rendering - only show dropdown for specific model
                        if model_mode == "Specific model (cost optimization)":
                            # Show budget-friendly models first
                            budget_models = [
                                "gpt-5-mini", "claude-4.5-haiku", "gemini-2.5-flash",
                                "gpt-4o-mini", "claude-3.5-haiku", "gemini-2.0-flash"
                            ]

                            budget_available = [m for m in budget_models if m in available_models]
                            other_models = [m for m in available_models if m not in budget_models]

                            all_options = budget_available + ["---"] + other_models

                            uses_model = st.selectbox(
                                "Select specific model",
                                options=all_options,
                                index=0 if budget_available else 2,
                                key=f"uses_model_{i}",
                                help="Recommended: Use cheap models like gpt-5-mini for extraction/judge"
                            )

                            if uses_model == "---":
                                uses_model = budget_available[0] if budget_available else available_models[0]

                            st.info(f"💡 **{uses_model}** will process outputs from all {len(selected_models)} models")
                        else:
                            uses_model = "current"
                            st.success(f"✅ All {len(selected_models)} selected models will be used")

                    token_strategy = st.selectbox(
                        "Input Token Strategy",
                        options=["fixed", "from_previous_output", "percent_of_previous_output"],
                        index=0 if i == 0 else 1,
                        key=f"token_strat_{i}",
                        help="How to determine input tokens for this step"
                    )

                with step_col2:
                    # Initialize variables
                    input_tokens = None
                    percent = None

                    if token_strategy == "fixed":
                        input_tokens = st.number_input(
                            "Fixed Input Tokens",
                            min_value=10,
                            max_value=10000,
                            value=150 if i == 0 else 500,
                            key=f"input_tokens_{i}"
                        )
                    elif token_strategy == "percent_of_previous_output":
                        percent = st.slider(
                            "Percent of Previous Output",
                            min_value=0.1,
                            max_value=2.0,
                            value=0.5,
                            step=0.1,
                            key=f"percent_{i}"
                        )

                    output_tokens = st.number_input(
                        "Expected Output Tokens",
                        min_value=10,
                        max_value=10000,
                        value=500 if i == 0 else 200,
                        key=f"output_tokens_{i}"
                    )

                step = FlowStep(
                    name=step_name,
                    uses_model=uses_model,
                    input_tokens_strategy=TokenStrategy(token_strategy),
                    fixed_input_tokens=input_tokens if token_strategy == "fixed" else None,
                    percent_of_previous=percent if token_strategy == "percent_of_previous_output" else None,
                    expected_output_tokens=output_tokens,
                    runs_per_prompt=1
                )
                flow_steps.append(step)

    with col2:
        st.subheader("💰 Cost Estimate")

        if selected_models and flow_steps:
            # Create scenario
            scenario = create_scenario_from_form(
                scenario_name,
                selected_models,
                intents_count,
                variants_per_intent,
                frequency,
                flow_steps
            )

            # Calculate
            with st.spinner("Calculating costs..."):
                result = st.session_state.calculator.calculate_scenario(scenario)

            # Display results
            st.metric(
                "Monthly Cost",
                f"${result.total_monthly_cost_usd:,.2f}",
                delta=None,
                help="Total estimated cost per month"
            )

            st.metric(
                "API Calls/Month",
                f"{result.total_calls_per_month:,}",
                help="Total number of LLM API calls"
            )

            st.metric(
                "Cost per 1K Calls",
                f"${(result.total_monthly_cost_usd / result.total_calls_per_month * 1000):.2f}",
                help="Unit cost per thousand calls"
            )

            st.divider()

            # Cost breakdown
            st.markdown("**Cost by Model:**")
            for item in sorted(result.by_model, key=lambda x: x["cost_usd"], reverse=True):
                model_name = st.session_state.prices[item["model"]].name
                pct = (item["cost_usd"] / result.total_monthly_cost_usd) * 100
                st.progress(pct / 100, text=f"{model_name}: ${item['cost_usd']:.2f} ({pct:.1f}%)")

            st.divider()

            # Save scenario button
            if st.button("💾 Save Scenario", use_container_width=True):
                # Save to scenarios folder
                filename = f"scenarios/{scenario.id}.json"
                with open(filename, "w") as f:
                    json.dump(scenario.model_dump(mode="json"), f, indent=2, default=str)
                st.success(f"Saved to {filename}")

            # Add to comparison
            if st.button("➕ Add to Comparison", use_container_width=True):
                st.session_state.scenarios.append((scenario, result))
                st.success(f"Added '{scenario_name}' to comparison!")


def cost_analysis_tab():
    """Detailed cost analysis with visualizations."""
    st.header("Cost Analysis & Visualization")

    if not st.session_state.prices:
        st.warning("Loading price data...")
        return

    # Load a scenario
    scenario_files = list(Path("scenarios").glob("*.json"))
    scenario_files = [f for f in scenario_files if f.name != "template.json"]

    selected_file = st.selectbox(
        "Select Scenario to Analyze",
        options=scenario_files,
        format_func=lambda x: x.stem.replace("_", " ").replace("-", " ").title()
    )

    if selected_file:
        with open(selected_file) as f:
            scenario_data = json.load(f)

        scenario = Scenario(**scenario_data)
        result = st.session_state.calculator.calculate_scenario(scenario)

        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Monthly Cost", f"${result.total_monthly_cost_usd:,.2f}")

        with col2:
            st.metric("API Calls", f"{result.total_calls_per_month:,}")

        with col3:
            st.metric("Models", len(scenario.models))

        with col4:
            cost_per_k = (result.total_monthly_cost_usd / result.total_calls_per_month * 1000)
            st.metric("$/1K Calls", f"${cost_per_k:.2f}")

        st.divider()

        # Visualizations
        col1, col2 = st.columns(2)

        with col1:
            # Cost by model pie chart
            st.subheader("Cost Distribution by Model")

            df_models = pd.DataFrame(result.by_model)
            fig = px.pie(
                df_models,
                values='cost_usd',
                names='model',
                title="Monthly Cost by Model"
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Cost by step bar chart
            st.subheader("Cost by Processing Step")

            df_steps = pd.DataFrame(result.by_step)
            fig = px.bar(
                df_steps,
                x='step',
                y='cost_usd',
                title="Monthly Cost by Flow Step",
                labels={'cost_usd': 'Cost (USD)', 'step': 'Processing Step'}
            )
            st.plotly_chart(fig, use_container_width=True)

        # Cost breakdown table
        st.subheader("Detailed Cost Breakdown")

        # Model comparison table
        df_models_detailed = pd.DataFrame(result.by_model)
        df_models_detailed['model_name'] = df_models_detailed['model'].apply(
            lambda x: st.session_state.prices[x].name
        )
        df_models_detailed['vendor'] = df_models_detailed['model'].apply(
            lambda x: st.session_state.prices[x].vendor
        )
        df_models_detailed['percentage'] = (
            df_models_detailed['cost_usd'] / result.total_monthly_cost_usd * 100
        )

        st.dataframe(
            df_models_detailed[['vendor', 'model_name', 'cost_usd', 'percentage']].sort_values('cost_usd', ascending=False),
            column_config={
                "vendor": "Vendor",
                "model_name": "Model",
                "cost_usd": st.column_config.NumberColumn("Monthly Cost", format="$%.2f"),
                "percentage": st.column_config.NumberColumn("% of Total", format="%.1f%%")
            },
            hide_index=True,
            use_container_width=True
        )

        # Frequency analysis
        st.divider()
        st.subheader("📈 Frequency Impact Analysis")

        st.markdown("See how different monitoring frequencies affect costs:")

        frequencies = ["hourly", "2_hourly", "4_hourly", "daily", "weekly"]
        freq_results = []

        for freq in frequencies:
            test_scenario = Scenario(
                id=scenario.id,
                name=scenario.name,
                models=scenario.models,
                intent_groups=[
                    IntentGroup(
                        name=group.name,
                        intents_count=group.intents_count,
                        variants_per_intent=group.variants_per_intent,
                        frequency=Frequency(freq),
                        flow_steps=group.flow_steps
                    )
                    for group in scenario.intent_groups
                ],
                days_per_month=scenario.days_per_month
            )
            test_result = st.session_state.calculator.calculate_scenario(test_scenario)
            freq_results.append({
                'frequency': freq.replace("_", " ").title(),
                'cost': test_result.total_monthly_cost_usd,
                'calls': test_result.total_calls_per_month
            })

        df_freq = pd.DataFrame(freq_results)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_freq['frequency'],
            y=df_freq['cost'],
            name='Monthly Cost',
            marker_color='lightblue',
            text=df_freq['cost'].apply(lambda x: f'${x:,.0f}'),
            textposition='outside'
        ))

        fig.update_layout(
            title="Cost Impact of Monitoring Frequency",
            xaxis_title="Frequency",
            yaxis_title="Monthly Cost (USD)",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)


def pricing_strategy_tab():
    """Pricing strategy calculator."""
    st.header("Pricing Strategy Calculator")

    st.markdown("""
    Use this calculator to determine your product pricing based on infrastructure costs.
    Set your target margins and see recommended SaaS tier pricing.
    """)

    if not st.session_state.prices:
        st.warning("Loading price data...")
        return

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Infrastructure Costs")

        # Choice between loading scenario or quick calculation
        scenario_mode = st.radio(
            "Scenario Source",
            options=["Load Existing Scenario", "Quick Calculation"],
            horizontal=True,
            help="Load a saved scenario from Scenario Builder or create a quick calculation"
        )

        if scenario_mode == "Load Existing Scenario":
            # Load available scenarios
            scenario_files = load_scenario_files()

            if not scenario_files:
                st.warning("No scenario files found in scenarios/ directory. Build one in the Scenario Builder tab first!")
                return

            # Let user select a scenario
            selected_scenario_key = st.selectbox(
                "Select Scenario",
                options=list(scenario_files.keys()),
                format_func=lambda x: scenario_files[x]["scenario"].name,
                help="Choose a scenario you've previously built or saved"
            )

            scenario = scenario_files[selected_scenario_key]["scenario"]

            # Display scenario info
            st.info(f"""
            **{scenario.name}**
            - Models: {len(scenario.models)} ({', '.join(scenario.models[:3])}{'...' if len(scenario.models) > 3 else ''})
            - Intent groups: {len(scenario.intent_groups)}
            - Total prompts: {sum(g.intents_count * g.variants_per_intent for g in scenario.intent_groups)}
            """)

            # Calculate total intents/variants for pricing display
            total_prompts = sum(g.intents_count * g.variants_per_intent for g in scenario.intent_groups)
            intents = total_prompts  # Simplified for display
            variants = 1
            frequency = scenario.intent_groups[0].frequency.value if scenario.intent_groups else "daily"
            num_models = len(scenario.models)

        else:
            # Quick scenario inputs
            intents = st.number_input("Intents to Track", min_value=1, value=50, step=10)
            variants = st.number_input("Variants per Intent", min_value=1, value=3, step=1)

            frequency = st.selectbox(
                "Monitoring Frequency",
                options=["daily", "2_hourly", "hourly", "weekly", "monthly"],
                index=0
            )

            num_models = st.slider("Number of Models", min_value=1, max_value=10, value=3)

            # Simple calculation
            popular_models = ["gpt-4o", "claude-3.7-sonnet", "gemini-2.5-flash"][:num_models]

            flow_steps = [
                FlowStep(
                    name="main-answer",
                    uses_model="current",
                    input_tokens_strategy=TokenStrategy.FIXED,
                    fixed_input_tokens=150,
                    expected_output_tokens=500,
                    runs_per_prompt=1
                ),
                FlowStep(
                    name="extract-entities",
                    uses_model="current",
                    input_tokens_strategy=TokenStrategy.FROM_PREVIOUS_OUTPUT,
                    expected_output_tokens=200,
                    runs_per_prompt=1
                )
            ]

            scenario = create_scenario_from_form(
                "Pricing Strategy",
                popular_models,
                intents,
                variants,
                frequency,
                flow_steps
            )

        result = st.session_state.calculator.calculate_scenario(scenario)

        st.metric("Monthly Infrastructure Cost", f"${result.total_monthly_cost_usd:.2f}")
        st.metric("Cost per 1K Calls", f"${(result.total_monthly_cost_usd / result.total_calls_per_month * 1000):.2f}")

    with col2:
        st.subheader("Pricing Strategy")

        # Markup settings
        markup_multiplier = st.slider(
            "Target Markup (multiplier)",
            min_value=1.5,
            max_value=10.0,
            value=3.5,
            step=0.5,
            help="How many times your cost to charge customers"
        )

        target_margin_pct = ((markup_multiplier - 1) / markup_multiplier) * 100
        st.info(f"💡 This gives you a **{target_margin_pct:.1f}%** gross margin")

        # Calculate pricing
        base_price = result.total_monthly_cost_usd * markup_multiplier

        st.divider()

        # Recommended tiers
        st.markdown("### 🎯 Recommended SaaS Tiers")

        # Starter tier (50% of base)
        starter_cost = result.total_monthly_cost_usd * 0.5
        starter_price = starter_cost * markup_multiplier

        st.markdown(f"""
        **Starter Tier** - ${starter_price:.0f}/month
        - {intents // 2} intents
        - {variants} variants
        - {frequency} monitoring
        - {num_models} models
        - Cost: ${starter_cost:.2f} | Margin: ${starter_price - starter_cost:.2f}
        """)

        # Professional tier (100% of base)
        st.markdown(f"""
        **Professional Tier** - ${base_price:.0f}/month
        - {intents} intents
        - {variants} variants
        - {frequency} monitoring
        - {num_models} models
        - Cost: ${result.total_monthly_cost_usd:.2f} | Margin: ${base_price - result.total_monthly_cost_usd:.2f}
        """)

        # Enterprise tier (200% of base)
        enterprise_cost = result.total_monthly_cost_usd * 2
        enterprise_price = enterprise_cost * markup_multiplier

        st.markdown(f"""
        **Enterprise Tier** - ${enterprise_price:.0f}/month
        - {intents * 2} intents
        - {variants + 2} variants
        - {frequency} monitoring
        - {num_models + 2} models
        - Cost: ${enterprise_cost:.2f} | Margin: ${enterprise_price - enterprise_cost:.2f}
        """)

        st.divider()

        # Per-unit pricing
        st.markdown("### 📊 Per-Unit Pricing")

        cost_per_intent = result.total_monthly_cost_usd / intents
        price_per_intent = cost_per_intent * markup_multiplier

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Cost per Intent", f"${cost_per_intent:.2f}")
        with col_b:
            st.metric("Charge per Intent", f"${price_per_intent:.2f}")

        # Overage pricing
        st.markdown("### 💳 Overage Pricing")
        overage_markup = st.slider(
            "Overage Multiplier",
            min_value=1.0,
            max_value=5.0,
            value=2.0,
            step=0.5,
            help="Charge extra for usage above tier limits"
        )

        overage_price = price_per_intent * overage_markup
        st.info(f"Charge **${overage_price:.2f} per additional intent** above tier limits")


def comparison_tab():
    """Compare multiple scenarios."""
    st.header("Scenario Comparison")

    if not st.session_state.prices:
        st.warning("Loading price data...")
        return

    # Load JTBD scenarios
    st.subheader("Compare Pre-built Scenarios")

    jtbd_files = sorted(Path("scenarios").glob("jtbd_*.json"))

    if st.button("🔄 Load All JTBD Scenarios"):
        st.session_state.scenarios = []
        for f in jtbd_files:
            with open(f) as file:
                scenario_data = json.load(file)
            scenario = Scenario(**scenario_data)
            result = st.session_state.calculator.calculate_scenario(scenario)
            st.session_state.scenarios.append((scenario, result))
        st.success(f"Loaded {len(jtbd_files)} scenarios!")

    if st.session_state.scenarios:
        # Comparison table
        comparison_data = []
        for scenario, result in st.session_state.scenarios:
            comparison_data.append({
                'Scenario': scenario.name,
                'Monthly Cost': result.total_monthly_cost_usd,
                'API Calls': result.total_calls_per_month,
                'Models': len(scenario.models),
                'Intents': sum(g.intents_count for g in scenario.intent_groups),
                'Cost per 1K': (result.total_monthly_cost_usd / result.total_calls_per_month * 1000)
            })

        df = pd.DataFrame(comparison_data)

        # Bar chart comparison
        fig = px.bar(
            df.sort_values('Monthly Cost'),
            x='Scenario',
            y='Monthly Cost',
            title="Monthly Cost Comparison",
            text='Monthly Cost',
            color='Monthly Cost',
            color_continuous_scale='Viridis'
        )
        fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        # Comparison table
        st.dataframe(
            df,
            column_config={
                "Monthly Cost": st.column_config.NumberColumn("Monthly Cost", format="$%.2f"),
                "API Calls": st.column_config.NumberColumn("API Calls", format="%d"),
                "Cost per 1K": st.column_config.NumberColumn("Cost per 1K Calls", format="$%.2f")
            },
            hide_index=True,
            use_container_width=True
        )

        # Cost efficiency analysis
        st.divider()
        st.subheader("Cost Efficiency Analysis")

        # Scatter plot: calls vs cost
        fig = px.scatter(
            df,
            x='API Calls',
            y='Monthly Cost',
            size='Intents',
            color='Models',
            hover_data=['Scenario'],
            title="Cost vs Usage (bubble size = number of intents)",
            labels={'Monthly Cost': 'Monthly Cost (USD)', 'API Calls': 'API Calls per Month'}
        )
        st.plotly_chart(fig, use_container_width=True)

        # Clear comparison
        if st.button("🗑️ Clear Comparison"):
            st.session_state.scenarios = []
            st.rerun()


def report_generator_tab():
    """Generate custom pricing strategy reports."""
    st.header("📄 Report Generator")

    st.markdown("""
    Generate a comprehensive pricing strategy report for selected scenarios.
    The report includes cost analysis, pricing recommendations, and unit economics.
    """)

    if not st.session_state.prices:
        st.warning("Loading price data...")
        return

    # Load all available scenarios
    scenario_files = load_scenario_files()

    if not scenario_files:
        st.warning("No scenario files found in scenarios/ directory.")
        return

    st.subheader("Select Scenarios")

    # Let user select scenarios to include
    selected_scenarios = st.multiselect(
        "Choose scenarios to include in the report",
        options=list(scenario_files.keys()),
        format_func=lambda x: scenario_files[x]["scenario"].name,
        default=list(scenario_files.keys())[:3]  # Default to first 3
    )

    if not selected_scenarios:
        st.info("Select at least one scenario to generate a report.")
        return

    # Markup strategy input
    col1, col2 = st.columns(2)
    with col1:
        default_markup = st.slider(
            "Target Markup Multiplier",
            min_value=2.0,
            max_value=10.0,
            value=4.0,
            step=0.5,
            help="Default markup to apply for pricing recommendations"
        )

    with col2:
        include_details = st.checkbox("Include detailed breakdowns", value=True)

    if st.button("📊 Generate Report", type="primary"):
        with st.spinner("Running simulations and generating report..."):
            # Run simulations
            results = []
            for scenario_key in selected_scenarios:
                scenario = scenario_files[scenario_key]["scenario"]
                result = st.session_state.calculator.calculate_scenario(scenario)
                results.append((scenario, result))

            # Generate report content
            report_content = generate_report_markdown(results, default_markup, include_details)

            # Display preview
            st.success("Report generated successfully!")

            # Download button
            st.download_button(
                label="📥 Download Report (Markdown)",
                data=report_content,
                file_name=f"llm_pricing_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                help="Download the report as a Markdown file"
            )

            # Show preview
            with st.expander("📄 Preview Report", expanded=False):
                st.markdown(report_content)


def generate_report_markdown(results, markup, include_details=True):
    """Generate a markdown report from simulation results."""
    from datetime import datetime

    report = []
    report.append("# LLM Pricing Strategy Report")
    report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**Scenarios Analyzed:** {len(results)}")
    report.append("\n---\n")

    # Executive Summary
    report.append("## Executive Summary\n")

    total_costs = [r[1].total_monthly_cost_usd for r in results]
    report.append(f"This report analyzes {len(results)} scenarios with infrastructure costs ranging from **${min(total_costs):.2f} to ${max(total_costs):.2f} per month**.\n")

    report.append("### Cost Overview\n")
    report.append("| Scenario | Monthly Cost | API Calls | Models | Recommended Price ({}x) |".format(markup))
    report.append("|----------|--------------|-----------|--------|------------------------|")

    for scenario, result in results:
        recommended = result.total_monthly_cost_usd * markup
        report.append(f"| {scenario.name} | ${result.total_monthly_cost_usd:.2f} | {result.total_calls_per_month:,} | {len(scenario.models)} | ${recommended:.0f} |")

    report.append("\n---\n")

    # Detailed Scenario Analysis
    report.append("## Detailed Scenario Analysis\n")

    for i, (scenario, result) in enumerate(results, 1):
        report.append(f"### {i}. {scenario.name}")
        report.append(f"\n**Monthly Infrastructure Cost:** ${result.total_monthly_cost_usd:.2f}\n")

        # Configuration
        report.append("#### Configuration\n")
        report.append(f"- **Models:** {len(scenario.models)} ({', '.join(scenario.models[:3])}{'...' if len(scenario.models) > 3 else ''})")

        total_prompts = sum(g.intents_count * g.variants_per_intent for g in scenario.intent_groups)
        report.append(f"- **Total Prompts:** {total_prompts}")
        report.append(f"- **Intent Groups:** {len(scenario.intent_groups)}")

        if scenario.intent_groups:
            freq = scenario.intent_groups[0].frequency.value
            report.append(f"- **Frequency:** {freq}")

        report.append(f"- **Total API Calls:** {result.total_calls_per_month:,}/month\n")

        if include_details:
            # Cost Breakdown
            report.append("#### Cost Breakdown\n")

            # By model
            if result.by_model:
                report.append("**By Model:**")
                for model_data in sorted(result.by_model, key=lambda x: x['cost_usd'], reverse=True):
                    if model_data['cost_usd'] > 0:
                        pct = (model_data['cost_usd'] / result.total_monthly_cost_usd) * 100
                        report.append(f"- {model_data['model']}: ${model_data['cost_usd']:.2f} ({pct:.0f}%)")
                report.append("")

            # By step
            if result.by_step:
                report.append("**By Flow Step:**")
                for step_data in sorted(result.by_step, key=lambda x: x['cost_usd'], reverse=True):
                    pct = (step_data['cost_usd'] / result.total_monthly_cost_usd) * 100
                    report.append(f"- {step_data['step']}: ${step_data['cost_usd']:.2f} ({pct:.0f}%)")
                report.append("")

        # Pricing Strategy
        report.append("#### Recommended Pricing Strategy\n")

        base_price = result.total_monthly_cost_usd * markup
        starter_price = (result.total_monthly_cost_usd * 0.5) * markup
        enterprise_price = (result.total_monthly_cost_usd * 2) * markup

        report.append("| Tier | Monthly Price | Infrastructure Cost | Margin | Markup |")
        report.append("|------|---------------|---------------------|--------|--------|")
        report.append(f"| Starter | ${starter_price:.0f} | ${result.total_monthly_cost_usd * 0.5:.2f} | ${starter_price - (result.total_monthly_cost_usd * 0.5):.0f} | {markup}x |")
        report.append(f"| Professional | ${base_price:.0f} | ${result.total_monthly_cost_usd:.2f} | ${base_price - result.total_monthly_cost_usd:.0f} | {markup}x |")
        report.append(f"| Enterprise | ${enterprise_price:.0f} | ${result.total_monthly_cost_usd * 2:.2f} | ${enterprise_price - (result.total_monthly_cost_usd * 2):.0f} | {markup}x |")
        report.append("")

        # Unit Economics
        report.append("#### Unit Economics\n")

        if total_prompts > 0:
            cost_per_prompt = result.total_monthly_cost_usd / total_prompts
            price_per_prompt = cost_per_prompt * markup
            report.append(f"- **Cost per prompt:** ${cost_per_prompt:.2f}")
            report.append(f"- **Recommended charge per prompt:** ${price_per_prompt:.2f}")

        if result.total_calls_per_month > 0:
            cost_per_1k = (result.total_monthly_cost_usd / result.total_calls_per_month) * 1000
            report.append(f"- **Cost per 1,000 API calls:** ${cost_per_1k:.2f}")

        report.append("\n---\n")

    # Recommendations
    report.append("## Pricing Recommendations\n")

    # Sort by cost
    sorted_results = sorted(results, key=lambda x: x[1].total_monthly_cost_usd)

    report.append("### By Cost Tier\n")

    for scenario, result in sorted_results:
        cost = result.total_monthly_cost_usd
        if cost < 100:
            tier = "Budget"
            target_markup = "3-7x"
            price_range = f"${cost * 3:.0f}-${cost * 7:.0f}"
        elif cost < 500:
            tier = "Standard"
            target_markup = "3-5x"
            price_range = f"${cost * 3:.0f}-${cost * 5:.0f}"
        elif cost < 2000:
            tier = "Professional"
            target_markup = "2.5-4x"
            price_range = f"${cost * 2.5:.0f}-${cost * 4:.0f}"
        else:
            tier = "Enterprise"
            target_markup = "2-3x"
            price_range = f"${cost * 2:.0f}-${cost * 3:.0f}"

        report.append(f"**{scenario.name}** ({tier})")
        report.append(f"- Infrastructure: ${cost:.2f}/month")
        report.append(f"- Recommended markup: {target_markup}")
        report.append(f"- Suggested pricing: {price_range}/month")
        report.append("")

    report.append("### Key Insights\n")
    report.append(f"- Target infrastructure costs to be **20-40%** of revenue")
    report.append(f"- With {markup}x markup, infrastructure represents {(1/markup)*100:.0f}% of revenue")
    report.append(f"- Lower cost scenarios need higher markup multiples for viability")
    report.append(f"- Higher cost scenarios can afford lower markup due to larger absolute margins")

    report.append("\n---\n")
    report.append("\n*Report generated by LLM Pricing Simulator*")
    report.append("\n*Dashboard: http://100.126.153.59:8501*")

    return "\n".join(report)


if __name__ == "__main__":
    main()
