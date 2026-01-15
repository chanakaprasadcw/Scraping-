#!/usr/bin/env python3
"""
Debug script to diagnose why searches aren't finding results.

This will test each component and show where the problem is.
"""

import sys
import time

def test_google_search_access():
    """Test if we can access Google search."""
    print("\n" + "=" * 70)
    print("TEST 1: Google Search Access")
    print("=" * 70)

    try:
        from utils.web_scraper import WebScraper

        print("\n→ Creating web scraper...")
        scraper = WebScraper(headless=True, timeout=30)

        print("→ Initializing Chrome driver...")
        scraper.init_driver()

        print("→ Attempting to access Google...")
        test_query = "test search"
        url = f"https://www.google.com/search?q={test_query}"

        scraper.driver.get(url)
        time.sleep(3)

        html = scraper.driver.page_source

        print(f"→ Page loaded, HTML length: {len(html)} characters")

        # Check if we got blocked
        if "unusual traffic" in html.lower() or "captcha" in html.lower():
            print("\n❌ PROBLEM: Google is blocking automated requests")
            print("   Detected CAPTCHA or rate limiting")
            scraper.close()
            return False

        # Check if we got results
        if "search" in html.lower():
            print("\n✅ SUCCESS: Google search is accessible")
            scraper.close()
            return True
        else:
            print("\n❌ PROBLEM: Unexpected response from Google")
            print(f"   First 500 chars: {html[:500]}")
            scraper.close()
            return False

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False


def test_search_scraper():
    """Test the search scraper component."""
    print("\n" + "=" * 70)
    print("TEST 2: Search Scraper")
    print("=" * 70)

    try:
        from utils.web_scraper import WebScraper
        from scrapers.search_scraper import SearchScraper

        print("\n→ Creating scrapers...")
        web_scraper = WebScraper(headless=True)
        search_scraper = SearchScraper(web_scraper)

        print("→ Searching for: 'CEO startup'")
        results = search_scraper.google_search("CEO startup", num_results=5)

        print(f"\n→ Found {len(results)} results")

        if len(results) == 0:
            print("\n❌ PROBLEM: No search results returned")
            print("   Possible causes:")
            print("   - Google is blocking the requests")
            print("   - Search result HTML structure changed")
            print("   - Network connectivity issues")
            web_scraper.close()
            return False

        print("\n✅ Search results found:")
        for i, result in enumerate(results[:3], 1):
            print(f"\n   {i}. {result.get('title', 'No title')}")
            print(f"      URL: {result.get('url', 'No URL')[:60]}...")

        # Check for LinkedIn results
        linkedin_results = [r for r in results if 'linkedin.com' in r.get('url', '')]
        print(f"\n→ LinkedIn URLs found: {len(linkedin_results)}")

        web_scraper.close()
        return True

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_nlp_extraction():
    """Test NLP extraction."""
    print("\n" + "=" * 70)
    print("TEST 3: NLP Extraction")
    print("=" * 70)

    try:
        from utils.nlp_extractor import NLPExtractor

        query = "Find startup founders in San Francisco"
        print(f"\n→ Testing query: \"{query}\"")

        criteria = NLPExtractor.extract_criteria(query)

        print(f"\n→ Extracted positions: {criteria.get('positions', [])}")
        print(f"→ Extracted company type: {criteria.get('company_type')}")
        print(f"→ Extracted location: {criteria.get('location')}")

        queries = NLPExtractor.generate_search_queries(criteria)
        print(f"\n→ Generated {len(queries)} search queries:")
        for i, q in enumerate(queries, 1):
            print(f"   {i}. {q}")

        if len(queries) > 0:
            print("\n✅ NLP extraction working correctly")
            return True
        else:
            print("\n❌ PROBLEM: No queries generated")
            return False

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_alternative_search():
    """Test alternative search approach."""
    print("\n" + "=" * 70)
    print("TEST 4: Alternative Search Methods")
    print("=" * 70)

    print("\n→ Current approach: Direct Google search scraping")
    print("   Problem: Google actively blocks automated requests")

    print("\n→ Alternative approaches that might work better:")
    print("   1. Use Google Custom Search API (requires API key)")
    print("   2. Use Bing search instead (less aggressive blocking)")
    print("   3. Use DuckDuckGo (no rate limiting)")
    print("   4. Use LinkedIn search directly (requires login)")
    print("   5. Use specialized lead databases/APIs")

    print("\n→ Recommendation: Implement multiple fallback methods")


def show_recommendations():
    """Show recommendations for improvement."""
    print("\n" + "=" * 70)
    print("RECOMMENDATIONS TO FIX 'NO RESULTS FOUND'")
    print("=" * 70)

    print("\n1️⃣  IMMEDIATE FIXES:")
    print("   • Increase delays between requests (try 5-10 seconds)")
    print("   • Use residential proxies or VPN")
    print("   • Add more random user agents")
    print("   • Try different times of day")

    print("\n2️⃣  ALTERNATIVE SEARCH ENGINES:")
    print("   • DuckDuckGo (no blocking)")
    print("   • Bing (less aggressive)")
    print("   • Ecosia, Brave Search, etc.")

    print("\n3️⃣  API-BASED APPROACHES:")
    print("   • Google Custom Search API (100 free queries/day)")
    print("   • Bing Search API")
    print("   • SerpAPI, ScraperAPI (paid)")

    print("\n4️⃣  DIRECT LINKEDIN:")
    print("   • Use LinkedIn login (scraper already supports it)")
    print("   • LinkedIn's own search is more reliable")
    print("   • Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env")

    print("\n5️⃣  SPECIALIZED TOOLS:")
    print("   • Apollo.io API")
    print("   • Hunter.io (email finding)")
    print("   • RocketReach API")
    print("   • Lusha, ZoomInfo, etc.")

    print("\n6️⃣  HYBRID APPROACH:")
    print("   • Use manual LinkedIn search to get profile URLs")
    print("   • Feed URLs to the scraper")
    print("   • Scraper extracts data from known URLs")


def main():
    """Run all diagnostic tests."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "DIAGNOSTIC: Why No Results Found?" + " " * 16 + "║")
    print("╚" + "=" * 68 + "╝")

    print("\nThis will test each component to find the problem...\n")

    # Run tests
    results = {}

    # Test 1: Google access
    results['google_access'] = test_google_search_access()

    # Test 2: Search scraper
    if results['google_access']:
        results['search_scraper'] = test_search_scraper()
    else:
        print("\n⚠️  Skipping search scraper test (Google access blocked)")
        results['search_scraper'] = False

    # Test 3: NLP
    results['nlp'] = test_nlp_extraction()

    # Test 4: Alternatives
    test_alternative_search()

    # Summary
    print("\n" + "=" * 70)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 70)

    print("\nTest Results:")
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {test_name.replace('_', ' ').title()}")

    # Recommendations
    show_recommendations()

    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)

    if not results.get('google_access'):
        print("\n⚠️  PRIMARY ISSUE: Google is blocking automated requests")
        print("\n   Quick fixes to try:")
        print("   1. Edit .env and increase DELAY_BETWEEN_REQUESTS to 10")
        print("   2. Try using a VPN")
        print("   3. Run at different time of day")
        print("   4. Use alternative search engines (see recommendations above)")
    elif not results.get('search_scraper'):
        print("\n⚠️  PRIMARY ISSUE: Search scraper not finding results")
        print("\n   This usually means:")
        print("   - Google HTML structure changed")
        print("   - Need to update CSS selectors")
        print("   - Or switch to API-based approach")
    else:
        print("\n✅ Basic functionality works!")
        print("   If you're still not getting results, try:")
        print("   - More specific search queries")
        print("   - Increase the limit")
        print("   - Check your internet connection")

    print("\n" + "=" * 70)
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
