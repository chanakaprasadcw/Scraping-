#!/usr/bin/env python3
"""
Lead Scraping Tool - Main CLI Application

This tool helps you find leads on the internet by scraping:
- LinkedIn profiles
- Email addresses
- Company information
- Job positions
- Personal publications and websites

Usage:
    python main.py --names "John Doe,Jane Smith" --company "Google"
    python main.py --company "Microsoft" --titles "CEO,CTO,VP"
    python main.py --config search_config.json
"""

import argparse
import json
import sys
from typing import List
from lead_scraper import LeadScraper
from data_exporter import DataExporter


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Internet Lead Scraping Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for specific people
  python main.py --names "John Doe,Jane Smith" --company "Google"

  # Search for people by company and titles
  python main.py --company "Microsoft" --titles "CEO,CTO,VP" --limit 20

  # Search with a config file
  python main.py --config config.json

  # Export to different formats
  python main.py --names "John Doe" --format excel --output my_leads
        """
    )

    # Search options
    parser.add_argument('--names', type=str, help='Comma-separated list of names to search')
    parser.add_argument('--company', type=str, help='Company name to filter/search')
    parser.add_argument('--titles', type=str, help='Comma-separated list of job titles')
    parser.add_argument('--limit', type=int, default=10, help='Maximum number of leads to find (default: 10)')

    # Config file
    parser.add_argument('--config', type=str, help='JSON config file with search criteria')

    # Output options
    parser.add_argument('--format', type=str, choices=['csv', 'json', 'excel'], default='csv',
                        help='Output format (default: csv)')
    parser.add_argument('--output', type=str, default='leads', help='Output filename without extension')

    # Scraper options
    parser.add_argument('--headless', action='store_true', default=True,
                        help='Run browser in headless mode (default: True)')
    parser.add_argument('--no-headless', dest='headless', action='store_false',
                        help='Run browser with visible window')

    return parser.parse_args()


def load_config_file(config_path: str) -> dict:
    """Load search criteria from JSON config file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config file: {e}")
        sys.exit(1)


def main():
    """Main application entry point."""
    args = parse_arguments()

    print("=" * 60)
    print("🔍 Lead Scraping Tool - Internet Search & Contact Finder")
    print("=" * 60)

    # Determine search criteria
    criteria = {}

    if args.config:
        print(f"\n📄 Loading search criteria from: {args.config}")
        criteria = load_config_file(args.config)
    else:
        # Build criteria from command line arguments
        if args.names:
            criteria['names'] = [name.strip() for name in args.names.split(',')]

        if args.company:
            criteria['company'] = args.company

        if args.titles:
            criteria['titles'] = [title.strip() for title in args.titles.split(',')]

        criteria['limit'] = args.limit

    if not criteria:
        print("\n❌ Error: No search criteria provided.")
        print("Use --names, --company, --titles, or --config to specify what to search.\n")
        sys.exit(1)

    print("\n📋 Search Criteria:")
    print(json.dumps(criteria, indent=2))

    # Create and run lead scraper
    with LeadScraper(headless=args.headless) as scraper:
        # Perform search
        leads = scraper.search_leads_by_criteria(criteria)

        if not leads:
            print("\n❌ No leads found.")
            return

        print(f"\n✅ Found {len(leads)} leads!")

        # Display summary
        exporter = DataExporter()
        summary = exporter.export_summary(leads)

        print("\n📊 Summary:")
        print(f"  Total Leads: {summary['total_leads']}")
        print(f"  Leads with Emails: {summary['leads_with_emails']}")
        print(f"  Leads with LinkedIn: {summary['leads_with_linkedin']}")
        print(f"  Unique Companies: {summary['unique_companies']}")
        print(f"  Total Emails Found: {summary['total_emails']}")

        # Export results
        output_file = scraper.export_leads(format=args.format, filename=args.output)

        if output_file:
            print(f"\n💾 Results saved to: {output_file}")

    print("\n✨ Done!")


if __name__ == '__main__':
    main()
