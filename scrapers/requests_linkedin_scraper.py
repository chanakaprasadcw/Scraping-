"""LinkedIn scraper using requests (no browser needed)."""

import requests
from bs4 import BeautifulSoup
import time
from typing import Dict, List
import re


class RequestsLinkedInScraper:
    """
    Scrape LinkedIn profiles using requests library (no Selenium).

    This is faster and more reliable than browser automation.
    Works for public profiles.
    """

    def __init__(self):
        """Initialize LinkedIn scraper."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })

    def scrape_profile(self, profile_url: str) -> Dict[str, any]:
        """
        Scrape a LinkedIn profile.

        Args:
            profile_url: LinkedIn profile URL

        Returns:
            Dictionary with profile information
        """
        profile_data = {
            'url': profile_url,
            'name': '',
            'headline': '',
            'location': '',
            'about': '',
            'current_company': '',
            'current_position': '',
            'experience': [],
            'education': [],
            'emails': []
        }

        try:
            print(f"   Fetching: {profile_url}")

            # Make request
            response = self.session.get(profile_url, timeout=10)

            if response.status_code != 200:
                print(f"   ⚠️  Status code: {response.status_code}")
                return profile_data

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract name - try multiple selectors
            name_selectors = [
                ('h1', {'class': re.compile('top-card.*name|text-heading-xlarge')}),
                ('h1', {'class': 'inline'}),
                ('h1', {}),
            ]

            for tag, attrs in name_selectors:
                name_elem = soup.find(tag, attrs)
                if name_elem:
                    profile_data['name'] = name_elem.get_text(strip=True)
                    break

            # Extract headline - try multiple selectors
            headline_selectors = [
                ('div', {'class': re.compile('top-card.*headline|text-body-medium')}),
                ('div', {'class': 'mt1'}),
                ('h2', {'class': 'mt1'}),
            ]

            for tag, attrs in headline_selectors:
                headline_elem = soup.find(tag, attrs)
                if headline_elem:
                    headline_text = headline_elem.get_text(strip=True)
                    if headline_text and len(headline_text) < 200:  # Sanity check
                        profile_data['headline'] = headline_text
                        break

            # Extract current position and company from headline
            if profile_data['headline']:
                # Try to split "Position at Company"
                if ' at ' in profile_data['headline']:
                    parts = profile_data['headline'].split(' at ', 1)
                    if len(parts) == 2:
                        profile_data['current_position'] = parts[0].strip()
                        profile_data['current_company'] = parts[1].strip()
                else:
                    # Just use headline as position
                    profile_data['current_position'] = profile_data['headline']

            # Extract location
            location_selectors = [
                ('span', {'class': re.compile('top-card.*location|text-body-small')}),
                ('span', {'class': 'inline'}),
            ]

            for tag, attrs in location_selectors:
                location_elem = soup.find(tag, attrs)
                if location_elem:
                    location_text = location_elem.get_text(strip=True)
                    # Filter out non-location text
                    if location_text and len(location_text) < 100 and ',' in location_text:
                        profile_data['location'] = location_text
                        break

            # Try to extract about section
            about_elem = soup.find('section', {'class': re.compile('summary|about')})
            if about_elem:
                about_text = about_elem.get_text(strip=True)
                if about_text and len(about_text) > 20:
                    profile_data['about'] = about_text[:500]  # Limit length

            # Extract experience (basic)
            exp_section = soup.find('section', {'id': re.compile('experience')})
            if exp_section:
                # Try to find experience items
                exp_items = exp_section.find_all('li', limit=5)
                for item in exp_items:
                    text = item.get_text(strip=True)
                    if text and len(text) > 10:
                        # Simple parsing - just store the text
                        profile_data['experience'].append({'text': text[:200]})

            print(f"   ✓ Extracted: {profile_data['name'] or 'Unknown'}")

        except Exception as e:
            print(f"   ✗ Error scraping {profile_url}: {e}")

        return profile_data

    def scrape_multiple_profiles(self, profile_urls: List[str], delay: int = 2) -> List[Dict[str, any]]:
        """
        Scrape multiple LinkedIn profiles.

        Args:
            profile_urls: List of LinkedIn URLs
            delay: Delay between requests (seconds)

        Returns:
            List of profile data dictionaries
        """
        profiles = []

        for i, url in enumerate(profile_urls, 1):
            print(f"\n[{i}/{len(profile_urls)}] Scraping profile...")

            profile_data = self.scrape_profile(url)

            if profile_data.get('name'):
                profiles.append(profile_data)

            # Delay between requests
            if i < len(profile_urls):
                time.sleep(delay)

        return profiles
