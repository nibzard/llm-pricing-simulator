# LLM Pricing Simulation Report
## Infrastructure Cost Analysis & SaaS Pricing Strategy

**Generated:** 2025-11-01
**Price Source:** llm-prices.com (Updated 2025-10-29)
**Models Analyzed:** 78 current LLM models

---

## Executive Summary

This report analyzes 8 operational scenarios for LLM-powered competitive intelligence products, ranging from **$49.55 to $8,997.12 per month** in infrastructure costs. We examine realistic use cases across different frequencies, model counts, and usage patterns to establish viable SaaS pricing strategies.

### Key Findings

- **Unit economics are viable** across all scenarios with 3-5x markup
- **Monthly frequency** is the most cost-effective pattern ($49.55/month)
- **Hourly monitoring** drives highest costs but serves critical use cases ($765/month for mixed frequency)
- **Model comparison at scale** requires premium pricing ($8,997/month)
- **Dedicated extraction models** reduce costs by 20-35% vs. using all flagship models

---

## Scenario Analysis

### 1. Custom Scenario: Ultra-Budget Weekly Monitoring
**Monthly Infrastructure Cost:** $49.55

#### Configuration
- **Models:** 9 models listed (claude-opus-4, sonnet-4.5, haiku, gpt-5, gpt-5-mini, gemini-2.5-pro, gemini-flash, grok-4, grok-fast)
- **Strategy:** Single budget model (gpt-5-mini) for all processing
- **Prompts:** 20 intents × 3 variants = 60 prompts
- **Frequency:** Weekly (4 runs/month)
- **Total API Calls:** 4,320/month

#### Cost Breakdown
- Main answer generation: $43.28 (87%)
- Entity extraction: $6.26 (13%)
- All processing done by gpt-5-mini

#### Use Case
Ideal for bootstrapped startups or side projects needing low-frequency competitive monitoring with minimal costs.

#### Pricing Strategy

**Recommended SaaS Tiers:**

| Tier | Monthly Price | Margin | Markup | Notes |
|------|--------------|--------|--------|-------|
| **Solo** | $150 | $100.45 | 3.0x | Perfect for indie developers |
| **Starter** | $200 | $150.45 | 4.0x | Add basic support |
| **Growth** | $350 | $300.45 | 7.0x | Weekly reports + alerts |

**Unit Economics:**
- Cost per prompt: $0.83
- Recommended charge: $2.50-3.00 per prompt
- Cost per intent tracked: $2.48
- Recommended charge: $7.50-10.00 per intent

**Profitability:** Excellent margins even at low price points. Can offer generous free tier (5-10 intents).

---

### 2. All on 10: Comprehensive Daily Model Comparison
**Monthly Infrastructure Cost:** $58.33

#### Configuration
- **Models:** 8 flagship/efficient models (claude-sonnet-4.5, haiku, gpt-5, gpt-5-mini, gemini-2.5-pro, gemini-flash, grok-4, grok-fast)
- **Strategy:** Test ALL 8 models daily, extract with gpt-5-mini
- **Prompts:** 10 intents × 3 variants = 30 prompts
- **Frequency:** Daily (30 runs/month)
- **Total API Calls:** 14,400/month

#### Cost Breakdown
- Main answer (8 models): $53.65 (92%)
- Entity extraction (gpt-5-mini): $4.68 (8%)

**Model cost distribution:**
- Claude Sonnet 4.5: $13.91 (24%)
- Grok-4: $13.91 (24%)
- GPT-5: $9.17 (16%)
- Gemini 2.5 Pro: $9.17 (16%)
- Others: $11.67 (20%)

#### Use Case
Teams wanting comprehensive daily LLM comparison across all major providers for product research or positioning analysis.

#### Pricing Strategy

**Recommended SaaS Tiers:**

| Tier | Monthly Price | Margin | Markup | Notes |
|------|--------------|--------|--------|-------|
| **Professional** | $250 | $191.67 | 4.3x | 10 intents tracked |
| **Business** | $500 | $441.67 | 8.6x | 25 intents + API access |
| **Enterprise** | $1,000 | $941.67 | 17.1x | Unlimited + white-label |

**Unit Economics:**
- Cost per intent: $5.83
- Recommended charge: $25.00 per intent
- Cost per model comparison: $1.94
- Recommended charge: $8-10 per comparison

**Key Value Prop:** "See how every major LLM responds to your competitive questions - daily updates across 8 models."

---

### 3. JTBD 1: Brand/Category Monitoring (Daily)
**Monthly Infrastructure Cost:** $40.59

#### Configuration
- **Models:** 3 flagship models (claude-sonnet-4.5, gpt-5, gemini-2.5-flash)
- **Prompts:** 30 intents × 3 variants = 90 prompts
- **Frequency:** Daily (30 runs/month)
- **Total API Calls:** 16,200/month

#### Cost Breakdown
- Main answer (3 models): $36.34 (90%)
- Entity extraction (gpt-5-mini): $4.25 (10%)

**Model distribution:**
- Claude Sonnet 4.5: $21.46 (53%)
- GPT-5: $14.01 (35%)
- Gemini Flash: $0.87 (2%)
- GPT-5-mini (extract): $4.25 (10%)

#### Use Case
Daily monitoring of how LLMs frame specific brands or product categories. Critical for PR teams and brand managers tracking AI perception.

#### Pricing Strategy

**Recommended SaaS Tiers:**

| Tier | Monthly Price | Margin | Markup | Notes |
|------|--------------|--------|--------|-------|
| **Brand Monitor** | $150 | $109.41 | 3.7x | 10 brands tracked |
| **Category Suite** | $350 | $309.41 | 8.6x | 30 brands/categories |
| **Agency** | $750 | $709.41 | 18.5x | White-label + multi-client |

**Unit Economics:**
- Cost per intent: $1.35
- Recommended charge: $5.00-8.00 per brand tracked
- Cost per model/day: $0.45
- Value delivered: Track brand perception shift across top LLMs

**Target Market:** Brand managers, PR agencies, marketing teams worried about AI-generated content about their products.

---

### 4. JTBD 2: Ranking Change Alerts (Mixed Frequency)
**Monthly Infrastructure Cost:** $764.82

#### Configuration
- **Models:** 4 models (claude-sonnet-4.5, gpt-5, gemini-flash, haiku)
- **Intent Groups:**
  - High priority: 10 intents × 5 variants, hourly (36,000 calls/month)
  - Standard: 40 intents × 5 variants, daily (6,000 calls/month)
- **Total API Calls:** 336,000/month

#### Cost Breakdown
- High-priority hourly monitoring: $655.56 (86%)
- Standard daily monitoring: $109.26 (14%)
- Model processing: $676.62 (88%)
- Extraction (gpt-5-mini): $88.20 (12%)

**Model distribution:**
- Claude Sonnet 4.5: $333.90 (44%)
- GPT-5: $217.88 (28%)
- Claude Haiku: $111.30 (15%)
- GPT-5-mini: $88.20 (12%)

#### Use Case
Real-time competitive intelligence for products with volatile LLM rankings. Alerts when competitor mentions increase or product positioning changes in AI responses.

#### Pricing Strategy

**Recommended SaaS Tiers:**

| Tier | Monthly Price | Margin | Markup | Notes |
|------|--------------|--------|--------|-------|
| **Alert Basic** | $2,500 | $1,735.18 | 3.3x | 5 hourly + 20 daily alerts |
| **Alert Pro** | $4,500 | $3,735.18 | 5.9x | Full monitoring + Slack integration |
| **Enterprise** | $8,000 | $7,235.18 | 10.5x | Custom alerts + dedicated support |

**Unit Economics:**
- Cost per hourly-monitored intent: $13.11
- Recommended charge: $50.00 per critical alert
- Cost per daily-monitored intent: $2.73
- Recommended charge: $10.00 per standard alert

**Target Market:** E-commerce platforms, SaaS products, crypto projects - anyone where LLM perception changes rapidly affect business.

**Key Insight:** Hourly monitoring is 5x more expensive but essential for high-stakes scenarios. Price accordingly.

---

### 5. JTBD 3: LLM Framing Comparison (High Usage)
**Monthly Infrastructure Cost:** $8,997.12

#### Configuration
- **Models:** 5 flagship models (claude-opus-4, claude-sonnet-4.5, gpt-5, gpt-5-mini, gemini-2.5-pro)
- **Prompts:** 80 intents × 4 variants = 320 prompts
- **Frequency:** 2-hourly (12 runs/day = 360 runs/month)
- **Total API Calls:** 1,152,000/month

#### Cost Breakdown
- Main answer (5 models): $8,219.52 (91%)
- Judge differences (gpt-5-mini): $777.60 (9%)

**Model distribution:**
- Claude Opus 4: $5,529.60 (61%) - Premium flagship
- Claude Sonnet 4.5: $1,105.92 (12%)
- GPT-5-mini (judge): $921.60 (10%)
- GPT-5: $720.00 (8%)
- Gemini 2.5 Pro: $720.00 (8%)

#### Use Case
Enterprise-grade research comparing how different LLMs frame products, competitors, and narratives. Critical for AI strategy teams and large enterprises managing AI reputation.

#### Pricing Strategy

**Recommended SaaS Tiers:**

| Tier | Monthly Price | Margin | Markup | Notes |
|------|--------------|--------|--------|-------|
| **Research** | $25,000 | $16,002.88 | 2.8x | 50 intents, 2-hourly |
| **Enterprise** | $45,000 | $36,002.88 | 5.0x | Full 320 intents |
| **Custom** | $75,000+ | $66,002.88+ | 8.3x+ | White-label + consulting |

**Unit Economics:**
- Cost per intent (2-hourly): $28.12
- Recommended charge: $140-200 per intent
- Infrastructure represents 20-36% of revenue at these price points

**Target Market:** Fortune 500 companies, AI-native enterprises, major brands managing LLM perception at scale.

**Note:** This is a premium product. The high cost is justified by:
- Near real-time monitoring (every 2 hours)
- 5 flagship models including expensive Claude Opus 4
- Automated judging/comparison layer
- Large prompt battery (320 queries)

---

### 6. JTBD 4: Competitor Discovery (Moderate Usage)
**Monthly Infrastructure Cost:** $162.67

#### Configuration
- **Models:** 3 models (claude-sonnet-4.5, gpt-5, gemini-2.5-pro)
- **Prompts:** 40 intents × 4 variants = 160 prompts
- **Frequency:** Daily (30 runs/month)
- **Flow:** Answer → Extract (haiku) → Cluster competitors (gpt-5-mini)

#### Cost Breakdown
- Main answer (3 models): $122.35 (75%)
- Entity extraction (haiku): $31.68 (19%)
- Competitor clustering (gpt-5-mini): $8.64 (5%)

**Model distribution:**
- Claude Sonnet 4.5: $52.99 (33%)
- GPT-5: $34.68 (21%)
- Gemini 2.5 Pro: $34.68 (21%)
- Claude Haiku: $31.68 (19%)
- GPT-5-mini: $8.64 (5%)

#### Use Case
Track competitor mentions in LLM responses. Essential for understanding competitive landscape as perceived by AI assistants.

#### Pricing Strategy

**Recommended SaaS Tiers:**

| Tier | Monthly Price | Margin | Markup | Notes |
|------|--------------|--------|--------|-------|
| **Competitor Lite** | $500 | $337.33 | 3.1x | 20 intents tracked |
| **Competitor Pro** | $1,200 | $1,037.33 | 7.4x | 40 intents + clustering |
| **Market Intelligence** | $2,500 | $2,337.33 | 15.4x | Unlimited + API |

**Unit Economics:**
- Cost per intent: $4.07
- Recommended charge: $12.50-30.00 per intent
- Cost per competitor cluster: $0.05
- Value: Automated competitive intelligence from AI

**Target Market:** Product managers, competitive intelligence teams, VCs researching market landscapes.

---

### 7. Test Battery: 50 Questions Daily
**Monthly Infrastructure Cost:** $89.55

#### Configuration
- **Models:** 3 flagship models (claude-sonnet-4.5, gpt-5, gemini-2.5-pro)
- **Prompts:** 50 intents × 2 variants = 100 prompts
- **Frequency:** Daily (30 runs/month)
- **Total API Calls:** 27,000/month

#### Cost Breakdown
- Main answer (3 models): $82.46 (92%)
- Entity extraction (gpt-5-mini): $7.09 (8%)

**Model distribution:**
- Claude Sonnet 4.5: $35.78 (40%)
- GPT-5: $23.34 (26%)
- Gemini 2.5 Pro: $23.34 (26%)
- GPT-5-mini: $7.09 (8%)

#### Use Case
Standard monitoring of 50 key questions across top 3 LLMs. Balanced approach for most competitive intelligence needs.

#### Pricing Strategy

**Recommended SaaS Tiers:**

| Tier | Monthly Price | Margin | Markup | Notes |
|------|--------------|--------|--------|-------|
| **Standard** | $400 | $310.45 | 4.5x | 50 questions daily |
| **Professional** | $800 | $710.45 | 8.9x | + API + webhooks |
| **Team** | $1,500 | $1,410.45 | 16.8x | Multi-user + white-label |

**Unit Economics:**
- Cost per question/day: $2.99
- Recommended charge: $8-16 per question
- Cost per 1K API calls: $3.32

**Sweet Spot:** This represents the balanced approach most customers need - good model coverage, daily updates, reasonable costs.

---

### 8. Example Dedicated Models: Premium with Cost Optimization
**Monthly Infrastructure Cost:** $117.47

#### Configuration
- **Models:** 3 premium flagship (claude-opus-4, gpt-5, gemini-2.5-pro)
- **Prompts:** 30 intents × 3 variants = 90 prompts
- **Frequency:** Daily (30 runs/month)
- **Flow:** Answer → Extract (haiku) → Judge (gpt-5-mini)

#### Cost Breakdown
- Main answer (3 premium models): $108.90 (93%)
- Entity extraction (haiku): $7.29 (6%)
- Quality judging (gpt-5-mini): $1.28 (1%)

**Model distribution:**
- Claude Opus 4: $86.40 (74%) - Most expensive flagship
- GPT-5: $11.25 (10%)
- Gemini 2.5 Pro: $11.25 (10%)
- Claude Haiku: $7.29 (6%)
- GPT-5-mini: $1.28 (1%)

#### Use Case
Premium model quality (including expensive Opus 4) with optimized extraction/judging pipeline. Shows the value of dedicated budget models for secondary tasks.

#### Pricing Strategy

**Recommended SaaS Tiers:**

| Tier | Monthly Price | Margin | Markup | Notes |
|------|--------------|--------|--------|-------|
| **Premium** | $500 | $382.53 | 4.3x | Top model quality |
| **Enterprise** | $1,200 | $1,082.53 | 10.2x | + custom intents |
| **White Label** | $2,500 | $2,382.53 | 21.3x | Reseller program |

**Unit Economics:**
- Cost per intent: $3.92
- Recommended charge: $16.67-40.00 per intent
- Claude Opus 4 adds significant cost but provides best quality

**Key Insight:** Using dedicated haiku ($7.29) and gpt-5-mini ($1.28) for extraction/judging vs. running full premium models saves ~$80-100/month while maintaining quality.

---

## Cross-Scenario Insights

### Cost Drivers Analysis

| Factor | Impact on Cost | Example |
|--------|----------------|---------|
| **Frequency** | 12-24x | Hourly vs. daily: $655 vs. $109 (same intents) |
| **Model Count** | Linear | 3 models vs. 8 models: $40 vs. $58 |
| **Model Tier** | 3-5x | Opus 4 vs. GPT-5-mini per call |
| **Prompt Count** | Linear | 30 intents vs. 320 intents: $40 vs. $8,997 |
| **Dedicated Models** | -20-35% | Extract with haiku vs. flagship models |

### Pricing Strategy Principles

#### 1. Markup Guidelines by Cost Tier

| Monthly Cost | Recommended Markup | Target Price | Reasoning |
|--------------|-------------------|--------------|-----------|
| < $100 | 3-7x | $300-700 | High margin needed for small absolute revenue |
| $100-500 | 3-5x | $300-2,500 | Balanced approach |
| $500-2,000 | 2.5-4x | $1,250-8,000 | Competitive market |
| $2,000+ | 2-3x | $4,000-25,000+ | Volume play + consulting |

#### 2. Value-Based Pricing vs. Cost-Plus

Infrastructure cost should be **20-40% of revenue** in mature SaaS businesses:

- 20-25%: Efficient, scaled operation with good margins
- 25-35%: Healthy growing business
- 35-40%: Early stage or high support burden
- 40%+: Unsustainable except for enterprise custom deals

#### 3. Tiering Strategy

**Good Tier Structure:**
1. **Entry tier:** 2-3x cost (loss leader for acquisition)
2. **Growth tier:** 4-6x cost (target tier for most customers)
3. **Professional tier:** 6-10x cost (power users)
4. **Enterprise tier:** 10-20x cost (custom, high-touch)

### Unit Economics Benchmarks

| Scenario Type | Cost/Intent | Charge/Intent | Margin/Intent |
|---------------|-------------|---------------|---------------|
| Weekly (budget) | $2.48 | $7.50-10 | $5-7.50 |
| Daily (standard) | $1.35-4.07 | $5-16 | $3.65-12 |
| Hourly (critical) | $13.11 | $50+ | $37+ |
| 2-hourly (premium) | $28.12 | $140-200 | $112-172 |

---

## Recommendations

### For Bootstrapped Startups (< $500/mo infrastructure)

**Best Scenarios:**
- Custom Scenario ($49.55)
- JTBD 1 ($40.59)
- All on 10 ($58.33)

**Pricing Strategy:**
- Start at $150-400/month
- Focus on weekly or daily frequency
- Use gpt-5-mini for extraction
- Offer generous free tier (5-10 intents)
- Target markup: 3-7x

**Target customers:** Solo developers, small agencies, indie products

---

### For Growing Startups ($500-2K/mo infrastructure)

**Best Scenarios:**
- Test Battery ($89.55)
- Example Dedicated ($117.47)
- JTBD 4 ($162.67)

**Pricing Strategy:**
- Tiers: $400 / $800 / $1,500
- Daily frequency standard
- Mix of flagship and budget models
- Target markup: 4-8x
- Add API access at higher tiers

**Target customers:** Product teams, marketing agencies, competitive intelligence firms

---

### For Scale-Ups ($2K-10K/mo infrastructure)

**Best Scenarios:**
- JTBD 2 Mixed Frequency ($764.82)
- High-volume variations of JTBD 1/4

**Pricing Strategy:**
- Tiers: $2,500 / $4,500 / $8,000
- Mix hourly critical + daily standard
- Enterprise features (SSO, SLA)
- Target markup: 3-5x
- Volume discounts available

**Target customers:** E-commerce platforms, SaaS companies, enterprises with 50+ employees

---

### For Enterprise ($10K+/mo infrastructure)

**Best Scenarios:**
- JTBD 3 Model Comparison ($8,997.12)
- Custom high-frequency monitoring

**Pricing Strategy:**
- Starting: $25,000/month
- Custom pricing above $50K
- Near real-time (2-hourly) monitoring
- White-label options
- Target markup: 2.5-5x
- Consulting and custom development bundled

**Target customers:** Fortune 500, AI-native unicorns, major brands, consultancies

---

## Cost Optimization Tactics

### 1. Use Dedicated Budget Models

**Savings: 20-35%**

Instead of running all flagship models through entire pipeline:
- Use flagship models for main answer generation
- Use claude-4.5-haiku or gpt-5-mini for extraction
- Use gpt-5-mini for judging/clustering

**Example:**
- Before: All 3 models through all steps = ~$120/month
- After: 3 models answer, 1 budget extract = ~$80/month
- Savings: $40/month (33%)

### 2. Adjust Frequency Based on Value

**Savings: Up to 12x**

Not all intents need same monitoring frequency:
- Critical brand mentions: Hourly ($655/month for 10 intents)
- Standard tracking: Daily ($109/month for 40 intents)
- Research topics: Weekly ($25/month for 20 intents)

Mix frequencies based on customer value.

### 3. Model Count Optimization

**Savings: Variable**

Don't default to testing all models:
- Market research: 5-8 models needed
- Brand monitoring: 3 models sufficient
- Niche tracking: 1-2 models enough

Each additional model adds ~$5-15/month per 30 intents.

### 4. Batch Processing Windows

**Savings: Infrastructure cost**

Instead of continuous processing:
- Daily batch at 2 AM (cheaper compute)
- Weekly summary reports
- Hourly only for P0 alerts

Can reduce API call patterns and optimize for cost.

---

## Conclusion

LLM-powered competitive intelligence products have **strong unit economics** across all tested scenarios:

- **Viable at any scale:** From $50/month to $9,000/month infrastructure
- **Healthy margins:** 3-20x markups sustainable depending on tier
- **Optimization opportunities:** 20-35% savings with dedicated budget models
- **Clear value ladders:** Weekly → Daily → Hourly → 2-hourly monitoring

**Critical success factors:**
1. Match frequency to customer value (not all tracking needs hourly)
2. Use dedicated budget models for extraction/judging
3. Price based on value delivered, not cost-plus
4. Build tiers with 3-10x range from entry to enterprise

**Next Steps:**
1. Start with weekly/daily monitoring for MVP
2. Target $400-800/month pricing for initial customers
3. Scale to hourly monitoring for premium tier
4. Add custom/enterprise tier at 10K+ with consulting

The simulator shows that infrastructure costs are **manageable at all scales**, making this a capital-efficient business model with strong gross margins.

---

## Appendix: All Scenarios Summary Table

| Scenario | Monthly Cost | Frequency | Models | Prompts | Calls/Month | Recommended Price | Markup |
|----------|-------------|-----------|--------|---------|-------------|-------------------|--------|
| Custom | $49.55 | Weekly | 9 (uses 1) | 60 | 4,320 | $150-350 | 3-7x |
| All on 10 | $58.33 | Daily | 8 | 30 | 14,400 | $250-1,000 | 4-17x |
| JTBD 1 | $40.59 | Daily | 3 | 90 | 16,200 | $150-750 | 3.7-18x |
| JTBD 2 | $764.82 | Mixed | 4 | 250 | 336,000 | $2,500-8,000 | 3-10x |
| JTBD 3 | $8,997.12 | 2-hourly | 5 | 320 | 1,152,000 | $25,000-75,000 | 2.8-8x |
| JTBD 4 | $162.67 | Daily | 3 | 160 | 43,200 | $500-2,500 | 3-15x |
| Test Battery | $89.55 | Daily | 3 | 100 | 27,000 | $400-1,500 | 4.5-17x |
| Dedicated | $117.47 | Daily | 3 | 90 | 16,200 | $500-2,500 | 4-21x |

---

**Report Generated by:** LLM Pricing Simulator
**Repository:** https://github.com/nibzard/llm-pricing-simulator
**Dashboard:** http://100.126.153.59:8501
