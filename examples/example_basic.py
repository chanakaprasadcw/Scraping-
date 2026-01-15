"""
Basic example of using the Lead Scraper.

This example shows how to search for specific people by name.
"""

from lead_scraper import LeadScraper


def main():
    # Create a lead scraper instance
    with LeadScraper(headless=True) as scraper:
        # Search for people by name
        names = [
            "Satya Nadella",
            "Sundar Pichai"
        ]

        print("Searching for leads...")
        leads = scraper.search_leads_by_name(
            names=names,
            company="",  # Optional: filter by company
            title=""     # Optional: filter by title
        )

        # Print results
        print(f"\nFound {len(leads)} leads:\n")
        for lead in leads:
            print(f"Name: {lead['name']}")
            print(f"Company: {lead.get('current_company', 'N/A')}")
            print(f"Position: {lead.get('current_position', 'N/A')}")
            print(f"LinkedIn: {lead.get('linkedin_url', 'N/A')}")
            print(f"Emails: {', '.join(lead.get('emails', [])) or 'N/A'}")
            print("-" * 50)

        # Export to CSV
        scraper.export_leads(format='csv', filename='my_leads')


if __name__ == '__main__':
    main()
