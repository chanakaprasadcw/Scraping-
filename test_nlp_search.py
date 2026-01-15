#!/usr/bin/env python3
"""
Test script for natural language search functionality.

This script demonstrates how the NLP extractor parses natural language
queries and generates search criteria.
"""

from utils.nlp_extractor import NLPExtractor


def test_query(query: str):
    """Test a single query and display results."""
    print("\n" + "=" * 80)
    print(f"Query: \"{query}\"")
    print("=" * 80)

    # Extract criteria
    criteria = NLPExtractor.extract_criteria(query)

    # Display formatted summary
    print(NLPExtractor.format_criteria_summary(criteria))

    # Generate search queries
    search_queries = NLPExtractor.generate_search_queries(criteria)

    print(f"\n🔍 Generated Search Queries ({len(search_queries)}):")
    for i, q in enumerate(search_queries, 1):
        print(f"  {i}. {q}")


def main():
    """Run tests with various natural language queries."""
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "Natural Language Search - Test Results" + " " * 18 + "║")
    print("╚" + "=" * 78 + "╝")

    # Test queries
    test_queries = [
        "Find startup founders in San Francisco with 2-5 team members",
        "Tech CEOs at companies founded in last 2 years",
        "VPs at fintech startups in New York",
        "Directors and managers at SaaS companies",
        "Co-founders of healthcare tech startups",
        "CTOs at AI companies with teams of 10-20 people",
        "Startup founders who started since 2024",
        "Engineering leads at cloud computing startups in Austin"
    ]

    for query in test_queries:
        test_query(query)

    # Summary
    print("\n" + "=" * 80)
    print("✅ Natural Language Search Testing Complete!")
    print("=" * 80)
    print("\n📚 To use natural language search:")
    print("   python main.py --query \"Your natural language query here\"")
    print("\n💡 Examples:")
    print("   python main.py --query \"Find startup founders in SF\" --limit 20")
    print("   python main.py --query \"Tech CEOs\" --format excel --output tech_ceos")
    print()


if __name__ == '__main__':
    main()
