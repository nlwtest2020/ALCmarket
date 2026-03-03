"""
Enhanced competitor intelligence scraper
Extracts: social metrics, courses, pricing, notifications
"""
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class CompetitorIntelligence:
    """Extract actionable competitor intelligence"""

    def __init__(self, competitor):
        self.competitor = competitor
        self.data = {
            'name': competitor['name'],
            'market': competitor['market'],
            'timestamp': datetime.utcnow().isoformat(),
            'social': {
                'facebook': {},
                'instagram': {}
            },
            'courses': [],
            'alerts': [],
            'pricing_range': None
        }

    def scrape_website_courses(self):
        """Extract course listings and pricing from website"""
        try:
            resp = requests.get(self.competitor['website'], timeout=10)
            if resp.status_code != 200:
                return

            soup = BeautifulSoup(resp.content, 'html.parser')

            # Look for course listings (common patterns)
            courses = []

            # Pattern 1: Look for course titles and prices
            for elem in soup.find_all(['div', 'section'], class_=lambda x: x and ('course' in x.lower() or 'class' in x.lower())):
                text = elem.get_text()
                # Extract potential prices ($ or EUR)
                if '$' in text or '€' in text or 'USD' in text:
                    courses.append({'raw': text.strip()[:200]})

            self.data['courses'] = courses[:5]  # Top 5 courses

        except Exception as e:
            logger.debug(f"Course scraping failed for {self.competitor['name']}: {e}")

    def get_facebook_metrics(self):
        """Get Facebook metrics (followers, engagement)"""
        # In production, use Facebook Graph API
        # For now, return structured format
        try:
            # This would use Facebook Graph API with access token
            # Placeholder for API call
            self.data['social']['facebook'] = {
                'followers': 'N/A',
                'engagement_rate': 'N/A',
                'posts_per_week': 'N/A',
                'recent_posts': []
            }
        except Exception as e:
            logger.debug(f"Facebook metrics failed: {e}")

    def get_instagram_metrics(self):
        """Get Instagram metrics (followers, engagement)"""
        # In production, use Instagram Graph API or scraping
        try:
            self.data['social']['instagram'] = {
                'followers': 'N/A',
                'engagement_rate': 'N/A',
                'posts_per_week': 'N/A',
                'recent_posts': [],
                'handle': self.competitor['instagram_handle']
            }
        except Exception as e:
            logger.debug(f"Instagram metrics failed: {e}")

    def detect_alerts(self):
        """Generate alerts for new courses, posts, price changes"""
        alerts = []

        # Check for new courses
        if self.data['courses']:
            alerts.append({
                'type': 'new_content',
                'message': f"Found {len(self.data['courses'])} course listings",
                'severity': 'info'
            })

        # These would be populated from actual data
        self.data['alerts'] = alerts

    def get_intelligence(self):
        """Run all scrapers and return intelligence"""
        self.scrape_website_courses()
        self.get_facebook_metrics()
        self.get_instagram_metrics()
        self.detect_alerts()
        return self.data


def scrape_all_competitors(competitors_df):
    """Scrape intelligence for all competitors"""
    all_intelligence = []

    for _, row in competitors_df.iterrows():
        intel = CompetitorIntelligence(row.to_dict())
        data = intel.get_intelligence()
        all_intelligence.append(data)

    return all_intelligence


def save_intelligence(intelligence_list, market):
    """Save competitor intelligence to JSON"""
    output_dir = Path(f"data/intelligence")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d')
    output_file = output_dir / f"{timestamp}_{market}.json"

    with open(output_file, 'w') as f:
        json.dump(intelligence_list, f, indent=2)

    return output_file


def generate_alerts_report(intelligence_list):
    """Generate summary alerts report"""
    alerts = {
        'timestamp': datetime.utcnow().isoformat(),
        'new_courses': [],
        'new_posts': [],
        'price_changes': [],
        'high_engagement': []
    }

    for intel in intelligence_list:
        # Collect all alerts
        for alert in intel.get('alerts', []):
            if alert['type'] == 'new_content':
                alerts['new_courses'].append({
                    'competitor': intel['name'],
                    'market': intel['market'],
                    'message': alert['message']
                })

    return alerts
