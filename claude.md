# Claude Implementation Notes

## Project Overview

This is a Reddit scraper designed to collect frequently asked questions about microscopy equipment to improve SEO and content for Evident Scientific.com category pages.

### Target Audience Context

**Primary Users:**
- **Academia**: Professors, Associate Professors, Principal Investigators, Students, Technicians, Core Facility Managers
  - Fields: Biology, Bio-Chemistry, Neuroscience, Bioengineering
- **Pharma & Biotechnology**: Research Scientists, Lab Managers, Core Facility Managers, Technicians, IT/Purchasing Departments

**Key Pain Points to Address:**
1. **Decision Makers**: Need to create publications to secure grants
2. **End Users**: Data quality, reproducibility, competitor comparisons, technology learning curve
3. **Organizations**: Cost concerns, software integration, brand recognition

**Value Propositions to Highlight:**
- Optical expertise and high-resolution imaging
- High-quality objective lenses
- Post-sales support and fast R&D
- High throughput capabilities

**Competitors to Monitor:**
- Nikon
- Leica
- Zeiss

## Implementation Details

### Current Features (v1.0)
- Reddit scraping using PRAW (Python Reddit API Wrapper)
- Support for 7 microscopy equipment categories
- Multi-subreddit search capability
- Question detection and filtering
- CSV and JSON export formats
- Configurable search parameters

### Architecture
- `config.py`: Centralized configuration for categories, keywords, and search parameters
- `reddit_scraper.py`: Main scraper implementation
- `.env`: Environment variables for API credentials (not committed)
- `output/`: Generated FAQ data files

### Microscopy Categories Covered
1. Inverted Microscopes
2. Confocal Microscopes
3. Digital Microscopes
4. Upright Microscopes
5. Stereo Microscopes
6. Digital Pathology Systems
7. Microscope Cameras

## Future Enhancements

### High Priority
- [ ] **Quora Integration**: Add Quora scraper alongside Reddit (mentioned in original request)
- [ ] **Deduplication**: Remove duplicate questions across categories and sources
- [ ] **Answer Extraction**: Scrape top-voted answers/comments for each question
- [ ] **Sentiment Analysis**: Identify pain points and common issues users face
- [ ] **Keyword Extraction**: Extract key terms and phrases for SEO optimization

### Medium Priority
- [ ] **Rate Limiting**: Add intelligent rate limiting to avoid API throttling
- [ ] **Incremental Updates**: Track previously scraped posts to only fetch new content
- [ ] **Data Quality Filters**: Filter out low-quality or off-topic posts
- [ ] **Topic Clustering**: Group similar questions using NLP techniques
- [ ] **Scheduling**: Add cron job support for automated periodic scraping
- [ ] **Database Storage**: Store results in SQLite/PostgreSQL instead of just files
- [ ] **Web Dashboard**: Create simple web UI to view and filter scraped FAQs

### Low Priority
- [ ] **Multi-language Support**: Scrape international forums/subreddits
- [ ] **Image Extraction**: Download referenced microscope images
- [ ] **Expert Identification**: Identify and tag responses from verified experts
- [ ] **Trending Detection**: Track emerging topics and new questions over time
- [ ] **Export to CMS**: Direct integration with Evident Scientific.com CMS

## Known Limitations

1. **Reddit API Rate Limits**: Limited to 60 requests per minute
2. **No Quora Support Yet**: Original request mentioned Quora but not yet implemented
3. **Question Detection**: Simple keyword-based, may miss some questions or include false positives
4. **No Authentication State**: Each run is independent, no tracking of previous scrapes
5. **Single-threaded**: Could be optimized with async/concurrent requests

## Implementation Decisions

### Why PRAW over web scraping?
- Official Reddit API support
- Better rate limiting handling
- More reliable and maintainable
- Respects Reddit's terms of service

### Why both CSV and JSON?
- CSV for easy Excel/Google Sheets analysis
- JSON for programmatic processing and richer data structure

### Why configurable categories?
- Easy to add new microscopy product categories
- Keywords can be refined based on results
- Flexible for different product lines

## Quora Integration Notes (TODO)

Quora scraping is more challenging than Reddit because:
- No official public API
- Requires web scraping or unofficial APIs
- More aggressive anti-bot measures
- May require authentication

Potential approaches:
1. Use `quora-api` Python package (unofficial)
2. Selenium-based web scraping
3. Consider if value justifies implementation complexity

## SEO Application Strategy

### How to use this data:

1. **FAQ Sections**: Create comprehensive FAQ sections on category pages
2. **Content Ideas**: Identify gaps in current content
3. **Long-tail Keywords**: Discover question-based search terms
4. **User Language**: Use actual terminology customers use
5. **Comparison Pages**: Create "Product A vs Product B" pages for common comparisons
6. **Buying Guides**: Address common purchase decision questions

### Metrics to track:
- Which categories have most questions (indicates high interest)
- Common pain points across categories
- Technical vs. beginner questions ratio
- Purchasing-intent questions vs. general knowledge

## Contributing

When adding features, update:
1. This claude.md file with implementation notes
2. README.md with user-facing documentation
3. config.py for new configuration options
4. requirements.txt if adding dependencies

## Session History

### Session 1: Initial Implementation
- Created project structure
- Implemented Reddit scraper
- Added 7 microscopy categories
- CSV/JSON export functionality
- Basic documentation
