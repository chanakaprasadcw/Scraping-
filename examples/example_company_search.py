"""
Example of searching for leads by company.

This example shows how to find people working at a specific company
with certain job titles.
"""

from lead_scraper import LeadScraper


def main():
    # Create a lead scraper instance
    with LeadScraper(headless=True) as scraper:
        # Search for people at a company
        company = "Tesla"
        titles = ["CEO", "CTO", "VP Engineering", "Director"]

        print(f"Searching for leads at {company}...")
        leads = scraper.search_leads_by_company(
            company=company,
            titles=titles,
            limit=15  # Maximum number of leads to find
        )

        # Print results
        print(f"\nFound {len(leads)} leads at {company}:\n")
        for i, lead in enumerate(leads, 1):
            print(f"{i}. {lead.get('name', 'N/A')}")
            print(f"   Position: {lead.get('current_position', 'N/A')}")
            print(f"   Location: {lead.get('location', 'N/A')}")
            print(f"   LinkedIn: {lead.get('url', 'N/A')}")
            print(f"   Emails: {', '.join(lead.get('emails', [])) or 'None found'}")
            print()

        # Export to Excel
        scraper.export_leads(format='excel', filename=f'{company}_leads')


if __name__ == '__main__':
    main()
