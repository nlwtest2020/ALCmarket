---
name: pricing-analyzer
description: Calculate and compare pricing strategies across all three markets
---

# Pricing Analyzer Skill

Compare pricing strategies across Moldova, Georgia, and Armenia. Help determine optimal pricing for new courses.

## Usage Examples

`/pricing-analyzer english-course 60-hours`
`/pricing-analyzer python-bootcamp 48-hours mid-tier`
`/pricing-analyzer specialized-training 30-hours georgia premium`

## Analysis Process

1. **Load all three market competitor files**:
   - `/data/moldova-competitors.json`
   - `/data/georgia-competitors.json`
   - `/data/armenia-competitors.json`

2. **Extract comparable courses**:
   - Find courses similar in type and duration
   - Convert all pricing to hourly rates (normalize 45min-1h15min units)
   - Identify tier pricing ranges

3. **Calculate pricing models**:
   - **Budget tier**: Floor price (lowest competitor in type)
   - **Mid tier**: Average competitor pricing + 15%
   - **Premium tier**: Top competitor pricing + 10-20%

4. **Instructor compensation analysis**:
   - Extract instructor rates/salaries by market
   - Calculate % of revenue needed for instructor payment
   - Recommend margin structure (target: 50-70% margin)

5. **Currency conversions**:
   - Convert to local currency for student pricing
   - Show EUR/USD equivalents
   - Note purchasing power parity adjustments

6. **Market validation**:
   - Check pricing against local income levels
   - Identify any outliers
   - Flag if pricing seems misaligned with market

## Output Format

For each market:
- Current competitor hourly rates (by tier)
- Recommended pricing (hourly + total for course hours)
- Local currency pricing (MDL, GEL, AMD)
- EUR/USD equivalent
- Instructor compensation required
- Recommended margin %
- Positioning rationale

Include summary table comparing recommended pricing across all three markets.
