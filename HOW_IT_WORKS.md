# 🎓 How The Lead Scraping System Works

## Quick Overview

This tool finds people on the internet (LinkedIn, personal websites) and extracts their:
- Name, position, company
- Email addresses
- LinkedIn profiles
- Social media links
- Work experience

**The Magic:** You can search using **natural language** instead of complicated filters!

---

## 🤖 Natural Language Search

### You Type This:
```bash
python main.py --query "Find startup founders in San Francisco with 2-5 team members"
```

### The System Does This:

**Step 1: Understanding Your Query**
```
Input: "Find startup founders in San Francisco with 2-5 team members"

Extracts:
✓ Job Title: Founder
✓ Company Type: Startup
✓ Location: San Francisco
✓ Team Size: 2-5 members
```

**Step 2: Creating Search Queries**
```
Generates:
→ "Founder startup San Francisco"
→ "site:linkedin.com/in/ Founder startup"
```

**Step 3: Searching Google**
```
Opens Chrome → Searches Google → Gets results:
- linkedin.com/in/johndoe (Founder at TechCo)
- linkedin.com/in/janesmith (Co-Founder at StartupXYZ)
- linkedin.com/in/bobwilson (Startup Founder)
```

**Step 4: Scraping LinkedIn Profiles**
```
For each profile:
→ Visit URL
→ Parse HTML
→ Extract: name, position, company, location, bio
→ Look for email addresses
```

**Step 5: Finding More Contact Info**
```
→ Visit personal websites from search results
→ Look for contact pages
→ Extract email addresses
→ Find social media links
```

**Step 6: Exporting Results**
```
→ Save to CSV/JSON/Excel
→ Include summary statistics
→ Ready to use!
```

---

## 🔍 How Each Component Works

### 1. NLP Extractor (`utils/nlp_extractor.py`)

**What it does:** Reads your text and figures out what you want

**How it works:**
```python
query = "Find startup founders in SF with 2-5 team members"

# Looks for keywords
if "founder" in query.lower():
    positions.append("Founder")

if "startup" in query.lower():
    company_type = "startup"

if "san francisco" or "sf" in query.lower():
    location = "San Francisco"

# Looks for patterns like "2-5 members"
match = re.search(r'(\d+)-(\d+)', query)
team_size = {min: 2, max: 5}
```

**Recognizes:**
- **Positions:** CEO, CTO, Founder, VP, Director, Manager, Engineer, etc.
- **Company Types:** Startup, Enterprise, SaaS, Fintech, Agency, etc.
- **Industries:** Tech, AI, Healthcare, Finance, etc.
- **Locations:** San Francisco, NYC, Austin, Seattle, etc.
- **Team Sizes:** 2-5, 10-20, 50-100, etc.
- **Dates:** "founded in last 2 years", "since 2024", etc.

---

### 2. Search Scraper (`scrapers/search_scraper.py`)

**What it does:** Searches Google for LinkedIn profiles

**How it works:**
```python
# 1. Build Google search URL
url = f"https://www.google.com/search?q={query}"

# 2. Open with Selenium (Chrome)
driver.get(url)

# 3. Wait for page to load
time.sleep(2)

# 4. Parse HTML with BeautifulSoup
soup = BeautifulSoup(html, 'lxml')

# 5. Find search result divs
results = soup.find_all('div', class_='g')

# 6. Extract title, URL, snippet from each result
for result in results:
    title = result.find('h3').get_text()
    url = result.find('a').get('href')
    snippet = result.find('div', class_='VwiC3b').get_text()

# 7. Filter for LinkedIn URLs
linkedin_results = [r for r in results if 'linkedin.com/in/' in r['url']]
```

---

### 3. LinkedIn Scraper (`scrapers/linkedin_scraper.py`)

**What it does:** Extracts information from LinkedIn profiles

**How it works:**
```python
# 1. Visit LinkedIn profile
driver.get("https://linkedin.com/in/johndoe")

# 2. Parse HTML
soup = BeautifulSoup(html, 'lxml')

# 3. Extract name (from h1 tag)
name = soup.find('h1', class_='text-heading-xlarge').get_text()

# 4. Extract headline (current position)
headline = soup.find('div', class_='text-body-medium').get_text()
# Result: "Founder at TechStartup Inc"

# 5. Parse headline to get position and company
parts = headline.split(' at ')
position = parts[0]  # "Founder"
company = parts[1]   # "TechStartup Inc"

# 6. Extract location
location = soup.find('span', class_='text-body-small').get_text()

# 7. Extract about section
about = soup.find('div', class_='pv-shared-text-with-see-more').get_text()

# 8. Extract experience
exp_section = soup.find('section', data-section='experience')
experiences = []
for item in exp_section.find_all('li'):
    position = item.find('span').get_text()
    company = item.find('span', class_='t-normal').get_text()
    experiences.append({'position': position, 'company': company})
```

**Example output:**
```json
{
  "name": "John Doe",
  "headline": "Founder at TechStartup Inc",
  "current_position": "Founder",
  "current_company": "TechStartup Inc",
  "location": "San Francisco, CA",
  "about": "Building innovative AI solutions...",
  "experience": [
    {"position": "Founder", "company": "TechStartup Inc"},
    {"position": "Engineer", "company": "Previous Corp"}
  ]
}
```

---

### 4. Email Extractor (`utils/email_extractor.py`)

**What it does:** Finds and validates email addresses

**How it works:**
```python
# 1. Define email pattern (regex)
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# 2. Find all matches in text
text = "Contact us at john@company.com or info@company.com"
matches = re.findall(EMAIL_PATTERN, text)
# Result: ['john@company.com', 'info@company.com']

# 3. Filter false positives
exclude_patterns = ['.png', '.jpg', 'example.com', '@2x']
for pattern in exclude_patterns:
    if pattern in email:
        skip  # Don't include image files, etc.

# 4. Validate format
try:
    validate_email(email)  # Uses email-validator library
    valid_emails.append(email)
except:
    pass  # Invalid format, skip

# 5. Remove duplicates
emails = list(set(valid_emails))
```

---

### 5. Web Scraper (`utils/web_scraper.py`)

**What it does:** Controls Chrome browser and loads pages

**How it works:**
```python
# 1. Configure Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # No visible window
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument(f'user-agent={random_ua}')

# 2. Initialize Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# 3. Set timeout
driver.set_page_load_timeout(30)

# 4. Load page
driver.get(url)

# 5. Wait for content
time.sleep(random.uniform(1, 3))  # Random delay

# 6. Get HTML
html = driver.page_source

# 7. Parse with BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
```

**Anti-Detection:**
- Random user agents (looks like different browsers)
- Delays between requests (2 seconds default)
- Headless mode (no visible window)
- Randomized timing

---

### 6. Data Exporter (`data_exporter.py`)

**What it does:** Saves results to files

**How it works:**

**CSV Export:**
```python
# Flatten nested data
flattened = []
for lead in leads:
    flattened.append({
        'name': lead['name'],
        'company': lead['current_company'],
        'position': lead['current_position'],
        'emails': ', '.join(lead['emails']),
        'linkedin': lead['linkedin_url']
    })

# Create DataFrame
df = pd.DataFrame(flattened)

# Save to CSV
df.to_csv('output/leads_20260115_143052.csv', index=False)
```

**JSON Export:**
```python
# Keep full structure
with open('output/leads.json', 'w') as f:
    json.dump(leads, f, indent=2)
```

**Excel Export:**
```python
# Create formatted workbook
with pd.ExcelWriter('output/leads.xlsx') as writer:
    df.to_excel(writer, sheet_name='Leads', index=False)
    
    # Auto-size columns
    for column in df.columns:
        width = max(len(str(column)), df[column].astype(str).map(len).max())
        worksheet.column_dimensions[column].width = width + 2
```

---

## 🔄 Complete Flow Example

Let's trace a complete search from start to finish:

### Input
```bash
python main.py --query "Find tech CEOs at startups" --limit 3
```

### Step-by-Step Process

**1. CLI Parsing** (`main.py`)
```
Parses arguments:
  query = "Find tech CEOs at startups"
  limit = 3
  format = csv (default)
```

**2. NLP Extraction** (`utils/nlp_extractor.py`)
```
Analyzing: "Find tech CEOs at startups"
✓ Positions: ['Ceo']
✓ Company Type: startup
✓ Industry: tech
```

**3. Query Generation**
```
Generated queries:
  1. "Ceo startup tech"
  2. "site:linkedin.com/in/ Ceo startup tech"
```

**4. Google Search** (`scrapers/search_scraper.py`)
```
Searching: "Ceo startup tech"

Opening Chrome... ✓
Loading Google... ✓
Parsing results... ✓

Found URLs:
  - linkedin.com/in/alice-johnson
  - linkedin.com/in/bob-smith
  - linkedin.com/in/carol-williams
```

**5. LinkedIn Scraping** (`scrapers/linkedin_scraper.py`)
```
[1/3] Scraping: linkedin.com/in/alice-johnson
  → Name: Alice Johnson
  → Position: CEO
  → Company: TechStartup Inc
  → Location: San Francisco, CA
  ✓ Done (2.3s)

[2/3] Scraping: linkedin.com/in/bob-smith
  → Name: Bob Smith
  → Position: CEO & Co-Founder
  → Company: InnovateTech
  → Location: New York, NY
  ✓ Done (2.1s)

[3/3] Scraping: linkedin.com/in/carol-williams
  → Name: Carol Williams
  → Position: Chief Executive Officer
  → Company: CloudSolutions
  → Location: Austin, TX
  ✓ Done (2.4s)
```

**6. Email Search** (`scrapers/profile_scraper.py`)
```
Checking personal websites for emails...

From search results:
  - Found: alice@techstartup.com
  - Found: bob@innovatetech.io
  - No email found for Carol Williams
```

**7. Data Collection**
```
Collected 3 leads:
{
  name: "Alice Johnson",
  current_position: "CEO",
  current_company: "TechStartup Inc",
  location: "San Francisco, CA",
  linkedin_url: "linkedin.com/in/alice-johnson",
  emails: ["alice@techstartup.com"]
}
{
  name: "Bob Smith",
  current_position: "CEO & Co-Founder",
  current_company: "InnovateTech",
  location: "New York, NY",
  linkedin_url: "linkedin.com/in/bob-smith",
  emails: ["bob@innovatetech.io"]
}
{
  name: "Carol Williams",
  current_position: "Chief Executive Officer",
  current_company: "CloudSolutions",
  location: "Austin, TX",
  linkedin_url: "linkedin.com/in/carol-williams",
  emails: []
}
```

**8. Export** (`data_exporter.py`)
```
Exporting to CSV...
Created: output/leads_20260115_143052.csv

Summary:
  Total Leads: 3
  Leads with Emails: 2
  Leads with LinkedIn: 3
  Total Emails: 2

✓ Done!
```

**9. Output File**
```csv
name,company,position,location,linkedin_url,emails
Alice Johnson,TechStartup Inc,CEO,"San Francisco, CA",linkedin.com/in/alice-johnson,alice@techstartup.com
Bob Smith,InnovateTech,CEO & Co-Founder,"New York, NY",linkedin.com/in/bob-smith,bob@innovatetech.io
Carol Williams,CloudSolutions,Chief Executive Officer,"Austin, TX",linkedin.com/in/carol-williams,
```

---

## ⏱️ Timing Breakdown

For the example above (3 leads):

| Step | Time | Notes |
|------|------|-------|
| CLI Parsing | 0.01s | Instant |
| NLP Extraction | 0.01s | Regex matching |
| Query Generation | 0.01s | String operations |
| Google Search | 2.5s | Network request |
| LinkedIn Scrape #1 | 2.3s | Network + parsing |
| LinkedIn Scrape #2 | 2.1s | Network + parsing |
| LinkedIn Scrape #3 | 2.4s | Network + parsing |
| Email Search | 3.0s | Multiple pages |
| Data Export | 0.1s | File I/O |
| **Total** | **~12.5s** | For 3 leads |

**Scaling:**
- 10 leads: ~30-60 seconds
- 50 leads: ~2-5 minutes
- 100 leads: ~5-10 minutes

---

## 🎯 Key Features

### 1. Natural Language Understanding
- No need to specify exact field names
- Just describe what you want
- System figures out the rest

### 2. Multi-Source Scraping
- Google search results
- LinkedIn profiles
- Personal websites
- Social media links

### 3. Smart Email Detection
- Finds emails in HTML
- Validates format
- Filters false positives
- Removes duplicates

### 4. Flexible Export
- CSV for spreadsheets
- JSON for processing
- Excel for presentations

### 5. Anti-Detection
- Random delays
- User agent rotation
- Headless mode
- Respectful scraping

---

## 📚 Files You Can Run

```bash
# Test everything works
python test_imports.py

# See NLP in action
python test_nlp_search.py

# Understand the system
python walkthrough.py

# See practical examples
python practical_example.py

# Run a real search
python main.py --query "Your query here" --limit 5
```

---

## 🎓 Summary

**What you type:**
```
"Find startup founders in SF"
```

**What happens:**
1. System extracts criteria (Founder, startup, SF)
2. Generates search queries
3. Searches Google
4. Finds LinkedIn profiles
5. Scrapes profile data
6. Looks for emails
7. Exports to file

**What you get:**
```
name,company,position,location,linkedin_url,emails
John Doe,TechCo,Founder,San Francisco,linkedin.com/in/johndoe,john@techco.com
Jane Smith,StartupXYZ,Co-Founder,San Francisco,linkedin.com/in/janesmith,jane@startupxyz.com
...
```

**That's it!** 🎉

The system handles all the complexity so you can focus on using the data.
