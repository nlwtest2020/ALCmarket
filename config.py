"""
Configuration settings for ALC Competitive Intelligence Tracker
"""
import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent
DATA_ROOT = PROJECT_ROOT / "data"
SNAPSHOTS_ROOT = PROJECT_ROOT / "snapshots"

# Data storage paths
FACEBOOK_DATA_DIR = DATA_ROOT / "facebook"
INSTAGRAM_DATA_DIR = DATA_ROOT / "instagram"
WEBSITE_DATA_DIR = DATA_ROOT / "websites"

# Competitor data
COMPETITORS_CSV = PROJECT_ROOT / "competitors.csv"

# Scraping settings
SCRAPING_CONFIG = {
    "facebook": {
        "enabled": True,
        "interval_hours": 24,  # Daily
        "mobile_site": "https://mbasic.facebook.com",
        "posts_to_fetch": 20,
    },
    "instagram": {
        "enabled": True,
        "interval_hours": 24,  # Daily
        "posts_to_fetch": 12,
    },
    "website": {
        "enabled": True,
        "interval_hours": 168,  # Weekly
        "min_change_threshold": 0.10,  # 10% text difference
        "subpages": ["/courses", "/programs", "/pricing", "/our-courses"],
    },
}

# User-Agent for requests
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]

# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": str(PROJECT_ROOT / "logs" / "tracker.log"),
        },
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
        },
    },
}

# Ensure directories exist
for directory in [FACEBOOK_DATA_DIR, INSTAGRAM_DATA_DIR, WEBSITE_DATA_DIR, SNAPSHOTS_ROOT]:
    directory.mkdir(parents=True, exist_ok=True)

# Create logs directory
logs_dir = PROJECT_ROOT / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)
