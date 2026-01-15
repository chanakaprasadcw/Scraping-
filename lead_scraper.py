"""Main lead scraping orchestrator."""

import time
from typing import List, Dict, Optional
from config import Config
from utils.web_scraper import WebScraper
from scrapers.search_scraper import SearchScraper
from scrapers.linkedin_scraper import LinkedInScraper
from scrapers.profile_scraper import ProfileScraper
from data_exporter import DataExporter


class LeadScraper:
    """Main class for scraping leads from the internet."""

    def __init__(self, headless: bool = True):
        """
        Initialize lead scraper.

        Args:
            headless: Run browser in headless mode
        """
        self.config = Config()
        self.scraper = WebScraper(
            headless=headless if headless is not None else self.config.HEADLESS_MODE,
            timeout=self.config.TIMEOUT
        )
        self.search_scraper = SearchScraper(self.scraper)
        self.linkedin_scraper = LinkedInScraper(self.scraper)
        self.profile_scraper = ProfileScraper(self.scraper)
        self.leads = []

    def search_leads_by_name(self, names: List[str], company: str = '', title: str = '') -> List[Dict]:
        """
        Search for leads by name.

        Args:
            names: List of person names
            company: Company name filter (optional)
            title: Job title filter (optional)

        Returns:
            List of lead data
        """
        print(f"\n🔍 Searching for {len(names)} leads...")

        for name in names:
            print(f"\nSearching for: {name}")

            lead_data = {
                'name': name,
                'company': company,
                'title': title,
                'linkedin_url': None,
                'emails': [],
                'current_position': '',
                'location': '',
                'about': '',
                'experience': [],
                'social_links': {},
                'search_results': []
            }

            # Search for the person
            search_results = self.search_scraper.search_for_person(name, company, title)
            lead_data['search_results'] = search_results[:5]

            # Try to find LinkedIn profile
            linkedin_results = self.search_scraper.search_linkedin_profiles(name, company)
            if linkedin_results:
                linkedin_url = linkedin_results[0]['url']
                lead_data['linkedin_url'] = linkedin_url
                print(f"  Found LinkedIn: {linkedin_url}")

                # Scrape LinkedIn profile
                profile_data = self.linkedin_scraper.scrape_profile(linkedin_url)
                lead_data.update({
                    'current_position': profile_data.get('current_position', ''),
                    'current_company': profile_data.get('current_company', ''),
                    'location': profile_data.get('location', ''),
                    'about': profile_data.get('about', ''),
                    'experience': profile_data.get('experience', []),
                    'emails': profile_data.get('emails', [])
                })

            # Try to scrape personal websites or other profiles
            for result in search_results[:3]:
                if 'linkedin.com' not in result['url']:
                    contact_data = self.profile_scraper.scrape_website_for_contacts(result['url'])
                    if contact_data['emails']:
                        lead_data['emails'].extend(contact_data['emails'])
                    if contact_data['social_links']:
                        lead_data['social_links'].update(contact_data['social_links'])

            # Remove duplicate emails
            lead_data['emails'] = list(set(lead_data['emails']))

            if lead_data['emails']:
                print(f"  Found {len(lead_data['emails'])} email(s)")

            self.leads.append(lead_data)

            # Delay between requests
            time.sleep(self.config.DELAY_BETWEEN_REQUESTS)

        return self.leads

    def search_leads_by_company(self, company: str, titles: List[str] = None, limit: int = 10) -> List[Dict]:
        """
        Search for leads by company.

        Args:
            company: Company name
            titles: List of job titles to search for (optional)
            limit: Maximum number of leads to find

        Returns:
            List of lead data
        """
        print(f"\n🔍 Searching for leads at {company}...")

        if not titles:
            titles = ['CEO', 'CTO', 'VP', 'Director', 'Manager']

        all_profiles = []

        for title in titles:
            print(f"\nSearching for {title} at {company}")
            results = self.search_scraper.search_company_employees(company, title)

            for result in results[:limit]:
                if 'linkedin.com/in/' in result['url']:
                    all_profiles.append(result)

        # Remove duplicates
        unique_profiles = {p['url']: p for p in all_profiles}.values()

        print(f"\nFound {len(unique_profiles)} unique LinkedIn profiles")

        # Scrape each profile
        for profile in list(unique_profiles)[:limit]:
            print(f"\nScraping: {profile['url']}")

            lead_data = self.linkedin_scraper.scrape_profile(profile['url'])
            lead_data['company'] = company

            self.leads.append(lead_data)

            # Delay between requests
            time.sleep(self.config.DELAY_BETWEEN_REQUESTS)

        return self.leads

    def search_leads_by_criteria(self, criteria: Dict[str, any]) -> List[Dict]:
        """
        Search for leads by multiple criteria.

        Args:
            criteria: Dictionary with search criteria
                {
                    'names': List[str],  # Optional
                    'company': str,      # Optional
                    'titles': List[str], # Optional
                    'keywords': List[str] # Optional
                }

        Returns:
            List of lead data
        """
        if criteria.get('names'):
            return self.search_leads_by_name(
                criteria['names'],
                criteria.get('company', ''),
                criteria.get('titles', [''])[0] if criteria.get('titles') else ''
            )
        elif criteria.get('company'):
            return self.search_leads_by_company(
                criteria['company'],
                criteria.get('titles'),
                criteria.get('limit', 10)
            )
        else:
            print("Please provide either names or company in criteria")
            return []

    def export_leads(self, format: str = 'csv', filename: str = 'leads') -> str:
        """
        Export leads to file.

        Args:
            format: Export format ('csv', 'json', or 'excel')
            filename: Output filename (without extension)

        Returns:
            Path to exported file
        """
        exporter = DataExporter(self.config.OUTPUT_DIRECTORY)

        if format == 'csv':
            return exporter.export_to_csv(self.leads, filename)
        elif format == 'json':
            return exporter.export_to_json(self.leads, filename)
        elif format == 'excel':
            return exporter.export_to_excel(self.leads, filename)
        else:
            print(f"Unknown format: {format}. Using CSV.")
            return exporter.export_to_csv(self.leads, filename)

    def get_leads(self) -> List[Dict]:
        """Get all collected leads."""
        return self.leads

    def clear_leads(self):
        """Clear all collected leads."""
        self.leads = []

    def close(self):
        """Close the scraper and clean up resources."""
        self.scraper.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
