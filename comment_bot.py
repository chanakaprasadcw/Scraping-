"""
LinkedIn Connection Comment Bot
Automatically engages with connections' posts by adding relevant, human-like comments.

This bot runs in VISIBLE browser mode (not headless) to work like a real person.
You can manually login and let the bot take over.
"""

import os
import json
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from utils.web_scraper import WebScraper
from utils.comment_generator import CommentGenerator
from scrapers.connection_scraper import ConnectionScraper
from config import Config


class CommentBot:
    """
    Bot for engaging with LinkedIn connections' posts through comments.

    Features:
    - Visible Chrome browser (not headless) - works like a real person
    - Manual login support - you login, bot takes over
    - Continuous running mode for all-day engagement
    - Filter connections by industry or location
    - Generate and post relevant, human-like comments
    - Smart delays to mimic human behavior
    - Track commented posts to avoid duplicates
    """

    def __init__(
        self,
        headless: bool = False,
        comment_style: str = "professional",
        max_comments_per_session: int = 20,
        delay_between_comments: tuple = (120, 300),
        chrome_profile_path: Optional[str] = None
    ):
        """
        Initialize the Comment Bot.

        Args:
            headless: Run browser in headless mode (default: False for visible browser)
            comment_style: 'professional', 'casual', or 'enthusiastic'
            max_comments_per_session: Maximum comments to post per session
            delay_between_comments: (min, max) seconds between comments (default: 2-5 minutes)
            chrome_profile_path: Path to Chrome profile for persistent login
        """
        self.headless = headless
        self.comment_style = comment_style
        self.max_comments = max_comments_per_session
        self.delay_range = delay_between_comments
        self.chrome_profile_path = chrome_profile_path

        self.web_scraper = None
        self.connection_scraper = None
        self.comment_generator = None

        self.commented_posts = set()
        self.session_comments = 0
        self.session_log = []
        self.is_running = False

        self._load_comment_history()

    def __enter__(self):
        """Context manager entry."""
        self._initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def _initialize(self):
        """Initialize all components with visible browser."""
        print("\n" + "="*60)
        print("LINKEDIN COMMENT BOT")
        print("="*60)
        print("Initializing with VISIBLE Chrome browser...")
        print("The browser will open and you can see all actions.")
        print("="*60 + "\n")

        # Initialize web scraper with visible browser
        self.web_scraper = WebScraper(
            use_selenium=True,
            headless=self.headless,
            chrome_profile_path=self.chrome_profile_path
        )

        # Initialize connection scraper
        self.connection_scraper = ConnectionScraper(self.web_scraper)

        # Initialize comment generator
        self.comment_generator = CommentGenerator(style=self.comment_style)

        print("Comment Bot initialized - Chrome browser ready")

    def _load_comment_history(self):
        """Load previously commented posts to avoid duplicates."""
        history_file = os.path.join(Config.OUTPUT_DIRECTORY, "comment_history.json")
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    data = json.load(f)
                    self.commented_posts = set(data.get("commented_posts", []))
                print(f"Loaded {len(self.commented_posts)} previously commented posts")
            except:
                self.commented_posts = set()

    def _save_comment_history(self):
        """Save commented posts history."""
        os.makedirs(Config.OUTPUT_DIRECTORY, exist_ok=True)
        history_file = os.path.join(Config.OUTPUT_DIRECTORY, "comment_history.json")

        data = {
            "commented_posts": list(self.commented_posts),
            "last_updated": datetime.now().isoformat()
        }

        with open(history_file, 'w') as f:
            json.dump(data, f, indent=2)

    def wait_for_manual_login(self, timeout: int = 300) -> bool:
        """
        Wait for user to manually login to LinkedIn.
        Opens the browser and waits for user to complete login.

        Args:
            timeout: Maximum seconds to wait (default: 5 minutes)

        Returns:
            True if login detected
        """
        return self.connection_scraper.wait_for_manual_login(timeout)

    def login(self, email: str = None, password: str = None) -> bool:
        """
        Login to LinkedIn automatically.

        Args:
            email: LinkedIn email (uses env var if not provided)
            password: LinkedIn password (uses env var if not provided)

        Returns:
            True if login successful
        """
        email = email or Config.LINKEDIN_EMAIL
        password = password or Config.LINKEDIN_PASSWORD

        if not email or not password:
            print("\n" + "="*60)
            print("NO CREDENTIALS PROVIDED")
            print("="*60)
            print("You can either:")
            print("  1. Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env file")
            print("  2. Use wait_for_manual_login() to login manually")
            print("="*60 + "\n")
            return False

        return self.connection_scraper.login(email, password)

    def check_login_status(self) -> bool:
        """Check if already logged into LinkedIn (useful with Chrome profile)."""
        return self.connection_scraper.check_if_logged_in()

    def get_filtered_connections(
        self,
        industry: Optional[str] = None,
        location: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        Get connections filtered by criteria.

        Args:
            industry: Filter by industry (e.g., 'technology', 'finance')
            location: Filter by location (e.g., 'San Francisco', 'New York')
            keywords: Filter by keywords in headline
            limit: Maximum connections to fetch

        Returns:
            List of filtered connection dictionaries
        """
        print(f"Fetching connections (limit: {limit})...")

        # Fetch all connections
        connections = self.connection_scraper.fetch_connections(limit=limit)

        if not connections:
            print("No connections found")
            return []

        # Apply filters
        if industry or location or keywords:
            print(f"Applying filters - Industry: {industry}, Location: {location}, Keywords: {keywords}")
            connections = self.connection_scraper.filter_connections(
                connections,
                industry=industry,
                location=location,
                keywords=keywords
            )
            print(f"Found {len(connections)} matching connections")

        return connections

    def engage_with_connections(
        self,
        industry: Optional[str] = None,
        location: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        max_connections: int = 10,
        posts_per_connection: int = 2,
        dry_run: bool = False
    ) -> Dict:
        """
        Main method to engage with connections' posts.

        Args:
            industry: Filter connections by industry
            location: Filter connections by location
            keywords: Filter connections by headline keywords
            max_connections: Maximum connections to engage with
            posts_per_connection: Maximum posts to comment on per connection
            dry_run: If True, don't actually post comments (for testing)

        Returns:
            Summary dictionary of the engagement session
        """
        if not self.connection_scraper.is_logged_in:
            print("Please login first using the login() method")
            return {"error": "Not logged in"}

        session_start = datetime.now()
        results = {
            "started_at": session_start.isoformat(),
            "connections_processed": 0,
            "posts_found": 0,
            "comments_added": 0,
            "comments_skipped": 0,
            "errors": [],
            "details": []
        }

        # Get filtered connections
        connections = self.get_filtered_connections(
            industry=industry,
            location=location,
            keywords=keywords,
            limit=max_connections * 2  # Fetch extra in case some don't have posts
        )

        if not connections:
            results["error"] = "No connections found matching criteria"
            return results

        # Shuffle connections for more natural engagement pattern
        random.shuffle(connections)

        print(f"\n{'='*50}")
        print("Starting engagement session")
        print(f"Connections to process: {min(len(connections), max_connections)}")
        print(f"Max comments per session: {self.max_comments}")
        print(f"Dry run: {dry_run}")
        print(f"{'='*50}\n")

        for connection in connections[:max_connections]:
            # Check session limits
            if self.session_comments >= self.max_comments:
                print(f"\nReached maximum comments ({self.max_comments}) for this session")
                break

            connection_result = self._engage_with_connection(
                connection,
                max_posts=posts_per_connection,
                dry_run=dry_run
            )

            results["connections_processed"] += 1
            results["posts_found"] += connection_result["posts_found"]
            results["comments_added"] += connection_result["comments_added"]
            results["comments_skipped"] += connection_result["comments_skipped"]
            results["details"].append(connection_result)

            if connection_result["errors"]:
                results["errors"].extend(connection_result["errors"])

            # Random delay between connections
            if self.session_comments < self.max_comments:
                delay = random.uniform(30, 60)
                print(f"Waiting {delay:.0f}s before next connection...")
                time.sleep(delay)

        # Save session results
        results["ended_at"] = datetime.now().isoformat()
        results["duration_seconds"] = (datetime.now() - session_start).total_seconds()

        self._save_session_log(results)
        self._save_comment_history()

        # Print summary
        self._print_session_summary(results)

        return results

    def _engage_with_connection(
        self,
        connection: Dict,
        max_posts: int = 2,
        dry_run: bool = False
    ) -> Dict:
        """
        Engage with a single connection's posts.

        Args:
            connection: Connection dictionary
            max_posts: Maximum posts to comment on
            dry_run: If True, don't actually post comments

        Returns:
            Result dictionary for this connection
        """
        result = {
            "name": connection.get("name", "Unknown"),
            "profile_url": connection.get("profile_url", ""),
            "posts_found": 0,
            "comments_added": 0,
            "comments_skipped": 0,
            "errors": [],
            "comments": []
        }

        print(f"\n--- Processing: {result['name']} ---")
        print(f"Industry: {connection.get('industry', 'Unknown')}")
        print(f"Headline: {connection.get('headline', '')[:50]}...")

        try:
            # Get connection's posts
            posts = self.connection_scraper.get_connection_posts(
                connection.get("profile_url", ""),
                max_posts=max_posts + 2  # Fetch extra in case some were already commented
            )

            result["posts_found"] = len(posts)

            if not posts:
                print(f"No recent posts found for {result['name']}")
                return result

            print(f"Found {len(posts)} posts")

            # Process each post
            for post in posts:
                if self.session_comments >= self.max_comments:
                    break

                if result["comments_added"] >= max_posts:
                    break

                # Skip if already commented
                post_id = post.get("post_id", post.get("content", "")[:100])
                if post_id in self.commented_posts:
                    result["comments_skipped"] += 1
                    continue

                # Skip posts with no content
                if not post.get("content"):
                    continue

                # Generate comment
                comment = self.comment_generator.generate_contextual_comment(
                    post.get("content", "")
                )

                # Validate comment
                if not self.comment_generator.validate_comment(comment):
                    comment = self.comment_generator.generate_comment(
                        post.get("content", "")
                    )

                print(f"\nPost: {post.get('content', '')[:80]}...")
                print(f"Generated comment: {comment}")

                if dry_run:
                    print("[DRY RUN - Comment not posted]")
                    result["comments_added"] += 1
                    result["comments"].append({
                        "post_content": post.get("content", "")[:200],
                        "comment": comment,
                        "status": "dry_run"
                    })
                else:
                    # Add random delay before commenting
                    delay = random.uniform(*self.delay_range)
                    print(f"Waiting {delay:.0f}s before posting comment...")
                    time.sleep(delay)

                    # Navigate back to activity page and find the post
                    # This is a simplified version - in production, you'd need
                    # to maintain reference to the post element
                    success = self._post_comment_to_feed(
                        connection.get("profile_url", ""),
                        post,
                        comment
                    )

                    if success:
                        result["comments_added"] += 1
                        self.session_comments += 1
                        self.commented_posts.add(post_id)
                        result["comments"].append({
                            "post_content": post.get("content", "")[:200],
                            "comment": comment,
                            "status": "posted"
                        })
                        print("Comment posted successfully!")
                    else:
                        result["errors"].append(f"Failed to post comment on {result['name']}'s post")

        except Exception as e:
            error_msg = f"Error engaging with {result['name']}: {str(e)}"
            print(error_msg)
            result["errors"].append(error_msg)

        return result

    def _post_comment_to_feed(
        self,
        profile_url: str,
        post: Dict,
        comment: str
    ) -> bool:
        """
        Post a comment to a specific post in the feed.

        Args:
            profile_url: Connection's profile URL
            post: Post dictionary
            comment: Comment text to post

        Returns:
            True if comment was posted successfully
        """
        driver = self.web_scraper.get_driver()

        try:
            # Navigate to activity page
            activity_url = profile_url.rstrip('/') + "/recent-activity/all/"
            driver.get(activity_url)
            time.sleep(random.uniform(2, 4))

            # Find the post by matching content
            post_elements = driver.find_elements(
                "css selector",
                "div.feed-shared-update-v2"
            )

            target_post = None
            post_content = post.get("content", "")[:50]

            for elem in post_elements:
                try:
                    elem_text = elem.text
                    if post_content and post_content in elem_text:
                        target_post = elem
                        break
                except:
                    continue

            if not target_post:
                print("Could not locate the target post")
                return False

            # Use the connection scraper to add comment
            return self.connection_scraper.add_comment_to_post(target_post, comment)

        except Exception as e:
            print(f"Error posting comment: {str(e)}")
            return False

    def _save_session_log(self, results: Dict):
        """Save session log to file."""
        os.makedirs(Config.OUTPUT_DIRECTORY, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(Config.OUTPUT_DIRECTORY, f"comment_session_{timestamp}.json")

        with open(log_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\nSession log saved to: {log_file}")

    def _print_session_summary(self, results: Dict):
        """Print session summary."""
        print(f"\n{'='*50}")
        print("SESSION SUMMARY")
        print(f"{'='*50}")
        print(f"Duration: {results.get('duration_seconds', 0):.0f} seconds")
        print(f"Connections processed: {results.get('connections_processed', 0)}")
        print(f"Posts found: {results.get('posts_found', 0)}")
        print(f"Comments added: {results.get('comments_added', 0)}")
        print(f"Comments skipped (duplicates): {results.get('comments_skipped', 0)}")
        if results.get('errors'):
            print(f"Errors: {len(results['errors'])}")
        print(f"{'='*50}\n")

    def run_continuous(
        self,
        industry: Optional[str] = None,
        location: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        comments_per_hour: int = 3,
        run_hours: int = 8,
        active_hours: tuple = (9, 17),
        dry_run: bool = False
    ) -> Dict:
        """
        Run the bot continuously throughout the day like a real person.

        Args:
            industry: Filter connections by industry
            location: Filter connections by location
            keywords: Filter connections by headline keywords
            comments_per_hour: Target comments per hour (default: 3)
            run_hours: Total hours to run (default: 8)
            active_hours: Tuple of (start_hour, end_hour) for active commenting (default: 9am-5pm)
            dry_run: If True, don't actually post comments

        Returns:
            Summary dictionary of all sessions
        """
        if not self.connection_scraper.is_logged_in:
            print("Please login first!")
            return {"error": "Not logged in"}

        self.is_running = True
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=run_hours)

        total_results = {
            "mode": "continuous",
            "started_at": start_time.isoformat(),
            "comments_per_hour_target": comments_per_hour,
            "total_comments": 0,
            "total_connections": 0,
            "sessions": []
        }

        print("\n" + "="*60)
        print("CONTINUOUS MODE ACTIVATED")
        print("="*60)
        print(f"Running for {run_hours} hours")
        print(f"Target: ~{comments_per_hour} comments per hour")
        print(f"Active hours: {active_hours[0]}:00 - {active_hours[1]}:00")
        print(f"Estimated end time: {end_time.strftime('%H:%M')}")
        print("\nPress Ctrl+C to stop at any time")
        print("="*60 + "\n")

        try:
            while datetime.now() < end_time and self.is_running:
                current_hour = datetime.now().hour

                # Check if within active hours
                if not (active_hours[0] <= current_hour < active_hours[1]):
                    wait_minutes = self._minutes_until_active(active_hours[0])
                    print(f"\nOutside active hours. Waiting {wait_minutes} minutes...")
                    self._human_wait(wait_minutes * 60)
                    continue

                # Calculate delay for target comments per hour
                # Spread comments randomly across the hour
                base_delay = 3600 / comments_per_hour  # seconds between comments
                delay_variance = base_delay * 0.4  # 40% variance
                next_delay = random.uniform(
                    base_delay - delay_variance,
                    base_delay + delay_variance
                )

                # Engage with one connection
                connections = self.get_filtered_connections(
                    industry=industry,
                    location=location,
                    keywords=keywords,
                    limit=20
                )

                if connections:
                    # Pick a random connection
                    connection = random.choice(connections)

                    result = self._engage_with_connection(
                        connection,
                        max_posts=1,
                        dry_run=dry_run
                    )

                    total_results["total_connections"] += 1
                    total_results["total_comments"] += result["comments_added"]
                    total_results["sessions"].append({
                        "time": datetime.now().isoformat(),
                        "connection": result["name"],
                        "comments": result["comments_added"]
                    })

                    self._save_comment_history()

                # Human-like wait with random variation
                print(f"\nNext action in ~{next_delay/60:.1f} minutes...")
                self._human_wait(next_delay)

        except KeyboardInterrupt:
            print("\n\nStopping continuous mode (Ctrl+C pressed)...")
            self.is_running = False

        total_results["ended_at"] = datetime.now().isoformat()
        total_results["actual_duration_hours"] = (
            datetime.now() - start_time
        ).total_seconds() / 3600

        self._save_session_log(total_results)
        self._print_continuous_summary(total_results)

        return total_results

    def _minutes_until_active(self, start_hour: int) -> int:
        """Calculate minutes until active hours begin."""
        now = datetime.now()
        if now.hour >= start_hour:
            # Next day
            target = now.replace(hour=start_hour, minute=0, second=0) + timedelta(days=1)
        else:
            target = now.replace(hour=start_hour, minute=0, second=0)
        return int((target - now).total_seconds() / 60)

    def _human_wait(self, seconds: float):
        """Wait with occasional small activities to appear human."""
        start = time.time()
        while time.time() - start < seconds:
            # Occasionally "do something" (scroll, move mouse simulation via small waits)
            chunk = min(random.uniform(30, 90), seconds - (time.time() - start))
            if chunk <= 0:
                break
            time.sleep(chunk)

            # Periodically show we're still alive
            remaining = seconds - (time.time() - start)
            if remaining > 60:
                print(f"  ... waiting ({remaining/60:.1f} min remaining)")

    def _print_continuous_summary(self, results: Dict):
        """Print continuous mode summary."""
        print(f"\n{'='*60}")
        print("CONTINUOUS MODE SUMMARY")
        print(f"{'='*60}")
        print(f"Duration: {results.get('actual_duration_hours', 0):.1f} hours")
        print(f"Total connections engaged: {results.get('total_connections', 0)}")
        print(f"Total comments added: {results.get('total_comments', 0)}")
        if results.get('actual_duration_hours', 0) > 0:
            rate = results.get('total_comments', 0) / results.get('actual_duration_hours', 1)
            print(f"Average comments per hour: {rate:.1f}")
        print(f"{'='*60}\n")

    def preview_comments(
        self,
        industry: Optional[str] = None,
        location: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        num_connections: int = 3
    ) -> List[Dict]:
        """
        Preview comments that would be generated (without posting).

        Args:
            industry: Filter connections by industry
            location: Filter connections by location
            keywords: Filter connections by headline keywords
            num_connections: Number of connections to preview

        Returns:
            List of preview dictionaries
        """
        if not self.connection_scraper.is_logged_in:
            print("Please login first using the login() method")
            return []

        previews = []

        connections = self.get_filtered_connections(
            industry=industry,
            location=location,
            keywords=keywords,
            limit=num_connections
        )

        for connection in connections:
            preview = {
                "name": connection.get("name"),
                "headline": connection.get("headline"),
                "posts": []
            }

            posts = self.connection_scraper.get_connection_posts(
                connection.get("profile_url", ""),
                max_posts=2
            )

            for post in posts:
                if post.get("content"):
                    comment = self.comment_generator.generate_contextual_comment(
                        post.get("content", "")
                    )
                    preview["posts"].append({
                        "content": post.get("content", "")[:200],
                        "generated_comment": comment
                    })

            previews.append(preview)

        return previews

    def set_comment_style(self, style: str):
        """
        Change the comment style.

        Args:
            style: 'professional', 'casual', or 'enthusiastic'
        """
        self.comment_style = style
        if self.comment_generator:
            self.comment_generator.set_style(style)
        print(f"Comment style set to: {style}")

    def close(self):
        """Clean up resources."""
        self._save_comment_history()

        if self.connection_scraper:
            self.connection_scraper.close()

        if self.web_scraper:
            self.web_scraper.close()

        print("Comment Bot closed")


def run_comment_bot(
    email: str = None,
    password: str = None,
    industry: str = None,
    location: str = None,
    keywords: List[str] = None,
    max_connections: int = 5,
    max_comments: int = 10,
    comment_style: str = "professional",
    dry_run: bool = True,
    headless: bool = False
) -> Dict:
    """
    Convenience function to run the comment bot.

    Args:
        email: LinkedIn email
        password: LinkedIn password
        industry: Filter by industry
        location: Filter by location
        keywords: Filter by headline keywords
        max_connections: Max connections to engage with
        max_comments: Max comments per session
        comment_style: 'professional', 'casual', or 'enthusiastic'
        dry_run: If True, don't post comments
        headless: Run browser in headless mode

    Returns:
        Session results dictionary
    """
    with CommentBot(
        headless=headless,
        comment_style=comment_style,
        max_comments_per_session=max_comments
    ) as bot:
        if not bot.login(email, password):
            return {"error": "Login failed"}

        return bot.engage_with_connections(
            industry=industry,
            location=location,
            keywords=keywords,
            max_connections=max_connections,
            dry_run=dry_run
        )


if __name__ == "__main__":
    # Example usage
    print("LinkedIn Connection Comment Bot")
    print("="*50)
    print("\nUsage:")
    print("  from comment_bot import CommentBot")
    print("")
    print("  with CommentBot(headless=False) as bot:")
    print("      bot.login('your@email.com', 'password')")
    print("      bot.engage_with_connections(")
    print("          industry='technology',")
    print("          max_connections=5,")
    print("          dry_run=True  # Set to False to actually post")
    print("      )")
