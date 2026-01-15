# Quick Start Guide - Lead Scraping Tool

## Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy environment config
cp .env.example .env

# 3. (Optional) Edit .env with your preferences
nano .env
```

## Test Installation

```bash
# Run import tests to verify everything is working
python test_imports.py

# Run the demo to see how it works
python demo.py
```

## Basic Usage

### Command Line

```bash
# Get help
python main.py --help

# Search for specific people
python main.py --names "John Doe,Jane Smith" --company "Google"

# Search by company and job titles
python main.py --company "Microsoft" --titles "CEO,CTO,VP" --limit 20

# Use a config file
python main.py --config examples/search_config.json

# Export to different formats
python main.py --company "Tesla" --format excel --output tesla_leads
```

### Python API

```python
from lead_scraper import LeadScraper

# Example 1: Search by name
with LeadScraper(headless=True) as scraper:
    leads = scraper.search_leads_by_name(
        names=["Satya Nadella"],
        company="Microsoft"
    )
    scraper.export_leads(format='csv', filename='leads')

# Example 2: Search by company
with LeadScraper() as scraper:
    leads = scraper.search_leads_by_company(
        company="Tesla",
        titles=["CEO", "VP", "Director"],
        limit=15
    )
    scraper.export_leads(format='excel')
```

## File Structure

```
Scraping-/
├── main.py              # CLI application
├── lead_scraper.py      # Main scraper class
├── config.py            # Configuration
├── data_exporter.py     # Export utilities
│
├── utils/               # Utility modules
│   ├── email_extractor.py
│   └── web_scraper.py
│
├── scrapers/            # Scraper modules
│   ├── search_scraper.py
│   ├── linkedin_scraper.py
│   └── profile_scraper.py
│
├── examples/            # Example scripts
│   ├── example_basic.py
│   ├── example_company_search.py
│   └── search_config.json
│
├── test_imports.py      # Test script
├── demo.py             # Demo script
└── output/             # Exported files (created automatically)
```

## Output Format

The tool exports leads with the following information:

- **Name**: Person's full name
- **Company**: Current company
- **Position**: Current job title
- **Location**: Geographic location
- **LinkedIn URL**: LinkedIn profile link
- **Emails**: Contact email addresses
- **About**: Bio/summary
- **Experience**: Work history
- **Social Links**: Twitter, GitHub, etc.

### Export Formats

1. **CSV** - Spreadsheet format, easy to import to Excel/Google Sheets
2. **JSON** - Full structured data with all fields
3. **Excel** - Formatted workbook with multiple sheets

## Configuration

Edit `.env` file to customize:

```bash
# Scraping Settings
HEADLESS_MODE=true          # Run browser hidden
TIMEOUT=30                  # Page load timeout (seconds)
DELAY_BETWEEN_REQUESTS=2    # Delay between requests (seconds)

# Output Settings
OUTPUT_FORMAT=csv           # Default format: csv, json, or excel
OUTPUT_DIRECTORY=./output   # Where to save files

# LinkedIn Settings (optional)
LINKEDIN_EMAIL=             # Your LinkedIn email
LINKEDIN_PASSWORD=          # Your LinkedIn password
```

## Examples

### 1. Search for Tech CEOs

```bash
python main.py --names "Elon Musk,Tim Cook,Satya Nadella" --format excel
```

### 2. Find Employees at a Company

```bash
python main.py --company "SpaceX" --titles "VP,Director,Manager" --limit 30
```

### 3. Use Config File

Create `my_search.json`:
```json
{
  "company": "Apple",
  "titles": ["VP", "Director"],
  "limit": 25
}
```

Run:
```bash
python main.py --config my_search.json --format excel
```

### 4. Python Script

```python
from lead_scraper import LeadScraper

criteria = {
    'company': 'Google',
    'titles': ['VP Engineering', 'Director'],
    'limit': 20
}

with LeadScraper(headless=True) as scraper:
    leads = scraper.search_leads_by_criteria(criteria)

    print(f"Found {len(leads)} leads")

    for lead in leads:
        print(f"{lead['name']} - {lead['current_position']}")
        if lead['emails']:
            print(f"  Email: {lead['emails'][0]}")

    scraper.export_leads(format='csv', filename='google_vps')
```

## Requirements

- Python 3.8+
- Chrome or Chromium browser
- Internet connection
- All dependencies from requirements.txt

## Important Notes

⚠️ **Legal & Ethical Use**
- Use only for legitimate lead generation
- Respect website terms of service
- Don't overload servers with requests
- Comply with data privacy laws (GDPR, CCPA)
- Use appropriate delays between requests

⚠️ **Rate Limiting**
- Search engines may block excessive requests
- Use delays (default: 2 seconds between requests)
- Consider using proxies for large-scale scraping
- Run in headless mode for better performance

⚠️ **Data Accuracy**
- Web scraping can be imprecise
- Always verify important information
- Not all profiles contain public emails
- LinkedIn limits access to public profiles only

## Troubleshooting

**No results found:**
- Check internet connection
- Verify search criteria
- Try broader search terms
- Increase the limit

**Chrome/ChromeDriver errors:**
- Ensure Chrome is installed
- ChromeDriver auto-installs via webdriver-manager
- Try running with --no-headless to see errors

**Rate limiting:**
- Increase DELAY_BETWEEN_REQUESTS in .env
- Use fewer concurrent searches
- Try again after some time

## Support

For issues or questions:
- Check the full README.md
- Review examples in examples/
- Run test_imports.py to verify setup
- Run demo.py to see how it works

---

**Created with Claude Code** 🤖
