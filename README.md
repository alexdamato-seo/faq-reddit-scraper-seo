# FAQ Reddit Scraper for Microscopy SEO

A Python-based scraper that collects frequently asked questions about microscopy equipment from Reddit to improve category pages for Evident Scientific.com.

## Features

- Scrapes Reddit for microscopy-related questions
- Supports multiple microscopy categories:
  - Inverted Microscopes
  - Confocal Microscopes
  - Digital Microscopes
  - Upright Microscopes
  - Stereo Microscopes
  - Digital Pathology Systems
  - Microscope Cameras
- Exports data to CSV and JSON formats
- Filters for question-based posts
- Collects post titles, content, upvotes, and comments

## Setup

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a Reddit API application:
   - Go to https://www.reddit.com/prefs/apps
   - Click "Create App" or "Create Another App"
   - Select "script" as the app type
   - Note your client_id, client_secret, and user_agent

4. Create a `.env` file from the template:
```bash
cp .env.example .env
```

5. Edit `.env` and add your Reddit API credentials:
```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=microscopy_faq_scraper_v1.0
```

## Usage

Run the scraper:
```bash
python reddit_scraper.py
```

The scraper will:
- Search Reddit for microscopy-related questions
- Filter for posts with question keywords
- Save results to `output/` directory as both CSV and JSON

### Output Files

- `output/microscopy_faqs.csv` - CSV format with all questions
- `output/microscopy_faqs.json` - JSON format with detailed data
- `output/microscopy_faqs_by_category.json` - Questions organized by category

## Configuration

Edit `config.py` to customize:
- Search keywords and categories
- Subreddits to search
- Time range for posts
- Minimum upvote threshold
- Number of results per category

## Output Data Fields

Each scraped question includes:
- **category**: Microscopy equipment category
- **title**: Post title
- **selftext**: Post content/description
- **url**: Reddit post URL
- **score**: Number of upvotes
- **num_comments**: Number of comments
- **created_utc**: Post creation timestamp
- **author**: Post author username
- **subreddit**: Source subreddit

## License

MIT
