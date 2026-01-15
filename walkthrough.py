#!/usr/bin/env python3
"""
Interactive walkthrough of how the lead scraping system works.

This script demonstrates each step of the process with a real example.
"""

from utils.nlp_extractor import NLPExtractor
from utils.email_extractor import EmailExtractor


def step_1_nlp_extraction():
    """Step 1: Extract criteria from natural language."""
    print("\n" + "=" * 80)
    print("STEP 1: Natural Language Processing")
    print("=" * 80)

    # User's natural language query
    query = "Find startup founders in San Francisco with 2-5 team members"

    print(f"\n📝 User Input:")
    print(f'   "{query}"')

    print("\n🤖 What the system does:")
    print("   1. Converts text to lowercase for matching")
    print("   2. Scans for job titles (founder, CEO, CTO, etc.)")
    print("   3. Detects company type (startup, enterprise, etc.)")
    print("   4. Identifies location (San Francisco, NYC, etc.)")
    print("   5. Extracts team size (2-5, 10-20, etc.)")
    print("   6. Pulls out general keywords")

    # Extract criteria
    criteria = NLPExtractor.extract_criteria(query)

    print("\n✅ Extracted Criteria:")
    print(f"   Positions: {criteria['positions']}")
    print(f"   Company Type: {criteria['company_type']}")
    print(f"   Location: {criteria['location']}")
    print(f"   Team Size: {criteria['team_size']}")
    print(f"   Keywords: {criteria['keywords'][:5]}")

    return criteria


def step_2_query_generation(criteria):
    """Step 2: Generate optimized search queries."""
    print("\n" + "=" * 80)
    print("STEP 2: Search Query Generation")
    print("=" * 80)

    print("\n🔍 What the system does:")
    print("   1. Combines extracted criteria into search queries")
    print("   2. Creates LinkedIn-specific searches")
    print("   3. Optimizes for Google search algorithm")

    # Generate queries
    queries = NLPExtractor.generate_search_queries(criteria)

    print("\n✅ Generated Search Queries:")
    for i, query in enumerate(queries, 1):
        print(f"   {i}. {query}")

    print("\n💡 Why these queries?")
    print("   - They combine multiple criteria for precise results")
    print("   - LinkedIn queries target professional profiles directly")
    print("   - Location + role + company type = highly targeted")

    return queries


def step_3_search_process(queries):
    """Step 3: Explain the search process."""
    print("\n" + "=" * 80)
    print("STEP 3: Web Scraping & Search")
    print("=" * 80)

    print(f"\n🌐 For each query (example: '{queries[0]}'):")
    print("\n   A. Google Search:")
    print("      1. Initialize Chrome browser (headless)")
    print("      2. Navigate to Google with query")
    print("      3. Extract search result titles, URLs, snippets")
    print("      4. Filter for LinkedIn profile URLs")

    print("\n   B. LinkedIn Profile Scraping:")
    print("      1. Visit LinkedIn profile URL")
    print("      2. Parse HTML with BeautifulSoup")
    print("      3. Extract:")
    print("         - Name (from h1 tag)")
    print("         - Headline (current position)")
    print("         - Location")
    print("         - About/bio section")
    print("         - Work experience")
    print("         - Education")

    print("\n   C. Additional Scraping:")
    print("      1. Check non-LinkedIn URLs from search results")
    print("      2. Look for contact pages")
    print("      3. Extract email addresses")
    print("      4. Find social media links")

    print("\n   D. Anti-Detection Measures:")
    print("      1. Random user agents")
    print("      2. 2-second delays between requests")
    print("      3. Headless browser mode")
    print("      4. Randomized timing")


def step_4_email_extraction():
    """Step 4: Email extraction process."""
    print("\n" + "=" * 80)
    print("STEP 4: Email Extraction & Validation")
    print("=" * 80)

    # Sample HTML content
    sample_html = """
    <div class="contact">
        Contact us at john.doe@techstartup.com for partnerships.
        You can also reach our team at info@techstartup.com.
        Image: logo@2x.png (this should be filtered out)
    </div>
    """

    print("\n📄 Sample HTML Content:")
    print(sample_html)

    print("\n🔍 What the system does:")
    print("   1. Use regex to find email patterns")
    print("   2. Filter out false positives (.png, .jpg, example.com)")
    print("   3. Validate email format")
    print("   4. Remove duplicates")

    # Extract emails (without validation due to environment)
    emails = EmailExtractor.extract_from_html(sample_html, validate=False)

    print("\n✅ Extracted & Validated Emails:")
    for email in emails:
        print(f"   - {email}")

    print("\n❌ Filtered Out:")
    print("   - logo@2x.png (image file)")


def step_5_data_structure():
    """Step 5: Show the data structure."""
    print("\n" + "=" * 80)
    print("STEP 5: Data Structure & Storage")
    print("=" * 80)

    print("\n📊 Each lead is stored as a dictionary:")

    sample_lead = {
        'name': 'John Doe',
        'headline': 'Founder at TechStartup Inc',
        'current_position': 'Founder',
        'current_company': 'TechStartup Inc',
        'location': 'San Francisco, CA',
        'linkedin_url': 'https://linkedin.com/in/johndoe',
        'emails': ['john@techstartup.com', 'johndoe@gmail.com'],
        'about': 'Passionate entrepreneur building innovative solutions...',
        'experience': [
            {'position': 'Founder', 'company': 'TechStartup Inc'},
            {'position': 'Engineer', 'company': 'Previous Corp'}
        ],
        'education': [
            {'school': 'Stanford University'}
        ],
        'social_links': {
            'twitter': 'https://twitter.com/johndoe',
            'github': 'https://github.com/johndoe'
        },
        'search_query': 'Founder startup San Francisco',
        'matched_criteria': {
            'positions': ['Founder'],
            'company_type': 'startup',
            'industry': None
        }
    }

    print("\n```python")
    import json
    print(json.dumps(sample_lead, indent=2))
    print("```")

    print("\n💡 This structure contains:")
    print("   ✓ All profile information")
    print("   ✓ Contact details")
    print("   ✓ Work history")
    print("   ✓ What search found them")


def step_6_export():
    """Step 6: Export process."""
    print("\n" + "=" * 80)
    print("STEP 6: Data Export")
    print("=" * 80)

    print("\n📁 The system supports 3 export formats:")

    print("\n1️⃣  CSV Export:")
    print("   - Flattens nested data")
    print("   - One row per lead")
    print("   - Columns: name, company, position, emails, location, etc.")
    print("   - Easy to open in Excel/Google Sheets")

    print("\n2️⃣  JSON Export:")
    print("   - Full hierarchical data")
    print("   - Preserves all nested structures")
    print("   - Good for further processing")

    print("\n3️⃣  Excel Export:")
    print("   - Formatted workbook")
    print("   - Auto-sized columns")
    print("   - Professional appearance")
    print("   - Easy to share")

    print("\n📊 Export includes summary statistics:")
    print("   - Total leads found")
    print("   - Leads with emails")
    print("   - Leads with LinkedIn")
    print("   - Unique companies")
    print("   - Total emails")


def complete_flow_example():
    """Show the complete flow."""
    print("\n\n" + "=" * 80)
    print("COMPLETE FLOW: From Query to Results")
    print("=" * 80)

    print("\n┌─────────────────────────────────────────────────────────────┐")
    print("│ User inputs natural language query                         │")
    print("│ \"Find startup founders in San Francisco with 2-5 team\"    │")
    print("└─────────────────────────────────────────────────────────────┘")
    print("                           ↓")
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│ NLP Extractor parses the query                             │")
    print("│ • Positions: [Founder]                                     │")
    print("│ • Company Type: startup                                    │")
    print("│ • Location: San Francisco                                  │")
    print("│ • Team Size: 2-5 members                                   │")
    print("└─────────────────────────────────────────────────────────────┘")
    print("                           ↓")
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│ Query Generator creates search strings                     │")
    print("│ • \"Founder startup San Francisco\"                         │")
    print("│ • \"site:linkedin.com/in/ Founder startup\"                 │")
    print("└─────────────────────────────────────────────────────────────┘")
    print("                           ↓")
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│ Search Scraper queries Google                              │")
    print("│ • Opens Chrome (headless)                                  │")
    print("│ • Submits search queries                                   │")
    print("│ • Extracts result URLs                                     │")
    print("└─────────────────────────────────────────────────────────────┘")
    print("                           ↓")
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│ LinkedIn Scraper visits profiles                           │")
    print("│ • Parses HTML                                              │")
    print("│ • Extracts name, position, company                         │")
    print("│ • Gets work history                                        │")
    print("└─────────────────────────────────────────────────────────────┘")
    print("                           ↓")
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│ Profile Scraper finds emails                               │")
    print("│ • Visits personal websites                                 │")
    print("│ • Extracts email addresses                                 │")
    print("│ • Validates and filters                                    │")
    print("└─────────────────────────────────────────────────────────────┘")
    print("                           ↓")
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│ Data Exporter saves results                                │")
    print("│ • Creates CSV/JSON/Excel file                              │")
    print("│ • Generates summary statistics                             │")
    print("│ • Saves to output/ directory                               │")
    print("└─────────────────────────────────────────────────────────────┘")
    print("                           ↓")
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│ ✅ DONE! Leads exported and ready to use                   │")
    print("└─────────────────────────────────────────────────────────────┘")


def main():
    """Run the complete walkthrough."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "HOW THE LEAD SCRAPING SYSTEM WORKS" + " " * 23 + "║")
    print("╚" + "=" * 78 + "╝")

    # Run each step
    criteria = step_1_nlp_extraction()
    queries = step_2_query_generation(criteria)
    step_3_search_process(queries)
    step_4_email_extraction()
    step_5_data_structure()
    step_6_export()
    complete_flow_example()

    # Final summary
    print("\n\n" + "=" * 80)
    print("KEY COMPONENTS")
    print("=" * 80)

    print("\n📁 File Responsibilities:")
    print("\n   utils/nlp_extractor.py:")
    print("   → Extracts criteria from natural language")
    print("   → Generates optimized search queries")

    print("\n   utils/web_scraper.py:")
    print("   → Manages Chrome/Selenium")
    print("   → Handles page loading and delays")
    print("   → Anti-detection measures")

    print("\n   utils/email_extractor.py:")
    print("   → Finds email addresses with regex")
    print("   → Validates email format")
    print("   → Filters false positives")

    print("\n   scrapers/search_scraper.py:")
    print("   → Performs Google searches")
    print("   → Extracts search results")
    print("   → Filters LinkedIn URLs")

    print("\n   scrapers/linkedin_scraper.py:")
    print("   → Scrapes LinkedIn profiles")
    print("   → Parses name, position, company")
    print("   → Extracts experience and education")

    print("\n   scrapers/profile_scraper.py:")
    print("   → Scrapes personal websites")
    print("   → Finds contact pages")
    print("   → Extracts social media links")

    print("\n   lead_scraper.py:")
    print("   → Orchestrates all components")
    print("   → Manages the search flow")
    print("   → Coordinates data collection")

    print("\n   data_exporter.py:")
    print("   → Exports to CSV/JSON/Excel")
    print("   → Generates summaries")
    print("   → Saves files")

    print("\n   main.py:")
    print("   → CLI interface")
    print("   → Parses arguments")
    print("   → Displays results")

    print("\n\n" + "=" * 80)
    print("⚡ PERFORMANCE & SAFETY")
    print("=" * 80)

    print("\n🛡️  Anti-Detection:")
    print("   • Random user agents (looks like different browsers)")
    print("   • 2-second delays (not too fast = suspicious)")
    print("   • Headless mode (no visible browser window)")
    print("   • Randomized wait times")

    print("\n⏱️  Timing:")
    print("   • ~2 seconds per search query")
    print("   • ~2 seconds per profile scraped")
    print("   • For 10 leads: ~30-60 seconds")
    print("   • Adjustable via DELAY_BETWEEN_REQUESTS in .env")

    print("\n💾 Data Storage:")
    print("   • All leads stored in memory during scraping")
    print("   • Exported to files in output/ directory")
    print("   • Files named with timestamp (leads_20260115_143022.csv)")

    print("\n\n" + "=" * 80)
    print("✅ Walkthrough Complete!")
    print("=" * 80)
    print("\nYou now understand how the system:")
    print("  1. Parses natural language into structured criteria")
    print("  2. Generates optimized search queries")
    print("  3. Scrapes Google for LinkedIn profiles")
    print("  4. Extracts detailed information from profiles")
    print("  5. Finds email addresses from websites")
    print("  6. Exports everything to usable formats")
    print()


if __name__ == '__main__':
    main()
