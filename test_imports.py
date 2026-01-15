#!/usr/bin/env python3
"""
Test script to validate that all modules import correctly
and demonstrate the structure of the lead scraping tool.
"""

import sys

def test_imports():
    """Test that all modules can be imported."""
    print("=" * 60)
    print("Testing Lead Scraping Tool - Module Imports")
    print("=" * 60)

    tests_passed = 0
    tests_failed = 0

    # Test 1: Config
    print("\n[1/8] Testing config module...")
    try:
        from config import Config
        config = Config()
        print(f"  ✅ Config loaded successfully")
        print(f"     - Headless mode: {config.HEADLESS_MODE}")
        print(f"     - Timeout: {config.TIMEOUT}s")
        print(f"     - Delay between requests: {config.DELAY_BETWEEN_REQUESTS}s")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Failed to load config: {e}")
        tests_failed += 1

    # Test 2: Email Extractor
    print("\n[2/8] Testing email extractor...")
    try:
        from utils.email_extractor import EmailExtractor

        # Test email extraction
        test_text = "Contact us at john.doe@example.com or jane@test.org for more info"
        emails = EmailExtractor.extract_emails(test_text, validate=False)

        print(f"  ✅ Email extractor working")
        print(f"     - Test text: '{test_text[:50]}...'")
        print(f"     - Extracted emails: {emails}")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Failed email extractor: {e}")
        tests_failed += 1

    # Test 3: Web Scraper
    print("\n[3/8] Testing web scraper module...")
    try:
        from utils.web_scraper import WebScraper
        print(f"  ✅ Web scraper module imported successfully")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Failed to import web scraper: {e}")
        tests_failed += 1

    # Test 4: Search Scraper
    print("\n[4/8] Testing search scraper module...")
    try:
        from scrapers.search_scraper import SearchScraper
        print(f"  ✅ Search scraper module imported successfully")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Failed to import search scraper: {e}")
        tests_failed += 1

    # Test 5: LinkedIn Scraper
    print("\n[5/8] Testing LinkedIn scraper module...")
    try:
        from scrapers.linkedin_scraper import LinkedInScraper
        print(f"  ✅ LinkedIn scraper module imported successfully")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Failed to import LinkedIn scraper: {e}")
        tests_failed += 1

    # Test 6: Profile Scraper
    print("\n[6/8] Testing profile scraper module...")
    try:
        from scrapers.profile_scraper import ProfileScraper
        print(f"  ✅ Profile scraper module imported successfully")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Failed to import profile scraper: {e}")
        tests_failed += 1

    # Test 7: Data Exporter
    print("\n[7/8] Testing data exporter...")
    try:
        from data_exporter import DataExporter

        # Test with sample data
        sample_leads = [
            {
                'name': 'John Doe',
                'company': 'Tech Corp',
                'title': 'CEO',
                'emails': ['john@techcorp.com'],
                'linkedin_url': 'https://linkedin.com/in/johndoe',
                'location': 'San Francisco, CA'
            },
            {
                'name': 'Jane Smith',
                'company': 'Innovation Inc',
                'title': 'CTO',
                'emails': ['jane@innovation.com', 'jane.smith@innovation.com'],
                'linkedin_url': 'https://linkedin.com/in/janesmith',
                'location': 'New York, NY'
            }
        ]

        exporter = DataExporter()
        summary = exporter.export_summary(sample_leads)

        print(f"  ✅ Data exporter working")
        print(f"     - Sample leads: {summary['total_leads']}")
        print(f"     - Leads with emails: {summary['leads_with_emails']}")
        print(f"     - Total emails: {summary['total_emails']}")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Failed data exporter: {e}")
        tests_failed += 1

    # Test 8: Main Lead Scraper
    print("\n[8/8] Testing main lead scraper...")
    try:
        from lead_scraper import LeadScraper
        print(f"  ✅ Lead scraper module imported successfully")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Failed to import lead scraper: {e}")
        tests_failed += 1

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"✅ Passed: {tests_passed}/8")
    print(f"❌ Failed: {tests_failed}/8")

    if tests_failed == 0:
        print("\n🎉 All modules loaded successfully!")
        print("\n📚 The tool is ready to use. Try:")
        print("   python main.py --help")
        print("\n⚠️  Note: Actual web scraping requires:")
        print("   - Chrome/Chromium browser installed")
        print("   - Internet connection")
        print("   - Proper configuration in .env file")
        return True
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == '__main__':
    success = test_imports()
    sys.exit(0 if success else 1)
