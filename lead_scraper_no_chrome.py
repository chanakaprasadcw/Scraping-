"""Lead scraper that works WITHOUT Chrome/Selenium.

This version uses requests-based scraping which is:
- More reliable
- Faster
- No browser required
- Less likely to be blocked
"""

import time
from typing import List, Dict
from utils.nlp_extractor import NLPExtractor
from scrapers.duckduckgo_scraper import DuckDuckGoScraper
from scrapers.requests_linkedin_scraper import RequestsLinkedInScraper
from data_exporter import DataExporter


class LeadScraperNoChrome:
    """Lead scraper using requests (no browser needed)."""

    def __init__(self, delay: int = 2):
        """
        Initialize lead scraper.

        Args:
            delay: Delay between requests in seconds
        """
        self.delay = delay
        self.search_scraper = DuckDuckGoScraper()
        self.linkedin_scraper = RequestsLinkedInScraper()
        self.leads = []

    def search_leads_natural_language(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for leads using natural language query.

        Args:
            query: Natural language search query
            limit: Maximum number of leads to find

        Returns:
            List of lead data
        """
        print("\n🤖 Processing natural language query...")
        print(f"Query: \"{query}\"\n")

        # Extract criteria from natural language
        criteria = NLPExtractor.extract_criteria(query)

        # Print extracted criteria
        print(NLPExtractor.format_criteria_summary(criteria))

        # Generate search queries
        search_queries = NLPExtractor.generate_search_queries(criteria)

        print(f"\n🔍 Generated {len(search_queries)} search queries:")
        for i, q in enumerate(search_queries, 1):
            print(f"  {i}. {q}")

        # Perform searches
        all_results = []

        for search_query in search_queries[:3]:  # Limit to 3 queries
            print(f"\n🔎 Searching: {search_query}")

            results = self.search_scraper.search(search_query, num_results=limit)
            all_results.extend(results)

            # Brief delay between searches
            time.sleep(self.delay)

        # Filter to LinkedIn profiles
        linkedin_profiles = []
        for result in all_results:
            if 'linkedin.com/in/' in result['url']:
                linkedin_profiles.append(result)

        # Remove duplicates
        unique_profiles = {p['url']: p for p in linkedin_profiles}.values()

        print(f"\n✅ Found {len(unique_profiles)} unique LinkedIn profiles")

        # Scrape each profile
        for profile in list(unique_profiles)[:limit]:
            print(f"\n📊 Scraping: {profile['title']}")

            lead_data = self.linkedin_scraper.scrape_profile(profile['url'])

            # Add search context
            lead_data['search_query'] = query
            lead_data['search_result_title'] = profile['title']
            lead_data['search_result_snippet'] = profile.get('snippet', '')

            self.leads.append(lead_data)

            # Delay between profile scrapes
            time.sleep(self.delay)

        return self.leads

    def search_leads_by_company(self, company: str, titles: List[str] = None, limit: int = 10) -> List[Dict]:
        """
        Search for leads by company.

        Args:
            company: Company name
            titles: List of job titles (optional)
            limit: Maximum number of leads

        Returns:
            List of lead data
        """
        print(f"\n🔍 Searching for leads at {company}...")

        if not titles:
            titles = ['CEO', 'CTO', 'Founder', 'VP', 'Director']

        all_results = []

        # Search for each title
        for title in titles:
            print(f"\n→ Searching for {title} at {company}")
            query = f"site:linkedin.com/in {title} {company}"

            results = self.search_scraper.search(query, num_results=limit)
            all_results.extend(results)

            time.sleep(self.delay)

        # Filter LinkedIn URLs
        linkedin_urls = []
        for result in all_results:
            if 'linkedin.com/in/' in result['url']:
                linkedin_urls.append(result)

        # Remove duplicates
        unique_profiles = {p['url']: p for p in linkedin_urls}.values()

        print(f"\n✅ Found {len(unique_profiles)} unique profiles")

        # Scrape each profile
        for profile in list(unique_profiles)[:limit]:
            print(f"\n📊 Scraping: {profile['title']}")

            lead_data = self.linkedin_scraper.scrape_profile(profile['url'])
            lead_data['company'] = company

            self.leads.append(lead_data)

            time.sleep(self.delay)

        return self.leads

    def scrape_linkedin_urls(self, urls: List[str]) -> List[Dict]:
        """
        Scrape specific LinkedIn URLs.

        This is useful if you already have a list of LinkedIn URLs
        and just want to extract the data.

        Args:
            urls: List of LinkedIn profile URLs

        Returns:
            List of lead data
        """
        print(f"\n📋 Scraping {len(urls)} LinkedIn profiles...")

        profiles = self.linkedin_scraper.scrape_multiple_profiles(urls, delay=self.delay)

        self.leads.extend(profiles)

        return profiles

    def export_leads(self, format: str = 'csv', filename: str = 'leads') -> str:
        """
        Export leads to file.

        Args:
            format: Export format ('csv', 'json', or 'excel')
            filename: Output filename (without extension)

        Returns:
            Path to exported file
        """
        exporter = DataExporter('./output')

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

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        pass  # No cleanup needed for requests-based scraping
