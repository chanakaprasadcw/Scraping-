"""Natural Language Processing for extracting search criteria from text."""

import re
from typing import Dict, List, Optional


class NLPExtractor:
    """Extract search criteria from natural language input."""

    # Patterns for extracting different criteria
    POSITION_KEYWORDS = [
        'founder', 'co-founder', 'ceo', 'cto', 'cfo', 'coo', 'president',
        'vp', 'vice president', 'director', 'manager', 'lead', 'head',
        'engineer', 'developer', 'designer', 'architect', 'analyst',
        'executive', 'officer', 'partner', 'owner', 'principal'
    ]

    COMPANY_TYPE_KEYWORDS = {
        'startup': ['startup', 'start-up', 'startups'],
        'enterprise': ['enterprise', 'corporation', 'corporate'],
        'agency': ['agency', 'agencies'],
        'consulting': ['consulting', 'consultancy'],
        'saas': ['saas', 'software as a service'],
        'ecommerce': ['e-commerce', 'ecommerce', 'online store'],
        'fintech': ['fintech', 'financial technology'],
        'healthtech': ['healthtech', 'health tech', 'healthcare technology']
    }

    INDUSTRY_KEYWORDS = [
        'tech', 'technology', 'software', 'ai', 'ml', 'machine learning',
        'cloud', 'saas', 'fintech', 'healthcare', 'education', 'edtech',
        'marketing', 'sales', 'finance', 'hr', 'recruiting', 'legal',
        'real estate', 'construction', 'manufacturing', 'retail',
        'hospitality', 'travel', 'entertainment', 'media', 'gaming'
    ]

    LOCATION_KEYWORDS = [
        'san francisco', 'sf', 'bay area', 'silicon valley', 'new york',
        'nyc', 'boston', 'austin', 'seattle', 'los angeles', 'la',
        'chicago', 'denver', 'miami', 'atlanta', 'london', 'berlin',
        'singapore', 'bangalore', 'toronto', 'remote', 'worldwide'
    ]

    @classmethod
    def extract_criteria(cls, text: str) -> Dict[str, any]:
        """
        Extract search criteria from natural language text.

        Args:
            text: Natural language search query

        Returns:
            Dictionary with extracted criteria
        """
        text_lower = text.lower()

        criteria = {
            'original_query': text,
            'positions': cls._extract_positions(text_lower),
            'company_type': cls._extract_company_type(text_lower),
            'industry': cls._extract_industry(text_lower),
            'location': cls._extract_location(text_lower),
            'team_size': cls._extract_team_size(text_lower),
            'founding_year': cls._extract_founding_year(text_lower),
            'keywords': cls._extract_general_keywords(text_lower),
            'company_names': cls._extract_company_names(text)
        }

        return criteria

    @classmethod
    def _extract_positions(cls, text: str) -> List[str]:
        """Extract job positions/titles from text."""
        positions = []

        for keyword in cls.POSITION_KEYWORDS:
            # Match whole words or word boundaries
            pattern = r'\b' + re.escape(keyword) + r's?\b'
            if re.search(pattern, text, re.IGNORECASE):
                # Capitalize properly
                positions.append(keyword.title())

        # Remove duplicates and return
        return list(set(positions))

    @classmethod
    def _extract_company_type(cls, text: str) -> Optional[str]:
        """Extract company type from text."""
        for company_type, keywords in cls.COMPANY_TYPE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    return company_type
        return None

    @classmethod
    def _extract_industry(cls, text: str) -> Optional[str]:
        """Extract industry from text."""
        for industry in cls.INDUSTRY_KEYWORDS:
            if industry in text:
                return industry
        return None

    @classmethod
    def _extract_location(cls, text: str) -> Optional[str]:
        """Extract location from text."""
        for location in cls.LOCATION_KEYWORDS:
            if location in text:
                return location.title()
        return None

    @classmethod
    def _extract_team_size(cls, text: str) -> Optional[Dict[str, int]]:
        """Extract team size from text."""
        # Patterns like "2-5 employees", "10 people", "team of 3"
        patterns = [
            r'(\d+)[-–](\d+)\s*(employees?|people|team members?|members?)',
            r'team\s*of\s*(\d+)[-–]?(\d+)?',
            r'(\d+)\s*to\s*(\d+)\s*(employees?|people)',
            r'(\d+)\s*(employees?|people|team members?)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                groups = [g for g in match.groups() if g and g.isdigit()]
                if len(groups) == 2:
                    return {'min': int(groups[0]), 'max': int(groups[1])}
                elif len(groups) == 1:
                    size = int(groups[0])
                    return {'min': size, 'max': size}

        return None

    @classmethod
    def _extract_founding_year(cls, text: str) -> Optional[Dict[str, int]]:
        """Extract founding year constraints from text."""
        # Patterns like "founded in last 2 years", "started in 2020"
        current_year = 2026  # Update this

        # Pattern: "in last X years" or "within X years"
        match = re.search(r'(?:in\s+(?:the\s+)?last|within)\s+(\d+)\s+years?', text)
        if match:
            years_ago = int(match.group(1))
            return {'min': current_year - years_ago, 'max': current_year}

        # Pattern: "started in 2020" or "founded in 2020"
        match = re.search(r'(?:started|founded)\s+in\s+(\d{4})', text)
        if match:
            year = int(match.group(1))
            return {'min': year, 'max': year}

        # Pattern: "since 2020"
        match = re.search(r'since\s+(\d{4})', text)
        if match:
            year = int(match.group(1))
            return {'min': year, 'max': current_year}

        return None

    @classmethod
    def _extract_general_keywords(cls, text: str) -> List[str]:
        """Extract general keywords from text."""
        # Remove common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'that', 'have', 'has', 'had', 'is', 'are',
            'was', 'were', 'be', 'been', 'being', 'this', 'these', 'those'
        }

        # Extract words
        words = re.findall(r'\b[a-z]{3,}\b', text)

        # Filter stop words
        keywords = [word for word in words if word not in stop_words]

        # Return unique keywords
        return list(set(keywords))[:10]  # Limit to 10 keywords

    @classmethod
    def _extract_company_names(cls, text: str) -> List[str]:
        """Extract company names from text (capitalized words)."""
        # Look for capitalized words that might be company names
        # This is a simple heuristic - proper NER would be better
        company_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b'
        matches = re.findall(company_pattern, text)

        # Filter out common non-company words
        common_words = {'The', 'A', 'An', 'In', 'On', 'At', 'To', 'For'}
        companies = [m for m in matches if m not in common_words]

        return list(set(companies))

    @classmethod
    def generate_search_queries(cls, criteria: Dict[str, any]) -> List[str]:
        """
        Generate search queries from extracted criteria.

        Args:
            criteria: Extracted search criteria

        Returns:
            List of search query strings
        """
        queries = []

        # Base query from positions and company type
        if criteria['positions']:
            for position in criteria['positions'][:3]:  # Limit to 3 positions
                query_parts = [position]

                if criteria['company_type']:
                    query_parts.append(criteria['company_type'])

                if criteria['industry']:
                    query_parts.append(criteria['industry'])

                if criteria['location']:
                    query_parts.append(criteria['location'])

                queries.append(' '.join(query_parts))

        # Add LinkedIn-specific queries
        if criteria['positions'] and criteria['company_type']:
            linkedin_query = f"site:linkedin.com/in/ {criteria['positions'][0]} {criteria['company_type']}"
            if criteria['industry']:
                linkedin_query += f" {criteria['industry']}"
            queries.append(linkedin_query)

        # If no structured queries, use keywords
        if not queries and criteria['keywords']:
            queries.append(' '.join(criteria['keywords'][:5]))

        return queries[:5]  # Limit to 5 queries

    @classmethod
    def format_criteria_summary(cls, criteria: Dict[str, any]) -> str:
        """
        Format extracted criteria as a readable summary.

        Args:
            criteria: Extracted search criteria

        Returns:
            Formatted string summary
        """
        lines = [
            "🔍 Extracted Search Criteria:",
            "-" * 50
        ]

        if criteria['positions']:
            lines.append(f"Positions: {', '.join(criteria['positions'])}")

        if criteria['company_type']:
            lines.append(f"Company Type: {criteria['company_type'].title()}")

        if criteria['industry']:
            lines.append(f"Industry: {criteria['industry'].title()}")

        if criteria['location']:
            lines.append(f"Location: {criteria['location']}")

        if criteria['team_size']:
            size = criteria['team_size']
            if size['min'] == size['max']:
                lines.append(f"Team Size: {size['min']} members")
            else:
                lines.append(f"Team Size: {size['min']}-{size['max']} members")

        if criteria['founding_year']:
            year = criteria['founding_year']
            if year['min'] == year['max']:
                lines.append(f"Founded: {year['min']}")
            else:
                lines.append(f"Founded: {year['min']}-{year['max']}")

        if criteria['company_names']:
            lines.append(f"Companies: {', '.join(criteria['company_names'])}")

        if criteria['keywords']:
            lines.append(f"Keywords: {', '.join(criteria['keywords'][:5])}")

        return '\n'.join(lines)
