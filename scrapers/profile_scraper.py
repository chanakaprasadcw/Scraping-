"""General profile and website scraping for contact information."""

import re
from typing import Dict, List
from bs4 import BeautifulSoup
from utils.web_scraper import WebScraper
from utils.email_extractor import EmailExtractor


class ProfileScraper:
    """Scrape websites and profiles for contact information."""

    def __init__(self, scraper: WebScraper):
        """
        Initialize profile scraper.

        Args:
            scraper: WebScraper instance
        """
        self.scraper = scraper

    def scrape_website_for_contacts(self, url: str) -> Dict[str, any]:
        """
        Scrape a website for contact information.

        Args:
            url: Website URL

        Returns:
            Dictionary with contact information
        """
        contact_data = {
            'url': url,
            'emails': [],
            'phones': [],
            'social_links': {},
            'contact_page': None
        }

        try:
            html = self.scraper.get_page_with_requests(url)
            if not html:
                return contact_data

            soup = self.scraper.parse_html(html)

            # Extract emails
            contact_data['emails'] = EmailExtractor.extract_from_html(html)

            # Extract phone numbers
            contact_data['phones'] = self._extract_phone_numbers(html)

            # Extract social media links
            contact_data['social_links'] = self._extract_social_links(soup)

            # Try to find contact page
            contact_data['contact_page'] = self._find_contact_page(soup, url)

        except Exception as e:
            print(f"Error scraping website {url}: {e}")

        return contact_data

    def _extract_phone_numbers(self, text: str) -> List[str]:
        """Extract phone numbers from text."""
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            r'\(\d{3}\)\s*\d{3}-\d{4}',
            r'\d{3}-\d{3}-\d{4}'
        ]

        phones = set()
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                # Clean and validate
                cleaned = re.sub(r'[^\d+]', '', match)
                if 10 <= len(cleaned) <= 15:
                    phones.add(match.strip())

        return list(phones)

    def _extract_social_links(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract social media profile links."""
        social_links = {}

        social_platforms = {
            'linkedin': r'linkedin\.com/in/[\w-]+',
            'twitter': r'twitter\.com/[\w-]+',
            'facebook': r'facebook\.com/[\w.-]+',
            'github': r'github\.com/[\w-]+',
            'instagram': r'instagram\.com/[\w.-]+'
        }

        all_links = soup.find_all('a', href=True)

        for link in all_links:
            href = link.get('href', '')

            for platform, pattern in social_platforms.items():
                if re.search(pattern, href, re.IGNORECASE):
                    if platform not in social_links:
                        social_links[platform] = href
                    break

        return social_links

    def _find_contact_page(self, soup: BeautifulSoup, base_url: str) -> str:
        """Find the contact page URL."""
        contact_keywords = ['contact', 'about', 'team', 'people']

        all_links = soup.find_all('a', href=True)

        for link in all_links:
            href = link.get('href', '').lower()
            text = link.get_text(strip=True).lower()

            for keyword in contact_keywords:
                if keyword in href or keyword in text:
                    # Convert relative URL to absolute
                    if href.startswith('http'):
                        return href
                    elif href.startswith('/'):
                        return base_url.rstrip('/') + href

        return None

    def scrape_about_page(self, url: str) -> Dict[str, any]:
        """
        Scrape about/team page for team member information.

        Args:
            url: About or team page URL

        Returns:
            Dictionary with team information
        """
        team_data = {
            'url': url,
            'team_members': [],
            'emails': [],
            'description': ''
        }

        try:
            html = self.scraper.get_page_with_requests(url)
            if not html:
                return team_data

            soup = self.scraper.parse_html(html)

            # Extract all emails
            team_data['emails'] = EmailExtractor.extract_from_html(html)

            # Try to extract team member names
            team_data['team_members'] = self._extract_team_members(soup)

            # Extract page description
            description = soup.find('meta', attrs={'name': 'description'})
            if description:
                team_data['description'] = description.get('content', '')

        except Exception as e:
            print(f"Error scraping about page {url}: {e}")

        return team_data

    def _extract_team_members(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract team member information from page."""
        members = []

        # Look for common team member patterns
        member_sections = soup.find_all(['div', 'li', 'article'], class_=re.compile(
            r'team|member|staff|person|profile|employee',
            re.IGNORECASE
        ))

        for section in member_sections[:20]:  # Limit to 20
            member = {}

            # Extract name
            name_elem = section.find(['h2', 'h3', 'h4', 'h5', 'strong'])
            if name_elem:
                member['name'] = name_elem.get_text(strip=True)

            # Extract title/position
            title_elem = section.find(class_=re.compile(r'title|position|role', re.IGNORECASE))
            if title_elem:
                member['title'] = title_elem.get_text(strip=True)

            if member.get('name'):
                members.append(member)

        return members
