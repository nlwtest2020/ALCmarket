# ALC Competitive Intelligence Tracker — Build Prompt

I have a project folder called `alc-competitor-tracker` with a `competitors.csv` file listing language school competitors across three markets: Moldova, Georgia, and Armenia. Each row has: market, name, website_url, facebook_url, instagram_handle, notes.

I need you to build a competitive intelligence tracking system with three scrapers and a local dashboard. Here's exactly what I need:

---

## 1. Facebook Page Tracker (`scrapers/facebook_tracker.py`)

Scrape public Facebook pages listed in competitors.csv. For each page, collect:
- Page name and URL
- Follower/like count
- Last 20 posts: date, text preview, post type (video/image/link/text), likes, comments, shares
- Calculate: average engagement rate, posting frequency (posts per week), percentage of posts that are video

Store results as JSON in `data/facebook/{date}_{market}.json` so we build history over time.

Handle errors gracefully — if a page is unavailable or URL is missing, skip it and log the issue.

Use `requests` and `BeautifulSoup` for scraping. Do NOT use Selenium or any browser automation — keep it lightweight.

**Important**: Facebook's mobile site (mbasic.facebook.com) is easier to scrape than the main site. Use that.

---

## 2. Instagram Profile Tracker (`scrapers/instagram_tracker.py`)

For each Instagram handle in competitors.csv, collect:
- Follower count
- Following count
- Total posts
- Last 12 posts: date, type (image/video/carousel), like count, comment count
- Calculate: average engagement rate, posting frequency

Store results as JSON in `data/instagram/{date}_{market}.json`.

Use public profile endpoints or lightweight scraping. No login required — public profiles only. Skip private accounts and log them.

---

## 3. Website Change Monitor (`scrapers/website_monitor.py`)

For each competitor website in competitors.csv:
- Fetch the main page and any `/courses`, `/programs`, `/pricing`, or `/our-courses` subpages
- Strip navigation, footers, scripts — extract just the main content text
- Save a cleaned text snapshot in `snapshots/{name}_{date}.txt`
- Compare against the previous snapshot using difflib
- If significant changes detected (more than 10% text difference), flag it and save a diff report in `data/websites/changes_{date}.json`

This is the "new course alert" system — when a competitor adds a new program or changes pricing, we'll see it.

---

## 4. Dashboard (`dashboard/app.py`)

Build a Flask web dashboard at localhost:5000 with these views:

**Main page — Market Overview:**
- Three tabs: Moldova, Georgia, Armenia
- Table showing each competitor: name, Facebook followers, Instagram followers, posting frequency, engagement rate, last website change detected
- ALC row highlighted for comparison
- Color coding: green if ALC is ahead, red if behind, yellow if close

**Trends page:**
- Line charts showing follower growth over time (Facebook and Instagram) for each market
- Use Chart.js loaded from CDN
- Date range selector: 30/60/90 days

**Content Analysis page:**
- Bar charts showing content type breakdown (video vs image vs text) by competitor
- Engagement rate comparison across competitors
- Posting frequency comparison

**Website Changes page:**
- List of all detected changes, newest first
- Show: competitor name, market, date, summary of what changed
- Link to full diff view

**Design:**
- Dark theme to match our existing ALC presentation style
- Clean, minimal — this is a tool, not a marketing site
- Responsive so it works on laptop and tablet
- Use Bootstrap 5 from CDN for layout

---

## 5. Configuration (`config.py`)

Central config file with:
- Path to competitors.csv
- Data storage paths
- Scraping intervals (default: daily for social, weekly for websites)
- User-agent strings for requests
- Logging configuration

---

## 6. Requirements (`requirements.txt`)

Include all Python dependencies needed:
- requests
- beautifulsoup4
- flask
- pandas
- schedule (for automated runs)
- difflib (standard library)
- Any other dependencies your implementation needs

---

## 7. Run Script (`run_all.py`)

A single script that:
- Runs all three scrapers in sequence
- Logs results
- Can be called manually or via cron/scheduler

---

## Key Principles

- **No API keys required** for the basic version. Scrape public data only.
- **Graceful error handling** — if one competitor fails, keep going with the rest.
- **Append, don't overwrite** — build history over time so we can see trends.
- **Keep it simple** — this is a monitoring tool for one person, not enterprise software.
- **Log everything** — I want to know what succeeded and what failed on each run.

Please build all of this, test it, and make sure the dashboard renders correctly with sample data. Read the competitors.csv to understand the market structure.
