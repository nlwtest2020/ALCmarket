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
        """Scrape Facebook page metrics from public page"""
        fb_url = self.competitor.get('facebook_url', '')
        if not fb_url:
            self.data['social']['facebook'] = None
            return

        try:
            # Scrape public Facebook page with requests
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            resp = requests.get(fb_url, headers=headers, timeout=10)
            if resp.status_code != 200:
                self.data['social']['facebook'] = None
                return

            soup = BeautifulSoup(resp.content, 'html.parser')

            # Look for follower count in page text
            page_text = soup.get_text()
            followers = 'N/A'
            engagement = 'N/A'

            # Extract any number followed by "followers" or "likes"
            import re
            follower_match = re.search(r'([\d,]+)\s*(?:followers?|people like this)', page_text, re.IGNORECASE)
            if follower_match:
                followers = follower_match.group(1)

            self.data['social']['facebook'] = {
                'followers': followers,
                'engagement_rate': engagement,
                'posts_per_week': 'N/A',
                'recent_posts': []
            }
        except Exception as e:
            logger.debug(f"Facebook scraping failed for {self.competitor['name']}: {e}")
            self.data['social']['facebook'] = None

    def get_instagram_metrics(self):
        """Scrape Instagram profile metrics from public profile"""
        ig_handle = self.competitor.get('instagram_handle', '')
        if not ig_handle:
            self.data['social']['instagram'] = None
            return

        try:
            # Scrape public Instagram profile
            url = f"https://instagram.com/{ig_handle}/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200:
                self.data['social']['instagram'] = None
                return

            soup = BeautifulSoup(resp.content, 'html.parser')
            page_text = soup.get_text()

            # Extract followers and posts from page text
            import re
            followers = 'N/A'
            posts = 'N/A'

            # Look for patterns like "1,234 followers" or "1.2M followers"
            follower_match = re.search(r'([\d.,MK]+)\s*followers?', page_text, re.IGNORECASE)
            if follower_match:
                followers = follower_match.group(1)

            post_match = re.search(r'([\d,]+)\s*posts?', page_text, re.IGNORECASE)
            if post_match:
                posts = post_match.group(1)

            self.data['social']['instagram'] = {
                'followers': followers,
                'engagement_rate': 'N/A',
                'posts_per_week': posts,
                'recent_posts': [],
                'handle': ig_handle
            }
        except Exception as e:
            logger.debug(f"Instagram scraping failed for {ig_handle}: {e}")
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
