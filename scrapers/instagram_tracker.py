"""
Instagram profile tracker for monitoring competitor social presence
Uses public profile endpoints without requiring authentication
"""
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

from config import INSTAGRAM_DATA_DIR, SCRAPING_CONFIG, USER_AGENTS

logger = logging.getLogger(__name__)


class InstagramTracker:
    """Scrapes public Instagram profiles for competitor intelligence"""

    def __init__(self):
        self.posts_to_fetch = SCRAPING_CONFIG["instagram"]["posts_to_fetch"]
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENTS[0]})

    def fetch_profile_data(self, handle: str) -> Optional[Dict]:
        """Fetch public data from an Instagram profile"""
        if not handle or not isinstance(handle, str):
            logger.warning(f"Invalid Instagram handle: {handle}")
            return None

        # Remove @ if present
        handle = handle.lstrip("@")

        try:
            # Instagram profile URL
            profile_url = f"https://www.instagram.com/{handle}/"
            response = self.session.get(profile_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Extract profile data from page HTML/metadata
            profile_data = {
                "handle": handle,
                "url": profile_url,
                "followers": None,
                "following": None,
                "total_posts": None,
                "posts": [],
                "scraped_at": datetime.now().isoformat(),
            }

            # Try to extract data from page
            self._extract_profile_stats(soup, profile_data)
            profile_data["posts"] = self._extract_posts(soup)

            if profile_data["posts"]:
                profile_data["engagement_metrics"] = self._calculate_engagement_metrics(
                    profile_data["posts"]
                )

            logger.info(
                f"Successfully scraped @{handle} - {len(profile_data['posts'])} posts"
            )
            return profile_data

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(f"Instagram profile @{handle} not found (404)")
            else:
                logger.error(f"HTTP error fetching @{handle}: {e}")
            return None
        except requests.RequestException as e:
            logger.error(f"Failed to fetch Instagram profile @{handle}: {e}")
            return None

    def _extract_profile_stats(self, soup: BeautifulSoup, profile_data: Dict):
        """Extract follower, following, and post counts from profile page"""
        text = soup.get_text()

        # Look for patterns like "1,234 followers" or "1.2K followers"
        # This is a simplified approach since Instagram uses JavaScript
        followers_match = re.search(r"([\d,]+(?:\.\d+)?[KMB]?)\s*followers?", text)
        if followers_match:
            profile_data["followers"] = self._parse_number(followers_match.group(1))

        following_match = re.search(r"([\d,]+(?:\.\d+)?[KMB]?)\s*following", text)
        if following_match:
            profile_data["following"] = self._parse_number(following_match.group(1))

        posts_match = re.search(r"([\d,]+(?:\.\d+)?[KMB]?)\s*posts?", text)
        if posts_match:
            profile_data["total_posts"] = self._parse_number(posts_match.group(1))

    def _parse_number(self, num_str: str) -> Optional[int]:
        """Parse number string like '1.2K' or '1,234' to integer"""
        try:
            num_str = num_str.strip().upper()
            multipliers = {"K": 1000, "M": 1000000, "B": 1000000000}

            for suffix, multiplier in multipliers.items():
                if suffix in num_str:
                    base = float(num_str.replace(suffix, ""))
                    return int(base * multiplier)

            # Remove commas and convert
            return int(num_str.replace(",", ""))
        except (ValueError, AttributeError):
            return None

    def _extract_posts(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract recent posts from profile"""
        posts = []

        # Instagram structure varies, but we can look for common patterns
        # This is limited without API, but we try basic extraction
        post_elements = soup.find_all("article")

        for element in post_elements[: self.posts_to_fetch]:
            post = self._parse_post(element)
            if post:
                posts.append(post)

        return posts

    def _parse_post(self, element) -> Optional[Dict]:
        """Parse individual post element"""
        try:
            post_data = {
                "type": self._detect_post_type(element),
                "likes": self._extract_engagement_count(element, "like"),
                "comments": self._extract_engagement_count(element, "comment"),
            }
            return post_data
        except Exception as e:
            logger.debug(f"Error parsing Instagram post: {e}")
            return None

    def _detect_post_type(self, element) -> str:
        """Detect post type (image, video, carousel)"""
        element_text = element.get_text().lower()
        html_str = str(element)

        if "carousel" in html_str or "multiple" in element_text:
            return "carousel"
        elif "video" in html_str or "<video" in html_str:
            return "video"
        elif "image" in element_text or "<img" in html_str:
            return "image"
        return "image"  # Default to image

    def _extract_engagement_count(self, element, engagement_type: str) -> int:
        """Extract like or comment count"""
        text = element.get_text()
        # Look for patterns like "1,234 likes" or "1.2K likes"
        pattern = rf"([\d,]+(?:\.\d+)?[KMB]?)\s*{engagement_type}s?"
        matches = re.findall(pattern, text)
        if matches:
            return self._parse_number(matches[0]) or 0
        return 0

    def _calculate_engagement_metrics(self, posts: List[Dict]) -> Dict:
        """Calculate aggregate engagement metrics"""
        if not posts:
            return {}

        total_likes = sum(p.get("likes", 0) for p in posts)
        total_comments = sum(p.get("comments", 0) for p in posts)

        total_engagement = total_likes + total_comments
        avg_engagement = total_engagement / len(posts) if posts else 0

        video_posts = sum(1 for p in posts if p.get("type") == "video")
        video_percentage = (video_posts / len(posts) * 100) if posts else 0

        # Estimate posting frequency
        posting_frequency = len(posts) / (7 / 2)  # Rough estimate

        return {
            "total_posts": len(posts),
            "avg_engagement_rate": round(avg_engagement, 2),
            "total_likes": total_likes,
            "total_comments": total_comments,
            "video_percentage": round(video_percentage, 1),
            "posts_per_week": round(posting_frequency, 2),
        }


def scrape_instagram_competitors(competitors_df) -> Dict:
    """Scrape Instagram data for all competitors"""
    tracker = InstagramTracker()
    results = {"scraped_at": datetime.now().isoformat(), "competitors": []}

    instagram_competitors = competitors_df[competitors_df["instagram_handle"].notna()]

    for _, row in instagram_competitors.iterrows():
        logger.info(f"Scraping Instagram for {row['name']} (@{row['instagram_handle']})")
        profile_data = tracker.fetch_profile_data(row["instagram_handle"])

        if profile_data:
            profile_data["competitor_name"] = row["name"]
            profile_data["market"] = row["market"]
            results["competitors"].append(profile_data)

    return results


def save_instagram_results(results: Dict, market: str):
    """Save Instagram scraping results to JSON file"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = INSTAGRAM_DATA_DIR / f"{date_str}_{market.lower()}.json"

    with open(filename, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    logger.info(f"Saved Instagram results to {filename}")
    return filename
