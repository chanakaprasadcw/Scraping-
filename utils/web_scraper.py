"""Web scraping utilities using Selenium and BeautifulSoup."""

import os
import time
import random
from typing import Optional, Dict, List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent


class WebScraper:
    """Web scraping utility class."""

    def __init__(
        self,
        headless: bool = False,
        timeout: int = 30,
        use_selenium: bool = True,
        chrome_profile_path: Optional[str] = None,
        window_size: tuple = (1280, 900)
    ):
        """
        Initialize web scraper.

        Args:
            headless: Run browser in headless mode (default: False for visible browser)
            timeout: Page load timeout in seconds
            use_selenium: Whether to use Selenium (default: True)
            chrome_profile_path: Path to Chrome user profile for persistent sessions
            window_size: Browser window size (width, height)
        """
        self.headless = headless
        self.timeout = timeout
        self.use_selenium = use_selenium
        self.chrome_profile_path = chrome_profile_path
        self.window_size = window_size
        self.driver: Optional[webdriver.Chrome] = None
        self.ua = UserAgent()

    def init_driver(self):
        """Initialize Selenium WebDriver with visible browser."""
        if self.driver:
            return

        chrome_options = Options()

        # Headless mode - OFF by default for visible automation
        if self.headless:
            chrome_options.add_argument('--headless=new')

        # Use Chrome profile for persistent login
        if self.chrome_profile_path:
            chrome_options.add_argument(f'--user-data-dir={self.chrome_profile_path}')
        else:
            # Create a default profile directory for session persistence
            default_profile = os.path.join(os.path.expanduser('~'), '.comment_bot_chrome_profile')
            if not os.path.exists(default_profile):
                os.makedirs(default_profile)
            chrome_options.add_argument(f'--user-data-dir={default_profile}')

        # Essential options
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Anti-detection settings
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Window size
        chrome_options.add_argument(f'--window-size={self.window_size[0]},{self.window_size[1]}')

        # Start maximized for better visibility
        chrome_options.add_argument('--start-maximized')

        # Disable infobars
        chrome_options.add_argument('--disable-infobars')

        # Set user agent
        chrome_options.add_argument(f'user-agent={self.ua.chrome}')

        # Suppress logging
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(self.timeout)

        # Additional anti-detection via JavaScript
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            '''
        })

    def get_driver(self):
        """Get the Selenium WebDriver instance."""
        self.init_driver()
        return self.driver

    def get_page_source(self, url: str, wait_for_element: Optional[str] = None) -> str:
        """
        Get page source using Selenium.

        Args:
            url: URL to fetch
            wait_for_element: CSS selector to wait for

        Returns:
            Page HTML source
        """
        self.init_driver()

        try:
            self.driver.get(url)

            if wait_for_element:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, wait_for_element))
                )

            time.sleep(random.uniform(1, 3))
            return self.driver.page_source
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""

    def get_page_with_requests(self, url: str) -> str:
        """
        Get page source using requests (faster for simple pages).

        Args:
            url: URL to fetch

        Returns:
            Page HTML source
        """
        try:
            headers = {
                'User-Agent': self.ua.random,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }

            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""

    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML with BeautifulSoup.

        Args:
            html: HTML content

        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html, 'lxml')

    def close(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
