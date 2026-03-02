"""
ALC Competitive Intelligence Tracker — Configuration
"""

import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
SNAPSHOTS_DIR = os.path.join(BASE_DIR, "snapshots")
COMPETITORS_CSV = os.path.join(BASE_DIR, "competitors.csv")

# Data subdirectories
FACEBOOK_DATA_DIR = os.path.join(DATA_DIR, "facebook")
INSTAGRAM_DATA_DIR = os.path.join(DATA_DIR, "instagram")
WEBSITE_DATA_DIR = os.path.join(DATA_DIR, "websites")

# Scraping settings
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
REQUEST_TIMEOUT = 15  # seconds
DELAY_BETWEEN_REQUESTS = 3  # seconds — be polite

# Website monitoring
WEBSITE_CHANGE_THRESHOLD = 0.10  # 10% text difference triggers an alert
WEBSITE_SUBPAGES_TO_CHECK = ["/courses", "/programs", "/pricing", "/our-courses", "/services"]

# Dashboard
DASHBOARD_HOST = "0.0.0.0"
DASHBOARD_PORT = 5000
DASHBOARD_DEBUG = True

# Logging
LOG_FILE = os.path.join(BASE_DIR, "tracker.log")
LOG_LEVEL = "INFO"

# Markets
MARKETS = ["moldova", "georgia", "armenia"]

# Create directories if they don't exist
for d in [DATA_DIR, SNAPSHOTS_DIR, FACEBOOK_DATA_DIR, INSTAGRAM_DATA_DIR, WEBSITE_DATA_DIR]:
    os.makedirs(d, exist_ok=True)
