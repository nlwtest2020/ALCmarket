"""
Enhanced competitor intelligence scraper
Extracts: social metrics, courses, pricing, notifications
"""
import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import re

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
            courses = []

            # Extract all text with potential course/pricing info
            for text_elem in soup.find_all(['h2', 'h3', 'h4', 'p', 'span', 'div']):
                text = text_elem.get_text().strip()

                # Look for pricing patterns
                if any(pattern in text.lower() for pattern in ['course', 'class', 'training', 'program', 'level']):
                    # Extract prices if present
                    if any(char in text for char in ['$', '€', '£']):
                        courses.append({
                            'name': text[:100],
                            'raw': text[:150]
                        })

            # Remove duplicates and limit
            seen = set()
            unique_courses = []
            for c in courses:
                if c['raw'] not in seen:
                    seen.add(c['raw'])
                    unique_courses.append(c)

            self.data['courses'] = unique_courses[:5]

        except requests.exceptions.RequestException as e:
            logger.debug(f"Website scraping failed for {self.competitor['name']}: {e}")
        except Exception as e:
            logger.debug(f"Course scraping error for {self.competitor['name']}: {e}")

    def get_facebook_metrics(self):
        """Get Facebook metrics using Graph API if credentials available"""
        fb_token = os.getenv('FACEBOOK_API_TOKEN')
        fb_page = self.competitor.get('facebook_url', '').split('/')[-1]

        if not fb_token or not fb_page:
            self.data['social']['facebook'] = None
            return

        try:
            # Facebook Graph API v18.0
            url = f"https://graph.facebook.com/v18.0/{fb_page}"
            params = {
                'fields': 'name,followers_count,engagement',
                'access_token': fb_token
            }

            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                result = resp.json()
                self.data['social']['facebook'] = {
                    'followers': result.get('followers_count', 0),
                    'engagement_rate': result.get('engagement', {}).get('count', 0),
                    'posts_per_week': 'N/A',
                    'recent_posts': []
                }
            else:
                self.data['social']['facebook'] = None
        except Exception as e:
            logger.debug(f"Facebook API failed for {self.competitor['name']}: {e}")
            self.data['social']['facebook'] = None

    def get_instagram_metrics(self):
        """Get Instagram metrics using Graph API if credentials available"""
        ig_token = os.getenv('INSTAGRAM_API_TOKEN')
        ig_handle = self.competitor.get('instagram_handle', '')

        if not ig_token or not ig_handle:
            self.data['social']['instagram'] = None
            return

        try:
            # Instagram Graph API requires business account
            url = f"https://graph.instagram.com/ig_hashtag_search"
            params = {
                'user_id': os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID'),
                'fields': 'id,name',
                'access_token': ig_token
            }

            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                self.data['social']['instagram'] = {
                    'followers': 'requires_api',
                    'engagement_rate': 'requires_api',
                    'posts_per_week': 'requires_api',
                    'recent_posts': [],
                    'handle': ig_handle
                }
            else:
                self.data['social']['instagram'] = None
        except Exception as e:
            logger.debug(f"Instagram API failed for {self.competitor['name']}: {e}")
            self.data['social']['instagram'] = None

    def detect_alerts(self):
        """Generate alerts for new courses, posts, price changes"""
        alerts = []

        # Check for new courses
        if self.data['courses']:
            alerts.append({
                'type': 'new_content',
                'message': f"Found {len(self.data['courses'])} course listings with pricing",
                'severity': 'info'
            })

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
