#!/usr/bin/env python3
"""
Lead Scraping Tool - NO CHROME REQUIRED

This version works WITHOUT Chrome/Selenium:
- Uses DuckDuckGo (no rate limiting)
- Uses requests library (faster, more reliable)
- No browser automation needed

Usage:
    python main_no_chrome.py --query "Find startup founders in SF"
    python main_no_chrome.py --company "Tesla" --titles "CEO,VP"
    python main_no_chrome.py --urls urls.txt
"""

import argparse
import json
import sys
from typing import List
from lead_scraper_no_chrome import LeadScraperNoChrome
from data_exporter import DataExporter


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Internet Lead Scraping Tool (No Chrome Required)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Natural language search
  python main_no_chrome.py --query "Find startup founders in SF"

  # Search by company
  python main_no_chrome.py --company "Microsoft" --titles "CEO,CTO,VP"

  # Scrape specific LinkedIn URLs
  python main_no_chrome.py --urls linkedin_urls.txt

  # Export to Excel
  python main_no_chrome.py --query "Tech CEOs" --format excel
        """
    )

    # Natural language search
    parser.add_argument('--query', type=str, help='Natural language search query')

    # Structured search
    parser.add_argument('--company', type=str, help='Company name to search')
    parser.add_argument('--titles', type=str, help='Comma-separated list of job titles')
    parser.add_argument('--limit', type=int, default=10, help='Maximum number of leads (default: 10)')

    # Direct URL scraping
    parser.add_argument('--urls', type=str, help='File with LinkedIn URLs (one per line)')

    # Output options
    parser.add_argument('--format', type=str, choices=['csv', 'json', 'excel'], default='csv',
                        help='Output format (default: csv)')
    parser.add_argument('--output', type=str, default='leads', help='Output filename without extension')

    # Delay
    parser.add_argument('--delay', type=int, default=2, help='Delay between requests in seconds (default: 2)')

    return parser.parse_args()


def load_urls_from_file(filepath: str) -> List[str]:
    """Load LinkedIn URLs from a text file."""
    try:
        with open(filepath, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and 'linkedin.com' in line]
        return urls
    except Exception as e:
        print(f"Error loading URLs from file: {e}")
        return []


def main():
    """Main application entry point."""
    args = parse_arguments()

    print("=" * 70)
    print("🔍 Lead Scraping Tool - No Chrome Required")
    print("=" * 70)
    print("Using: DuckDuckGo search + Requests library")
    print("Benefits: Faster, more reliable, no browser needed")
    print("=" * 70)

    # Create scraper
    with LeadScraperNoChrome(delay=args.delay) as scraper:

        # Mode 1: Natural language query
        if args.query:
            print("\n🤖 Natural Language Search Mode")
            leads = scraper.search_leads_natural_language(args.query, limit=args.limit)

        # Mode 2: Company search
        elif args.company:
            print("\n🏢 Company Search Mode")
            titles = [t.strip() for t in args.titles.split(',')] if args.titles else None
            leads = scraper.search_leads_by_company(args.company, titles=titles, limit=args.limit)

        # Mode 3: Direct URL scraping
        elif args.urls:
            print(f"\n📋 URL Scraping Mode")
            urls = load_urls_from_file(args.urls)

            if not urls:
                print(f"❌ No valid URLs found in {args.urls}")
                sys.exit(1)

            print(f"Loaded {len(urls)} URLs from file")
            leads = scraper.scrape_linkedin_urls(urls)

        # No search criteria
        else:
            print("\n❌ Error: No search criteria provided.")
            print("\nOptions:")
            print("  --query    : Natural language search")
            print("  --company  : Search by company")
            print("  --urls     : Scrape specific LinkedIn URLs")
            print("\nRun: python main_no_chrome.py --help")
            sys.exit(1)

        # Check if we found anything
        if not leads:
            print("\n❌ No leads found.")
            print("\nPossible reasons:")
            print("  • Search was too specific")
            print("  • No LinkedIn profiles found for query")
            print("  • Network connectivity issues")
            print("\nTry:")
            print("  • Broader search terms")
            print("  • Different query")
            print("  • Increase --limit")
            return

        print(f"\n✅ Found {len(leads)} leads!")

        # Display summary
        exporter = DataExporter()
        summary = exporter.export_summary(leads)

        print("\n📊 Summary:")
        print(f"  Total Leads: {summary['total_leads']}")
        print(f"  Leads with Emails: {summary['leads_with_emails']}")
        print(f"  Leads with LinkedIn: {summary['leads_with_linkedin']}")
        print(f"  Total Emails Found: {summary['total_emails']}")

        # Show sample of leads
        print("\n📋 Sample Leads:")
        for i, lead in enumerate(leads[:3], 1):
            print(f"\n  {i}. {lead.get('name', 'Unknown')}")
            print(f"     Position: {lead.get('current_position', 'N/A')}")
            print(f"     Company: {lead.get('current_company', 'N/A')}")
            print(f"     LinkedIn: {lead.get('url', 'N/A')}")

        if len(leads) > 3:
            print(f"\n  ... and {len(leads) - 3} more")

        # Export results
        output_file = scraper.export_leads(format=args.format, filename=args.output)

        if output_file:
            print(f"\n💾 Results saved to: {output_file}")

    print("\n✨ Done!")


if __name__ == '__main__':
    main()
