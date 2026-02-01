#!/usr/bin/env python3
"""
LinkedIn Connection Comment Bot - CLI Entry Point

Automatically engages with your LinkedIn connections' posts by adding
short, relevant, and human-like comments.

Usage:
    # Preview mode (recommended for first run)
    python comment_bot_main.py --industry technology --preview

    # Dry run (shows what would happen without posting)
    python comment_bot_main.py --industry technology --dry-run

    # Actual engagement
    python comment_bot_main.py --industry technology --max-connections 5

    # Filter by location
    python comment_bot_main.py --location "San Francisco" --max-connections 3

    # Multiple filters
    python comment_bot_main.py --industry technology --keywords "founder,ceo" --style casual
"""

import argparse
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from comment_bot import CommentBot, run_comment_bot


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="LinkedIn Connection Comment Bot - Engage with your network's posts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview comments for technology connections
  python comment_bot_main.py --industry technology --preview

  # Dry run - simulate commenting on finance connections
  python comment_bot_main.py --industry finance --dry-run

  # Actually post comments to startup founders
  python comment_bot_main.py --keywords founder,startup --max-connections 5

  # Casual style comments for local connections
  python comment_bot_main.py --location "New York" --style casual --max-connections 3

  # Using config file
  python comment_bot_main.py --config comment_config.json
        """
    )

    # Authentication
    auth_group = parser.add_argument_group("Authentication")
    auth_group.add_argument(
        "--email",
        type=str,
        help="LinkedIn email (or set LINKEDIN_EMAIL env var)"
    )
    auth_group.add_argument(
        "--password",
        type=str,
        help="LinkedIn password (or set LINKEDIN_PASSWORD env var)"
    )

    # Filtering options
    filter_group = parser.add_argument_group("Connection Filters")
    filter_group.add_argument(
        "--industry",
        type=str,
        help="Filter connections by industry (e.g., 'technology', 'finance', 'healthcare')"
    )
    filter_group.add_argument(
        "--location",
        type=str,
        help="Filter connections by location (e.g., 'San Francisco', 'New York')"
    )
    filter_group.add_argument(
        "--keywords",
        type=str,
        help="Filter by headline keywords, comma-separated (e.g., 'founder,ceo,startup')"
    )

    # Engagement options
    engage_group = parser.add_argument_group("Engagement Settings")
    engage_group.add_argument(
        "--max-connections",
        type=int,
        default=5,
        help="Maximum connections to engage with (default: 5)"
    )
    engage_group.add_argument(
        "--max-comments",
        type=int,
        default=10,
        help="Maximum comments per session (default: 10)"
    )
    engage_group.add_argument(
        "--posts-per-connection",
        type=int,
        default=2,
        help="Maximum posts to comment on per connection (default: 2)"
    )
    engage_group.add_argument(
        "--style",
        type=str,
        choices=["professional", "casual", "enthusiastic"],
        default="professional",
        help="Comment style (default: professional)"
    )

    # Mode options
    mode_group = parser.add_argument_group("Run Modes")
    mode_group.add_argument(
        "--preview",
        action="store_true",
        help="Preview mode - show connections and generated comments without engaging"
    )
    mode_group.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run - simulate engagement without posting comments"
    )
    mode_group.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode (no visible window)"
    )

    # Config file
    parser.add_argument(
        "--config",
        type=str,
        help="Path to JSON config file"
    )

    # Output options
    output_group = parser.add_argument_group("Output")
    output_group.add_argument(
        "--output",
        type=str,
        default="output",
        help="Output directory for logs (default: output)"
    )
    output_group.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )

    return parser.parse_args()


def load_config_file(config_path: str) -> dict:
    """Load configuration from JSON file."""
    import json
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config file: {e}")
        return {}


def run_preview_mode(bot: CommentBot, args) -> None:
    """Run in preview mode - show what comments would be generated."""
    print("\n" + "="*60)
    print("PREVIEW MODE - No comments will be posted")
    print("="*60 + "\n")

    keywords = args.keywords.split(",") if args.keywords else None

    previews = bot.preview_comments(
        industry=args.industry,
        location=args.location,
        keywords=keywords,
        num_connections=min(args.max_connections, 3)
    )

    if not previews:
        print("No connections found matching your criteria.")
        return

    for i, preview in enumerate(previews, 1):
        print(f"\n{'='*50}")
        print(f"Connection {i}: {preview['name']}")
        print(f"Headline: {preview['headline']}")
        print(f"{'='*50}")

        if not preview['posts']:
            print("No recent posts found")
            continue

        for j, post in enumerate(preview['posts'], 1):
            print(f"\n  Post {j}:")
            print(f"  Content: {post['content'][:150]}...")
            print(f"  \n  Generated Comment: \"{post['generated_comment']}\"")

    print("\n" + "-"*60)
    print("To actually engage, run without --preview flag")
    print("Recommended: Use --dry-run first to test the full flow")
    print("-"*60 + "\n")


def run_engagement(bot: CommentBot, args) -> dict:
    """Run the engagement process."""
    keywords = args.keywords.split(",") if args.keywords else None

    print("\n" + "="*60)
    if args.dry_run:
        print("DRY RUN MODE - Comments will NOT be posted")
    else:
        print("LIVE MODE - Comments WILL be posted")
        print("Press Ctrl+C to cancel...")
        import time
        time.sleep(3)  # Give user time to cancel
    print("="*60 + "\n")

    return bot.engage_with_connections(
        industry=args.industry,
        location=args.location,
        keywords=keywords,
        max_connections=args.max_connections,
        posts_per_connection=args.posts_per_connection,
        dry_run=args.dry_run
    )


def main():
    """Main entry point."""
    args = parse_arguments()

    # Load config file if provided
    config = {}
    if args.config:
        config = load_config_file(args.config)

    # Get credentials
    email = args.email or config.get("email") or os.getenv("LINKEDIN_EMAIL")
    password = args.password or config.get("password") or os.getenv("LINKEDIN_PASSWORD")

    if not email or not password:
        print("Error: LinkedIn credentials required.")
        print("\nProvide credentials via:")
        print("  1. Command line: --email and --password")
        print("  2. Environment variables: LINKEDIN_EMAIL and LINKEDIN_PASSWORD")
        print("  3. Config file: --config with 'email' and 'password' keys")
        print("  4. .env file: LINKEDIN_EMAIL=... and LINKEDIN_PASSWORD=...")
        sys.exit(1)

    # Merge config with args (args take precedence)
    if config:
        args.industry = args.industry or config.get("industry")
        args.location = args.location or config.get("location")
        args.keywords = args.keywords or config.get("keywords")
        args.max_connections = args.max_connections or config.get("max_connections", 5)
        args.max_comments = args.max_comments or config.get("max_comments", 10)
        args.style = args.style or config.get("style", "professional")

    print("\n" + "="*60)
    print("LinkedIn Connection Comment Bot")
    print("="*60)
    print(f"\nSettings:")
    print(f"  Industry filter: {args.industry or 'All'}")
    print(f"  Location filter: {args.location or 'All'}")
    print(f"  Keywords: {args.keywords or 'None'}")
    print(f"  Max connections: {args.max_connections}")
    print(f"  Max comments: {args.max_comments}")
    print(f"  Comment style: {args.style}")
    print(f"  Headless: {args.headless}")
    print(f"  Mode: {'Preview' if args.preview else 'Dry Run' if args.dry_run else 'Live'}")

    try:
        with CommentBot(
            headless=args.headless,
            comment_style=args.style,
            max_comments_per_session=args.max_comments
        ) as bot:
            # Login
            print("\nLogging in to LinkedIn...")
            if not bot.login(email, password):
                print("Login failed. Please check your credentials.")
                sys.exit(1)

            print("Login successful!")

            if args.preview:
                run_preview_mode(bot, args)
            else:
                results = run_engagement(bot, args)

                if results.get("error"):
                    print(f"\nError: {results['error']}")
                    sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

    print("\nDone!")


if __name__ == "__main__":
    main()
