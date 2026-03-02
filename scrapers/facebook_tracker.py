"""
Facebook page tracker for monitoring competitor social presence
Scrapes public Facebook pages using mobile site (mbasic.facebook.com)
"""
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

from config import FACEBOOK_DATA_DIR, SCRAPING_CONFIG, USER_AGENTS

logger = logging.getLogger(__name__)


class FacebookTracker:
    """Scrapes public Facebook pages for competitor intelligence"""

    def __init__(self):
        self.mobile_base = SCRAPING_CONFIG["facebook"]["mobile_site"]
        self.posts_to_fetch = SCRAPING_CONFIG["facebook"]["posts_to_fetch"]
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENTS[0]})

    def extract_page_name_from_url(self, url: str) -> Optional[str]:
        """Extract Facebook page name/ID from URL"""
        # Handle both facebook.com/pagename and facebook.com/pages/... formats
        match = re.search(r"facebook\.com/([a-zA-Z0-9._-]+)", url)
        if match:
            return match.group(1)
        return None

    def fetch_page_data(self, page_url: str) -> Optional[Dict]:
        """Fetch public data from a Facebook page"""
        page_name = self.extract_page_name_from_url(page_url)
        if not page_name:
            logger.warning(f"Could not extract page name from {page_url}")
            return None

        try:
            # Mobile site URL
            mobile_url = f"{self.mobile_base}/{page_name}"
            response = self.session.get(mobile_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Extract page data
            page_data = {
                "url": page_url,
                "mobile_url": mobile_url,
                "name": self._extract_page_name(soup),
                "followers": self._extract_follower_count(soup),
                "posts": self._extract_posts(soup),
                "scraped_at": datetime.now().isoformat(),
            }

            if page_data["posts"]:
                page_data["engagement_metrics"] = self._calculate_engagement_metrics(
                    page_data["posts"]
                )

            logger.info(
                f"Successfully scraped {page_data['name']} - {len(page_data['posts'])} posts"
            )
            return page_data

        except requests.RequestException as e:
            logger.error(f"Failed to fetch page {page_url}: {e}")
            return None

    def _extract_page_name(self, soup: BeautifulSoup) -> str:
        """Extract page name from HTML"""
        # Try to get from title tag or page header
        title = soup.find("title")
        if title:
            return title.get_text().strip()
        return "Unknown"

    def _extract_follower_count(self, soup: BeautifulSoup) -> Optional[int]:
        """Extract follower/like count from page"""
        # Look for follower count patterns in page
        text = soup.get_text()
        # Match patterns like "X people like this" or "X followers"
        matches = re.findall(r"(\d+(?:,\d+)?)\s*(?:people like|followers?|likes)", text)
        if matches:
            # Return the first match, cleaned
            count_str = matches[0].replace(",", "")
            try:
                return int(count_str)
            except ValueError:
                pass
        return None

    def _extract_posts(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract recent posts from page"""
        posts = []
        post_elements = soup.find_all("div", class_="story")

        for element in post_elements[: self.posts_to_fetch]:
            post = self._parse_post(element)
            if post:
                posts.append(post)

        return posts

    def _parse_post(self, element) -> Optional[Dict]:
        """Parse individual post element"""
        try:
            post_data = {
                "text": self._extract_post_text(element),
                "type": self._detect_post_type(element),
                "date": self._extract_post_date(element),
                "likes": self._extract_engagement_count(element, "like"),
                "comments": self._extract_engagement_count(element, "comment"),
                "shares": self._extract_engagement_count(element, "share"),
            }
            return post_data
        except Exception as e:
            logger.debug(f"Error parsing post: {e}")
            return None

    def _extract_post_text(self, element) -> str:
        """Extract post text content"""
        text_elements = element.find_all("div", class_="msg")
        if text_elements:
            return text_elements[0].get_text().strip()[:500]  # Max 500 chars
        return ""

    def _detect_post_type(self, element) -> str:
        """Detect post type (video, image, link, text)"""
        text = element.get_text().lower()
        if "video" in text or element.find("video"):
            return "video"
        elif "photo" in text or "image" in text or element.find("img"):
            return "image"
        elif "link" in text or element.find("a", href=True):
            return "link"
        return "text"

    def _extract_post_date(self, element) -> Optional[str]:
        """Extract post date"""
        time_elem = element.find("abbr")
        if time_elem and time_elem.get("title"):
            return time_elem["title"]
        return None

    def _extract_engagement_count(self, element, engagement_type: str) -> int:
        """Extract like/comment/share count"""
        text = element.get_text().lower()
        pattern = rf"(\d+(?:,\d+)?)\s*{engagement_type}s?"
        matches = re.findall(pattern, text)
        if matches:
            count_str = matches[0].replace(",", "")
            try:
                return int(count_str)
            except ValueError:
                pass
        return 0

    def _calculate_engagement_metrics(self, posts: List[Dict]) -> Dict:
        """Calculate aggregate engagement metrics"""
        if not posts:
            return {}

        total_likes = sum(p.get("likes", 0) for p in posts)
        total_comments = sum(p.get("comments", 0) for p in posts)
        total_shares = sum(p.get("shares", 0) for p in posts)

        total_engagement = total_likes + total_comments + total_shares
        avg_engagement = total_engagement / len(posts) if posts else 0

        video_posts = sum(1 for p in posts if p.get("type") == "video")
        video_percentage = (video_posts / len(posts) * 100) if posts else 0

        # Estimate posting frequency (posts per week)
        # Assume posts span a few days
        posting_frequency = len(posts) / (7 / 2)  # Rough estimate

        return {
            "total_posts": len(posts),
            "avg_engagement_rate": round(avg_engagement, 2),
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_shares": total_shares,
            "video_percentage": round(video_percentage, 1),
            "posts_per_week": round(posting_frequency, 2),
        }


def scrape_facebook_competitors(competitors_df) -> Dict:
    """Scrape Facebook data for all competitors"""
    tracker = FacebookTracker()
    results = {"scraped_at": datetime.now().isoformat(), "competitors": []}

    facebook_competitors = competitors_df[competitors_df["facebook_url"].notna()]

    for _, row in facebook_competitors.iterrows():
        logger.info(f"Scraping Facebook for {row['name']} ({row['market']})")
        page_data = tracker.fetch_page_data(row["facebook_url"])

        if page_data:
            page_data["competitor_name"] = row["name"]
            page_data["market"] = row["market"]
            results["competitors"].append(page_data)

    return results


def save_facebook_results(results: Dict, market: str):
    """Save Facebook scraping results to JSON file"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = FACEBOOK_DATA_DIR / f"{date_str}_{market.lower()}.json"

    with open(filename, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    logger.info(f"Saved Facebook results to {filename}")
    return filename
