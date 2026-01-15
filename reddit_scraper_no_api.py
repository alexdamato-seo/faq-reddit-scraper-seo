#!/usr/bin/env python3
"""
Reddit FAQ Scraper for Microscopy Equipment (No API Required)
Uses Reddit's public JSON endpoints - no authentication needed!

This version scrapes Reddit without requiring API credentials by using
Reddit's public JSON endpoints (append .json to any Reddit URL).
"""

import os
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict
from urllib.parse import urlencode

import requests
import pandas as pd

from config import (
    MICROSCOPY_CATEGORIES,
    SUBREDDITS,
    QUESTION_KEYWORDS,
    SEARCH_CONFIG,
    OUTPUT_CONFIG
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RedditJSONScraper:
    """
    Scraper using Reddit's public JSON endpoints (no API key required)
    """

    def __init__(self, rate_limit_delay=2.0):
        """
        Initialize the scraper

        Args:
            rate_limit_delay: Seconds to wait between requests (default: 2.0)
        """
        self.rate_limit_delay = rate_limit_delay
        self.session = requests.Session()

        # Set a user agent to identify our scraper
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; MicroscopyFAQBot/1.0; Educational research scraper)'
        })

        self.all_posts = []
        self.posts_by_category = defaultdict(list)

        logger.info("JSON scraper initialized (no API required)")

    def make_request(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make a request to Reddit with rate limiting

        Args:
            url: URL to request
            params: Query parameters

        Returns:
            JSON response as dictionary
        """
        try:
            # Rate limiting - be respectful
            time.sleep(self.rate_limit_delay)

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {str(e)}")
            return {}

    def search_subreddit(self, subreddit: str, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Search a subreddit using Reddit's JSON endpoint

        Args:
            subreddit: Subreddit name
            query: Search query
            limit: Maximum results (max 100 per request)

        Returns:
            List of post dictionaries
        """
        # Reddit JSON search endpoint
        url = f"https://www.reddit.com/r/{subreddit}/search.json"

        params = {
            'q': query,
            'restrict_sr': 'on',  # Restrict search to this subreddit
            'sort': SEARCH_CONFIG['sort'],
            't': SEARCH_CONFIG['time_filter'],
            'limit': min(limit, 100)  # Reddit max is 100 per request
        }

        data = self.make_request(url, params)

        posts = []
        if data and 'data' in data and 'children' in data['data']:
            for child in data['data']['children']:
                if child['kind'] == 't3':  # t3 = link/post
                    posts.append(child['data'])

        return posts

    def is_question(self, title: str, selftext: str) -> bool:
        """
        Determine if a post is likely a question

        Args:
            title: Post title
            selftext: Post content

        Returns:
            True if post appears to be a question
        """
        combined_text = f"{title.lower()} {selftext.lower()}"
        return any(keyword in combined_text for keyword in QUESTION_KEYWORDS)

    def extract_post_data(self, post_data: Dict[str, Any], category: str) -> Dict[str, Any]:
        """
        Extract relevant data from a Reddit post

        Args:
            post_data: Raw post data from Reddit JSON
            category: Microscopy category

        Returns:
            Dictionary containing formatted post data
        """
        return {
            'category': category,
            'title': post_data.get('title', ''),
            'selftext': post_data.get('selftext', ''),
            'url': f"https://reddit.com{post_data.get('permalink', '')}",
            'score': post_data.get('score', 0),
            'num_comments': post_data.get('num_comments', 0),
            'created_utc': datetime.fromtimestamp(post_data.get('created_utc', 0)).isoformat(),
            'author': post_data.get('author', '[deleted]'),
            'subreddit': post_data.get('subreddit', ''),
            'post_id': post_data.get('id', '')
        }

    def search_category(self, category_key: str, category_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search Reddit for posts related to a specific microscopy category

        Args:
            category_key: Category identifier
            category_data: Category configuration with name and keywords

        Returns:
            List of post data dictionaries
        """
        category_name = category_data['name']
        keywords = category_data['keywords']

        logger.info(f"Searching for: {category_name}")

        posts_found = []
        seen_ids = set()

        # Search each subreddit
        for subreddit_name in SUBREDDITS:
            # Search for each keyword in the category
            for keyword in keywords:
                logger.info(f"  Searching r/{subreddit_name} for '{keyword}'")

                try:
                    search_results = self.search_subreddit(
                        subreddit_name,
                        keyword,
                        limit=SEARCH_CONFIG['limit']
                    )

                    for post_data in search_results:
                        post_id = post_data.get('id', '')
                        score = post_data.get('score', 0)

                        # Skip if already seen or below score threshold
                        if post_id in seen_ids or score < SEARCH_CONFIG['min_score']:
                            continue

                        title = post_data.get('title', '')
                        selftext = post_data.get('selftext', '')

                        # Check if it's a question
                        if self.is_question(title, selftext):
                            formatted_post = self.extract_post_data(post_data, category_name)
                            posts_found.append(formatted_post)
                            seen_ids.add(post_id)

                            logger.info(f"    Found: {title[:60]}... (score: {score})")

                except Exception as e:
                    logger.error(f"Error searching r/{subreddit_name} for {keyword}: {str(e)}")
                    continue

        # Sort by score and limit results
        posts_found.sort(key=lambda x: x['score'], reverse=True)
        posts_found = posts_found[:SEARCH_CONFIG['max_results_per_category']]

        logger.info(f"Found {len(posts_found)} questions for {category_name}")
        return posts_found

    def scrape_all_categories(self):
        """Scrape all microscopy categories"""
        logger.info("Starting scrape of all microscopy categories")
        logger.info(f"Target categories: {len(MICROSCOPY_CATEGORIES)}")
        logger.info(f"Target subreddits: {len(SUBREDDITS)}")
        logger.info(f"Rate limit delay: {self.rate_limit_delay}s between requests")

        for category_key, category_data in MICROSCOPY_CATEGORIES.items():
            posts = self.search_category(category_key, category_data)

            # Store posts
            self.posts_by_category[category_data['name']] = posts
            self.all_posts.extend(posts)

        logger.info(f"Scraping complete! Total posts found: {len(self.all_posts)}")

    def save_results(self):
        """Save scraped results to CSV and JSON files"""
        # Create output directory
        output_dir = OUTPUT_CONFIG['directory']
        os.makedirs(output_dir, exist_ok=True)

        if not self.all_posts:
            logger.warning("No posts to save!")
            return

        # Save to CSV
        csv_path = os.path.join(output_dir, OUTPUT_CONFIG['csv_filename'])
        df = pd.DataFrame(self.all_posts)
        df.to_csv(csv_path, index=False, encoding='utf-8')
        logger.info(f"Saved CSV to: {csv_path}")

        # Save to JSON (all posts)
        json_path = os.path.join(output_dir, OUTPUT_CONFIG['json_filename'])
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.all_posts, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved JSON to: {json_path}")

        # Save to JSON (organized by category)
        json_cat_path = os.path.join(output_dir, OUTPUT_CONFIG['json_by_category_filename'])
        with open(json_cat_path, 'w', encoding='utf-8') as f:
            json.dump(dict(self.posts_by_category), f, indent=2, ensure_ascii=False)
        logger.info(f"Saved categorized JSON to: {json_cat_path}")

        # Print summary
        print("\n" + "="*60)
        print("SCRAPING SUMMARY")
        print("="*60)
        print(f"Total questions scraped: {len(self.all_posts)}")
        print("\nBreakdown by category:")
        for category, posts in sorted(self.posts_by_category.items()):
            print(f"  {category}: {len(posts)} questions")
        print("\nOutput files:")
        print(f"  - {csv_path}")
        print(f"  - {json_path}")
        print(f"  - {json_cat_path}")
        print("="*60)

    def run(self):
        """Main execution method"""
        try:
            self.scrape_all_categories()
            self.save_results()
            logger.info("Scraping completed successfully!")
            return True
        except Exception as e:
            logger.error(f"Scraping failed: {str(e)}", exc_info=True)
            return False


def main():
    """Main entry point"""
    print("="*60)
    print("MICROSCOPY FAQ SCRAPER FOR REDDIT (NO API REQUIRED)")
    print("Evident Scientific SEO Enhancement Tool")
    print("="*60)
    print()
    print("This scraper uses Reddit's public JSON endpoints.")
    print("No API key or authentication required!")
    print()

    # You can adjust the rate limit delay here (in seconds)
    # 2.0 seconds is respectful and shouldn't trigger rate limiting
    scraper = RedditJSONScraper(rate_limit_delay=2.0)
    success = scraper.run()

    if success:
        print("\n✓ Scraping completed successfully!")
        return 0
    else:
        print("\n✗ Scraping failed. Check logs for details.")
        return 1


if __name__ == "__main__":
    exit(main())
