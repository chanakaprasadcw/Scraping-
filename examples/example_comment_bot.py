#!/usr/bin/env python3
"""
Example: LinkedIn Connection Comment Bot

This example demonstrates how to use the Comment Bot to engage
with your LinkedIn connections' posts automatically.

IMPORTANT:
- Always start with preview or dry-run mode
- Use responsibly and don't spam your connections
- LinkedIn may rate-limit or restrict accounts that post too frequently
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from comment_bot import CommentBot


def example_preview_comments():
    """
    Example 1: Preview mode
    See what comments would be generated without posting anything.
    """
    print("\n" + "="*60)
    print("Example 1: Preview Mode")
    print("="*60)

    with CommentBot(headless=False, comment_style="professional") as bot:
        # Login (use environment variables or pass directly)
        email = os.getenv("LINKEDIN_EMAIL")
        password = os.getenv("LINKEDIN_PASSWORD")

        if not bot.login(email, password):
            print("Login failed!")
            return

        # Preview comments for technology connections
        previews = bot.preview_comments(
            industry="technology",
            num_connections=2
        )

        for preview in previews:
            print(f"\nConnection: {preview['name']}")
            print(f"Headline: {preview['headline']}")
            for post in preview['posts']:
                print(f"  Post: {post['content'][:100]}...")
                print(f"  Comment: {post['generated_comment']}")


def example_dry_run():
    """
    Example 2: Dry run mode
    Simulates the full engagement process without posting.
    """
    print("\n" + "="*60)
    print("Example 2: Dry Run Mode")
    print("="*60)

    with CommentBot(
        headless=False,
        comment_style="professional",
        max_comments_per_session=5
    ) as bot:
        email = os.getenv("LINKEDIN_EMAIL")
        password = os.getenv("LINKEDIN_PASSWORD")

        if not bot.login(email, password):
            print("Login failed!")
            return

        # Dry run - engage with technology connections
        results = bot.engage_with_connections(
            industry="technology",
            max_connections=3,
            posts_per_connection=2,
            dry_run=True  # No comments will be posted
        )

        print(f"\nDry run results:")
        print(f"  Connections processed: {results['connections_processed']}")
        print(f"  Posts found: {results['posts_found']}")
        print(f"  Comments that would be added: {results['comments_added']}")


def example_filter_by_location():
    """
    Example 3: Filter connections by location
    """
    print("\n" + "="*60)
    print("Example 3: Filter by Location")
    print("="*60)

    with CommentBot(headless=False) as bot:
        email = os.getenv("LINKEDIN_EMAIL")
        password = os.getenv("LINKEDIN_PASSWORD")

        if not bot.login(email, password):
            return

        # Get connections in San Francisco
        connections = bot.get_filtered_connections(
            location="San Francisco",
            limit=20
        )

        print(f"\nFound {len(connections)} connections in San Francisco:")
        for conn in connections[:5]:
            print(f"  - {conn['name']}: {conn['headline'][:50]}...")


def example_filter_by_keywords():
    """
    Example 4: Filter connections by headline keywords
    """
    print("\n" + "="*60)
    print("Example 4: Filter by Keywords")
    print("="*60)

    with CommentBot(headless=False) as bot:
        email = os.getenv("LINKEDIN_EMAIL")
        password = os.getenv("LINKEDIN_PASSWORD")

        if not bot.login(email, password):
            return

        # Get connections who are founders or CEOs
        connections = bot.get_filtered_connections(
            keywords=["founder", "ceo", "co-founder"],
            limit=20
        )

        print(f"\nFound {len(connections)} founders/CEOs:")
        for conn in connections[:5]:
            print(f"  - {conn['name']}: {conn['headline'][:50]}...")


def example_casual_style():
    """
    Example 5: Use casual comment style
    """
    print("\n" + "="*60)
    print("Example 5: Casual Comment Style")
    print("="*60)

    with CommentBot(
        headless=False,
        comment_style="casual"  # More relaxed tone
    ) as bot:
        email = os.getenv("LINKEDIN_EMAIL")
        password = os.getenv("LINKEDIN_PASSWORD")

        if not bot.login(email, password):
            return

        # Preview with casual style
        previews = bot.preview_comments(
            industry="startup",
            num_connections=2
        )

        for preview in previews:
            print(f"\n{preview['name']}:")
            for post in preview['posts']:
                print(f"  Comment: {post['generated_comment']}")


def example_actual_engagement():
    """
    Example 6: Actually post comments (USE WITH CAUTION)

    WARNING: This will post real comments to your connections' posts.
    Always test with dry_run=True first!
    """
    print("\n" + "="*60)
    print("Example 6: Actual Engagement (LIVE MODE)")
    print("="*60)
    print("\nWARNING: This will post real comments!")
    print("Press Ctrl+C to cancel...")

    import time
    time.sleep(5)

    with CommentBot(
        headless=False,
        comment_style="professional",
        max_comments_per_session=3,  # Keep it low
        delay_between_comments=(90, 180)  # Longer delays for safety
    ) as bot:
        email = os.getenv("LINKEDIN_EMAIL")
        password = os.getenv("LINKEDIN_PASSWORD")

        if not bot.login(email, password):
            return

        # Engage with a small number of connections
        results = bot.engage_with_connections(
            industry="technology",
            max_connections=2,
            posts_per_connection=1,
            dry_run=False  # LIVE MODE
        )

        print(f"\nEngagement complete!")
        print(f"  Comments posted: {results['comments_added']}")


if __name__ == "__main__":
    print("LinkedIn Connection Comment Bot - Examples")
    print("="*60)
    print("\nAvailable examples:")
    print("  1. Preview comments (safe)")
    print("  2. Dry run (safe)")
    print("  3. Filter by location")
    print("  4. Filter by keywords")
    print("  5. Casual style comments")
    print("  6. Actual engagement (LIVE - use with caution)")

    choice = input("\nEnter example number (1-6): ").strip()

    examples = {
        "1": example_preview_comments,
        "2": example_dry_run,
        "3": example_filter_by_location,
        "4": example_filter_by_keywords,
        "5": example_casual_style,
        "6": example_actual_engagement,
    }

    if choice in examples:
        examples[choice]()
    else:
        print("Invalid choice. Please enter 1-6.")
