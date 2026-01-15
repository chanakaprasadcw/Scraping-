"""Email extraction utilities."""

import re
from typing import List, Set
from email_validator import validate_email, EmailNotValidError


class EmailExtractor:
    """Extract and validate email addresses from text and web pages."""

    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Common false positive patterns to exclude
    EXCLUDE_PATTERNS = [
        r'\.png$', r'\.jpg$', r'\.jpeg$', r'\.gif$', r'\.svg$',
        r'example\.com$', r'test\.com$', r'sample\.com$',
        r'@sentry', r'@2x\.', r'@3x\.'
    ]

    @classmethod
    def extract_emails(cls, text: str, validate: bool = True) -> List[str]:
        """
        Extract email addresses from text.

        Args:
            text: Text to extract emails from
            validate: Whether to validate emails

        Returns:
            List of unique email addresses
        """
        if not text:
            return []

        # Find all potential emails
        potential_emails = re.findall(cls.EMAIL_PATTERN, text, re.IGNORECASE)

        # Remove duplicates and convert to lowercase
        emails: Set[str] = {email.lower() for email in potential_emails}

        # Filter out false positives
        filtered_emails = []
        for email in emails:
            if cls._is_valid_email(email, validate):
                filtered_emails.append(email)

        return filtered_emails

    @classmethod
    def _is_valid_email(cls, email: str, validate: bool = True) -> bool:
        """
        Check if email is valid and not a false positive.

        Args:
            email: Email address to validate
            validate: Whether to perform full validation

        Returns:
            True if email is valid
        """
        # Check exclusion patterns
        for pattern in cls.EXCLUDE_PATTERNS:
            if re.search(pattern, email, re.IGNORECASE):
                return False

        # Perform full validation if requested
        if validate:
            try:
                validate_email(email)
                return True
            except EmailNotValidError:
                return False

        return True

    @classmethod
    def extract_from_html(cls, html: str, validate: bool = True) -> List[str]:
        """
        Extract emails from HTML content.

        Args:
            html: HTML content
            validate: Whether to validate emails

        Returns:
            List of unique email addresses
        """
        # Remove HTML tags but keep text content
        text = re.sub(r'<[^>]+>', ' ', html)
        # Decode HTML entities
        text = text.replace('&at;', '@').replace('&#64;', '@')
        text = text.replace('&dot;', '.').replace('&#46;', '.')

        return cls.extract_emails(text, validate)
