"""Configuration settings for the lead scraping tool."""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for scraping settings."""

    # Search settings
    SEARCH_ENGINE = os.getenv('SEARCH_ENGINE', 'google')
    MAX_RESULTS_PER_SEARCH = int(os.getenv('MAX_RESULTS_PER_SEARCH', '10'))

    # Scraping settings
    HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'true').lower() == 'true'
    TIMEOUT = int(os.getenv('TIMEOUT', '30'))
    DELAY_BETWEEN_REQUESTS = int(os.getenv('DELAY_BETWEEN_REQUESTS', '2'))

    # Output settings
    OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT', 'csv')
    OUTPUT_DIRECTORY = os.getenv('OUTPUT_DIRECTORY', './output')

    # LinkedIn settings
    LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL', '')
    LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD', '')

    # User agents
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
    ]

    # Email regex pattern
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
