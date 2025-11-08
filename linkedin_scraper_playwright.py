#!/usr/bin/env python3
"""
LinkedIn Post Engagement Scraper (Playwright)

Scrapes engagement data (likes, comments) from YOUR OWN LinkedIn posts using
browser automation with Playwright (modern, more reliable than Selenium).

Requirements:
    pip install playwright
    playwright install chromium

Usage:
    python linkedin_scraper_playwright.py --posts 10 --output my_engagement.csv

First run will open a browser for you to log in manually. Session is saved.
"""

import argparse
import csv
import asyncio
import json
from playwright.async_api import async_playwright, Page, Browser
from datetime import datetime
from typing import List, Dict, Set
from pathlib import Path


class LinkedInEngagementScraper:
    """Scrapes engagement data from your own LinkedIn posts using Playwright."""

    def __init__(self, headless: bool = False, state_file: str = "./linkedin_state.json"):
        """
        Initialize scraper.

        Args:
            headless: Run browser in headless mode (no GUI)
            state_file: File to save browser session state
        """
        self.state_file = Path(state_file)
        self.headless = headless
        self.engagers: Set[str] = set()
        self.engagement_data: List[Dict] = []
        self.browser: Browser = None
        self.page: Page = None

    async def _setup_browser(self, playwright):
        """Set up browser with persistent state."""

        # Launch browser
        self.browser = await playwright.chromium.launch(headless=self.headless)

        # Create context (with saved state if exists)
        if self.state_file.exists():
            print("✓ Loading saved session...")
            with open(self.state_file, 'r') as f:
                state = json.load(f)
            context = await self.browser.new_context(storage_state=state)
        else:
            print("✓ Creating new session...")
            context = await self.browser.new_context()

        self.page = await context.new_page()
        print("✓ Browser initialized\n")

        return context

    async def login_check(self, context):
        """
        Check if user is logged in. If not, prompt for manual login.
        """
        await self.page.goto("https://www.linkedin.com/feed/")
        await asyncio.sleep(3)

        # Check if we're on login page
        if "login" in self.page.url or "authwall" in self.page.url:
            print("\n" + "="*60)
            print("🔐 MANUAL LOGIN REQUIRED")
            print("="*60)
            print("Please log in to LinkedIn in the browser window.")
            print("Your session will be saved for future runs.")
            print("\nWaiting for you to complete login...")
            print("(Script will continue once you reach your feed)")
            print("="*60 + "\n")

            # Wait for login (user lands on feed)
            await self.page.wait_for_url("**/feed/**", timeout=300000)

            # Save session state
            state = await context.storage_state()
            with open(self.state_file, 'w') as f:
                json.dump(state, f)

            print("✓ Login successful! Session saved.\n")
            await asyncio.sleep(2)
        else:
            print("✓ Already logged in\n")

    async def get_post_urls(self, num_posts: int = 10) -> List[str]:
        """
        Navigate to your activity page and collect recent post URLs.

        Args:
            num_posts: Number of recent posts to scrape

        Returns:
            List of post URLs
        """
        print(f"📝 Collecting your last {num_posts} post URLs...\n")

        # Go to your posts
        await self.page.goto("https://www.linkedin.com/in/me/recent-activity/all/")
        await asyncio.sleep(3)

        post_urls = []
        scroll_attempts = 0
        max_scrolls = 20

        while len(post_urls) < num_posts and scroll_attempts < max_scrolls:
            try:
                # Find post links
                links = await self.page.query_selector_all("a[href*='/posts/']")

                for link in links:
                    url = await link.get_attribute('href')
                    if url and 'activity-' in url and url not in post_urls:
                        # Clean URL (remove tracking params)
                        url = url.split('?')[0]
                        post_urls.append(url)
                        print(f"  Found post {len(post_urls)}: {url[:80]}...")

                    if len(post_urls) >= num_posts:
                        break

                # Scroll down to load more
                await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(2)
                scroll_attempts += 1

            except Exception as e:
                print(f"⚠ Error finding posts: {e}")
                break

        print(f"\n✓ Collected {len(post_urls)} post URLs\n")
        return post_urls[:num_posts]

    async def scrape_post_engagement(self, post_url: str) -> Dict:
        """
        Scrape engagement (reactions, comments) from a single post.

        Args:
            post_url: URL of the LinkedIn post

        Returns:
            Dict with post info and engagers
        """
        print(f"🔍 Scraping: {post_url[:60]}...")

        await self.page.goto(post_url)
        await asyncio.sleep(3)

        post_data = {
            'url': post_url,
            'date_scraped': datetime.now().isoformat(),
            'likers': [],
            'commenters': []
        }

        # Get reactions (likes)
        try:
            # Find and click reactions button
            reactions_button = await self.page.wait_for_selector(
                "button[aria-label*='reaction']",
                timeout=10000
            )

            if reactions_button:
                await reactions_button.click()
                await asyncio.sleep(2)

                # Find modal
                modal = await self.page.wait_for_selector("div[role='dialog']", timeout=5000)

                if modal:
                    # Scroll through modal to load all reactions
                    last_height = 0
                    scroll_attempts = 0
                    max_scroll_attempts = 10

                    while scroll_attempts < max_scroll_attempts:
                        # Scroll within modal
                        await modal.evaluate("el => el.scrollTo(0, el.scrollHeight)")
                        await asyncio.sleep(1)

                        new_height = await modal.evaluate("el => el.scrollHeight")

                        if new_height == last_height:
                            break

                        last_height = new_height
                        scroll_attempts += 1

                    # Extract names
                    name_elements = await modal.query_selector_all("span[aria-hidden='true']")

                    for elem in name_elements:
                        name = await elem.text_content()
                        name = name.strip() if name else ""

                        # Filter out UI elements
                        if name and len(name) > 2 and name not in [
                            'Reactions', 'All', 'Like', 'Celebrate', 'Support',
                            'Love', 'Insightful', 'Funny', 'Curious'
                        ]:
                            post_data['likers'].append(name)
                            self.engagers.add(name)

                    # Close modal
                    close_button = await modal.query_selector("button[aria-label*='Dismiss']")
                    if close_button:
                        await close_button.click()
                        await asyncio.sleep(1)

            print(f"  ✓ Found {len(post_data['likers'])} reactions")

        except Exception as e:
            print(f"  ⚠ No reactions found: {str(e)[:50]}")

        # Get comments
        try:
            comment_elements = await self.page.query_selector_all(
                "span.comments-comment-item__main-content a.app-aware-link span[aria-hidden='true']"
            )

            for elem in comment_elements:
                name = await elem.text_content()
                name = name.strip() if name else ""

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

        # Also create summary file for connection_analyzer.py
        summary_file = filepath.replace('.csv', '_summary.csv')

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

    async def run(self, num_posts: int = 10, output_file: str = "engagement.csv"):
        """
        Main execution flow.

        Args:
            num_posts: Number of recent posts to scrape
            output_file: Output CSV filepath
        """
        async with async_playwright() as p:
            try:
                # Setup browser
                context = await self._setup_browser(p)

                # Check login
                await self.login_check(context)

                # Get post URLs
                post_urls = await self.get_post_urls(num_posts)

                if not post_urls:
                    print("❌ No posts found. Make sure you have recent posts on LinkedIn.")
                    return

                # Scrape each post
                print(f"\n{'='*60}")
                print(f"SCRAPING {len(post_urls)} POSTS")
                print(f"{'='*60}\n")

                for i, url in enumerate(post_urls, 1):
                    print(f"\n[{i}/{len(post_urls)}]")
                    await self.scrape_post_engagement(url)

                    # Rate limiting
                    if i < len(post_urls):
                        wait_time = 3
                        print(f"  ⏱ Waiting {wait_time}s before next post...")
                        await asyncio.sleep(wait_time)

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
                import traceback
                traceback.print_exc()
            finally:
                if self.browser:
                    print("\n🔒 Closing browser...")
                    await self.browser.close()


def main():
    parser = argparse.ArgumentParser(
        description='Scrape engagement from your own LinkedIn posts (Playwright)'
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
    print("LINKEDIN ENGAGEMENT SCRAPER (Playwright)")
    print("="*60)
    print("This tool scrapes YOUR engagement data from YOUR posts.")
    print("No third-party tools needed - completely free and ethical.")
    print("="*60 + "\n")

    scraper = LinkedInEngagementScraper(headless=args.headless)
    asyncio.run(scraper.run(num_posts=args.posts, output_file=args.output))


if __name__ == '__main__':
    main()
