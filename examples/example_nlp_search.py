"""
Example of using natural language search with the Lead Scraper.

This example shows how to use natural language queries to find leads
without specifying structured criteria.
"""

from lead_scraper import LeadScraper


def main():
    print("=" * 70)
    print("Natural Language Lead Search Example")
    print("=" * 70)

    # Example 1: Search for startup founders
    query1 = "Find startup founders in San Francisco with 2-5 team members"

    print(f"\n[Example 1] Query: \"{query1}\"")
    print("-" * 70)

    with LeadScraper(headless=True) as scraper:
        # Search using natural language
        leads = scraper.search_leads_natural_language(query1, limit=5)

        # Print results
        print(f"\n✅ Found {len(leads)} leads:")
        for i, lead in enumerate(leads, 1):
            print(f"\n{i}. {lead.get('name', 'N/A')}")
            print(f"   Position: {lead.get('current_position', 'N/A')}")
            print(f"   Company: {lead.get('current_company', 'N/A')}")
            print(f"   LinkedIn: {lead.get('url', 'N/A')}")

        # Export to CSV
        scraper.export_leads(format='csv', filename='sf_startup_founders')

    # Example 2: Search for tech executives
    query2 = "Tech CEOs at companies founded in last 2 years"

    print(f"\n\n[Example 2] Query: \"{query2}\"")
    print("-" * 70)

    with LeadScraper(headless=True) as scraper:
        # Search using natural language
        leads = scraper.search_leads_natural_language(query2, limit=5)

        print(f"\n✅ Found {len(leads)} leads")

        # Export to Excel
        scraper.export_leads(format='excel', filename='tech_ceos_new_companies')

    # Example 3: Search for fintech leaders
    query3 = "VPs and Directors at fintech startups in New York"

    print(f"\n\n[Example 3] Query: \"{query3}\"")
    print("-" * 70)

    with LeadScraper(headless=True) as scraper:
        # Search using natural language
        leads = scraper.search_leads_natural_language(query3, limit=10)

        print(f"\n✅ Found {len(leads)} leads")

        # Show emails found
        emails_found = sum(1 for lead in leads if lead.get('emails'))
        print(f"📧 Leads with emails: {emails_found}")

        # Export to JSON for detailed data
        scraper.export_leads(format='json', filename='ny_fintech_leaders')

    print("\n" + "=" * 70)
    print("✨ Examples complete!")
    print("=" * 70)


if __name__ == '__main__':
    # NOTE: This example requires:
    # - Chrome/Chromium browser installed
    # - Internet connection
    # - The scraper will actually make web requests

    print("\n⚠️  This example requires Chrome and internet connection")
    print("    To run: python examples/example_nlp_search.py\n")

    # Uncomment the line below to run the examples
    # main()
