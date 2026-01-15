#!/usr/bin/env python3
"""
Demo script showing how the Lead Scraping Tool works.

This demo shows the API usage without making actual web requests.
For real usage, you need Chrome installed and internet connection.
"""

from utils.email_extractor import EmailExtractor
from data_exporter import DataExporter


def demo_email_extraction():
    """Demonstrate email extraction capabilities."""
    print("=" * 70)
    print("DEMO 1: Email Extraction")
    print("=" * 70)

    test_samples = [
        "Contact John Doe at john.doe@techcorp.com for partnerships",
        "Reach out to jane.smith@innovation.io or call +1-555-0123",
        """
        About Us:

        Our team is available at:
        - Sales: sales@company.com
        - Support: support@company.com
        - CEO: ceo@company.com

        Follow us on social media!
        """,
        "Email me at test@example.com or backup@sample.org"
    ]

    for i, sample in enumerate(test_samples, 1):
        print(f"\n[Sample {i}]")
        print(f"Text: {sample[:60].strip()}...")

        emails = EmailExtractor.extract_emails(sample, validate=False)
        print(f"Found: {len(emails)} email(s)")
        if emails:
            for email in emails:
                print(f"  - {email}")


def demo_data_export():
    """Demonstrate data export capabilities."""
    print("\n" + "=" * 70)
    print("DEMO 2: Data Export")
    print("=" * 70)

    # Sample lead data
    sample_leads = [
        {
            'name': 'Alice Johnson',
            'company': 'Tech Innovators Inc',
            'title': 'CEO',
            'current_position': 'Chief Executive Officer',
            'current_company': 'Tech Innovators Inc',
            'location': 'San Francisco, CA',
            'linkedin_url': 'https://linkedin.com/in/alicejohnson',
            'emails': ['alice@techinnovators.com', 'ajohnson@gmail.com'],
            'headline': 'CEO at Tech Innovators Inc',
            'about': 'Passionate technology leader with 15+ years of experience...',
            'experience': [
                {'position': 'CEO', 'company': 'Tech Innovators Inc'},
                {'position': 'VP Engineering', 'company': 'Previous Corp'}
            ],
            'social_links': {
                'twitter': 'https://twitter.com/alicejohnson',
                'github': 'https://github.com/alicejohnson'
            }
        },
        {
            'name': 'Bob Williams',
            'company': 'Digital Solutions Ltd',
            'title': 'CTO',
            'current_position': 'Chief Technology Officer',
            'current_company': 'Digital Solutions Ltd',
            'location': 'New York, NY',
            'linkedin_url': 'https://linkedin.com/in/bobwilliams',
            'emails': ['bob@digitalsolutions.com'],
            'headline': 'CTO at Digital Solutions Ltd',
            'about': 'Building scalable systems and leading engineering teams...',
            'experience': [
                {'position': 'CTO', 'company': 'Digital Solutions Ltd'},
                {'position': 'Senior Architect', 'company': 'Tech Corp'}
            ],
            'social_links': {
                'linkedin': 'https://linkedin.com/in/bobwilliams',
                'github': 'https://github.com/bwilliams'
            }
        },
        {
            'name': 'Carol Martinez',
            'company': 'Cloud Systems Inc',
            'title': 'VP Engineering',
            'current_position': 'Vice President of Engineering',
            'current_company': 'Cloud Systems Inc',
            'location': 'Austin, TX',
            'linkedin_url': 'https://linkedin.com/in/carolmartinez',
            'emails': ['carol@cloudsystems.com', 'cmartinez@cloudsystems.com'],
            'headline': 'VP Engineering at Cloud Systems Inc',
            'about': 'Leading distributed teams to build cloud-native solutions...',
            'experience': [
                {'position': 'VP Engineering', 'company': 'Cloud Systems Inc'},
                {'position': 'Director Engineering', 'company': 'StartUp Co'}
            ],
            'social_links': {}
        }
    ]

    print(f"\n📊 Sample Lead Data ({len(sample_leads)} leads)")
    print("-" * 70)

    for i, lead in enumerate(sample_leads, 1):
        print(f"\n[{i}] {lead['name']}")
        print(f"    Position: {lead['title']}")
        print(f"    Company: {lead['company']}")
        print(f"    Location: {lead['location']}")
        print(f"    LinkedIn: {lead['linkedin_url']}")
        print(f"    Emails: {', '.join(lead['emails'])}")
        if lead['social_links']:
            print(f"    Social: {', '.join(lead['social_links'].keys())}")

    # Generate summary
    exporter = DataExporter()
    summary = exporter.export_summary(sample_leads)

    print("\n" + "=" * 70)
    print("📈 Summary Statistics")
    print("=" * 70)
    print(f"Total Leads:           {summary['total_leads']}")
    print(f"Leads with Emails:     {summary['leads_with_emails']}")
    print(f"Leads with LinkedIn:   {summary['leads_with_linkedin']}")
    print(f"Unique Companies:      {summary['unique_companies']}")
    print(f"Total Emails Found:    {summary['total_emails']}")


def demo_usage_examples():
    """Show usage examples."""
    print("\n" + "=" * 70)
    print("DEMO 3: Usage Examples")
    print("=" * 70)

    examples = [
        {
            'title': 'Search for specific people',
            'command': 'python main.py --names "John Doe,Jane Smith" --company "Google"',
            'description': 'Find contact information for specific individuals'
        },
        {
            'title': 'Search by company and titles',
            'command': 'python main.py --company "Microsoft" --titles "CEO,CTO,VP" --limit 20',
            'description': 'Find executives at a specific company'
        },
        {
            'title': 'Use a config file',
            'command': 'python main.py --config examples/search_config.json',
            'description': 'Load search criteria from a JSON file'
        },
        {
            'title': 'Export to Excel',
            'command': 'python main.py --company "Tesla" --titles "Director" --format excel',
            'description': 'Export results to Excel format'
        }
    ]

    for i, example in enumerate(examples, 1):
        print(f"\n[Example {i}] {example['title']}")
        print(f"Description: {example['description']}")
        print(f"Command:")
        print(f"  $ {example['command']}")


def demo_python_api():
    """Show Python API usage."""
    print("\n" + "=" * 70)
    print("DEMO 4: Python API Usage")
    print("=" * 70)

    code_examples = [
        {
            'title': 'Basic search by name',
            'code': '''from lead_scraper import LeadScraper

with LeadScraper(headless=True) as scraper:
    leads = scraper.search_leads_by_name(
        names=["John Doe", "Jane Smith"],
        company="Google"
    )
    scraper.export_leads(format='csv', filename='google_leads')'''
        },
        {
            'title': 'Search by company',
            'code': '''from lead_scraper import LeadScraper

with LeadScraper() as scraper:
    leads = scraper.search_leads_by_company(
        company="Microsoft",
        titles=["CEO", "CTO", "VP"],
        limit=20
    )
    scraper.export_leads(format='excel', filename='microsoft_execs')'''
        },
        {
            'title': 'Advanced search with criteria',
            'code': '''from lead_scraper import LeadScraper

criteria = {
    'company': 'Tesla',
    'titles': ['VP Engineering', 'Director'],
    'limit': 15
}

with LeadScraper() as scraper:
    leads = scraper.search_leads_by_criteria(criteria)

    for lead in leads:
        print(f"{lead['name']} - {lead['current_position']}")
        print(f"Emails: {', '.join(lead['emails'])}")'''
        }
    ]

    for i, example in enumerate(code_examples, 1):
        print(f"\n[{i}] {example['title']}")
        print("-" * 70)
        print(example['code'])


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "Lead Scraping Tool - Demonstration" + " " * 19 + "║")
    print("╚" + "=" * 68 + "╝")
    print()

    # Run demos
    demo_email_extraction()
    demo_data_export()
    demo_usage_examples()
    demo_python_api()

    print("\n" + "=" * 70)
    print("✨ Demo Complete!")
    print("=" * 70)
    print("\n📚 To use the tool for real scraping:")
    print("   1. Make sure Chrome/Chromium is installed")
    print("   2. Configure .env file (copy from .env.example)")
    print("   3. Run: python main.py --help")
    print("\n⚠️  Remember to use responsibly and respect:")
    print("   - Website terms of service")
    print("   - Rate limiting")
    print("   - Data privacy laws (GDPR, CCPA, etc.)")
    print()


if __name__ == '__main__':
    main()
