# Market Research & Campaign Advisor Tool

Strategic advisor for launching academic, skill-based, and language learning courses in Moldova, Georgia, and Armenia.

## Quick Start

### Use the Market Analysis Skill
```
/market-analysis python-skills moldova premium
```

Analyzes competitive landscape for a specific course type, market, and pricing tier.

### Use the Pricing Analyzer
```
/pricing-analyzer english-course 60-hours georgia
```

Compares pricing across all three markets and recommends optimal pricing strategy.

### Generate a Lesson Plan
```
/lesson-plan-generator english-professional georgia 60-hours intermediate
```

Drafts market-backed lesson plans with competitive positioning.

### Create a Campaign Plan
```
/campaign-planner python-bootcamp moldova launch-strategy
```

Generates comprehensive launch campaign strategy with market-backed positioning.

## Project Structure

```
/data/
  - moldova-competitors.json    # Chișinău market analysis
  - georgia-competitors.json    # Tbilisi market analysis
  - armenia-competitors.json    # Yerevan market analysis

/.claude/skills/
  - market-analysis/            # Analyze market opportunities
  - pricing-analyzer/           # Compare pricing strategies
  - lesson-plan-generator/      # Generate course outlines
  - campaign-planner/           # Create launch strategies

CLAUDE.md                        # Project context and conventions
```

## Market Data Summary

### Moldova (Chișinău)
- **Budget tier**: €3/hour (group courses)
- **Mid tier**: €15/hour (established schools)
- **Premium tier**: €30/hour (individual lessons)
- **Main gap**: Tech skills training underdeveloped

### Georgia (Tbilisi)
- **Budget tier**: €12/hour (group language courses)
- **Mid tier**: €15/hour (one-to-one instruction)
- **Premium tier**: €100/hour (tech bootcamps)
- **Opportunity**: Mid-tier tech skills (between bootcamp and basic courses)

### Armenia (Yerevan)
- **Budget tier**: $8/hour (subsidized, free programs)
- **Mid tier**: $12/hour (established schools)
- **Premium tier**: $25/hour (Berlitz, specialized training)
- **Main gap**: Premium language training, niche skill combinations

## Key Metrics

All pricing is **distilled to per-academic-hour** basis:
- 1 academic hour = 45-75 minutes of instruction
- Normalized across all course types for fair comparison

**Example calculation:**
- Course: 3 months, 6 hours/week = 72 total hours
- Total cost: €1,200
- **Hourly rate: €1,200 ÷ 72 = €16.67/hour**

## Instructor Compensation Context

- **Software dev/tech**: $25-99/hour (market rate)
- **Language instructor**: €500/month (Moldova), ~$2,000/month (Armenia)
- **General course instructor**: 30-40% of course revenue per hour taught

## What's Included

✅ **Competitive pricing data** for all major course types in capital cities
✅ **Market tier analysis** (budget/mid/premium positioning)
✅ **Instructor rate intelligence** for compensation modeling
✅ **Gap identification** for underserved market segments
✅ **Reusable skills** for ongoing analysis
✅ **Templates** for lesson plans and campaigns

## Next Steps

1. Choose a course type (e.g., Python, English, Digital Marketing)
2. Choose a market (Moldova, Georgia, Armenia)
3. Run market analysis: `/market-analysis [type] [market] [tier]`
4. Generate pricing recommendation: `/pricing-analyzer [course] [hours]`
5. Draft lesson plan: `/lesson-plan-generator [type] [market] [hours]`
6. Create campaign: `/campaign-planner [course] [market] launch-strategy`

## Data Sources

Research completed February 2026 from:
- Language course platforms (Language International, Language Course, Georgian Courses)
- Tech training providers (The Knowledge Academy, AZTech Training)
- Academic institutions (AUA, ICLT, Berlitz)
- Market salary data (TimeCamp, Paylab, Trading Economics)

All data is public and from official institute websites and market research sources.
