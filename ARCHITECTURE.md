# System Architecture

## 📊 High-Level Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                          USER INPUT                                │
├────────────────────────────────────────────────────────────────────┤
│  Natural Language Query  │  Structured Input  │  Config File       │
│  "Find tech founders"    │  --company Tesla   │  search.json       │
└────────────────────────────────────────────────────────────────────┘
                                   ↓
┌────────────────────────────────────────────────────────────────────┐
│                        main.py (CLI)                               │
│  • Parses command line arguments                                   │
│  • Routes to appropriate search method                             │
│  • Displays results and statistics                                 │
└────────────────────────────────────────────────────────────────────┘
                                   ↓
┌────────────────────────────────────────────────────────────────────┐
│                   lead_scraper.py (Orchestrator)                   │
│  • Coordinates all scraping components                             │
│  • Manages search flow                                             │
│  • Collects and stores lead data                                   │
└────────────────────────────────────────────────────────────────────┘
                                   ↓
┌──────────────────────┬──────────────────────┬──────────────────────┐
│  NLP Extractor       │  Search Scraper      │  Profile Scrapers    │
│  (Natural Language)  │  (Google Search)     │  (LinkedIn, etc.)    │
├──────────────────────┼──────────────────────┼──────────────────────┤
│ • Parse text         │ • Query Google       │ • Scrape LinkedIn    │
│ • Extract criteria   │ • Extract results    │ • Parse profiles     │
│ • Generate queries   │ • Filter URLs        │ • Extract emails     │
└──────────────────────┴──────────────────────┴──────────────────────┘
                                   ↓
┌────────────────────────────────────────────────────────────────────┐
│                     Web Scraper (Selenium)                         │
│  • Chrome browser automation                                       │
│  • Page loading and waiting                                        │
│  • Anti-detection measures                                         │
└────────────────────────────────────────────────────────────────────┘
                                   ↓
┌────────────────────────────────────────────────────────────────────┐
│                    Data Exporter (Output)                          │
│  • CSV export (flattened data)                                     │
│  • JSON export (full structure)                                    │
│  • Excel export (formatted)                                        │
└────────────────────────────────────────────────────────────────────┘
                                   ↓
┌────────────────────────────────────────────────────────────────────┐
│                         OUTPUT FILES                               │
│  output/leads_20260115_143052.csv                                  │
│  output/leads_20260115_143052.json                                 │
│  output/leads_20260115_143052.xlsx                                 │
└────────────────────────────────────────────────────────────────────┘
```

## 🔧 Component Details

### 1. **Main Entry Point** (`main.py`)

```
main.py
├── Parses CLI arguments (--query, --names, --company, etc.)
├── Loads config files if specified
├── Creates LeadScraper instance
├── Routes to appropriate search method
└── Displays results and exports data
```

**Key Functions:**
- `parse_arguments()` - Parse CLI args
- `load_config_file()` - Load JSON config
- `main()` - Main execution flow

---

### 2. **Lead Scraper** (`lead_scraper.py`)

```
LeadScraper
├── __init__() - Initialize all scrapers
├── search_leads_natural_language() - NLP-based search ⭐ NEW
├── search_leads_by_name() - Search specific people
├── search_leads_by_company() - Search by company
├── search_leads_by_criteria() - Generic search
└── export_leads() - Export results
```

**Manages:**
- WebScraper instance
- SearchScraper instance
- LinkedInScraper instance
- ProfileScraper instance
- Lead data collection

---

### 3. **NLP Extractor** (`utils/nlp_extractor.py`) ⭐ NEW

```
NLPExtractor
├── extract_criteria() - Main extraction method
├── _extract_positions() - Find job titles
├── _extract_company_type() - Identify company type
├── _extract_industry() - Find industry
├── _extract_location() - Detect location
├── _extract_team_size() - Parse team size
├── _extract_founding_year() - Get founding dates
├── generate_search_queries() - Create search strings
└── format_criteria_summary() - Display extracted info
```

**Extracts:**
- Job positions (CEO, Founder, etc.)
- Company types (startup, SaaS, etc.)
- Industries (tech, fintech, etc.)
- Locations (SF, NYC, etc.)
- Team sizes (2-5, 10-20, etc.)
- Founding dates (last 2 years, etc.)

---

### 4. **Web Scraper** (`utils/web_scraper.py`)

```
WebScraper
├── init_driver() - Start Chrome/Selenium
├── get_page_source() - Load page with Selenium
├── get_page_with_requests() - Load page with requests
├── parse_html() - Parse with BeautifulSoup
└── close() - Clean up browser
```

**Features:**
- Headless Chrome
- Random user agents
- Configurable delays
- Automatic ChromeDriver installation

---

### 5. **Search Scraper** (`scrapers/search_scraper.py`)

```
SearchScraper
├── google_search() - Perform Google search
├── search_for_person() - Search for person + company/title
├── search_linkedin_profiles() - LinkedIn-specific search
└── search_company_employees() - Find employees
```

**Does:**
- Submits queries to Google
- Parses search results
- Extracts titles, URLs, snippets
- Filters for LinkedIn profiles

---

### 6. **LinkedIn Scraper** (`scrapers/linkedin_scraper.py`)

```
LinkedInScraper
├── login() - Optional LinkedIn login
├── scrape_profile() - Main profile scraper
├── _extract_experience() - Get work history
└── _extract_education() - Get education
```

**Extracts:**
- Name
- Headline (current position)
- Location
- About/bio section
- Work experience
- Education
- Emails (if public)

---

### 7. **Profile Scraper** (`scrapers/profile_scraper.py`)

```
ProfileScraper
├── scrape_website_for_contacts() - Scrape any website
├── scrape_about_page() - Scrape about/team pages
├── _extract_phone_numbers() - Find phone numbers
├── _extract_social_links() - Find social media
├── _find_contact_page() - Locate contact page
└── _extract_team_members() - Parse team members
```

**Finds:**
- Email addresses
- Phone numbers
- Social media links (Twitter, GitHub, etc.)
- Contact pages
- Team member info

---

### 8. **Email Extractor** (`utils/email_extractor.py`)

```
EmailExtractor
├── extract_emails() - Main extraction method
├── extract_from_html() - Extract from HTML
├── _is_valid_email() - Validate email
└── EMAIL_PATTERN - Regex pattern
```

**Features:**
- Regex-based extraction
- Email validation
- False positive filtering
- HTML entity decoding

---

### 9. **Data Exporter** (`data_exporter.py`)

```
DataExporter
├── export_to_csv() - CSV export
├── export_to_json() - JSON export
├── export_to_excel() - Excel export
└── export_summary() - Generate statistics
```

**Exports:**
- CSV (spreadsheet format)
- JSON (full structured data)
- Excel (formatted workbook)
- Summary statistics

---

## 🔄 Data Flow

### Example: Natural Language Search

```
1. User Input
   ↓
   "Find startup founders in SF with 2-5 team members"

2. NLP Extraction
   ↓
   {
     positions: ['Founder'],
     company_type: 'startup',
     location: 'San Francisco',
     team_size: {min: 2, max: 5}
   }

3. Query Generation
   ↓
   [
     "Founder startup San Francisco",
     "site:linkedin.com/in/ Founder startup"
   ]

4. Google Search
   ↓
   [
     {url: "linkedin.com/in/johndoe", title: "John Doe - Founder"},
     {url: "linkedin.com/in/janesmith", title: "Jane Smith - Co-Founder"},
     ...
   ]

5. Profile Scraping
   ↓
   {
     name: "John Doe",
     current_position: "Founder",
     current_company: "TechStartup Inc",
     location: "San Francisco, CA",
     emails: ["john@techstartup.com"],
     ...
   }

6. Data Export
   ↓
   output/leads_20260115_143052.csv
```

## 🛡️ Anti-Detection Layer

```
┌─────────────────────────────────────┐
│      Anti-Detection Measures        │
├─────────────────────────────────────┤
│ • Random User Agents                │
│   → Looks like different browsers   │
│                                     │
│ • Delays Between Requests           │
│   → 2 second default (configurable) │
│   → Randomized timing               │
│                                     │
│ • Headless Browser                  │
│   → No visible window               │
│   → Faster performance              │
│                                     │
│ • Request Throttling                │
│   → Limits on concurrent requests   │
│   → Respects rate limits            │
└─────────────────────────────────────┘
```

## ⚙️ Configuration System

```
config.py
├── Loads from .env file
├── Default values for all settings
└── Exports Config class

Settings:
• HEADLESS_MODE (true/false)
• TIMEOUT (seconds)
• DELAY_BETWEEN_REQUESTS (seconds)
• OUTPUT_FORMAT (csv/json/excel)
• OUTPUT_DIRECTORY (./output)
• LINKEDIN_EMAIL (optional)
• LINKEDIN_PASSWORD (optional)
```

## 📦 Dependencies

```
Core:
├── selenium - Browser automation
├── beautifulsoup4 - HTML parsing
├── requests - HTTP requests
└── lxml - XML/HTML parser

Data:
├── pandas - Data manipulation
├── openpyxl - Excel export
└── python-dotenv - Environment config

Utilities:
├── webdriver-manager - Auto ChromeDriver
├── fake-useragent - User agent rotation
└── email-validator - Email validation
```

## 🎯 Design Patterns Used

1. **Context Manager Pattern**
   - `with LeadScraper() as scraper:`
   - Automatic resource cleanup

2. **Factory Pattern**
   - Query generation from criteria
   - Dynamic scraper selection

3. **Strategy Pattern**
   - Different search strategies
   - Multiple export formats

4. **Observer Pattern**
   - Progress reporting
   - Status updates

5. **Singleton Pattern**
   - Config class
   - WebDriver instance

## 📊 Performance Characteristics

```
Operation                 Time              Notes
─────────────────────────────────────────────────────────────
NLP Extraction           ~0.01s            Regex-based, fast
Query Generation         ~0.01s            String operations
Google Search            ~2-5s/query       Network + parsing
LinkedIn Profile         ~2-5s/profile     Network + parsing
Email Extraction         ~0.1s/page        Regex + validation
Data Export (CSV)        ~0.1s/100 leads   File I/O
Data Export (Excel)      ~0.5s/100 leads   Formatting overhead

Total for 10 leads:      ~30-60 seconds
Total for 50 leads:      ~2-5 minutes
Total for 100 leads:     ~5-10 minutes
```

## 🔒 Security Considerations

1. **No Credentials Stored**
   - LinkedIn login is optional
   - Credentials only in .env (gitignored)

2. **Public Data Only**
   - Only scrapes publicly accessible info
   - Respects robots.txt

3. **Rate Limiting**
   - Built-in delays
   - Configurable throttling

4. **Data Privacy**
   - No data sent to third parties
   - All processing local

## 🚀 Scalability

```
Current:
• Single-threaded
• Sequential processing
• Local storage

Potential Improvements:
• Multi-threading for parallel scraping
• Database backend for large datasets
• Proxy rotation for higher volume
• Caching to avoid re-scraping
• Distributed processing
```

## 📝 Error Handling

```
Try/Catch at Multiple Levels:
├── Network errors (timeout, connection)
├── Parsing errors (missing elements)
├── Validation errors (invalid emails)
└── File I/O errors (disk full, permissions)

Graceful Degradation:
• Missing fields → Empty string
• Failed profile → Skip and continue
• No emails found → Empty list
```

---

**This architecture enables:**
✅ Flexible input (CLI, API, config)
✅ Natural language understanding
✅ Multiple data sources
✅ Robust error handling
✅ Multiple export formats
✅ Easy extension and customization
