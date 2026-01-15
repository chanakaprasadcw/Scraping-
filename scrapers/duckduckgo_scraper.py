"""DuckDuckGo search scraper - No browser required, no rate limiting."""

import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
from typing import List, Dict


class DuckDuckGoScraper:
    """
    Scrape DuckDuckGo search results without browser automation.

    Advantages:
    - No Chrome/Selenium required
    - No rate limiting
    - Faster than browser automation
    - More reliable
    """

    def __init__(self):
        """Initialize DuckDuckGo scraper."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

    def search(self, query: str, num_results: int = 10) -> List[Dict[str, str]]:
        """
        Search DuckDuckGo and return results.

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            List of search results with title, url, snippet
        """
        results = []

        try:
            # DuckDuckGo HTML search endpoint
            encoded_query = urllib.parse.quote_plus(query)
            url = f"https://html.duckduckgo.com/html/?q={encoded_query}"

            # Make request
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find result divs
            result_divs = soup.find_all('div', class_='result')

            for result_div in result_divs[:num_results]:
                try:
                    # Extract title and URL
                    title_elem = result_div.find('a', class_='result__a')
                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)
                    url = title_elem.get('href', '')

                    # Extract snippet
                    snippet_elem = result_div.find('a', class_='result__snippet')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''

                    if url and title:
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet
                        })

                except Exception as e:
                    print(f"Error parsing result: {e}")
                    continue

            print(f"   DuckDuckGo found {len(results)} results for: {query}")

        except Exception as e:
            print(f"Error searching DuckDuckGo: {e}")

        return results

    def search_linkedin_profiles(self, name: str, company: str = '') -> List[Dict[str, str]]:
        """
        Search for LinkedIn profiles on DuckDuckGo.

        Args:
            name: Person's name
            company: Company name (optional)

        Returns:
            List of LinkedIn profile results
        """
        query_parts = ['site:linkedin.com/in', name]

        if company:
            query_parts.append(company)

        query = ' '.join(query_parts)
        results = self.search(query)

        # Filter to only LinkedIn URLs
        linkedin_results = [
            r for r in results
            if 'linkedin.com/in/' in r['url'].lower()
        ]

        return linkedin_results

    def search_company_employees(self, company: str, title: str = '', num_results: int = 20) -> List[Dict[str, str]]:
        """
        Search for employees of a company.

        Args:
            company: Company name
            title: Job title (optional)
            num_results: Number of results

        Returns:
            List of search results
        """
        query_parts = ['site:linkedin.com/in', company]

        if title:
            query_parts.append(title)

        query = ' '.join(query_parts)
        return self.search(query, num_results)
