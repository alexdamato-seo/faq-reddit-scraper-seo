# CLAUDE.md - AI Assistant Guide

> **Last Updated**: 2026-01-23
> **Project**: FAQ Reddit Scraper for Microscopy SEO
> **Purpose**: This document provides comprehensive context for AI assistants working on this codebase.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Codebase Structure](#codebase-structure)
3. [Architecture & Design](#architecture--design)
4. [Development Workflows](#development-workflows)
5. [Key Conventions](#key-conventions)
6. [Common Tasks](#common-tasks)
7. [Configuration Management](#configuration-management)
8. [Business Context](#business-context)
9. [Known Limitations](#known-limitations)
10. [Future Enhancements](#future-enhancements)

---

## Project Overview

### Purpose
A Python-based web scraper that collects frequently asked questions about microscopy equipment from Reddit to improve SEO and content strategy for **Evident Scientific's** category pages.

### Goals
- **SEO Enhancement**: Discover real user questions for long-tail keywords
- **Content Strategy**: Identify content gaps and pain points
- **User Language**: Understand how customers discuss microscopy products
- **Competitive Intelligence**: Monitor competitor mentions (Nikon, Leica, Zeiss)

### Target Output
- 200-350 real microscopy questions from Reddit
- Organized by 7 equipment categories
- Exportable to CSV (for analysis) and JSON (for programmatic use)

### Key Features
- **Dual scraping modes**: API-based (faster) and API-free (no setup)
- **Multi-subreddit search**: 19 relevant subreddits
- **7 microscopy categories**: Inverted, Confocal, Digital, Upright, Stereo, Digital Pathology, Cameras
- **Question detection**: Keyword-based filtering
- **Rate limiting**: Respectful delays (2s between requests for API-free)
- **Multiple output formats**: CSV, JSON, categorized JSON

---

## Codebase Structure

```
faq-reddit-scraper-seo/
│
├── config.py                          # Centralized configuration
├── reddit_scraper.py                  # API-based scraper (PRAW)
├── reddit_scraper_no_api.py          # API-free scraper (JSON endpoints)
│
├── requirements.txt                   # Full dependencies (with PRAW)
├── requirements_no_api.txt           # Minimal dependencies (no PRAW)
│
├── .env.example                       # Environment variable template
├── .gitignore                         # Git ignore patterns
│
├── run_scraper.sh                     # One-click runner (Unix/Mac)
├── run_scraper.bat                    # One-click runner (Windows)
│
├── README.md                          # User-facing documentation
├── BEGINNER_GUIDE.md                 # Non-technical user guide
├── claude.md                          # Original AI notes (lowercase)
├── CLAUDE.md                          # This file (comprehensive AI guide)
│
├── sample_output/                     # Example output data
│   ├── SAMPLE_ANALYSIS.md            # Analysis of sample data
│   ├── SAMPLE_microscopy_faqs.csv    # Sample CSV output
│   └── SAMPLE_microscopy_faqs.json   # Sample JSON output
│
└── output/                            # Generated output (gitignored)
    ├── microscopy_faqs.csv
    ├── microscopy_faqs.json
    └── microscopy_faqs_by_category.json
```

### File Descriptions

#### Core Python Files

**`config.py`** (149 lines)
- Centralized configuration module
- Defines `MICROSCOPY_CATEGORIES` dict with 7 categories and keywords
- Lists 19 `SUBREDDITS` to search
- `QUESTION_KEYWORDS` list for detecting questions
- `SEARCH_CONFIG` dict with search parameters (time filter, sort, limits)
- `OUTPUT_CONFIG` dict with file paths and names
- **IMPORTANT**: All configuration changes should happen here only

**`reddit_scraper.py`** (253 lines)
- API-based scraper using PRAW (Python Reddit API Wrapper)
- Requires Reddit API credentials in `.env` file
- Class: `RedditMicroscopyFAQScraper`
- Methods:
  - `__init__()`: Initialize PRAW client, validate env vars
  - `is_question()`: Detect if post is a question
  - `extract_post_data()`: Extract relevant fields from post
  - `search_category()`: Search Reddit for category keywords
  - `scrape_all_categories()`: Main scraping loop
  - `save_results()`: Export to CSV/JSON
  - `run()`: Main execution method
- **Pros**: Faster, better rate limit handling, official API
- **Cons**: Requires API setup

**`reddit_scraper_no_api.py`** (316 lines)
- API-free scraper using Reddit's public JSON endpoints
- No authentication or credentials needed
- Class: `RedditJSONScraper`
- Methods:
  - `__init__(rate_limit_delay=2.0)`: Initialize requests session
  - `make_request()`: HTTP request with rate limiting
  - `search_subreddit()`: Search using `r/subreddit/search.json`
  - `is_question()`: Same question detection logic
  - `extract_post_data()`: Extract fields from JSON response
  - `search_category()`: Search Reddit for category keywords
  - `scrape_all_categories()`: Main scraping loop
  - `save_results()`: Export to CSV/JSON
  - `run()`: Main execution method
- **Pros**: No setup, no API keys, easier for beginners
- **Cons**: Slower (2s delay between requests)
- **RECOMMENDED**: Default choice for first-time users

#### Configuration Files

**`.env.example`**
- Template for Reddit API credentials
- Users copy to `.env` and fill in values
- Required variables:
  - `REDDIT_CLIENT_ID`: From reddit.com/prefs/apps
  - `REDDIT_CLIENT_SECRET`: From reddit.com/prefs/apps
  - `REDDIT_USER_AGENT`: Custom user agent string

**`requirements.txt`**
- Full dependencies including PRAW
- For API-based scraper
- Dependencies:
  - `praw==7.7.1` (Reddit API wrapper)
  - `python-dotenv==1.0.0` (env var management)
  - `pandas==2.1.4` (data handling)
  - `requests==2.31.0` (HTTP requests)

**`requirements_no_api.txt`**
- Minimal dependencies for API-free scraper
- Only 2 dependencies:
  - `requests==2.31.0` (HTTP requests)
  - `pandas==2.1.4` (data handling)

#### Runner Scripts

**`run_scraper.sh`** (Unix/Mac/Linux)
- One-click bash script
- Installs dependencies automatically
- Runs API-free scraper
- Shows progress and completion message
- Waits for user input before closing

**`run_scraper.bat`** (Windows)
- One-click batch script
- Same functionality as .sh version
- Windows-compatible commands

#### Documentation Files

**`README.md`**
- User-facing documentation
- Quick start guide
- Feature comparison table
- Configuration instructions
- Output format descriptions

**`BEGINNER_GUIDE.md`**
- Non-technical guide
- Step-by-step instructions with screenshots
- Troubleshooting section
- No terminal experience required
- Targets non-developer users

**`claude.md`** (lowercase, original)
- Earlier AI assistant notes
- Project context and implementation decisions
- Session history
- TODO list for future features
- Business context notes

**`CLAUDE.md`** (this file)
- Comprehensive AI assistant guide
- Detailed codebase documentation
- Development workflows
- Architectural decisions
- Best practices and conventions

#### Sample Output

**`sample_output/SAMPLE_ANALYSIS.md`**
- Analysis of sample scraping results
- Insights and patterns
- SEO opportunities
- Content ideas
- Demonstrates value of scraped data

**`sample_output/SAMPLE_microscopy_faqs.csv`**
- Example CSV output format
- Shows data structure
- Useful for demos without running scraper

**`sample_output/SAMPLE_microscopy_faqs.json`**
- Example JSON output format
- Shows data structure
- Useful for testing downstream processing

---

## Architecture & Design

### Design Principles

1. **Dual Implementation**: Two scrapers (API vs API-free) for flexibility
2. **Configuration-Driven**: All settings in `config.py` for easy modification
3. **Modular Design**: Clean separation of concerns (search, filter, extract, save)
4. **Respectful Scraping**: Built-in rate limiting to avoid overloading Reddit
5. **Multiple Output Formats**: CSV for humans, JSON for machines
6. **Idempotent Operations**: Each run is independent, no state persistence

### Class Architecture

Both scrapers follow the same design pattern:

```python
class RedditScraper:
    def __init__(self):
        # Initialize client (PRAW or requests)
        # Set up data structures

    def is_question(self, title, selftext) -> bool:
        # Detect if post is a question

    def extract_post_data(self, post, category) -> dict:
        # Extract relevant fields from post

    def search_category(self, category_key, category_data) -> list:
        # Search Reddit for one category
        # Returns list of post dicts

    def scrape_all_categories(self):
        # Loop through all categories
        # Populate self.all_posts and self.posts_by_category

    def save_results(self):
        # Write to CSV and JSON files

    def run(self):
        # Main execution: scrape + save
```

### Data Flow

1. **Input**: Configuration from `config.py`
2. **Search**: Query Reddit for each category × keyword × subreddit
3. **Filter**: Keep only posts that appear to be questions
4. **Deduplicate**: Use post IDs to avoid duplicates
5. **Score Filter**: Remove posts below minimum score threshold
6. **Sort**: Order by score (descending)
7. **Limit**: Keep top N results per category
8. **Export**: Save to CSV and JSON formats

### Output Schema

Each scraped post contains:

```python
{
    "category": str,           # "Confocal Microscopes"
    "title": str,              # Post title
    "selftext": str,           # Post content/body
    "url": str,                # Full Reddit URL
    "score": int,              # Upvotes (Reddit score)
    "num_comments": int,       # Comment count
    "created_utc": str,        # ISO 8601 timestamp
    "author": str,             # Reddit username
    "subreddit": str,          # Source subreddit
    "post_id": str            # Unique Reddit ID
}
```

### Rate Limiting Strategy

**API-based scraper (`reddit_scraper.py`)**:
- PRAW handles rate limiting automatically
- Reddit API limit: 60 requests/minute
- PRAW queues requests and throttles as needed

**API-free scraper (`reddit_scraper_no_api.py`)**:
- Manual rate limiting with `time.sleep(2.0)`
- 2 seconds between requests (30 requests/minute)
- Conservative to avoid triggering Reddit's anti-bot measures

### Error Handling

Both scrapers use try/except blocks around:
- Subreddit searches (catch bad subreddit names)
- HTTP requests (catch network errors)
- Data extraction (catch malformed responses)

Errors are logged but don't stop execution - scraper continues with next item.

---

## Development Workflows

### Initial Setup

```bash
# Clone repository
git clone <repo-url>
cd faq-reddit-scraper-seo

# For API-free scraper (recommended for beginners)
pip install -r requirements_no_api.txt
python reddit_scraper_no_api.py

# For API-based scraper
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Reddit API credentials
python reddit_scraper.py
```

### Running the Scraper

**Method 1: Direct Python execution**
```bash
python reddit_scraper_no_api.py    # API-free
python reddit_scraper.py           # API-based
```

**Method 2: One-click scripts**
```bash
./run_scraper.sh     # Unix/Mac
run_scraper.bat      # Windows (double-click)
```

### Testing Changes

When modifying the code:

1. **Test with limited scope**:
   ```python
   # In config.py, temporarily reduce:
   SEARCH_CONFIG = {
       "limit": 10,              # Instead of 100
       "max_results_per_category": 5  # Instead of 50
   }
   ```

2. **Test with single category**:
   ```python
   # In config.py, temporarily keep only one:
   MICROSCOPY_CATEGORIES = {
       "confocal_microscopes": {...}  # Just this one
   }
   ```

3. **Test with fewer subreddits**:
   ```python
   # In config.py:
   SUBREDDITS = ["microscopy", "labrats"]  # Just 2 for testing
   ```

4. **Check output files**: Verify CSV/JSON are generated correctly

### Adding New Categories

To add a new microscopy category:

1. Edit `config.py`
2. Add new entry to `MICROSCOPY_CATEGORIES`:
   ```python
   "category_key": {
       "name": "Display Name",
       "keywords": [
           "keyword1",
           "keyword2",
           "keyword3"
       ]
   }
   ```
3. No code changes needed in scrapers - they're configuration-driven

### Adding New Subreddits

1. Edit `config.py`
2. Add subreddit name to `SUBREDDITS` list (order matters - most relevant first)
3. No code changes needed

### Modifying Question Detection

Edit `is_question()` method in either scraper:

```python
def is_question(self, title: str, selftext: str) -> bool:
    combined_text = f"{title.lower()} {selftext.lower()}"

    # Option 1: Check for keywords (current approach)
    return any(keyword in combined_text for keyword in QUESTION_KEYWORDS)

    # Option 2: Add custom logic
    # has_question_mark = '?' in combined_text
    # has_question_word = any(word in combined_text for word in ['how', 'what', 'why'])
    # return has_question_mark or has_question_word
```

### Changing Output Format

To modify CSV columns or JSON structure:

1. Update `extract_post_data()` method to change fields
2. Both scrapers use the same format, so update both if needed

Example - adding a new field:
```python
def extract_post_data(self, post, category: str) -> Dict[str, Any]:
    return {
        'category': category,
        'title': post.title,
        # ... existing fields ...
        'is_distinguished': post.distinguished,  # NEW FIELD
    }
```

---

## Key Conventions

### Code Style

- **PEP 8 compliant**: Follow Python style guide
- **Type hints**: Use for function parameters and returns
- **Docstrings**: Every class and method has docstring
- **Logging**: Use `logging` module, not print statements (except for user-facing output)
- **Constants**: ALL_CAPS for module-level constants in `config.py`

### Naming Conventions

- **Classes**: PascalCase (`RedditMicroscopyFAQScraper`)
- **Functions/Methods**: snake_case (`extract_post_data()`)
- **Variables**: snake_case (`posts_found`, `category_key`)
- **Constants**: UPPER_SNAKE_CASE (`MICROSCOPY_CATEGORIES`, `SUBREDDITS`)
- **Private members**: Prefix with underscore (`_internal_method()`)

### Import Organization

```python
# Standard library imports
import os
import json
import logging

# Third-party imports
import praw
import pandas as pd

# Local imports
from config import MICROSCOPY_CATEGORIES, SUBREDDITS
```

### Error Handling Philosophy

- **Fail gracefully**: Don't crash on single errors
- **Log everything**: Use `logger.error()` for debugging
- **Continue scraping**: One failure shouldn't stop entire job
- **Validate inputs**: Check environment variables, config values

### Configuration Over Code

**GOOD**: Change settings in `config.py`
```python
SEARCH_CONFIG = {
    "time_filter": "year",  # Changed from "all"
}
```

**BAD**: Hardcode in scraper
```python
search_results = subreddit.search(keyword, time_filter="year")  # Don't do this
```

### Logging Levels

- `logger.info()`: Normal operation progress (category searched, results found)
- `logger.warning()`: Unusual but not error (no posts found, empty output)
- `logger.error()`: Failures that don't stop execution (network error, bad subreddit)
- `logger.debug()`: Detailed debugging info (not used currently, but available)

---

## Common Tasks

### Task: Change Search Time Range

**File**: `config.py`
**Line**: 135

```python
SEARCH_CONFIG = {
    "time_filter": "year",  # Change from "all" to "year", "month", "week", or "day"
}
```

### Task: Increase Results Per Category

**File**: `config.py`
**Line**: 139

```python
SEARCH_CONFIG = {
    "max_results_per_category": 100  # Change from 50 to 100
}
```

### Task: Add Minimum Comment Threshold

Currently only filters by score. To add comment threshold:

**File**: `reddit_scraper.py` or `reddit_scraper_no_api.py`
**Location**: `search_category()` method

```python
# Add to SEARCH_CONFIG in config.py
SEARCH_CONFIG = {
    "min_comments": 5,  # NEW
}

# In search_category() method, change:
if post.id in seen_ids or post.score < SEARCH_CONFIG['min_score']:
    continue

# To:
if (post.id in seen_ids or
    post.score < SEARCH_CONFIG['min_score'] or
    post.num_comments < SEARCH_CONFIG.get('min_comments', 0)):
    continue
```

### Task: Export to Database Instead of Files

Add database export in `save_results()` method:

```python
def save_results(self):
    # Existing CSV/JSON export...

    # Add database export
    import sqlite3
    conn = sqlite3.connect('microscopy_faqs.db')
    df = pd.DataFrame(self.all_posts)
    df.to_sql('faqs', conn, if_exists='replace', index=False)
    conn.close()
    logger.info("Saved to database: microscopy_faqs.db")
```

### Task: Add Quora Scraping

Quora doesn't have a public API. Options:

1. **Unofficial API** (quora-api package):
   ```python
   from quora import Quora
   # Similar structure to Reddit scraper
   ```

2. **Web scraping with Selenium**:
   ```python
   from selenium import webdriver
   # More complex, requires browser driver
   ```

3. **Manual Quora search** + **CSV import**:
   - Search Quora manually
   - Export to CSV
   - Merge with Reddit data

### Task: Schedule Periodic Scraping

**Option 1: Cron (Unix/Mac)**
```bash
# Run daily at 2 AM
0 2 * * * cd /path/to/scraper && python reddit_scraper_no_api.py
```

**Option 2: Task Scheduler (Windows)**
- Create scheduled task in Windows Task Scheduler
- Point to `run_scraper.bat`

**Option 3: Python script with schedule library**
```python
import schedule
import time

def job():
    scraper = RedditJSONScraper()
    scraper.run()

schedule.every().day.at("02:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Task: Deduplicate Across Runs

Currently no deduplication across runs. To add:

1. **Load previous results**:
   ```python
   def load_previous_ids(self):
       if os.path.exists('output/previous_ids.json'):
           with open('output/previous_ids.json', 'r') as f:
               self.seen_ids = set(json.load(f))
       else:
           self.seen_ids = set()
   ```

2. **Save post IDs after each run**:
   ```python
   def save_post_ids(self):
       post_ids = [post['post_id'] for post in self.all_posts]
       with open('output/previous_ids.json', 'w') as f:
           json.dump(list(self.seen_ids.union(post_ids)), f)
   ```

3. **Skip previously seen posts**:
   ```python
   if post_id in self.seen_ids:
       continue
   ```

### Task: Extract Top Comments/Answers

Add comment extraction to `extract_post_data()`:

**For API-based scraper**:
```python
def extract_post_data(self, post, category: str) -> Dict[str, Any]:
    # Get top comments
    post.comments.replace_more(limit=0)  # Remove MoreComments
    top_comments = [
        {
            'author': comment.author.name if comment.author else '[deleted]',
            'body': comment.body,
            'score': comment.score
        }
        for comment in sorted(post.comments.list(), key=lambda x: x.score, reverse=True)[:3]
    ]

    return {
        # ... existing fields ...
        'top_comments': top_comments
    }
```

---

## Configuration Management

### Environment Variables (.env)

**Purpose**: Store sensitive Reddit API credentials
**Format**: KEY=value (no quotes, no spaces around =)
**Location**: Root directory (gitignored)

**Required for API-based scraper**:
- `REDDIT_CLIENT_ID`: From https://www.reddit.com/prefs/apps
- `REDDIT_CLIENT_SECRET`: From https://www.reddit.com/prefs/apps
- `REDDIT_USER_AGENT`: Custom string (e.g., "microscopy_faq_scraper_v1.0")

**Not required for API-free scraper**

### Configuration File (config.py)

**Microscopy Categories**:
- Add/remove categories as needed
- Each category has `name` (display name) and `keywords` (search terms)
- Keywords should be specific but not too narrow
- Test different keyword variations to find best matches

**Subreddits**:
- Ordered by relevance (most relevant first)
- Target audience: academic researchers, lab managers, technicians
- Avoid general subreddits (too much noise)
- Can add industry-specific subreddits (biotech, pharma)

**Question Keywords**:
- Used to detect if a post is a question
- Case-insensitive matching
- Includes question words, question mark, help-seeking phrases
- Balance: too few = miss questions, too many = false positives

**Search Configuration**:
- `time_filter`: "all", "year", "month", "week", "day"
- `sort`: "relevance", "hot", "top", "new", "comments"
- `limit`: Max results per search (100 is Reddit's limit)
- `min_score`: Minimum upvotes (1 = include all)
- `max_results_per_category`: Final limit per category (50 recommended)

**Output Configuration**:
- `directory`: Where to save files (default: "output")
- File names for CSV and JSON outputs

### Git Configuration (.gitignore)

**Ignored files**:
- `.env` - Contains API secrets
- `output/` - Generated data (can be large)
- `__pycache__/` - Python bytecode
- `*.pyc` - Compiled Python files
- `.vscode/`, `.idea/` - IDE settings
- `venv/`, `env/` - Virtual environments

**NOT ignored**:
- `sample_output/` - Example data for demos
- `.env.example` - Template (no secrets)

---

## Business Context

### Client: Evident Scientific (formerly Olympus Life Science)

**Business**: Microscopy equipment manufacturer
**Website**: evident-scientific.com
**Goal**: Improve SEO and content for category pages

### Target Audience

**Primary Users**:
1. **Academic Researchers**
   - Professors, Associate Professors, Principal Investigators
   - PhD students, Postdocs
   - Core facility managers
   - Research technicians
   - Fields: Biology, Biochemistry, Neuroscience, Bioengineering

2. **Industry Professionals**
   - Research scientists in pharma/biotech
   - Lab managers
   - Quality control specialists
   - Purchasing departments

### User Pain Points (from business requirements)

1. **Decision Makers**:
   - Need to justify purchases for grant applications
   - Need to publish papers with high-quality data

2. **End Users (Researchers)**:
   - Data quality and reproducibility concerns
   - Comparing competitors (Nikon, Leica, Zeiss)
   - Technology learning curve
   - Integration with existing workflows

3. **Organizations**:
   - High equipment costs (>$100k for confocal systems)
   - Software/hardware integration challenges
   - Brand recognition and trust
   - Service contracts and maintenance costs

### Evident Scientific Value Propositions

When creating content from scraped FAQs, emphasize:
- **Optical expertise**: High-resolution imaging capabilities
- **Quality lenses**: Industry-leading objective lenses
- **Post-sales support**: Training, service, technical support
- **Innovation**: Fast R&D, cutting-edge technology
- **Throughput**: High-throughput imaging for large studies

### Competitive Context

**Main Competitors**:
- Nikon (strong in confocal, research microscopes)
- Leica (strong in confocal, digital pathology)
- Zeiss (premium brand, wide range)

**Monitoring Strategy**:
- Track mentions of competitor brands in scraped data
- Identify comparison questions (e.g., "Olympus vs Nikon")
- Create comparison content addressing real user questions

### SEO Strategy

**How to use scraped data**:

1. **Long-tail keywords**: Question-based searches
   - "how to choose confocal microscope"
   - "best inverted microscope for cell culture"

2. **FAQ sections**: Add to category pages
   - Real questions from target audience
   - Natural language (not corporate speak)

3. **Comparison pages**: "X vs Y"
   - Common comparisons from Reddit
   - Feature tables, use cases

4. **Buying guides**: Decision frameworks
   - Budget considerations
   - Application-specific needs
   - Total cost of ownership

5. **Blog content**: Deep dives
   - Address specific pain points
   - Technical explanations
   - Application notes

### Content Calendar Ideas

Based on scraped data:
- **Monthly**: Top 10 microscopy questions from Reddit
- **Quarterly**: Trend analysis (emerging topics)
- **Ad-hoc**: Response to specific highly-engaged questions
- **Seasonal**: Academic calendar (grant season, teaching prep)

---

## Known Limitations

### Technical Limitations

1. **Reddit API Rate Limits**
   - API-based: 60 requests/minute
   - API-free: Self-imposed 30 requests/minute
   - Large scrapes take 30-60 minutes

2. **No Quora Support**
   - Original requirement mentioned Quora
   - Quora has no public API
   - Would require web scraping (more complex)

3. **Question Detection Accuracy**
   - Keyword-based (not ML/NLP)
   - May miss questions without keywords
   - May include false positives

4. **No State Persistence**
   - Each run is independent
   - No tracking of previously scraped posts
   - Can result in duplicate data across runs

5. **Single-threaded Execution**
   - Synchronous requests (one at a time)
   - Could be optimized with async/concurrent requests
   - Current approach is simpler and more reliable

6. **Limited Data Enrichment**
   - Doesn't extract top comments/answers
   - Doesn't perform sentiment analysis
   - Doesn't identify expert users

7. **No Authentication State**
   - API-free scraper has no auth
   - Could be detected as bot by Reddit
   - Mitigated by user agent and rate limiting

### Data Quality Limitations

1. **Duplicate Questions**
   - Same question across different subreddits
   - Duplicates within categories (different keywords match same post)
   - No fuzzy matching or deduplication

2. **Off-topic Results**
   - Keywords may match non-question posts
   - May match unrelated microscopy topics
   - Requires manual review of results

3. **Incomplete Coverage**
   - Only searches specified subreddits
   - Misses questions from unlisted subreddits
   - Misses questions from other platforms (Quora, Stack Exchange)

4. **Temporal Limitations**
   - Reddit search may not return all results
   - Older posts may be less accessible
   - No real-time monitoring

---

## Future Enhancements

### High Priority

**1. Quora Integration**
- Add Quora scraper module
- Options: unofficial API, Selenium, manual import
- Same output format as Reddit scraper
- Merge results from both sources

**2. Deduplication**
- Fuzzy matching for similar questions
- Use NLP embeddings (sentence-transformers)
- Group duplicate/similar questions
- Keep highest-scored version

**3. Answer Extraction**
- Scrape top comments from Reddit threads
- Extract highest-quality answers
- Include expert responses (users with flair)
- Format as Q&A pairs for content

**4. Sentiment Analysis**
- Identify pain points and frustrations
- Detect brand mentions (positive/negative)
- Categorize by sentiment (problem, question, comparison, recommendation)
- Use for content prioritization

**5. Keyword Extraction**
- NLP-based keyword extraction
- Identify trending terms
- Discover new product categories/features
- Feed into SEO strategy

### Medium Priority

**6. Intelligent Rate Limiting**
- Adaptive delays based on response times
- Exponential backoff on errors
- Parallel requests where safe
- Optimize for speed while respecting limits

**7. Incremental Updates**
- Track previously scraped post IDs
- Only fetch new posts since last run
- Update existing posts with new scores/comments
- Reduce redundant API calls

**8. Data Quality Filters**
- Machine learning classifier for question quality
- Filter spam, off-topic, low-effort posts
- Prioritize detailed questions with context
- Score posts by relevance to business goals

**9. Topic Clustering**
- Group questions by topic using NLP
- Identify common themes (e.g., "sample preparation", "live cell imaging")
- Create topic-based content bundles
- Visualize topic relationships

**10. Automated Scheduling**
- Built-in scheduler (no cron needed)
- Configurable schedule (daily, weekly, monthly)
- Email/Slack notifications on completion
- Error alerts

**11. Database Storage**
- SQLite for local storage
- PostgreSQL for production
- Schema for posts, comments, topics
- Historical tracking and versioning

**12. Web Dashboard**
- Flask/FastAPI web interface
- Browse and search scraped FAQs
- Filter by category, date, score
- Export subsets to CSV/JSON
- Visualize trends over time

### Low Priority

**13. Multi-language Support**
- Scrape non-English subreddits
- Translate questions to English
- Identify international market opportunities
- Localized content strategy

**14. Image Extraction**
- Download referenced microscopy images
- OCR on image text
- Tag images by microscope type
- Use for visual content library

**15. Expert Identification**
- Identify users with expertise (verified flair, post history)
- Track influential users
- Potential for outreach/collaboration
- Citation in content ("According to Reddit user X...")

**16. Trend Detection**
- Track question volume over time
- Identify emerging topics
- Seasonal patterns (e.g., grant season)
- Predict future content needs

**17. CMS Integration**
- Direct integration with Evident Scientific CMS
- Auto-populate FAQ sections
- Schedule content publication
- A/B testing of FAQ content

**18. Competitive Intelligence Dashboard**
- Track competitor mentions
- Sentiment analysis by brand
- Feature comparison mentions
- Alert on negative mentions

### Enhancement Implementation Priority Matrix

| Priority | Effort | Impact | Start With |
|----------|--------|--------|------------|
| High | Low | High | ✅ Deduplication |
| High | Medium | High | ✅ Answer Extraction |
| High | High | High | ⏳ Quora Integration |
| Medium | Low | Medium | ✅ Database Storage |
| Medium | Medium | Medium | ⏳ Web Dashboard |
| Low | High | Low | ❌ CMS Integration |

---

## AI Assistant Guidelines

### When Working on This Project

**DO**:
- Read configuration from `config.py` (never hardcode)
- Update both scrapers if changing core logic
- Test with limited scope before full runs
- Add logging for debugging
- Update this CLAUDE.md when making significant changes
- Check sample_output/ to understand expected results
- Consider beginner users (non-technical audience)

**DON'T**:
- Don't break backwards compatibility without good reason
- Don't commit `.env` files or `output/` directory
- Don't remove rate limiting (respect Reddit's servers)
- Don't make API calls without delays
- Don't assume users have programming experience

### Understanding User Intent

When users ask for features:

1. **Clarify scope**: Single run or persistent feature?
2. **Check config first**: Can it be solved with config changes?
3. **Consider both scrapers**: Does it apply to API and API-free versions?
4. **Think about output**: How will this affect CSV/JSON exports?
5. **Validate business value**: Does this help SEO/content goals?

### Testing Your Changes

1. **Unit test level**: Test individual functions
2. **Integration test level**: Run with limited config (1 category, 2 subreddits, limit=10)
3. **Full test level**: Run complete scrape (takes 30-60 minutes)
4. **Output validation**: Check CSV/JSON files are valid and complete

### Common Pitfalls

1. **Forgetting rate limits**: Always maintain delays between requests
2. **Hardcoding values**: Use config.py instead
3. **Breaking API-free scraper**: Remember some users don't have API access
4. **Ignoring edge cases**: Empty results, network errors, malformed data
5. **Over-engineering**: Keep it simple - this is a data collection tool, not a platform

### Code Review Checklist

Before committing changes:
- [ ] Updated both scrapers if needed
- [ ] Added/updated docstrings
- [ ] Added logging for new operations
- [ ] Updated config.py if adding new settings
- [ ] Tested with limited scope
- [ ] Updated README.md if user-facing changes
- [ ] Updated this CLAUDE.md if architectural changes
- [ ] No secrets or credentials in code
- [ ] Maintained backwards compatibility or documented breaking changes

---

## Quick Reference

### File Locations

```bash
# Configuration
config.py:135          # SEARCH_CONFIG
config.py:6            # MICROSCOPY_CATEGORIES
config.py:84           # SUBREDDITS

# Main classes
reddit_scraper.py:35   # RedditMicroscopyFAQScraper
reddit_scraper_no_api.py:38  # RedditJSONScraper

# Key methods
reddit_scraper.py:64   # is_question()
reddit_scraper.py:104  # search_category()
reddit_scraper.py:163  # scrape_all_categories()
reddit_scraper.py:178  # save_results()
```

### Common Commands

```bash
# Install dependencies
pip install -r requirements_no_api.txt   # API-free (recommended)
pip install -r requirements.txt          # API-based

# Run scrapers
python reddit_scraper_no_api.py          # API-free
python reddit_scraper.py                 # API-based

# One-click run
./run_scraper.sh                         # Unix/Mac
run_scraper.bat                          # Windows

# Quick test (edit config.py first to limit scope)
python reddit_scraper_no_api.py

# View output
cat output/microscopy_faqs.csv           # CSV
cat output/microscopy_faqs.json          # JSON
```

### Key Constants

```python
# From config.py
MICROSCOPY_CATEGORIES  # 7 categories with keywords
SUBREDDITS            # 19 subreddits to search
QUESTION_KEYWORDS     # 30+ question indicators
SEARCH_CONFIG         # Search parameters
OUTPUT_CONFIG         # File paths
```

### Output Files

```bash
output/microscopy_faqs.csv                    # Spreadsheet format
output/microscopy_faqs.json                   # All posts as JSON array
output/microscopy_faqs_by_category.json       # Organized by category
```

---

## Version History

**v1.0** - Initial implementation
- API-based scraper with PRAW
- 7 microscopy categories
- CSV/JSON export

**v1.1** - API-free option
- Added `reddit_scraper_no_api.py`
- No authentication required
- Public JSON endpoints

**v1.2** - Usability improvements
- One-click runner scripts
- BEGINNER_GUIDE.md for non-technical users
- Sample output data

**v1.3** - Documentation overhaul
- Comprehensive CLAUDE.md (this file)
- Improved code comments
- Architecture documentation

---

## Contact & Support

**Repository**: alexdamato-seo/faq-reddit-scraper-seo
**Primary User**: Evident Scientific SEO team
**Technical Contact**: [Repository owner]

For issues, feature requests, or questions:
1. Check this CLAUDE.md first
2. Review README.md and BEGINNER_GUIDE.md
3. Check sample_output/ for examples
4. Open GitHub issue with details

---

## Conclusion

This scraper is designed to be **simple, reliable, and accessible** to non-technical users while remaining **flexible and extensible** for developers. The dual-scraper approach (API vs API-free) ensures users can get started quickly without API setup, while power users can leverage faster API-based scraping.

The configuration-driven design means most customizations can be done without touching code. When code changes are needed, the modular architecture and comprehensive documentation make it straightforward to extend.

**Key Takeaway**: This is a data collection tool, not a platform. Keep it simple, reliable, and focused on the core mission: collecting real user questions to improve SEO and content strategy for Evident Scientific.

---

*Last updated: 2026-01-23 by Claude (AI Assistant)*
