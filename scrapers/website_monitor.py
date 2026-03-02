"""
Website change monitor for detecting competitor pricing and course updates
Monitors main page and course/pricing subpages for significant changes
"""
import difflib
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup

from config import SCRAPING_CONFIG, SNAPSHOTS_ROOT, WEBSITE_DATA_DIR, USER_AGENTS

logger = logging.getLogger(__name__)


class WebsiteMonitor:
    """Monitors competitor websites for changes"""

    def __init__(self):
        self.min_change_threshold = SCRAPING_CONFIG["website"]["min_change_threshold"]
        self.subpages = SCRAPING_CONFIG["website"]["subpages"]
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENTS[0]})

    def fetch_and_clean_page(self, url: str) -> Optional[str]:
        """Fetch page and extract main content, removing nav/footer/scripts"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Remove script tags, style tags, navigation, footer
            for tag in soup.find_all(["script", "style", "nav", "footer"]):
                tag.decompose()

            # Extract main content
            main_content = None
            # Try common main content selectors
            for selector in ["main", "article", '[role="main"]']:
                main_content = soup.select_one(selector)
                if main_content:
                    break

            if not main_content:
                main_content = soup.body if soup.body else soup

            # Get text and clean it
            text = main_content.get_text(separator="\n", strip=True)
            # Remove extra whitespace
            text = re.sub(r"\n\s*\n", "\n", text)
            return text

        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None

    def get_page_snapshot_path(self, competitor_name: str) -> Path:
        """Get path for storing page snapshots"""
        sanitized_name = re.sub(r"[^a-zA-Z0-9_-]", "_", competitor_name)
        return SNAPSHOTS_ROOT / f"{sanitized_name}_current.txt"

    def get_previous_snapshot(self, competitor_name: str) -> Optional[str]:
        """Get previous snapshot of competitor website"""
        snapshot_path = self.get_page_snapshot_path(competitor_name)
        if snapshot_path.exists():
            with open(snapshot_path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    def save_snapshot(self, competitor_name: str, content: str):
        """Save current snapshot of competitor website"""
        snapshot_path = self.get_page_snapshot_path(competitor_name)
        with open(snapshot_path, "w", encoding="utf-8") as f:
            f.write(content)

    def calculate_diff_percentage(self, old_text: str, new_text: str) -> float:
        """Calculate percentage of text that has changed"""
        if not old_text and not new_text:
            return 0.0
        if not old_text or not new_text:
            return 1.0

        matcher = difflib.SequenceMatcher(None, old_text, new_text)
        return 1.0 - matcher.ratio()

    def detect_changes(
        self, competitor_name: str, new_content: str
    ) -> Tuple[bool, Optional[Dict]]:
        """Detect if there are significant changes from previous snapshot"""
        old_content = self.get_previous_snapshot(competitor_name)

        if old_content is None:
            # First time monitoring this competitor
            self.save_snapshot(competitor_name, new_content)
            logger.info(f"First snapshot saved for {competitor_name}")
            return False, None

        diff_percentage = self.calculate_diff_percentage(old_content, new_content)

        if diff_percentage > self.min_change_threshold:
            # Significant change detected
            diff_lines = list(
                difflib.unified_diff(
                    old_content.splitlines(),
                    new_content.splitlines(),
                    lineterm="",
                    n=2,
                )
            )

            change_summary = {
                "change_percentage": round(diff_percentage * 100, 2),
                "old_length": len(old_content),
                "new_length": len(new_content),
                "lines_changed": len([l for l in diff_lines if l.startswith("+")]),
                "diff_preview": "\n".join(diff_lines[:50]),  # First 50 lines
            }

            self.save_snapshot(competitor_name, new_content)
            logger.info(
                f"Change detected for {competitor_name}: {diff_percentage*100:.1f}% different"
            )
            return True, change_summary

        return False, None

    def monitor_competitor_website(self, competitor: Dict) -> Optional[Dict]:
        """Monitor a competitor's website for changes"""
        name = competitor.get("name")
        website_url = competitor.get("website_url")
        market = competitor.get("market")

        if not website_url:
            logger.warning(f"No website URL for {name}")
            return None

        monitor_result = {
            "competitor_name": name,
            "market": market,
            "website_url": website_url,
            "checked_at": datetime.now().isoformat(),
            "pages_monitored": [],
        }

        # Check main page
        logger.info(f"Monitoring {name} website")
        main_content = self.fetch_and_clean_page(website_url)

        if main_content:
            changed, diff_info = self.detect_changes(name, main_content)
            monitor_result["pages_monitored"].append(
                {
                    "url": website_url,
                    "page_type": "main",
                    "content_length": len(main_content),
                    "changed": changed,
                    "change_details": diff_info,
                }
            )

        # Check subpages
        for subpage in self.subpages:
            subpage_url = website_url.rstrip("/") + subpage
            subpage_name = f"{name}_{subpage.lstrip('/')}"

            subpage_content = self.fetch_and_clean_page(subpage_url)
            if subpage_content:
                changed, diff_info = self.detect_changes(subpage_name, subpage_content)
                monitor_result["pages_monitored"].append(
                    {
                        "url": subpage_url,
                        "page_type": subpage.lstrip("/"),
                        "content_length": len(subpage_content),
                        "changed": changed,
                        "change_details": diff_info,
                    }
                )

        return monitor_result


def monitor_all_competitors(competitors_df) -> Dict:
    """Monitor all competitor websites for changes"""
    monitor = WebsiteMonitor()
    results = {"monitored_at": datetime.now().isoformat(), "changes_detected": []}

    for _, row in competitors_df.iterrows():
        result = monitor.monitor_competitor_website(row.to_dict())
        if result:
            # Filter to only changes detected
            significant_changes = [
                p for p in result["pages_monitored"] if p.get("changed")
            ]
            if significant_changes:
                result["pages_monitored"] = significant_changes
                results["changes_detected"].append(result)

    return results


def save_website_monitoring_results(results: Dict):
    """Save website monitoring results to JSON file"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = WEBSITE_DATA_DIR / f"changes_{date_str}.json"

    with open(filename, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    logger.info(f"Saved website monitoring results to {filename}")
    logger.info(f"Detected changes in {len(results['changes_detected'])} competitors")
    return filename
