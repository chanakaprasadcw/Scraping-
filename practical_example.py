#!/usr/bin/env python3
"""
Practical example showing how to use the lead scraper.

This demonstrates the complete workflow from query to results.
"""

print("\n" + "=" * 80)
print("PRACTICAL EXAMPLE: Using the Lead Scraper")
print("=" * 80)

print("\n📋 SCENARIO:")
print("   You want to find startup founders in San Francisco")
print("   who have small teams (2-5 people) and are in tech.")
print()

print("=" * 80)
print("METHOD 1: Command Line Interface (CLI)")
print("=" * 80)

print("\n1️⃣  Natural Language Query (Easiest!):")
print("-" * 80)
print("\n   $ python main.py --query \"Find startup founders in San Francisco with 2-5 team members\" --limit 10\n")

print("   What happens:")
print("   ✓ System extracts: Founder, startup, San Francisco, 2-5 members")
print("   ✓ Generates search queries automatically")
print("   ✓ Searches Google and LinkedIn")
print("   ✓ Scrapes up to 10 profiles")
print("   ✓ Exports to CSV (default)")

print("\n2️⃣  Structured Search:")
print("-" * 80)
print("\n   $ python main.py --company \"TechStartup Inc\" --titles \"Founder,CEO\" --limit 5\n")

print("   What happens:")
print("   ✓ Searches for Founder OR CEO at TechStartup Inc")
print("   ✓ Finds LinkedIn profiles")
print("   ✓ Scrapes up to 5 profiles")

print("\n3️⃣  Export to Different Formats:")
print("-" * 80)
print("\n   $ python main.py --query \"Tech founders\" --format excel --output my_leads\n")

print("   What happens:")
print("   ✓ Searches for tech founders")
print("   ✓ Exports to Excel format")
print("   ✓ Saves as: output/my_leads_TIMESTAMP.xlsx")

print("\n\n" + "=" * 80)
print("METHOD 2: Python API (More Control)")
print("=" * 80)

print("\n4️⃣  Using Python Code:")
print("-" * 80)

print("""
from lead_scraper import LeadScraper

# Create scraper
with LeadScraper(headless=True) as scraper:
    # Natural language search
    query = "Find startup founders in SF with small teams"
    leads = scraper.search_leads_natural_language(query, limit=10)

    # Print what we found
    print(f"Found {len(leads)} leads")

    for lead in leads:
        print(f"\\n{lead['name']}")
        print(f"  Company: {lead.get('current_company', 'N/A')}")
        print(f"  Position: {lead.get('current_position', 'N/A')}")
        print(f"  Emails: {', '.join(lead.get('emails', []))}")

    # Export to Excel
    scraper.export_leads(format='excel', filename='sf_founders')
""")

print("\n5️⃣  Search by Company:")
print("-" * 80)

print("""
from lead_scraper import LeadScraper

with LeadScraper() as scraper:
    # Find employees at a specific company
    leads = scraper.search_leads_by_company(
        company="Microsoft",
        titles=["CEO", "CTO", "VP Engineering"],
        limit=20
    )

    scraper.export_leads(format='csv', filename='microsoft_execs')
""")

print("\n6️⃣  Search Specific People:")
print("-" * 80)

print("""
from lead_scraper import LeadScraper

with LeadScraper() as scraper:
    # Search for specific individuals
    leads = scraper.search_leads_by_name(
        names=["Satya Nadella", "Sundar Pichai"],
        company="",
        title=""
    )

    for lead in leads:
        print(f"{lead['name']}: {lead.get('linkedin_url', 'Not found')}")
""")

print("\n\n" + "=" * 80)
print("METHOD 3: Config File (Reproducible)")
print("=" * 80)

print("\n7️⃣  Using JSON Config:")
print("-" * 80)

print("\n   Create: my_search.json")
print("""
{
  "company": "Tesla",
  "titles": ["VP", "Director", "Senior Manager"],
  "limit": 25
}
""")

print("   Run:")
print("   $ python main.py --config my_search.json --format excel\n")

print("\n\n" + "=" * 80)
print("UNDERSTANDING THE OUTPUT")
print("=" * 80)

print("\n📊 While Running:")
print("-" * 80)

print("""
🤖 Processing natural language query...
Query: "Find startup founders in San Francisco with 2-5 team members"

🔍 Extracted Search Criteria:
--------------------------------------------------
Positions: Founder
Company Type: startup
Location: San Francisco
Team Size: 2-5 members

🔍 Generated 2 search queries:
  1. Founder startup San Francisco
  2. site:linkedin.com/in/ Founder startup

🔎 Searching: Founder startup San Francisco
✅ Found 5 unique LinkedIn profiles

📊 Scraping: Brian Doe - Founder at TechCo
📊 Scraping: Sarah Smith - Co-Founder at StartupXYZ
...

✅ Found 5 leads!

📊 Summary:
  Total Leads: 5
  Leads with Emails: 3
  Leads with LinkedIn: 5
  Unique Companies: 5
  Total Emails Found: 4

💾 Results saved to: output/leads_20260115_143052.csv
""")

print("\n📁 Output File (CSV):")
print("-" * 80)

print("""
name,company,position,location,linkedin_url,emails,about,headline
Brian Doe,TechCo,Founder,"San Francisco, CA",https://linkedin.com/in/briandoe,"brian@techco.com","Building AI solutions...",Founder at TechCo
Sarah Smith,StartupXYZ,Co-Founder,"San Francisco, CA",https://linkedin.com/in/sarahsmith,"sarah@startupxyz.com,s.smith@gmail.com","Passionate about innovation...",Co-Founder at StartupXYZ
...
""")

print("\n\n" + "=" * 80)
print("COMMON USE CASES")
print("=" * 80)

print("\n🎯 Use Case 1: Recruiting")
print("-" * 80)
print("   Query: \"Senior engineers at AI companies in Seattle\"")
print("   Output: Contact info for recruiting outreach")

print("\n🎯 Use Case 2: Sales Prospecting")
print("-" * 80)
print("   Query: \"CTOs at SaaS startups with 10-50 employees\"")
print("   Output: Decision-makers for B2B sales")

print("\n🎯 Use Case 3: Partnership Development")
print("-" * 80)
print("   Query: \"Founders of healthcare tech companies in Boston\"")
print("   Output: Potential partners in your industry")

print("\n🎯 Use Case 4: Investor Research")
print("-" * 80)
print("   Query: \"CEOs at fintech startups founded in last 2 years\"")
print("   Output: Investment opportunities")

print("\n🎯 Use Case 5: Event Outreach")
print("-" * 80)
print("   Query: \"VPs and Directors at enterprise software companies\"")
print("   Output: Guest speakers for conferences")

print("\n\n" + "=" * 80)
print("TIPS & BEST PRACTICES")
print("=" * 80)

print("\n💡 Writing Good Queries:")
print("-" * 80)
print("   ✓ Include job title (Founder, CEO, VP, etc.)")
print("   ✓ Specify company type (startup, enterprise, SaaS, etc.)")
print("   ✓ Add location if relevant (San Francisco, NYC, etc.)")
print("   ✓ Mention team size if important (2-5 people, 10-20 employees)")
print("   ✓ Add industry keywords (tech, AI, fintech, healthcare)")

print("\n   Examples of GOOD queries:")
print("   • \"Find startup founders in SF with small teams\"")
print("   • \"Tech CEOs at companies founded in last 2 years\"")
print("   • \"VPs at fintech companies in New York\"")
print("   • \"Engineering leads at cloud computing startups\"")

print("\n   Examples of POOR queries:")
print("   • \"People\" (too vague)")
print("   • \"Jobs\" (not specific)")
print("   • \"Everyone at Google\" (too broad)")

print("\n⚡ Performance:")
print("-" * 80)
print("   • Start with small limits (--limit 5) to test")
print("   • Increase delay if getting blocked (edit .env file)")
print("   • Use headless mode for faster performance (default)")
print("   • Run during off-peak hours for better success rate")

print("\n🛡️  Safety:")
print("-" * 80)
print("   • Don't run too many searches in a row")
print("   • Respect rate limits (use delays)")
print("   • Verify emails before using them")
print("   • Follow data privacy laws (GDPR, CCPA)")

print("\n📧 Email Validation:")
print("-" * 80)
print("   • System finds emails from public sources")
print("   • Not all profiles will have emails")
print("   • Always verify before sending emails")
print("   • Use for legitimate business purposes only")

print("\n\n" + "=" * 80)
print("TROUBLESHOOTING")
print("=" * 80)

print("\n❌ No results found:")
print("   → Try broader search terms")
print("   → Increase the limit")
print("   → Check your internet connection")

print("\n❌ Chrome/ChromeDriver errors:")
print("   → Install Chrome browser")
print("   → ChromeDriver auto-installs, but check for errors")

print("\n❌ Rate limiting/blocking:")
print("   → Increase DELAY_BETWEEN_REQUESTS in .env")
print("   → Wait before trying again")
print("   → Use smaller limits")

print("\n❌ Few emails found:")
print("   → Not all profiles have public emails")
print("   → System checks LinkedIn + personal websites")
print("   → Some people don't publish contact info")

print("\n\n" + "=" * 80)
print("NEXT STEPS")
print("=" * 80)

print("\n1. Try the test scripts:")
print("   $ python test_imports.py     # Verify installation")
print("   $ python test_nlp_search.py  # Test NLP extraction")
print("   $ python demo.py             # See examples")

print("\n2. Run a simple search:")
print("   $ python main.py --query \"Tech founders\" --limit 5")

print("\n3. Check the output:")
print("   $ ls output/")
print("   $ cat output/leads_*.csv")

print("\n4. Review the examples:")
print("   $ ls examples/")
print("   $ python examples/example_basic.py")

print("\n5. Read the docs:")
print("   $ cat README.md")
print("   $ cat QUICKSTART.md")

print("\n\n" + "=" * 80)
print("✅ You're Ready to Start!")
print("=" * 80)
print()
