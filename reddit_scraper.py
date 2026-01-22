#!/usr/bin/env python3
"""
Reddit FAQ Scraper for Microscopy Equipment
Scrapes Reddit for questions about microscopy to improve Evident Scientific's SEO
"""

import os
import json
import csv
import logging
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict

import praw
from dotenv import load_dotenv
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


class RedditMicroscopyFAQScraper:
    """Scraper for microscopy-related FAQs from Reddit"""

    def __init__(self):
        """Initialize the Reddit API client"""
        load_dotenv()

        # Validate environment variables
        required_vars = ['REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET', 'REDDIT_USER_AGENT']
        missing_vars = [var for var in required_vars if not os.getenv(var)]

        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}\n"
                "Please create a .env file with your Reddit API credentials."
            )

        # Initialize Reddit API client
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )

        self.all_posts = []
        self.posts_by_category = defaultdict(list)

        logger.info("Reddit API client initialized successfully")

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

        # Check for question keywords
        return any(keyword in combined_text for keyword in QUESTION_KEYWORDS)

    def extract_post_data(self, post, category: str) -> Dict[str, Any]:
        """
        Extract relevant data from a Reddit post

        Args:
            post: PRAW submission object
            category: Microscopy category

        Returns:
            Dictionary containing post data
        """
        return {
            'category': category,
            'title': post.title,
            'selftext': post.selftext,
            'url': f"https://reddit.com{post.permalink}",
            'score': post.score,
            'num_comments': post.num_comments,
            'created_utc': datetime.fromtimestamp(post.created_utc).isoformat(),
            'author': str(post.author) if post.author else '[deleted]',
            'subreddit': str(post.subreddit),
            'post_id': post.id
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
            try:
                subreddit = self.reddit.subreddit(subreddit_name)

                # Search for each keyword in the category
                for keyword in keywords:
                    logger.info(f"  Searching r/{subreddit_name} for '{keyword}'")

                    search_results = subreddit.search(
                        keyword,
                        sort=SEARCH_CONFIG['sort'],
                        time_filter=SEARCH_CONFIG['time_filter'],
                        limit=SEARCH_CONFIG['limit']
                    )

                    for post in search_results:
                        # Skip if already seen or below score threshold
                        if post.id in seen_ids or post.score < SEARCH_CONFIG['min_score']:
                            continue

                        # Check if it's a question
                        if self.is_question(post.title, post.selftext):
                            post_data = self.extract_post_data(post, category_name)
                            posts_found.append(post_data)
                            seen_ids.add(post.id)

                            logger.info(f"    Found: {post.title[:60]}... (score: {post.score})")

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

        # Deduplicate posts based on post_id
        original_count = len(self.all_posts)
        seen_ids = set()
        deduplicated_posts = []

        for post in self.all_posts:
            post_id = post.get('post_id')
            if post_id and post_id not in seen_ids:
                seen_ids.add(post_id)
                deduplicated_posts.append(post)

        self.all_posts = deduplicated_posts
        duplicates_removed = original_count - len(self.all_posts)

        if duplicates_removed > 0:
            logger.info(f"Removed {duplicates_removed} duplicate posts (kept {len(self.all_posts)} unique posts)")

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
    print("MICROSCOPY FAQ SCRAPER FOR REDDIT")
    print("Evident Scientific SEO Enhancement Tool")
    print("="*60)
    print()

    scraper = RedditMicroscopyFAQScraper()
    success = scraper.run()

    if success:
        print("\n✓ Scraping completed successfully!")
        return 0
    else:
        print("\n✗ Scraping failed. Check logs for details.")
        return 1


if __name__ == "__main__":
    exit(main())
