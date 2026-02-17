---
name: market-analysis
description: Analyze market opportunity in a specific country, course type, and pricing tier
---

# Market Analysis Skill

Analyze competitive landscape and identify market opportunities across Moldova, Georgia, and Armenia.

## Usage Examples

`/market-analysis python skills moldova premium`
`/market-analysis english language georgia mid`
`/market-analysis business-skills armenia budget`

## Analysis Process

1. **Load competitor data** from `/data/{country}-competitors.json`

2. **Filter by course type and tier**:
   - Course types: language-learning, tech-skills, professional-development, academic
   - Tiers: budget, mid, premium

3. **Calculate market metrics**:
   - Hourly pricing ranges in local currency and EUR/USD
   - Instructor compensation models (% of revenue or fixed rates)
   - Course structure patterns (duration, frequency, group size)
   - Market saturation level

4. **Identify opportunities**:
   - Pricing gaps (where no competitors exist in specific tier/type)
   - Underserved specializations (e.g., language + tech combinations)
   - Instructor shortage indicators
   - Demand signals from market context

5. **Generate outputs**:
   - 3-5 competitive positioning strategies
   - Recommended hourly pricing (with tier positioning)
   - 2-3 course topic suggestions with demand signals
   - 5-8 lesson outline template for strongest opportunity
   - Instructor compensation model recommendation

## Data Structure

Each competitor file contains:
- Competitor name, type, tier (budget/mid/premium)
- Pricing (distilled to hourly rates)
- Services offered
- Instructor market data (salaries, rates)
- Market gaps and observations

## Output Format

Always include:
- Market summary (competitor count, price ranges, saturation)
- Recommended positioning (tier + differentiation strategy)
- Pricing recommendation (hourly rate with rationale)
- Course topic recommendations (3-5 options)
- Sample lesson outline (5-8 lessons with LOs)
- Instructor compensation model
- Risk/opportunity assessment
- Sources cited from competitor data
