"""Search engine scraping functionality."""

import time
import urllib.parse
from typing import List, Dict
from bs4 import BeautifulSoup
from utils.web_scraper import WebScraper


class SearchScraper:
    """Scrape search engine results to find people and profiles."""

    def __init__(self, scraper: WebScraper):
        """
        Initialize search scraper.

        Args:
            scraper: WebScraper instance
        """
        self.scraper = scraper

    def google_search(self, query: str, num_results: int = 10) -> List[Dict[str, str]]:
        """
        Perform Google search and extract results.

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            List of search results with title, link, and snippet
        """
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded_query}&num={num_results}"

        html = self.scraper.get_page_source(url)
        if not html:
            return []

        soup = self.scraper.parse_html(html)
        results = []

        # Find all search result divs
        search_results = soup.find_all('div', class_='g')

        for result in search_results[:num_results]:
            try:
                # Extract title and link
                title_elem = result.find('h3')
                link_elem = result.find('a')

                if not title_elem or not link_elem:
                    continue

                title = title_elem.get_text(strip=True)
                link = link_elem.get('href', '')

                # Extract snippet
                snippet_elem = result.find('div', class_=['VwiC3b', 'yXK7lf'])
                snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''

                if link and title:
                    results.append({
                        'title': title,
                        'url': link,
                        'snippet': snippet
                    })
            except Exception as e:
                print(f"Error parsing search result: {e}")
                continue

        return results

    def search_for_person(self, name: str, company: str = '', title: str = '') -> List[Dict[str, str]]:
        """
        Search for a person with optional company and title.

        Args:
            name: Person's name
            company: Company name (optional)
            title: Job title (optional)

        Returns:
            List of search results
        """
        query_parts = [name]

        if company:
            query_parts.append(company)
        if title:
            query_parts.append(title)

        query = ' '.join(query_parts)
        return self.google_search(query)

    def search_linkedin_profiles(self, name: str, company: str = '') -> List[Dict[str, str]]:
        """
        Search for LinkedIn profiles.

        Args:
            name: Person's name
            company: Company name (optional)

        Returns:
            List of LinkedIn profile search results
        """
        query_parts = ['site:linkedin.com/in/', name]

        if company:
            query_parts.append(company)

        query = ' '.join(query_parts)
        results = self.google_search(query)

        # Filter to only LinkedIn URLs
        linkedin_results = [
            r for r in results
            if 'linkedin.com/in/' in r['url'].lower()
        ]

        return linkedin_results

    def search_company_employees(self, company: str, title: str = '') -> List[Dict[str, str]]:
        """
        Search for employees of a specific company.

        Args:
            company: Company name
            title: Job title to filter (optional)

        Returns:
            List of search results
        """
        query_parts = ['site:linkedin.com/in/', company]

        if title:
            query_parts.append(title)

        query = ' '.join(query_parts)
        return self.google_search(query, num_results=20)
