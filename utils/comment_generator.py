"""
Human-like Comment Generator
Generates short, relevant, and natural-sounding comments for LinkedIn posts.
"""

import random
import re
from typing import List, Dict, Optional


class CommentGenerator:
    """
    Generates human-like comments for LinkedIn posts based on content analysis.
    """

    def __init__(self, style: str = "professional"):
        """
        Initialize the comment generator.

        Args:
            style: Comment style - 'professional', 'casual', or 'enthusiastic'
        """
        self.style = style
        self._load_templates()

    def _load_templates(self):
        """Load comment templates for different scenarios."""

        # Achievement/Success posts
        self.achievement_templates = {
            "professional": [
                "Congratulations on this milestone!",
                "Well deserved. Great to see your progress.",
                "Impressive achievement. Keep up the great work!",
                "This is inspiring. Congratulations!",
                "Fantastic news! Well earned.",
                "Great accomplishment. Wishing you continued success.",
                "Congratulations! This is well deserved.",
                "Amazing milestone. Looking forward to seeing more.",
            ],
            "casual": [
                "This is awesome! Congrats!",
                "So happy for you! Well done!",
                "Love seeing this. Congrats!",
                "This is great news! Congratulations!",
                "Well done! You've earned it.",
                "Congrats! This is fantastic!",
            ],
            "enthusiastic": [
                "Absolutely amazing! Huge congratulations!",
                "This is incredible! So well deserved!",
                "Wow! What an achievement! Congratulations!",
                "So inspiring! Massive congratulations!",
                "This is phenomenal! Well done!",
            ]
        }

        # Insight/Knowledge sharing posts
        self.insight_templates = {
            "professional": [
                "Great insight. Thanks for sharing.",
                "This is a valuable perspective. Appreciate you sharing.",
                "Interesting point. Something to think about.",
                "Well articulated. Thanks for the insight.",
                "This resonates. Great perspective.",
                "Thoughtful analysis. Thanks for sharing this.",
                "Good point. I hadn't considered this angle.",
                "This is helpful. Appreciate the insight.",
            ],
            "casual": [
                "Great point! Thanks for sharing.",
                "This is so true. Thanks for posting.",
                "Love this perspective!",
                "Really helpful insight. Thanks!",
                "Good stuff! Appreciate you sharing.",
            ],
            "enthusiastic": [
                "Brilliant insight! Thanks for sharing this!",
                "This is exactly what I needed to hear!",
                "Such a valuable perspective! Thank you!",
                "Absolutely spot on! Great insight!",
            ]
        }

        # Question/Discussion posts
        self.question_templates = {
            "professional": [
                "Great question. Looking forward to seeing the responses.",
                "Interesting topic for discussion.",
                "This is worth exploring further.",
                "Good question. I'd be curious to hear different perspectives.",
                "Thought-provoking question.",
            ],
            "casual": [
                "Great question! Curious to see what others think.",
                "Interesting! Would love to hear more thoughts on this.",
                "Good topic to discuss!",
            ],
            "enthusiastic": [
                "What a great question! Can't wait to see the discussion!",
                "Love this topic! Excited to see the responses!",
            ]
        }

        # Announcement/News posts
        self.announcement_templates = {
            "professional": [
                "Thanks for sharing this update.",
                "Good to know. Appreciate the update.",
                "Thanks for keeping us informed.",
                "Interesting development. Thanks for sharing.",
                "Appreciate the update on this.",
            ],
            "casual": [
                "Thanks for the update!",
                "Good to know! Thanks for sharing.",
                "Appreciate you sharing this!",
            ],
            "enthusiastic": [
                "Exciting news! Thanks for sharing!",
                "This is great! Thanks for the update!",
            ]
        }

        # Motivational/Inspirational posts
        self.motivational_templates = {
            "professional": [
                "Well said. This is a great reminder.",
                "Powerful message. Thanks for sharing.",
                "This resonates. Important reminder.",
                "Great perspective. Needed to hear this today.",
                "Wise words. Appreciate you sharing.",
            ],
            "casual": [
                "Love this! Great reminder.",
                "So true! Thanks for posting.",
                "Needed this today. Thanks!",
                "Great message! Thanks for sharing.",
            ],
            "enthusiastic": [
                "Absolutely love this! So inspiring!",
                "This is so powerful! Thank you for sharing!",
                "Needed this reminder today! Great post!",
            ]
        }

        # Generic positive templates
        self.generic_templates = {
            "professional": [
                "Thanks for sharing this.",
                "Interesting post. Appreciate you sharing.",
                "Good point. Thanks for posting.",
                "This is helpful. Thanks for sharing.",
                "Appreciate you sharing this perspective.",
            ],
            "casual": [
                "Great post! Thanks for sharing.",
                "Nice! Thanks for posting this.",
                "Good stuff! Appreciate it.",
            ],
            "enthusiastic": [
                "Great post! Love it!",
                "This is awesome! Thanks for sharing!",
            ]
        }

        # Topic-specific additions (to append to base comment)
        self.topic_additions = {
            "ai": ["AI is transforming everything.", "The AI space is evolving so fast.", "Exciting times in AI."],
            "leadership": ["Leadership lessons are always valuable.", "Great leadership insight."],
            "career": ["Career advice is always appreciated.", "Valuable career perspective."],
            "startup": ["Startup journey insights are always valuable.", "Love hearing startup stories."],
            "tech": ["Tech insights are always welcome.", "The tech space moves fast."],
            "hiring": ["The job market is interesting right now.", "Good hiring insights."],
            "product": ["Product thinking is crucial.", "Great product perspective."],
            "sales": ["Sales insights are always valuable.", "Good sales perspective."],
            "marketing": ["Marketing landscape keeps evolving.", "Great marketing insight."],
            "remote": ["Remote work has changed so much.", "Interesting take on remote work."],
            "growth": ["Growth mindset is key.", "Great growth perspective."],
        }

        # Emoji variations (used sparingly for casual/enthusiastic styles)
        self.emojis = {
            "achievement": ["🎉", "👏", "🙌", "💪", "🌟"],
            "insight": ["💡", "🎯", "✨"],
            "positive": ["👍", "🔥", "✅"],
            "thinking": ["🤔", "💭"],
        }

    def analyze_post(self, content: str) -> Dict:
        """
        Analyze post content to determine type and topics.

        Args:
            content: Post text content

        Returns:
            Dictionary with post analysis
        """
        content_lower = content.lower()

        analysis = {
            "type": "generic",
            "topics": [],
            "sentiment": "positive",
            "has_question": "?" in content,
            "is_short": len(content) < 100,
            "is_long": len(content) > 500,
        }

        # Detect post type
        achievement_words = ["excited", "thrilled", "proud", "achieved", "milestone", "accomplished",
                            "promotion", "new role", "joining", "started", "accepted", "launched",
                            "celebrating", "happy to announce", "pleased to share", "grateful"]
        insight_words = ["learned", "realized", "insight", "lesson", "tip", "advice", "truth is",
                         "here's what", "the key is", "remember that", "don't forget", "important to"]
        question_words = ["what do you think", "thoughts?", "what's your", "how do you", "anyone else",
                          "curious to know", "would love to hear", "what are your"]
        announcement_words = ["announcing", "news", "update", "introducing", "launching", "released",
                              "now available", "coming soon"]
        motivational_words = ["never give up", "keep going", "believe", "mindset", "success is",
                              "remember", "don't let", "you can", "stay focused", "be the"]

        if any(word in content_lower for word in achievement_words):
            analysis["type"] = "achievement"
        elif any(word in content_lower for word in question_words) or analysis["has_question"]:
            analysis["type"] = "question"
        elif any(word in content_lower for word in announcement_words):
            analysis["type"] = "announcement"
        elif any(word in content_lower for word in motivational_words):
            analysis["type"] = "motivational"
        elif any(word in content_lower for word in insight_words):
            analysis["type"] = "insight"

        # Detect topics
        topic_keywords = {
            "ai": ["ai", "artificial intelligence", "machine learning", "ml", "gpt", "llm", "chatgpt"],
            "leadership": ["leadership", "leader", "team lead", "managing", "management"],
            "career": ["career", "job", "interview", "resume", "cv", "hire"],
            "startup": ["startup", "founder", "entrepreneur", "venture", "funding", "raise"],
            "tech": ["technology", "software", "developer", "coding", "programming", "tech"],
            "hiring": ["hiring", "recruiting", "talent", "open role", "job opening", "we're looking"],
            "product": ["product", "feature", "roadmap", "launch", "user experience", "ux"],
            "sales": ["sales", "revenue", "deals", "pipeline", "quota", "closing"],
            "marketing": ["marketing", "brand", "campaign", "content", "social media", "seo"],
            "remote": ["remote", "wfh", "hybrid", "work from home", "distributed"],
            "growth": ["growth", "scale", "grow", "expand", "metrics"],
        }

        for topic, keywords in topic_keywords.items():
            if any(kw in content_lower for kw in keywords):
                analysis["topics"].append(topic)

        return analysis

    def generate_comment(self, post_content: str, author_name: str = "") -> str:
        """
        Generate a human-like comment for a post.

        Args:
            post_content: The post's text content
            author_name: Name of the post author (optional)

        Returns:
            Generated comment string
        """
        if not post_content:
            return random.choice(self.generic_templates[self.style])

        analysis = self.analyze_post(post_content)

        # Select appropriate template based on post type
        templates = {
            "achievement": self.achievement_templates,
            "insight": self.insight_templates,
            "question": self.question_templates,
            "announcement": self.announcement_templates,
            "motivational": self.motivational_templates,
            "generic": self.generic_templates,
        }

        template_set = templates.get(analysis["type"], self.generic_templates)
        base_comment = random.choice(template_set[self.style])

        # Occasionally add topic-specific addition (30% chance)
        if analysis["topics"] and random.random() < 0.3:
            topic = random.choice(analysis["topics"])
            if topic in self.topic_additions:
                addition = random.choice(self.topic_additions[topic])
                base_comment = f"{base_comment} {addition}"

        # Add emoji occasionally for casual/enthusiastic styles (20% chance)
        if self.style in ["casual", "enthusiastic"] and random.random() < 0.2:
            emoji_type = "achievement" if analysis["type"] == "achievement" else "positive"
            if emoji_type in self.emojis:
                emoji = random.choice(self.emojis[emoji_type])
                base_comment = f"{base_comment} {emoji}"

        # Personalize with author name occasionally (15% chance)
        if author_name and random.random() < 0.15:
            first_name = author_name.split()[0]
            name_prefix = random.choice([
                f"Great post, {first_name}!",
                f"Thanks for sharing, {first_name}.",
                f"Well said, {first_name}.",
            ])
            base_comment = name_prefix

        return base_comment

    def generate_contextual_comment(
        self,
        post_content: str,
        key_points: Optional[List[str]] = None
    ) -> str:
        """
        Generate a more contextual comment by referencing specific points.

        Args:
            post_content: The post's text content
            key_points: Optional list of key points extracted from the post

        Returns:
            Generated contextual comment
        """
        analysis = self.analyze_post(post_content)

        # Extract potential talking points from content
        sentences = re.split(r'[.!?]', post_content)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

        # Generate context-aware comment
        if analysis["type"] == "achievement":
            return self._generate_achievement_comment(post_content, analysis)
        elif analysis["type"] == "insight":
            return self._generate_insight_comment(post_content, analysis, sentences)
        elif analysis["type"] == "question":
            return self._generate_question_comment(post_content, analysis)
        else:
            return self.generate_comment(post_content)

    def _generate_achievement_comment(self, content: str, analysis: Dict) -> str:
        """Generate comment for achievement posts."""
        content_lower = content.lower()

        # Detect specific achievement types
        if "new role" in content_lower or "joining" in content_lower or "started" in content_lower:
            return random.choice([
                "Congratulations on the new role! Exciting times ahead.",
                "Great move! Wishing you all the best in your new position.",
                "Congratulations! Looking forward to seeing what you accomplish.",
                "Exciting news! Best of luck in your new role.",
            ])
        elif "promotion" in content_lower:
            return random.choice([
                "Congratulations on the promotion! Well deserved.",
                "Great news! The hard work paid off. Congratulations!",
                "Well earned promotion! Congratulations!",
            ])
        elif "launch" in content_lower or "shipped" in content_lower:
            return random.choice([
                "Congratulations on the launch! Exciting to see this come to life.",
                "Great to see this ship! Congratulations on the launch.",
                "Congrats on the launch! Looking forward to checking it out.",
            ])
        else:
            return random.choice(self.achievement_templates[self.style])

    def _generate_insight_comment(self, content: str, analysis: Dict, sentences: List[str]) -> str:
        """Generate comment for insight/educational posts."""
        content_lower = content.lower()

        # Reference specific topics if detected
        if "ai" in analysis["topics"] or "artificial intelligence" in content_lower:
            return random.choice([
                "Great perspective on AI. The space is evolving rapidly.",
                "Interesting AI insight. Thanks for sharing.",
                "Good point about AI. Appreciate the perspective.",
            ])
        elif "leadership" in analysis["topics"]:
            return random.choice([
                "Great leadership insight. This resonates.",
                "Valuable leadership lesson. Thanks for sharing.",
                "Good leadership perspective. Appreciate you sharing this.",
            ])
        elif "career" in analysis["topics"]:
            return random.choice([
                "Valuable career advice. Thanks for sharing.",
                "Great career insight. Appreciate you posting this.",
                "Helpful perspective. Thanks for sharing.",
            ])
        else:
            return random.choice(self.insight_templates[self.style])

    def _generate_question_comment(self, content: str, analysis: Dict) -> str:
        """Generate comment for question/discussion posts."""
        return random.choice([
            "Great question! Looking forward to the discussion.",
            "Interesting topic. Curious to see different perspectives.",
            "Good question. This is worth exploring.",
            "Thought-provoking question. Thanks for starting this discussion.",
        ])

    def validate_comment(self, comment: str) -> bool:
        """
        Validate that a comment is appropriate and natural.

        Args:
            comment: Comment text to validate

        Returns:
            True if comment passes validation
        """
        if not comment:
            return False

        # Check length (LinkedIn comments should be concise)
        if len(comment) < 10 or len(comment) > 300:
            return False

        # Check for spam-like patterns
        spam_patterns = [
            r"check out my",
            r"visit my profile",
            r"follow me",
            r"dm me",
            r"message me",
            r"http[s]?://",
            r"www\.",
            r"click here",
            r"buy now",
            r"free money",
        ]

        comment_lower = comment.lower()
        for pattern in spam_patterns:
            if re.search(pattern, comment_lower):
                return False

        return True

    def set_style(self, style: str):
        """
        Change the comment style.

        Args:
            style: 'professional', 'casual', or 'enthusiastic'
        """
        if style in ["professional", "casual", "enthusiastic"]:
            self.style = style
        else:
            print(f"Unknown style: {style}. Using 'professional'.")
            self.style = "professional"
