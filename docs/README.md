# ALC Competitive Intelligence Tracker

**Monitor competitor social media, engagement, and website changes across Moldova, Georgia, and Armenia language learning markets.**

## 📊 What Is This?

A complete system for tracking competitors in three key markets (Moldova, Georgia, Armenia) by monitoring:

- **Facebook Pages**: Follower counts, post engagement, posting frequency, video content
- **Instagram Profiles**: Follower growth, engagement metrics, content strategy
- **Website Changes**: Pricing updates, new courses, curriculum changes

## 🚀 Features

### Real-Time Monitoring
- Track 15+ competitors across 3 markets
- Automatic scraping every 24 hours
- No API keys required (public data only)

### Interactive Dashboard
- **Overview**: Market comparison table
- **Trends**: Follower growth charts (30/60/90 days)
- **Content Analysis**: Engagement rates and posting frequency
- **Website Changes**: Timeline of detected updates with diffs

### Smart Detection
- Website change threshold: 10% (configurable)
- Automatic engagement rate calculations
- Video vs. image content breakdown
- Follower growth trend analysis

## 📍 Markets Covered

### 🇲🇩 Moldova (Chișinău)
- Chisinau Language School
- Top English School
- DGNI - Romanian Language Program

### 🇬🇪 Georgia (Tbilisi)
- Georgian Courses
- Language International Schools
- The Knowledge Academy
- AZTech Training

### 🇦🇲 Armenia (Yerevan)
- ICLT - Yerevan
- Berlitz Yerevan
- BDG Training Center
- 42 Yerevan
- American University of Armenia
- And more...

## 🛠️ Technology Stack

- **Backend**: Python 3.11+
- **Scraping**: BeautifulSoup4, Requests
- **Web Framework**: Flask
- **Frontend**: Bootstrap 5, Chart.js
- **Data**: JSON, CSV, SQLite (optional)

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/nlwtest2020/ALCmarket.git
cd ALCmarket

# Install dependencies
pip install -r requirements.txt

# Run all scrapers
python run_all.py

# Start the dashboard
python -m flask --app dashboard/app.py run
```

Visit: **http://localhost:5000**

## 📊 Key Metrics

### Social Media Metrics
- **Followers**: Real-time follower counts
- **Engagement Rate**: Average likes, comments, shares per post
- **Posting Frequency**: Posts per week
- **Video Percentage**: Portion of video content
- **Reach**: Estimated audience size

### Website Metrics
- **Pricing Changes**: Course pricing updates
- **New Courses**: Course launches and announcements
- **Content Changes**: Curriculum and description updates
- **Change Percentage**: How much of page changed
- **Timestamp**: When changes were detected

## 🎯 Use Cases

1. **Competitive Pricing Analysis**
   - Monitor competitor course pricing
   - Track promotional offers
   - Identify market gaps

2. **Marketing Strategy**
   - Analyze competitor social media activity
   - Compare engagement tactics
   - Identify content trends

3. **Course Development**
   - Discover demand signals from competitor offerings
   - Identify underserved niches
   - Benchmark course quality

4. **Business Intelligence**
   - Track competitor growth
   - Monitor market trends
   - Early detection of strategic pivots

## 📈 Sample Data

Pre-populated data available for testing:
- `data/facebook/` - Facebook metrics for all markets
- `data/instagram/` - Instagram metrics for all markets
- `data/websites/` - Website change detection samples

Run the dashboard immediately without needing to scrape first!

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Scraping intervals
"schedule": "daily"  # hourly, daily, weekly

# Website monitoring
"min_change_threshold": 0.10  # 10% change detection

# Number of posts to collect
"posts_to_fetch": 20  # Facebook
"posts_to_fetch": 12  # Instagram

# Data paths
DATA_DIR = Path("data")
FACEBOOK_DATA_DIR = DATA_DIR / "facebook"
```

## 📚 Documentation

- **[TRACKER_README.md](../TRACKER_README.md)** - Comprehensive guide with setup, usage, and troubleshooting
- **[GitHub Repository](https://github.com/nlwtest2020/ALCmarket)** - Source code and development branch

## 🔗 Links

- **[Source Code](https://github.com/nlwtest2020/ALCmarket/tree/claude/build-competitor-tracker-0U6x1)** - Full implementation
- **[Dashboard](http://localhost:5000)** - Local web interface
- **[Competitors CSV](../competitors.csv)** - List of tracked competitors

## 📊 Dashboard Features

### Overview Page
- Quick market summary
- Competitor metrics table
- Follower/engagement comparison
- Direct links to competitor websites

### Trends Page
- Facebook follower growth chart
- Instagram follower growth chart
- Date range selector (30/60/90 days)
- Interactive Chart.js visualizations

### Content Analysis Page
- Engagement rate comparisons (bar charts)
- Posting frequency analysis
- Content type breakdown (video, image, carousel)
- Market-wide benchmarking

### Website Changes Page
- Timeline of detected changes
- Change percentage indicator
- Diff preview (exact lines changed)
- Organized by market and competitor

## 🔄 Automated Scheduling

Run scrapers on a schedule:

```bash
# Via cron job (daily at midnight)
0 0 * * * cd /path/to/ALCmarket && python run_all.py >> logs/cron.log 2>&1
```

Or use the `schedule` library for a long-running process.

## 📝 Output Formats

### Facebook Data
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
      }
    }
  ]
}
```

### Website Changes
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
          "changed": true,
          "change_details": {
            "change_percentage": 15.5,
            "diff_preview": "..."
          }
        }
      ]
    }
  ]
}
```

## ⚡ Performance

- Facebook scraping: ~2-5 seconds per page
- Instagram scraping: ~1-3 seconds per profile
- Website monitoring: ~2-10 seconds per site
- Total runtime: ~2-5 minutes for all competitors

## 🔒 Legal & Ethical

- ✅ Scrapes only **public data** (no authentication required)
- ✅ **No API rate limit violations** (no API keys needed)
- ✅ **Respects robots.txt** and website ToS
- ✅ **No spam or automated attacks**
- ✅ **Educational and business intelligence only**

## 🐛 Troubleshooting

### Dashboard shows no data
```bash
python run_all.py  # Generate fresh data
```

### Scraper returns no results
- Check `logs/tracker.log` for errors
- Verify competitor URLs in `competitors.csv`
- Ensure network connectivity

### Website monitoring not working
- Check minimum change threshold in `config.py`
- Verify website is publicly accessible
- Check `snapshots/` directory for previous data

## 💡 Future Enhancements

- Email alerts for significant changes
- Automated benchmarking reports
- Course curriculum analysis
- Price history tracking
- Growth projections
- API endpoint for programmatic access
- Slack/Discord integration

## 📄 License

Open source - available for research, analysis, and educational purposes.

## 👤 Author

Built by Claude Code - AI-powered development assistant

---

**Ready to get started?** [View the Source Code](https://github.com/nlwtest2020/ALCmarket)
