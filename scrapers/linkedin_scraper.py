"""LinkedIn profile scraping functionality."""

import time
import re
from typing import Optional, Dict, List
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.web_scraper import WebScraper
from utils.email_extractor import EmailExtractor


class LinkedInScraper:
    """Scrape LinkedIn profiles for professional information."""

    def __init__(self, scraper: WebScraper):
        """
        Initialize LinkedIn scraper.

        Args:
            scraper: WebScraper instance
        """
        self.scraper = scraper
        self.is_logged_in = False

    def login(self, email: str, password: str) -> bool:
        """
        Login to LinkedIn (optional, provides more data access).

        Args:
            email: LinkedIn email
            password: LinkedIn password

        Returns:
            True if login successful
        """
        if not email or not password:
            print("LinkedIn credentials not provided. Scraping in guest mode.")
            return False

        try:
            self.scraper.init_driver()
            self.scraper.driver.get('https://www.linkedin.com/login')

            time.sleep(2)

            # Find and fill email
            email_field = self.scraper.driver.find_element(By.ID, 'username')
            email_field.send_keys(email)

            # Find and fill password
            password_field = self.scraper.driver.find_element(By.ID, 'password')
            password_field.send_keys(password)

            # Click login button
            login_button = self.scraper.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            login_button.click()

            time.sleep(5)

            # Check if login successful
            if 'feed' in self.scraper.driver.current_url:
                self.is_logged_in = True
                print("Successfully logged in to LinkedIn")
                return True
            else:
                print("LinkedIn login failed")
                return False

        except Exception as e:
            print(f"Error logging in to LinkedIn: {e}")
            return False

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
            'skills': [],
            'emails': []
        }

        try:
            html = self.scraper.get_page_source(profile_url)
            if not html:
                return profile_data

            soup = self.scraper.parse_html(html)

            # Extract name
            name_elem = soup.find('h1', class_=re.compile('text-heading-xlarge|inline'))
            if name_elem:
                profile_data['name'] = name_elem.get_text(strip=True)

            # Extract headline
            headline_elem = soup.find('div', class_=re.compile('text-body-medium|mt1'))
            if headline_elem:
                profile_data['headline'] = headline_elem.get_text(strip=True)

            # Extract location
            location_elem = soup.find('span', class_=re.compile('text-body-small|inline|break-words'))
            if location_elem and 'text-body-small' in str(location_elem.get('class', [])):
                profile_data['location'] = location_elem.get_text(strip=True)

            # Extract current position and company from headline
            if profile_data['headline']:
                parts = profile_data['headline'].split(' at ')
                if len(parts) == 2:
                    profile_data['current_position'] = parts[0].strip()
                    profile_data['current_company'] = parts[1].strip()
                else:
                    profile_data['current_position'] = profile_data['headline']

            # Extract about section
            about_section = soup.find('div', class_=re.compile('pv-shared-text-with-see-more'))
            if about_section:
                about_text = about_section.find('span', attrs={'aria-hidden': 'true'})
                if about_text:
                    profile_data['about'] = about_text.get_text(strip=True)

            # Try to extract emails from page content
            profile_data['emails'] = EmailExtractor.extract_from_html(html)

            # Extract experience
            profile_data['experience'] = self._extract_experience(soup)

            # Extract education
            profile_data['education'] = self._extract_education(soup)

        except Exception as e:
            print(f"Error scraping LinkedIn profile {profile_url}: {e}")

        return profile_data

    def _extract_experience(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract experience section."""
        experience = []

        try:
            exp_section = soup.find('section', attrs={'data-section': 'experience'})
            if not exp_section:
                exp_section = soup.find('div', id=re.compile('experience'))

            if exp_section:
                exp_items = exp_section.find_all('li', class_=re.compile('pvs-list__item'))

                for item in exp_items[:5]:  # Get top 5 experiences
                    exp_data = {}

                    # Extract position
                    position_elem = item.find('span', attrs={'aria-hidden': 'true'})
                    if position_elem:
                        exp_data['position'] = position_elem.get_text(strip=True)

                    # Extract company
                    company_elem = item.find('span', class_=re.compile('t-14|t-normal'))
                    if company_elem:
                        exp_data['company'] = company_elem.get_text(strip=True)

                    if exp_data:
                        experience.append(exp_data)

        except Exception as e:
            print(f"Error extracting experience: {e}")

        return experience

    def _extract_education(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract education section."""
        education = []

        try:
            edu_section = soup.find('section', attrs={'data-section': 'education'})
            if not edu_section:
                edu_section = soup.find('div', id=re.compile('education'))

            if edu_section:
                edu_items = edu_section.find_all('li', class_=re.compile('pvs-list__item'))

                for item in edu_items[:3]:  # Get top 3 education entries
                    edu_data = {}

                    # Extract school name
                    school_elem = item.find('span', attrs={'aria-hidden': 'true'})
                    if school_elem:
                        edu_data['school'] = school_elem.get_text(strip=True)

                    if edu_data:
                        education.append(edu_data)

        except Exception as e:
            print(f"Error extracting education: {e}")

        return education

    def get_profile_from_search(self, name: str, company: str = '') -> Optional[str]:
        """
        Get LinkedIn profile URL from search results.

        Args:
            name: Person's name
            company: Company name (optional)

        Returns:
            LinkedIn profile URL or None
        """
        from scrapers.search_scraper import SearchScraper

        search_scraper = SearchScraper(self.scraper)
        results = search_scraper.search_linkedin_profiles(name, company)

        if results:
            return results[0]['url']

        return None
