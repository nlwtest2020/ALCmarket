# ALC Competitive Intelligence Tracker

## What This Project Does

Monitors competitors across Moldova, Georgia, and Armenia on three fronts:
1. **Facebook page tracking** — follower counts, posting frequency, engagement rates, content types
2. **Instagram tracking** — follower counts, posting frequency, content mix
3. **Website/course monitoring** — detects when competitors change their course offerings, pricing pages, or program listings

Results feed into a local web dashboard you can check anytime.

---

## Project Structure

```
alc-competitor-tracker/
├── README.md                  ← You are here
├── competitors.csv            ← Fill this in with competitor URLs
├── CLAUDE_CODE_PROMPT.md      ← Paste this into Claude Code to build the project
├── scrapers/
│   ├── facebook_tracker.py    ← Facebook page scraper
│   ├── instagram_tracker.py   ← Instagram profile scraper
│   └── website_monitor.py     ← Website change detector
├── dashboard/
│   └── app.py                 ← Local web dashboard (Flask)
├── data/                      ← Where scraped data gets stored
│   ├── facebook/
│   ├── instagram/
│   └── websites/
├── snapshots/                 ← Website page snapshots for change detection
├── requirements.txt           ← Python dependencies
└── config.py                  ← Central configuration
```

---

## How to Get Started

### Step 1: Fill in competitors.csv

Open `competitors.csv` and add the URLs for each competitor. You need:
- **website_url** — their main website (e.g., https://example.com)
- **facebook_url** — their Facebook page URL (e.g., https://facebook.com/pagename)
- **instagram_handle** — just the handle, no @ sign (e.g., linguata_md)

You don't need all three for every competitor. Fill in what you can find.

### Step 2: Open Claude Code in your browser

Go to Claude Code and paste the contents of `CLAUDE_CODE_PROMPT.md` as your first message. Claude Code will use it to build out all the scrapers, the dashboard, and the scheduling logic.

### Step 3: Run the initial scrape

```bash
python scrapers/facebook_tracker.py
python scrapers/instagram_tracker.py
python scrapers/website_monitor.py
```

### Step 4: Launch the dashboard

```bash
python dashboard/app.py
```

Then open http://localhost:5000 in your browser.

### Step 5: Set up automated runs (optional)

Claude Code can help you set up a cron job or scheduled task to run the scrapers daily or weekly.

---

## What You'll See in the Dashboard

- **Market Overview** — side-by-side comparison of all competitors by market
- **Follower Trends** — 30/60/90 day growth charts for Facebook and Instagram
- **Posting Activity** — who's posting how often, and what type of content
- **Engagement Comparison** — likes, comments, shares relative to follower count
- **Website Changes** — flagged changes to competitor course/program pages
- **ALC Benchmarks** — your accounts shown alongside competitors for direct comparison

---

## Important Notes

- **Facebook scraping**: Uses public page data only. No login required. Facebook may rate-limit aggressive scraping, so the default is one check per day.
- **Instagram scraping**: Public profiles only. Instagram is more restrictive — if a profile is private, it can't be tracked.
- **Website monitoring**: Takes a snapshot of specified pages and compares them on each run. You'll get alerts when content changes significantly (not just minor HTML tweaks).
- **Data storage**: Everything is stored locally in CSV files in the `/data` folder. Nothing is sent anywhere.
- **No API keys needed** for the basic version. If you want deeper Facebook/Instagram analytics later, you can add Meta Graph API access.
