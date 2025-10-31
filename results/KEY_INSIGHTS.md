# LLM Pricing Simulator - Key Insights

## Executive Summary

Based on simulations of 4 job-to-be-done scenarios for an LLM visibility/competitor-tracking product, here are the key cost findings:

## Cost Range by Use Case

| Scenario | Monthly Cost | Calls/Month | Cost per 1K Calls |
|----------|--------------|-------------|-------------------|
| **JTBD 1**: Brand Monitoring (Daily) | **$58** | 16,200 | $3.60 |
| **JTBD 2**: Alerts (Mixed Freq) | **$1,046** | 336,000 | $3.11 |
| **JTBD 3**: Model Comparison (2hr) | **$3,891** | 1,152,000 | $3.38 |
| **JTBD 4**: Competitor Discovery | **$176** | 43,200 | $4.07 |

## Key Findings

### 1. Model Cost Comparison

**Most Expensive**: Claude 3.7 Sonnet consistently costs the most
- JTBD 1: $33.62 (58% of total)
- JTBD 2: $522.90 (50% of total)
- JTBD 3: $1,900.80 (49% of total)
- JTBD 4: $101.23 (58% of total)

**Most Economical**: Gemini 2.5 Flash is 24-47x cheaper than Claude
- JTBD 1: $1.40 (2% of total)
- JTBD 2: $21.73 (2% of total)
- JTBD 3: $79.49 (2% of total)
- JTBD 4: $4.23 (2% of total)

**Budget Option**: Claude 3.5 Haiku and GPT-4o-mini offer good balance
- ~70-80% cheaper than flagship models
- Suitable for extraction and classification tasks

### 2. Frequency Impact

Frequency is the biggest cost driver:
- **Hourly monitoring** (JTBD 2 high-priority): $897/month for just 10 intents
- **Daily monitoring** (JTBD 1): $58/month for 30 intents
- **Every 2 hours** (JTBD 3): $3,891/month for 80 intents

**Rule of thumb**: Hourly monitoring costs ~15x more than daily for similar intent counts.

### 3. Multi-Pass Processing

Additional LLM steps add significant cost:
- **2 steps** (answer + extract): Base cost
- **3 steps** (answer + extract + cluster): +30-50% additional cost
- **Judge/comparison step**: Adds ~40% to total (JTBD 3)

### 4. Pricing Strategy Implications

**Conservative Base Package** ($100-150/month):
- 50 intents, 3 variants
- Daily frequency
- 3 models
- 2-step processing
- Estimated cost: ~$100

**Professional Package** ($500-750/month):
- 100 intents, 5 variants
- 4-hourly on top 20, daily on rest
- 4 models
- 2-3 step processing
- Estimated cost: ~$400-600

**Enterprise Package** ($2,000-3,000/month):
- 200+ intents, 5 variants
- Hourly on top 30, 2-hourly on 50, daily on rest
- 5 models
- 3-step processing
- Estimated cost: ~$1,500-2,500

### 5. Cost Optimization Strategies

**High Impact**:
1. **Use Gemini for high-volume tasks**: 20-40x cheaper, good for initial filtering
2. **Tier your monitoring**: Hourly only for critical intents
3. **Smart model selection**: Use Haiku/mini for extraction, flagship for main answers

**Medium Impact**:
4. **Batch similar queries**: Reduce redundant processing
5. **Cache-aware prompting**: Could save 20-30% with prompt caching
6. **Optimize token usage**: Shorter prompts, concise outputs

**Low Impact**:
7. **Provider switching**: 10-30% savings by choosing optimal provider per task
8. **Time-based pricing**: Some providers offer off-peak discounts

## Viability Assessment

**Unit Economics Look Good**:
- Even expensive scenario (JTBD 3) costs $3.38 per 1,000 calls
- With 3-5x markup, can charge $10-17 per 1,000 calls
- Or package as $150-500/month SaaS tiers with healthy margins

**Biggest Risks**:
1. **Price volatility**: OpenAI has changed prices 3x in 18 months
2. **Usage explosion**: If customers add many more intents than expected
3. **Model requirements**: If only Claude Sonnet produces acceptable quality

**Mitigation**:
- Build 30-40% buffer into pricing
- Hard limits on free/starter tiers
- Design for model flexibility (can swap Gemini for GPT)

## Next Steps

1. **Validate token estimates**: Run real prompts through tokenizers
2. **Quality testing**: Confirm Gemini/Haiku work for extraction tasks
3. **Historical analysis**: Check price volatility over past 6-12 months
4. **Pilot pricing**: Test $199/mo for 100-intent package with early customers
5. **Build alerts**: Monitor when costs exceed thresholds
