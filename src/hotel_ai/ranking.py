from __future__ import annotations

from typing import Any


class HotelRankingEngine:
    def __init__(self) -> None:
        pass

    def rank_hotels(self, hotels: list[dict[str, Any]]) -> list[dict[str, Any]]:
        ranked = []
        for hotel in hotels:
            rating = float(hotel.get("rating", 0))
            price = float(hotel.get("price", 0))
            budget = float(hotel.get("budget", price if price > 0 else 5000))
            sentiment = float(hotel.get("sentiment", 0.5))
            amenities = hotel.get("amenities", [])
            amenity_score = min(1.0, len(amenities) / 5)

            price_ratio = 1.0 if budget <= 0 else max(0.0, 1.0 - abs(price - budget) / max(budget, 1))
            rating_score = rating / 5.0
            sentiment_score = sentiment

            combined = (
                0.35 * rating_score +
                0.20 * price_ratio +
                0.25 * sentiment_score +
                0.20 * amenity_score
            ) * 100

            result = dict(hotel)
            result["ranking_score"] = round(combined, 2)
            ranked.append(result)

        ranked.sort(key=lambda item: item["ranking_score"], reverse=True)
        return ranked
