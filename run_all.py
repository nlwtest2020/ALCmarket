"""
Run all competitor intelligence scrapers
Orchestrates Facebook, Instagram, and Website monitoring
"""
import logging
import logging.config
from datetime import datetime
from pathlib import Path

import pandas as pd

from config import COMPETITORS_CSV, LOGGING_CONFIG, SCRAPING_CONFIG
from scrapers.facebook_tracker import save_facebook_results, scrape_facebook_competitors
from scrapers.instagram_tracker import save_instagram_results, scrape_instagram_competitors
from scrapers.website_monitor import monitor_all_competitors, save_website_monitoring_results

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def load_competitors() -> pd.DataFrame:
    """Load competitors from CSV"""
    try:
        df = pd.read_csv(COMPETITORS_CSV)
        logger.info(f"Loaded {len(df)} competitors from {COMPETITORS_CSV}")
        return df
    except FileNotFoundError:
        logger.error(f"Competitors CSV not found at {COMPETITORS_CSV}")
        raise
    except Exception as e:
        logger.error(f"Error loading competitors CSV: {e}")
        raise


def run_facebook_tracking(competitors_df: pd.DataFrame):
    """Run Facebook page tracking"""
    if not SCRAPING_CONFIG["facebook"]["enabled"]:
        logger.info("Facebook tracking disabled in config")
        return

    logger.info("=" * 50)
    logger.info("Starting Facebook page tracking")
    logger.info("=" * 50)

    try:
        # Group by market and scrape
        for market in competitors_df["market"].unique():
            market_competitors = competitors_df[competitors_df["market"] == market]
            logger.info(f"\nScraping Facebook for {market} ({len(market_competitors)} competitors)")

            results = scrape_facebook_competitors(market_competitors)
            save_facebook_results(results, market)

        logger.info("✓ Facebook tracking completed successfully")
    except Exception as e:
        logger.error(f"✗ Facebook tracking failed: {e}", exc_info=True)


def run_instagram_tracking(competitors_df: pd.DataFrame):
    """Run Instagram profile tracking"""
    if not SCRAPING_CONFIG["instagram"]["enabled"]:
        logger.info("Instagram tracking disabled in config")
        return

    logger.info("\n" + "=" * 50)
    logger.info("Starting Instagram profile tracking")
    logger.info("=" * 50)

    try:
        # Group by market and scrape
        for market in competitors_df["market"].unique():
            market_competitors = competitors_df[competitors_df["market"] == market]
            logger.info(f"\nScraping Instagram for {market} ({len(market_competitors)} competitors)")

            results = scrape_instagram_competitors(market_competitors)
            save_instagram_results(results, market)

        logger.info("✓ Instagram tracking completed successfully")
    except Exception as e:
        logger.error(f"✗ Instagram tracking failed: {e}", exc_info=True)


def run_website_monitoring(competitors_df: pd.DataFrame):
    """Run website change monitoring"""
    if not SCRAPING_CONFIG["website"]["enabled"]:
        logger.info("Website monitoring disabled in config")
        return

    logger.info("\n" + "=" * 50)
    logger.info("Starting website change monitoring")
    logger.info("=" * 50)

    try:
        logger.info(f"Monitoring {len(competitors_df)} competitor websites")

        results = monitor_all_competitors(competitors_df)
        save_website_monitoring_results(results)

        logger.info("✓ Website monitoring completed successfully")
    except Exception as e:
        logger.error(f"✗ Website monitoring failed: {e}", exc_info=True)


def main():
    """Run all scrapers"""
    logger.info("\n" + "=" * 70)
    logger.info("ALC COMPETITIVE INTELLIGENCE TRACKER - RUN ALL")
    logger.info(f"Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 70)

    try:
        # Load competitor data
        competitors_df = load_competitors()
        logger.info(f"Markets: {', '.join(competitors_df['market'].unique())}")

        # Run all trackers
        run_facebook_tracking(competitors_df)
        run_instagram_tracking(competitors_df)
        run_website_monitoring(competitors_df)

        logger.info("\n" + "=" * 70)
        logger.info("✓ ALL SCRAPING RUNS COMPLETED SUCCESSFULLY")
        logger.info(f"Finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 70)

    except Exception as e:
        logger.error("\n" + "=" * 70)
        logger.error("✗ SCRAPING RUN FAILED")
        logger.error(f"Error: {e}")
        logger.error("=" * 70, exc_info=True)
        raise


if __name__ == "__main__":
    main()
