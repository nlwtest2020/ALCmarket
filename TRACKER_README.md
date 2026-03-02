# ALC Competitive Intelligence Tracker

A comprehensive system for tracking competitor social media presence, engagement, and website changes across Moldova, Georgia, and Armenia language learning markets.

## Features

- **Facebook Tracking**: Collect follower counts, post engagement, posting frequency, and content types
- **Instagram Tracking**: Monitor profile metrics, follower growth, and content engagement
- **Website Monitoring**: Detect significant changes to competitor websites and pricing pages
- **Interactive Dashboard**: Dark-themed web interface for analyzing competitor metrics
- **Historical Data**: Build trends over time to track competitor growth
- **Error Handling**: Gracefully handles missing data and network errors

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run All Scrapers

```bash
python run_all.py
```

This will:
- Scrape Facebook pages for all competitors in `competitors.csv`
- Collect Instagram profile metrics
- Monitor websites for pricing and course changes
- Save results as JSON files in `data/` directories

### 3. Start the Dashboard

```bash
python -m flask --app dashboard/app.py run
```

Visit `http://localhost:5000` to view the dashboard.

## Project Structure

```
.
├── competitors.csv                  # List of competitors to track
├── config.py                        # Configuration settings
├── run_all.py                       # Main orchestration script
├── requirements.txt                 # Python dependencies
├── scrapers/
│   ├── __init__.py
│   ├── facebook_tracker.py          # Facebook scraper
│   ├── instagram_tracker.py         # Instagram scraper
│   └── website_monitor.py           # Website change detection
├── dashboard/
│   ├── __init__.py
│   ├── app.py                       # Flask application
│   ├── templates/
│   │   ├── base.html               # Base template
│   │   ├── index.html              # Market overview
│   │   ├── trends.html             # Follower trends
│   │   ├── content_analysis.html   # Engagement analysis
│   │   ├── website_changes.html    # Change detection
│   │   └── error.html              # Error page
│   └── static/
│       ├── css/
│       │   └── style.css           # Dark theme styling
│       └── js/
│           └── main.js             # Dashboard utilities
├── data/
│   ├── facebook/                   # Facebook scraping results
│   ├── instagram/                  # Instagram scraping results
│   └── websites/                   # Website change logs
├── snapshots/                      # Website content snapshots
└── logs/                           # Scraper logs
```

## Competitors CSV Format

The `competitors.csv` file should have these columns:

```csv
market,name,website_url,facebook_url,instagram_handle,notes
Moldova,Chisinau Language School,https://...,https://facebook.com/...,handle,description
```

## Configuration

Edit `config.py` to customize:

- Scraping intervals (hourly, daily, weekly)
- Website change detection threshold (default 10%)
- Number of posts/profiles to collect
- Data storage paths

## Dashboard Pages

### Overview (/)
- Market comparison table
- Competitor metrics (followers, engagement, posting frequency)
- Quick view of all tracked competitors

### Trends (/trends)
- Facebook follower growth charts over 30/60/90 days
- Instagram follower growth over time
- Date range selector

### Content Analysis (/content-analysis)
- Engagement rate comparisons (Facebook vs Instagram)
- Posting frequency by competitor
- Content type breakdown (video vs image vs carousel)

### Website Changes (/website-changes)
- Timeline of detected website changes
- Diff preview of what changed
- Change percentage indicator
- Organized by market and competitor

## How It Works

### Facebook Tracking
1. Uses mobile site (mbasic.facebook.com) for easier scraping
2. Extracts public page data without API keys
3. Collects: follower count, recent posts, engagement metrics
4. Calculates: posting frequency, engagement rate, video percentage

### Instagram Tracking
1. Scrapes public profile pages
2. Extracts: follower/following count, total posts
3. Collects recent posts with engagement data
4. Detects: video vs image vs carousel posts

### Website Monitoring
1. Fetches main page and course/pricing subpages
2. Strips navigation, scripts, and footers
3. Compares text content to previous snapshot
4. Flags changes > 10% as significant
5. Saves diff preview for manual review

## Output Files

### Facebook Data
`data/facebook/YYYY-MM-DD_market.json`
```json
{
  "scraped_at": "2026-03-02T15:00:00",
  "competitors": [
    {
      "competitor_name": "School Name",
      "market": "Moldova",
      "followers": 1234,
      "engagement_metrics": {
        "avg_engagement_rate": 45.5,
        "posts_per_week": 3.2,
        "video_percentage": 25.0
      },
      "posts": [...]
    }
  ]
}
```

### Website Changes
`data/websites/changes_YYYY-MM-DD.json`
```json
{
  "monitored_at": "2026-03-02T15:00:00",
  "changes_detected": [
    {
      "competitor_name": "School",
      "market": "Georgia",
      "pages_monitored": [
        {
          "url": "https://...",
          "page_type": "courses",
          "changed": true,
          "change_details": {
            "change_percentage": 15.5,
            "lines_changed": 42,
            "diff_preview": "..."
          }
        }
      ]
    }
  ]
}
```

## Error Handling

All scrapers gracefully handle:
- Network timeouts
- Missing pages (404)
- Private/restricted profiles
- Invalid URLs
- Missing competitor data

Errors are logged to `logs/tracker.log` for debugging.

## Running on a Schedule

To run scrapers daily via cron:

```bash
0 0 * * * cd /path/to/ALCmarket && python run_all.py >> logs/cron.log 2>&1
```

Or use the `schedule` library in a long-running process:

```python
import schedule
import time
from run_all import main

schedule.every().day.at("00:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Dashboard Dark Theme

The dashboard features a dark theme optimized for competitive intelligence analysis:
- Dark background (#1a1a1a) reduces eye strain
- Color-coded metrics (green/yellow/red performance indicators)
- Bootstrap 5 responsive design
- Chart.js for dynamic visualizations

## Troubleshooting

### Scraper returns no data
- Check network connection
- Verify URLs in `competitors.csv`
- Check logs: `logs/tracker.log`
- Try manual URL in browser to confirm accessibility

### Dashboard shows no data
- Run `python run_all.py` to populate data
- Check `data/` directories for JSON files
- Verify Flask is running on port 5000

### Website monitoring not detecting changes
- Change threshold is 10% by default (configurable in `config.py`)
- Website snapshots stored in `snapshots/` directory
- Check `logs/tracker.log` for scraping issues

## Performance Notes

- Facebook scraping: ~2-5 seconds per page
- Instagram scraping: ~1-3 seconds per profile
- Website monitoring: ~2-10 seconds per site
- Total run time: ~2-5 minutes for all competitors

## Legal & Ethical

- Only scrapes public data (no authentication required)
- Respects robots.txt and website terms of service
- No automated bulk downloading or spam
- Designed for market research and business intelligence
- Used for competitive analysis only

## Future Enhancements

- Email alerts for significant changes
- Automated competitor benchmarking
- Pricing history tracking
- Course curriculum analysis
- Competitor growth predictions
- Integration with Google Sheets
- API endpoint for programmatic access

## Support

For issues, check:
1. `logs/tracker.log` for error messages
2. `competitors.csv` for URL validity
3. Network connectivity
4. Flask port availability (5000)
