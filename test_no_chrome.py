#!/usr/bin/env python3
"""Test the no-Chrome version to verify it works."""

print("\n" + "=" * 70)
print("Testing No-Chrome Lead Scraper")
print("=" * 70)

# Test 1: DuckDuckGo search
print("\n[TEST 1] Testing DuckDuckGo search...")
try:
    from scrapers.duckduckgo_scraper import DuckDuckGoScraper

    scraper = DuckDuckGoScraper()
    results = scraper.search("startup founder", num_results=3)

    print(f"✓ Found {len(results)} results")
    for i, result in enumerate(results[:2], 1):
        print(f"  {i}. {result['title'][:60]}...")
        print(f"     {result['url'][:60]}...")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: LinkedIn profile scraping
print("\n[TEST 2] Testing LinkedIn scraping with requests...")
try:
    from scrapers.requests_linkedin_scraper import RequestsLinkedInScraper

    linkedin = RequestsLinkedInScraper()

    # Use a known public profile URL (example)
    test_url = "https://www.linkedin.com/in/williamhgates"  # Bill Gates

    print(f"→ Testing with: {test_url}")
    profile = linkedin.scrape_profile(test_url)

    print(f"✓ Name: {profile.get('name', 'Not extracted')}")
    print(f"✓ Headline: {profile.get('headline', 'Not extracted')[:60]}...")
    print(f"✓ Location: {profile.get('location', 'Not extracted')}")

except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: NLP extraction
print("\n[TEST 3] Testing NLP extraction...")
try:
    from utils.nlp_extractor import NLPExtractor

    query = "Find tech CEOs at startups"
    criteria = NLPExtractor.extract_criteria(query)

    print(f"✓ Query: \"{query}\"")
    print(f"✓ Extracted positions: {criteria.get('positions', [])}")
    print(f"✓ Extracted company type: {criteria.get('company_type')}")

    queries = NLPExtractor.generate_search_queries(criteria)
    print(f"✓ Generated {len(queries)} search queries")

except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 70)
print("Summary")
print("=" * 70)
print("\nThe no-Chrome version uses:")
print("  ✓ DuckDuckGo for search (no rate limiting)")
print("  ✓ Requests library for scraping (fast & reliable)")
print("  ✓ No browser automation needed")
print("\nThis should work where the Chrome version failed!")
print()
