from __future__ import annotations

import re
from typing import Any


class HotelSentimentAnalyzer:
    def __init__(self) -> None:
        self.positive_words = {
            "good", "great", "excellent", "clean", "friendly", "helpful", "comfortable", "spacious",
            "beautiful", "amazing", "nice", "safe", "fast", "delicious", "breakfast", "service",
            "wonderful", "pleasant", "value", "smooth", "happy"
        }
        self.negative_words = {
            "bad", "poor", "dirty", "unsafe", "slow", "noisy", "rude", "unhelpful", "broken",
            "small", "expensive", "smelly", "average", "late", "terrible", "awful", "cold"
        }

    def _normalize(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    def classify(self, review_text: str) -> dict[str, Any]:
        normalized = self._normalize(review_text)
        words = normalized.split()

        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        total_score = positive_count - negative_count

        if total_score > 0:
            label = "positive"
        elif total_score < 0:
            label = "negative"
        else:
            label = "neutral"

        confidence = min(0.99, max(0.5, 0.5 + (abs(total_score) / max(1, len(words) + 1)) * 1.3))

        return {
            "label": label,
            "confidence": round(confidence, 3),
            "positive_hits": positive_count,
            "negative_hits": negative_count,
            "score": total_score,
        }
