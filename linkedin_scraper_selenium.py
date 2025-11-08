#!/usr/bin/env python3
"""
LinkedIn Post Engagement Scraper (Selenium)

Scrapes engagement data (likes, comments) from YOUR OWN LinkedIn posts using
browser automation. This is YOUR data from YOUR account - ethical and free.

Requirements:
    pip install selenium

Usage:
    python linkedin_scraper_selenium.py --posts 10 --output my_engagement.csv

First run will open a browser for you to log in manually. Session is saved.
"""

import argparse
import csv
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
from typing import List, Dict, Set


class LinkedInEngagementScraper:
    """Scrapes engagement data from your own LinkedIn posts."""

    def __init__(self, headless: bool = False, profile_dir: str = "./linkedin_profile"):
        """
        Initialize scraper with persistent browser profile.

        Args:
            headless: Run browser in headless mode (no GUI)
            profile_dir: Directory to store browser profile (preserves login)
        """
        self.profile_dir = profile_dir
        self.driver = None
        self.engagers: Set[str] = set()
        self.engagement_data: List[Dict] = []
        self.headless = headless

        self._setup_driver()

    def _setup_driver(self):
        """Set up Chrome WebDriver with persistent profile."""
        chrome_options = Options()

        # Use persistent profile to save login session
        chrome_options.add_argument(f"user-data-dir={os.path.abspath(self.profile_dir)}")

        if self.headless:
            chrome_options.add_argument("--headless")

        # Additional options for stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Start driver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)

        print("✓ Browser initialized")

    def login_check(self):
        """
        Check if user is logged in. If not, prompt for manual login.
        """
        self.driver.get("https://www.linkedin.com/feed/")
        time.sleep(3)

        # Check if we're on login page
        if "login" in self.driver.current_url or "authwall" in self.driver.current_url:
            print("\n" + "="*60)
            print("🔐 MANUAL LOGIN REQUIRED")
            print("="*60)
            print("Please log in to LinkedIn in the browser window.")
            print("Your session will be saved for future runs.")
            print("\nWaiting for you to complete login...")
            print("(Script will continue once you reach your feed)")
            print("="*60 + "\n")

            # Wait for login (user lands on feed)
            WebDriverWait(self.driver, 300).until(
                lambda d: "feed" in d.current_url or "mynetwork" in d.current_url
            )

            print("✓ Login successful! Session saved.\n")
            time.sleep(2)
        else:
            print("✓ Already logged in\n")

    def get_post_urls(self, num_posts: int = 10) -> List[str]:
        """
        Navigate to your activity page and collect recent post URLs.

        Args:
            num_posts: Number of recent posts to scrape

        Returns:
            List of post URLs
        """
        print(f"📝 Collecting your last {num_posts} post URLs...\n")

        # Go to your posts
        self.driver.get("https://www.linkedin.com/in/me/recent-activity/all/")
        time.sleep(3)

        post_urls = []
        scroll_attempts = 0
        max_scrolls = 20

        while len(post_urls) < num_posts and scroll_attempts < max_scrolls:
            # Find post links
            try:
                # Posts have links with "urn:li:activity" or "posts/"
                links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/posts/']")

                for link in links:
                    url = link.get_attribute('href')
                    if url and 'activity-' in url and url not in post_urls:
                        post_urls.append(url)
                        print(f"  Found post {len(post_urls)}: {url[:80]}...")

                    if len(post_urls) >= num_posts:
                        break

                # Scroll down to load more
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                scroll_attempts += 1

            except Exception as e:
                print(f"⚠ Error finding posts: {e}")
                break

        print(f"\n✓ Collected {len(post_urls)} post URLs\n")
        return post_urls[:num_posts]

    def scrape_post_engagement(self, post_url: str) -> Dict:
        """
        Scrape engagement (reactions, comments) from a single post.

        Args:
            post_url: URL of the LinkedIn post

        Returns:
            Dict with post info and engagers
        """
        print(f"🔍 Scraping: {post_url[:60]}...")

        self.driver.get(post_url)
        time.sleep(3)

        post_data = {
            'url': post_url,
            'date_scraped': datetime.now().isoformat(),
            'likers': [],
            'commenters': []
        }

        # Get reactions (likes)
        try:
            # Click on reactions count to see modal
            reactions_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='reaction']"))
            )
            reactions_button.click()
            time.sleep(2)

            # Scroll through reactions modal
            modal = self.driver.find_element(By.CSS_SELECTOR, "div[role='dialog']")

            # Scroll to load all reactions
            last_height = 0
            scroll_attempts = 0
            max_scroll_attempts = 10

            while scroll_attempts < max_scroll_attempts:
                # Scroll within modal
                self.driver.execute_script(
                    "arguments[0].scrollTo(0, arguments[0].scrollHeight);",
                    modal
                )
                time.sleep(1)

                new_height = self.driver.execute_script(
                    "return arguments[0].scrollHeight",
                    modal
                )

                if new_height == last_height:
                    break

                last_height = new_height
                scroll_attempts += 1

            # Extract names
            name_elements = modal.find_elements(By.CSS_SELECTOR, "span[aria-hidden='true']")

            for elem in name_elements:
                name = elem.text.strip()
                if name and len(name) > 2 and name not in ['Reactions', 'All', 'Like', 'Celebrate']:
                    post_data['likers'].append(name)
                    self.engagers.add(name)

            # Close modal
            close_button = modal.find_element(By.CSS_SELECTOR, "button[aria-label*='Dismiss']")
            close_button.click()
            time.sleep(1)

            print(f"  ✓ Found {len(post_data['likers'])} reactions")

        except TimeoutException:
            print("  ⚠ No reactions found or couldn't open reactions")
        except Exception as e:
            print(f"  ⚠ Error scraping reactions: {str(e)[:50]}")

        # Get comments
        try:
            # Find comment section
            comment_elements = self.driver.find_elements(
                By.CSS_SELECTOR,
                "span.comments-comment-item__main-content a.app-aware-link span[aria-hidden='true']"
            )

            for elem in comment_elements:
                name = elem.text.strip()
                if name and len(name) > 2:
                    post_data['commenters'].append(name)
                    self.engagers.add(name)

            print(f"  ✓ Found {len(post_data['commenters'])} commenters")

        except Exception as e:
            print(f"  ⚠ Error scraping comments: {str(e)[:50]}")

        # Record engagement
        for name in post_data['likers']:
            self.engagement_data.append({
                'Name': name,
                'Type': 'Reaction',
                'Post URL': post_url,
                'Date': post_data['date_scraped']
            })

        for name in post_data['commenters']:
            self.engagement_data.append({
                'Name': name,
                'Type': 'Comment',
                'Post URL': post_url,
                'Date': post_data['date_scraped']
            })

        return post_data

    def export_to_csv(self, filepath: str):
        """Export engagement data to CSV."""

        if not self.engagement_data:
            print("⚠ No engagement data to export")
            return

        # Write detailed engagement log
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['Name', 'Type', 'Post URL', 'Date']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.engagement_data)

        print(f"\n✓ Exported {len(self.engagement_data)} engagements to {filepath}")

        # Also create summary file
        summary_file = filepath.replace('.csv', '_summary.csv')

        # Count engagements per person
        from collections import defaultdict
        engagement_counts = defaultdict(int)

        for entry in self.engagement_data:
            engagement_counts[entry['Name']] += 1

        with open(summary_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['Name', 'Total Engagements']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for name, count in sorted(engagement_counts.items(), key=lambda x: x[1], reverse=True):
                writer.writerow({'Name': name, 'Total Engagements': count})

        print(f"✓ Exported summary to {summary_file}")
        print(f"\n📊 Stats:")
        print(f"  Total engagements: {len(self.engagement_data)}")
        print(f"  Unique engagers: {len(self.engagers)}")

    def run(self, num_posts: int = 10, output_file: str = "engagement.csv"):
        """
        Main execution flow.

        Args:
            num_posts: Number of recent posts to scrape
            output_file: Output CSV filepath
        """
        try:
            # Check login
            self.login_check()

            # Get post URLs
            post_urls = self.get_post_urls(num_posts)

            if not post_urls:
                print("❌ No posts found. Make sure you have recent posts on LinkedIn.")
                return

            # Scrape each post
            print(f"\n{'='*60}")
            print(f"SCRAPING {len(post_urls)} POSTS")
            print(f"{'='*60}\n")

            for i, url in enumerate(post_urls, 1):
                print(f"\n[{i}/{len(post_urls)}]")
                self.scrape_post_engagement(url)

                # Rate limiting
                if i < len(post_urls):
                    wait_time = 3
                    print(f"  ⏱ Waiting {wait_time}s before next post...")
                    time.sleep(wait_time)

            # Export results
            self.export_to_csv(output_file)

            print(f"\n{'='*60}")
            print("✅ SCRAPING COMPLETE!")
            print(f"{'='*60}\n")
            print(f"Next step: Use this data with connection_analyzer.py")
            print(f"  python connection_analyzer.py \\")
            print(f"    --connections Connections.csv \\")
            print(f"    --engagement {output_file.replace('.csv', '_summary.csv')}")
            print()

        except KeyboardInterrupt:
            print("\n\n⚠ Scraping interrupted by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Close browser."""
        if self.driver:
            print("\n🔒 Closing browser...")
            self.driver.quit()


def main():
    parser = argparse.ArgumentParser(
        description='Scrape engagement from your own LinkedIn posts'
    )
    parser.add_argument(
        '--posts',
        type=int,
        default=10,
        help='Number of recent posts to scrape (default: 10)'
    )
    parser.add_argument(
        '--output',
        default='my_engagement.csv',
        help='Output CSV filepath (default: my_engagement.csv)'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode (after first login)'
    )

    args = parser.parse_args()

    print("\n" + "="*60)
    print("LINKEDIN ENGAGEMENT SCRAPER")
    print("="*60)
    print("This tool scrapes YOUR engagement data from YOUR posts.")
    print("No third-party tools needed - completely free and ethical.")
    print("="*60 + "\n")

    scraper = LinkedInEngagementScraper(headless=args.headless)
    scraper.run(num_posts=args.posts, output_file=args.output)


if __name__ == '__main__':
    main()
