#!/usr/bin/env python3
"""
LinkedIn Connection Comment Bot - CLI Entry Point

A visible Chrome browser automation tool that engages with your
LinkedIn connections' posts by adding short, relevant, human-like comments.

KEY FEATURES:
- Visible browser (not headless) - you can see everything happening
- Manual login support - you login, bot takes over
- Continuous mode - runs throughout the day like a real person
- Smart delays - mimics human behavior

USAGE EXAMPLES:

  # Manual login mode (RECOMMENDED for first use)
  python comment_bot_main.py --manual-login --industry technology

  # Continuous mode - run all day
  python comment_bot_main.py --manual-login --continuous --hours 8

  # Preview mode (safe - no comments posted)
  python comment_bot_main.py --manual-login --preview

  # Dry run (simulate without posting)
  python comment_bot_main.py --manual-login --dry-run --industry startup
"""

import argparse
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from comment_bot import CommentBot


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="LinkedIn Comment Bot - Engage with your network like a real person",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
RECOMMENDED WORKFLOW:

  1. First time - Use manual login:
     python comment_bot_main.py --manual-login --preview

  2. Test with dry-run:
     python comment_bot_main.py --manual-login --dry-run --industry technology

  3. Run continuously:
     python comment_bot_main.py --manual-login --continuous --hours 8

EXAMPLES:

  # Filter by industry
  python comment_bot_main.py --manual-login --industry technology

  # Filter by location
  python comment_bot_main.py --manual-login --location "San Francisco"

  # Filter by keywords (founders, CEOs)
  python comment_bot_main.py --manual-login --keywords "founder,ceo,startup"

  # Casual comment style
  python comment_bot_main.py --manual-login --style casual

  # Run for 4 hours, 2 comments per hour
  python comment_bot_main.py --manual-login --continuous --hours 4 --rate 2
        """
    )

    # Login options
    login_group = parser.add_argument_group("Login Options")
    login_group.add_argument(
        "--manual-login",
        action="store_true",
        help="Open browser and wait for you to login manually (RECOMMENDED)"
    )
    login_group.add_argument(
        "--email",
        type=str,
        help="LinkedIn email for auto-login (or set LINKEDIN_EMAIL env var)"
    )
    login_group.add_argument(
        "--password",
        type=str,
        help="LinkedIn password for auto-login (or set LINKEDIN_PASSWORD env var)"
    )
    login_group.add_argument(
        "--login-timeout",
        type=int,
        default=300,
        help="Seconds to wait for manual login (default: 300)"
    )

    # Filtering options
    filter_group = parser.add_argument_group("Connection Filters")
    filter_group.add_argument(
        "--industry",
        type=str,
        help="Filter by industry (technology, finance, healthcare, startup, etc.)"
    )
    filter_group.add_argument(
        "--location",
        type=str,
        help="Filter by location (e.g., 'San Francisco', 'New York')"
    )
    filter_group.add_argument(
        "--keywords",
        type=str,
        help="Filter by headline keywords, comma-separated (e.g., 'founder,ceo')"
    )

    # Continuous mode options
    continuous_group = parser.add_argument_group("Continuous Mode (Run All Day)")
    continuous_group.add_argument(
        "--continuous",
        action="store_true",
        help="Run continuously throughout the day"
    )
    continuous_group.add_argument(
        "--hours",
        type=int,
        default=8,
        help="Hours to run in continuous mode (default: 8)"
    )
    continuous_group.add_argument(
        "--rate",
        type=int,
        default=3,
        help="Target comments per hour in continuous mode (default: 3)"
    )
    continuous_group.add_argument(
        "--active-start",
        type=int,
        default=9,
        help="Hour to start commenting (24h format, default: 9)"
    )
    continuous_group.add_argument(
        "--active-end",
        type=int,
        default=17,
        help="Hour to stop commenting (24h format, default: 17)"
    )

    # Single session options
    session_group = parser.add_argument_group("Single Session Settings")
    session_group.add_argument(
        "--max-connections",
        type=int,
        default=5,
        help="Max connections to engage with per session (default: 5)"
    )
    session_group.add_argument(
        "--max-comments",
        type=int,
        default=10,
        help="Max comments per session (default: 10)"
    )
    session_group.add_argument(
        "--posts-per-connection",
        type=int,
        default=1,
        help="Max posts to comment on per connection (default: 1)"
    )

    # Comment settings
    comment_group = parser.add_argument_group("Comment Settings")
    comment_group.add_argument(
        "--style",
        type=str,
        choices=["professional", "casual", "enthusiastic"],
        default="professional",
        help="Comment style (default: professional)"
    )
    comment_group.add_argument(
        "--min-delay",
        type=int,
        default=120,
        help="Minimum seconds between comments (default: 120)"
    )
    comment_group.add_argument(
        "--max-delay",
        type=int,
        default=300,
        help="Maximum seconds between comments (default: 300)"
    )

    # Mode options
    mode_group = parser.add_argument_group("Run Modes")
    mode_group.add_argument(
        "--preview",
        action="store_true",
        help="Preview mode - see generated comments without posting"
    )
    mode_group.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run - simulate full engagement without posting"
    )

    # Browser options
    browser_group = parser.add_argument_group("Browser Settings")
    browser_group.add_argument(
        "--chrome-profile",
        type=str,
        help="Path to Chrome profile directory for persistent sessions"
    )

    # Output options
    parser.add_argument(
        "--output",
        type=str,
        default="output",
        help="Output directory for logs (default: output)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )

    return parser.parse_args()


def print_banner():
    """Print welcome banner."""
    print("\n" + "="*60)
    print("   LINKEDIN CONNECTION COMMENT BOT")
    print("   Engage with your network like a real person")
    print("="*60)


def run_preview_mode(bot: CommentBot, args) -> None:
    """Run in preview mode."""
    print("\n" + "="*60)
    print("PREVIEW MODE - See what comments would be generated")
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
            print("  No recent posts found")
            continue

        for j, post in enumerate(preview['posts'], 1):
            print(f"\n  Post {j}:")
            print(f"  {post['content'][:150]}...")
            print(f"\n  >>> Generated Comment: \"{post['generated_comment']}\"")

    print("\n" + "-"*60)
    print("To actually engage:")
    print("  - Use --dry-run to test the full flow")
    print("  - Remove --preview to post comments")
    print("-"*60 + "\n")


def run_continuous_mode(bot: CommentBot, args) -> dict:
    """Run in continuous mode."""
    keywords = args.keywords.split(",") if args.keywords else None

    print("\n" + "="*60)
    print("CONTINUOUS MODE")
    if args.dry_run:
        print("(DRY RUN - No comments will be posted)")
    else:
        print("LIVE MODE - Comments WILL be posted!")
    print("="*60)
    print(f"\nSettings:")
    print(f"  Run duration: {args.hours} hours")
    print(f"  Target rate: {args.rate} comments/hour")
    print(f"  Active hours: {args.active_start}:00 - {args.active_end}:00")
    print(f"  Industry: {args.industry or 'All'}")
    print(f"  Location: {args.location or 'All'}")
    print(f"\nPress Ctrl+C to stop at any time")

    if not args.dry_run:
        print("\nStarting in 5 seconds...")
        import time
        time.sleep(5)

    return bot.run_continuous(
        industry=args.industry,
        location=args.location,
        keywords=keywords,
        comments_per_hour=args.rate,
        run_hours=args.hours,
        active_hours=(args.active_start, args.active_end),
        dry_run=args.dry_run
    )


def run_single_session(bot: CommentBot, args) -> dict:
    """Run a single engagement session."""
    keywords = args.keywords.split(",") if args.keywords else None

    print("\n" + "="*60)
    if args.dry_run:
        print("DRY RUN MODE - No comments will be posted")
    else:
        print("LIVE MODE - Comments WILL be posted!")
        print("Press Ctrl+C to cancel...")
        import time
        time.sleep(3)
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
    print_banner()

    print(f"\nSettings:")
    print(f"  Login: {'Manual' if args.manual_login else 'Auto'}")
    print(f"  Mode: {'Continuous' if args.continuous else 'Preview' if args.preview else 'Single Session'}")
    print(f"  Industry: {args.industry or 'All'}")
    print(f"  Location: {args.location or 'All'}")
    print(f"  Keywords: {args.keywords or 'None'}")
    print(f"  Style: {args.style}")
    print(f"  Dry run: {args.dry_run}")

    try:
        with CommentBot(
            headless=False,  # Always visible
            comment_style=args.style,
            max_comments_per_session=args.max_comments,
            delay_between_comments=(args.min_delay, args.max_delay),
            chrome_profile_path=args.chrome_profile
        ) as bot:

            # Handle login
            logged_in = False

            if args.manual_login:
                print("\n" + "="*60)
                print("MANUAL LOGIN")
                print("="*60)
                print("The browser will open LinkedIn.")
                print("Please login manually in the browser window.")
                print(f"You have {args.login_timeout} seconds to complete login.")
                print("="*60 + "\n")

                logged_in = bot.wait_for_manual_login(timeout=args.login_timeout)
            else:
                # Try auto-login
                email = args.email or os.getenv("LINKEDIN_EMAIL")
                password = args.password or os.getenv("LINKEDIN_PASSWORD")

                if email and password:
                    logged_in = bot.login(email, password)
                else:
                    # Check if already logged in (using Chrome profile)
                    print("\nChecking if already logged in...")
                    logged_in = bot.check_login_status()

                    if not logged_in:
                        print("\nNo credentials provided and not logged in.")
                        print("Use --manual-login to login manually.")
                        sys.exit(1)

            if not logged_in:
                print("\nLogin failed or timed out.")
                sys.exit(1)

            print("\nLogin successful! Starting bot...\n")

            # Run appropriate mode
            if args.preview:
                run_preview_mode(bot, args)
            elif args.continuous:
                results = run_continuous_mode(bot, args)
                if results.get("error"):
                    print(f"\nError: {results['error']}")
                    sys.exit(1)
            else:
                results = run_single_session(bot, args)
                if results.get("error"):
                    print(f"\nError: {results['error']}")
                    sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nStopped by user (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

    print("\nDone! Check the output folder for session logs.")


if __name__ == "__main__":
    main()
