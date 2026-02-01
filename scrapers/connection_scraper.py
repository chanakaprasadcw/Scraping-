"""
LinkedIn Connection Scraper
Fetches and filters existing LinkedIn connections by industry or location.
"""

import time
import random
from typing import List, Dict, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class ConnectionScraper:
    """Scraper for LinkedIn connections with filtering capabilities."""

    def __init__(self, web_scraper):
        """
        Initialize the connection scraper.

        Args:
            web_scraper: WebScraper instance with active browser session
        """
        self.web_scraper = web_scraper
        self.driver = None
        self.connections_url = "https://www.linkedin.com/mynetwork/invite-connect/connections/"
        self.is_logged_in = False

    def _get_driver(self):
        """Get or initialize the Selenium driver."""
        if self.driver is None:
            self.driver = self.web_scraper.get_driver()
        return self.driver

    def login(self, email: str, password: str) -> bool:
        """
        Login to LinkedIn.

        Args:
            email: LinkedIn email
            password: LinkedIn password

        Returns:
            True if login successful, False otherwise
        """
        driver = self._get_driver()

        try:
            driver.get("https://www.linkedin.com/login")
            time.sleep(2)

            # Fill email
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.clear()
            email_field.send_keys(email)

            # Fill password
            password_field = driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys(password)

            # Click login button
            login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()

            # Wait for login to complete
            time.sleep(3)

            # Check if login was successful
            if "feed" in driver.current_url or "mynetwork" in driver.current_url:
                self.is_logged_in = True
                print("Successfully logged in to LinkedIn")
                return True
            else:
                print("Login may have failed - check for security verification")
                return False

        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False

    def _random_delay(self, min_sec: float = 1.0, max_sec: float = 3.0):
        """Add random delay to mimic human behavior."""
        time.sleep(random.uniform(min_sec, max_sec))

    def fetch_connections(self, limit: int = 50) -> List[Dict]:
        """
        Fetch connections from LinkedIn.

        Args:
            limit: Maximum number of connections to fetch

        Returns:
            List of connection dictionaries
        """
        if not self.is_logged_in:
            print("Please login first using the login() method")
            return []

        driver = self._get_driver()
        connections = []

        try:
            driver.get(self.connections_url)
            self._random_delay(2, 4)

            # Scroll to load more connections
            last_height = driver.execute_script("return document.body.scrollHeight")
            scroll_attempts = 0
            max_scrolls = limit // 10 + 3  # Estimate scrolls needed

            while len(connections) < limit and scroll_attempts < max_scrolls:
                # Find connection cards
                connection_cards = driver.find_elements(
                    By.CSS_SELECTOR,
                    "li.mn-connection-card"
                )

                for card in connection_cards:
                    if len(connections) >= limit:
                        break

                    try:
                        connection = self._parse_connection_card(card)
                        if connection and connection not in connections:
                            connections.append(connection)
                    except Exception as e:
                        continue

                # Scroll down
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self._random_delay(1.5, 2.5)

                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    scroll_attempts += 1
                else:
                    scroll_attempts = 0
                    last_height = new_height

            print(f"Fetched {len(connections)} connections")
            return connections

        except Exception as e:
            print(f"Error fetching connections: {str(e)}")
            return connections

    def _parse_connection_card(self, card) -> Optional[Dict]:
        """
        Parse a connection card element.

        Args:
            card: Selenium WebElement for connection card

        Returns:
            Dictionary with connection info or None
        """
        try:
            # Get profile link and name
            profile_link = card.find_element(
                By.CSS_SELECTOR,
                "a.mn-connection-card__link"
            )
            profile_url = profile_link.get_attribute("href")

            name_elem = card.find_element(
                By.CSS_SELECTOR,
                "span.mn-connection-card__name"
            )
            name = name_elem.text.strip()

            # Get occupation/headline
            occupation = ""
            try:
                occupation_elem = card.find_element(
                    By.CSS_SELECTOR,
                    "span.mn-connection-card__occupation"
                )
                occupation = occupation_elem.text.strip()
            except NoSuchElementException:
                pass

            return {
                "name": name,
                "profile_url": profile_url,
                "headline": occupation,
                "industry": self._extract_industry(occupation),
                "location": ""  # Will be fetched from profile if needed
            }

        except Exception:
            return None

    def _extract_industry(self, headline: str) -> str:
        """
        Extract industry from headline.

        Args:
            headline: LinkedIn headline text

        Returns:
            Extracted industry or empty string
        """
        # Industry keywords mapping
        industry_keywords = {
            "technology": ["software", "developer", "engineer", "tech", "it ", "data", "ai", "ml", "cloud", "devops", "programming"],
            "finance": ["finance", "banking", "investment", "trading", "fintech", "accounting", "cfo", "financial"],
            "healthcare": ["health", "medical", "doctor", "nurse", "pharma", "biotech", "clinical", "hospital"],
            "marketing": ["marketing", "digital marketing", "seo", "content", "brand", "advertising", "social media"],
            "sales": ["sales", "business development", "account executive", "revenue", "bd "],
            "consulting": ["consultant", "consulting", "advisory", "strategy"],
            "education": ["teacher", "professor", "education", "academic", "university", "school"],
            "legal": ["lawyer", "attorney", "legal", "law firm", "counsel"],
            "real estate": ["real estate", "property", "realtor", "broker"],
            "manufacturing": ["manufacturing", "production", "factory", "operations"],
            "retail": ["retail", "ecommerce", "e-commerce", "store", "shop"],
            "media": ["media", "journalist", "editor", "writer", "content creator", "influencer"],
            "hr": ["hr ", "human resources", "recruiter", "talent", "people operations"],
            "design": ["designer", "ux", "ui", "graphic", "creative", "art director"],
            "startup": ["founder", "co-founder", "entrepreneur", "startup", "ceo", "cto"]
        }

        headline_lower = headline.lower()
        for industry, keywords in industry_keywords.items():
            for keyword in keywords:
                if keyword in headline_lower:
                    return industry

        return "other"

    def filter_connections(
        self,
        connections: List[Dict],
        industry: Optional[str] = None,
        location: Optional[str] = None,
        keywords: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Filter connections by industry, location, or keywords.

        Args:
            connections: List of connection dictionaries
            industry: Industry to filter by
            location: Location to filter by
            keywords: List of keywords to match in headline

        Returns:
            Filtered list of connections
        """
        filtered = connections

        if industry:
            industry_lower = industry.lower()
            filtered = [
                c for c in filtered
                if industry_lower in c.get("industry", "").lower() or
                   industry_lower in c.get("headline", "").lower()
            ]

        if location:
            location_lower = location.lower()
            filtered = [
                c for c in filtered
                if location_lower in c.get("location", "").lower() or
                   location_lower in c.get("headline", "").lower()
            ]

        if keywords:
            keywords_lower = [k.lower() for k in keywords]
            filtered = [
                c for c in filtered
                if any(
                    kw in c.get("headline", "").lower()
                    for kw in keywords_lower
                )
            ]

        return filtered

    def get_connection_profile_details(self, profile_url: str) -> Dict:
        """
        Get detailed profile information for a connection.

        Args:
            profile_url: LinkedIn profile URL

        Returns:
            Dictionary with detailed profile info
        """
        driver = self._get_driver()
        profile_data = {
            "url": profile_url,
            "name": "",
            "headline": "",
            "location": "",
            "industry": "",
            "about": "",
            "current_company": ""
        }

        try:
            driver.get(profile_url)
            self._random_delay(2, 4)

            # Get name
            try:
                name_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1.text-heading-xlarge"))
                )
                profile_data["name"] = name_elem.text.strip()
            except:
                pass

            # Get headline
            try:
                headline_elem = driver.find_element(
                    By.CSS_SELECTOR,
                    "div.text-body-medium"
                )
                profile_data["headline"] = headline_elem.text.strip()
                profile_data["industry"] = self._extract_industry(profile_data["headline"])
            except:
                pass

            # Get location
            try:
                location_elem = driver.find_element(
                    By.CSS_SELECTOR,
                    "span.text-body-small.inline"
                )
                profile_data["location"] = location_elem.text.strip()
            except:
                pass

            # Get about section
            try:
                about_section = driver.find_element(
                    By.CSS_SELECTOR,
                    "section.pv-about-section div.display-flex span[aria-hidden='true']"
                )
                profile_data["about"] = about_section.text.strip()
            except:
                pass

            return profile_data

        except Exception as e:
            print(f"Error fetching profile details: {str(e)}")
            return profile_data

    def get_connection_posts(self, profile_url: str, max_posts: int = 5) -> List[Dict]:
        """
        Get recent posts from a connection's activity.

        Args:
            profile_url: LinkedIn profile URL
            max_posts: Maximum number of posts to fetch

        Returns:
            List of post dictionaries
        """
        driver = self._get_driver()
        posts = []

        # Navigate to activity/posts section
        activity_url = profile_url.rstrip('/') + "/recent-activity/all/"

        try:
            driver.get(activity_url)
            self._random_delay(2, 4)

            # Wait for posts to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed-shared-update-v2"))
            )

            # Find post elements
            post_elements = driver.find_elements(
                By.CSS_SELECTOR,
                "div.feed-shared-update-v2"
            )

            for post_elem in post_elements[:max_posts]:
                try:
                    post = self._parse_post(post_elem)
                    if post and post.get("content"):
                        posts.append(post)
                except Exception:
                    continue

            print(f"Found {len(posts)} posts for {profile_url}")
            return posts

        except TimeoutException:
            print(f"No posts found for {profile_url}")
            return []
        except Exception as e:
            print(f"Error fetching posts: {str(e)}")
            return posts

    def _parse_post(self, post_elem) -> Optional[Dict]:
        """
        Parse a post element to extract content.

        Args:
            post_elem: Selenium WebElement for post

        Returns:
            Dictionary with post info or None
        """
        try:
            post_data = {
                "content": "",
                "post_id": "",
                "post_url": "",
                "has_image": False,
                "has_video": False,
                "engagement": {
                    "likes": 0,
                    "comments": 0
                }
            }

            # Get post content/text
            try:
                content_elem = post_elem.find_element(
                    By.CSS_SELECTOR,
                    "div.feed-shared-update-v2__description span.break-words"
                )
                post_data["content"] = content_elem.text.strip()
            except:
                # Try alternate selector
                try:
                    content_elem = post_elem.find_element(
                        By.CSS_SELECTOR,
                        "span.break-words"
                    )
                    post_data["content"] = content_elem.text.strip()
                except:
                    pass

            # Get post URN/ID for commenting
            try:
                post_data["post_id"] = post_elem.get_attribute("data-urn")
            except:
                pass

            # Check for media
            try:
                post_elem.find_element(By.CSS_SELECTOR, "img.feed-shared-image__image")
                post_data["has_image"] = True
            except:
                pass

            try:
                post_elem.find_element(By.CSS_SELECTOR, "video")
                post_data["has_video"] = True
            except:
                pass

            # Get engagement counts
            try:
                reactions = post_elem.find_element(
                    By.CSS_SELECTOR,
                    "span.social-details-social-counts__reactions-count"
                )
                post_data["engagement"]["likes"] = self._parse_count(reactions.text)
            except:
                pass

            try:
                comments = post_elem.find_element(
                    By.CSS_SELECTOR,
                    "button.social-details-social-counts__comments"
                )
                post_data["engagement"]["comments"] = self._parse_count(comments.text)
            except:
                pass

            return post_data if post_data["content"] else None

        except Exception:
            return None

    def _parse_count(self, count_str: str) -> int:
        """Parse engagement count string to integer."""
        try:
            count_str = count_str.strip().lower()
            if 'k' in count_str:
                return int(float(count_str.replace('k', '').replace(',', '')) * 1000)
            elif 'm' in count_str:
                return int(float(count_str.replace('m', '').replace(',', '')) * 1000000)
            else:
                return int(count_str.replace(',', '').split()[0])
        except:
            return 0

    def add_comment_to_post(self, post_elem, comment: str) -> bool:
        """
        Add a comment to a post.

        Args:
            post_elem: Post element or post URL
            comment: Comment text to add

        Returns:
            True if comment was added successfully
        """
        driver = self._get_driver()

        try:
            # Click comment button to open comment box
            comment_button = post_elem.find_element(
                By.CSS_SELECTOR,
                "button.comment-button, button[aria-label*='Comment']"
            )
            driver.execute_script("arguments[0].click();", comment_button)
            self._random_delay(1, 2)

            # Find comment input
            comment_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "div.comments-comment-box__form div.ql-editor, div[data-placeholder='Add a comment…']"
                ))
            )

            # Type comment with human-like delay
            comment_input.click()
            self._random_delay(0.5, 1)

            # Type character by character for more human-like behavior
            for char in comment:
                comment_input.send_keys(char)
                time.sleep(random.uniform(0.03, 0.08))

            self._random_delay(1, 2)

            # Click post button
            post_button = driver.find_element(
                By.CSS_SELECTOR,
                "button.comments-comment-box__submit-button"
            )
            driver.execute_script("arguments[0].click();", post_button)

            self._random_delay(2, 3)
            print(f"Comment added: {comment[:50]}...")
            return True

        except Exception as e:
            print(f"Error adding comment: {str(e)}")
            return False

    def close(self):
        """Close the browser session."""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
