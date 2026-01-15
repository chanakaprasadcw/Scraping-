# Lead Scraping Tool - Internet Search & Contact Finder

A powerful Python-based web scraping tool to find leads on the internet without using any APIs. This tool can extract:

- 📧 **Email addresses**
- 👔 **LinkedIn profiles**
- 🏢 **Company information**
- 💼 **Job positions**
- 📝 **Personal publications and websites**
- 📱 **Social media profiles**

## Features

🤖 **NEW! Natural Language Search** - Describe what you're looking for in plain English
✨ **No API Required** - Pure web scraping, no API keys or subscriptions needed
🔍 **Multi-Source Search** - Google search, LinkedIn, personal websites
📊 **Multiple Export Formats** - CSV, JSON, Excel
🎯 **Smart Keyword Extraction** - Automatically extracts criteria from natural text
⚡ **Flexible Search** - Search by name, company, job title, or combinations
🛡️ **Anti-Detection** - Rotating user agents, delays, headless browser

## Installation

### Prerequisites

- Python 3.8 or higher
- Chrome/Chromium browser (for Selenium)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Scraping-
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create environment configuration:
```bash
cp .env.example .env
```

4. (Optional) Edit `.env` file to customize settings

## Quick Start

### 🤖 Natural Language Search (NEW!)

Simply describe what you're looking for in plain English:

```bash
# Find startup founders
python main.py --query "Find startup founders in San Francisco with 2-5 team members"

# Search for executives
python main.py --query "Tech CEOs at companies founded in last 2 years"

# Find specific roles
python main.py --query "VPs and Directors at fintech startups in New York"

# Export to Excel
python main.py --query "Engineering leads at cloud computing companies" --format excel
```

The system automatically:
- Extracts job titles (CEO, CTO, VP, Founder, etc.)
- Identifies company types (startup, enterprise, SaaS, fintech, etc.)
- Detects locations (San Francisco, New York, Austin, etc.)
- Understands team sizes (2-5 members, 10-20 people, etc.)
- Recognizes founding dates (founded in last 2 years, since 2024, etc.)
- Generates optimized search queries

### Command Line Usage

#### Search for specific people:
```bash
python main.py --names "John Doe,Jane Smith" --company "Google"
```

#### Search for people by company and job titles:
```bash
python main.py --company "Microsoft" --titles "CEO,CTO,VP" --limit 20
```

#### Use a config file:
```bash
python main.py --config examples/search_config.json
```

#### Export to different formats:
```bash
python main.py --names "Elon Musk" --format excel --output tech_leads
```

### Python API Usage

#### Example 1: Search by Name

```python
from lead_scraper import LeadScraper

# Create scraper
with LeadScraper(headless=True) as scraper:
    # Search for people
    leads = scraper.search_leads_by_name(
        names=["Satya Nadella", "Sundar Pichai"],
        company="",  # Optional filter
        title=""     # Optional filter
    )

    # Export results
    scraper.export_leads(format='csv', filename='tech_ceos')
```

#### Example 2: Search by Company

```python
from lead_scraper import LeadScraper

# Create scraper
with LeadScraper(headless=True) as scraper:
    # Find leads at a company
    leads = scraper.search_leads_by_company(
        company="Tesla",
        titles=["CEO", "CTO", "VP", "Director"],
        limit=20
    )

    # Export to Excel
    scraper.export_leads(format='excel', filename='tesla_leads')
```

#### Example 3: Advanced Search with Criteria

```python
from lead_scraper import LeadScraper

criteria = {
    'company': 'SpaceX',
    'titles': ['CEO', 'CTO', 'VP Engineering'],
    'limit': 15
}

with LeadScraper() as scraper:
    leads = scraper.search_leads_by_criteria(criteria)

    # Print results
    for lead in leads:
        print(f"{lead['name']} - {lead['current_position']}")
        print(f"Emails: {lead['emails']}")
        print(f"LinkedIn: {lead['linkedin_url']}")
```

## Configuration

### Environment Variables (.env file)

```bash
# Search Configuration
SEARCH_ENGINE=google
MAX_RESULTS_PER_SEARCH=10

# Scraping Settings
HEADLESS_MODE=true
TIMEOUT=30
DELAY_BETWEEN_REQUESTS=2

# Output Settings
OUTPUT_FORMAT=csv
OUTPUT_DIRECTORY=./output

# LinkedIn Settings (optional, for better data access)
LINKEDIN_EMAIL=your-email@example.com
LINKEDIN_PASSWORD=your-password
```

### Search Config File (JSON)

Create a JSON file with your search criteria:

```json
{
  "company": "Apple",
  "titles": [
    "CEO",
    "CTO",
    "VP Engineering",
    "Director of Product"
  ],
  "limit": 25
}
```

Then use it:
```bash
python main.py --config my_search.json
```

## Output Format

### CSV Export

The tool exports leads to CSV with the following columns:

- Name
- Company
- Position
- Location
- LinkedIn URL
- Emails (comma-separated)
- About (truncated bio)
- Headline
- Previous Position
- Previous Company
- Social Media URLs

### JSON Export

Full data export including:
- All profile information
- Experience history
- Education
- Skills
- Search results
- Social links

### Excel Export

Multi-sheet workbook with:
- Main leads sheet with key information
- Formatted and auto-sized columns

## Project Structure

```
Scraping-/
├── main.py                    # Main CLI application
├── lead_scraper.py           # Main lead scraper orchestrator
├── config.py                 # Configuration management
├── data_exporter.py          # Data export utilities
├── requirements.txt          # Python dependencies
├── .env.example              # Environment configuration template
├── README.md                 # This file
│
├── utils/
│   ├── __init__.py
│   ├── email_extractor.py    # Email extraction and validation
│   └── web_scraper.py        # Web scraping utilities
│
├── scrapers/
│   ├── __init__.py
│   ├── search_scraper.py     # Search engine scraping
│   ├── linkedin_scraper.py   # LinkedIn profile scraping
│   └── profile_scraper.py    # General profile scraping
│
├── examples/
│   ├── example_basic.py      # Basic usage example
│   ├── example_company_search.py  # Company search example
│   └── search_config.json    # Example config file
│
└── output/                   # Exported files (created automatically)
```

## Features in Detail

### Email Extraction
- Regex-based email detection
- Email validation
- False positive filtering
- HTML entity decoding

### LinkedIn Scraping
- Profile information extraction
- Experience and education parsing
- Current position and company
- Location and bio
- Optional login for enhanced access

### Search Engine Integration
- Google search results parsing
- LinkedIn profile discovery
- Company employee search
- Customizable result limits

### Profile Scraping
- Personal website scraping
- Contact page detection
- Phone number extraction
- Social media link discovery

## Limitations & Best Practices

### Limitations
- **Rate Limiting**: Search engines may block excessive requests
- **Dynamic Content**: Some sites require JavaScript rendering
- **LinkedIn**: Public profiles only (without login)
- **Email Finding**: Not all profiles contain public emails

### Best Practices
1. **Use delays** between requests (default: 2 seconds)
2. **Run in headless mode** for faster performance
3. **Validate emails** before using them
4. **Respect robots.txt** and terms of service
5. **Use proxies** for large-scale scraping
6. **Verify data** - web scraping can be imprecise

## Troubleshooting

### Common Issues

**Chrome/ChromeDriver not found:**
```bash
# The tool uses webdriver-manager which auto-installs ChromeDriver
# Ensure Chrome/Chromium is installed on your system
```

**No results found:**
- Try broader search terms
- Increase the limit
- Check your internet connection
- Verify the search criteria

**Rate limiting/blocking:**
- Increase DELAY_BETWEEN_REQUESTS in .env
- Use headless mode
- Try different search queries
- Consider using proxies

## Legal & Ethical Considerations

⚖️ **Important**: Web scraping may be subject to legal restrictions and website terms of service. This tool is for:

- ✅ Educational purposes
- ✅ Personal research
- ✅ Publicly available information
- ✅ Compliance with robots.txt

**Always:**
- Respect website terms of service
- Don't overload servers with requests
- Use collected data responsibly
- Comply with data protection laws (GDPR, CCPA, etc.)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is provided as-is for educational purposes.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the examples/ directory

---

**Note**: This tool was created to automate lead generation that was previously done manually. It respects ethical web scraping practices and should be used responsibly.