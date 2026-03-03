"""
Main runner for enhanced competitor intelligence scraping
"""
import pandas as pd
import logging
from scrapers.enhanced_scraper import scrape_all_competitors, save_intelligence, generate_alerts_report
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("=" * 70)
    logger.info("COMPETITOR INTELLIGENCE SCRAPER - ENHANCED")
    logger.info(f"Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 70)

    # Load competitors
    try:
        competitors_df = pd.read_csv('competitors.csv')
        logger.info(f"Loaded {len(competitors_df)} competitors")
    except Exception as e:
        logger.error(f"Failed to load competitors: {e}")
        raise

    # Scrape by market
    all_alerts = []
    for market in competitors_df['market'].unique():
        market_competitors = competitors_df[competitors_df['market'] == market]
        logger.info(f"\nScraping intelligence for {market} ({len(market_competitors)} competitors)")

        try:
            intelligence = scrape_all_competitors(market_competitors)
            save_intelligence(intelligence, market.lower())

            # Collect alerts
            market_alerts = generate_alerts_report(intelligence)
            all_alerts.extend(market_alerts.get('new_courses', []))

            logger.info(f"✓ Intelligence saved for {market}")

        except Exception as e:
            logger.error(f"✗ Intelligence scraping failed for {market}: {e}")

    # Generate summary report
    logger.info("\n" + "=" * 70)
    logger.info("24-HOUR INTELLIGENCE SUMMARY")
    logger.info("=" * 70)

    if all_alerts:
        logger.info(f"\n🆕 NEW CONTENT DETECTED: {len(all_alerts)} items")
        for alert in all_alerts[:10]:  # Show top 10
            logger.info(f"  • {alert['competitor']} ({alert['market']}): {alert['message']}")
    else:
        logger.info("\n✓ No significant changes detected")

    logger.info("\n" + "=" * 70)
    logger.info(f"Finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 70)

if __name__ == "__main__":
    main()
