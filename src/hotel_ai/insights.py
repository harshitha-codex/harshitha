from __future__ import annotations

from typing import Any


class HotelInsightsEngine:
    """Turn model outputs into concise, user-facing hotel explanations."""

    def generate(self, hotel: dict[str, Any], preferences: dict[str, Any] | None = None) -> dict[str, Any]:
        preferences = preferences or {}
        budget = float(preferences.get("budget", hotel.get("price", 0)))
        predicted_price = float(hotel.get("predicted_price", hotel.get("price", 0)))
        rating = float(hotel.get("rating", 0))
        sentiment = float(hotel.get("sentiment", 0.5))
        amenities = [str(item) for item in hotel.get("amenities", [])]

        reasons: list[str] = []
        if rating >= 4.5:
            reasons.append("excellent guest rating")
        elif rating >= 4.0:
            reasons.append("strong guest rating")
        if sentiment >= 0.8:
            reasons.append("highly positive review sentiment")
        if predicted_price <= budget:
            reasons.append("predicted price is within budget")
        if amenities:
            reasons.append(f"includes {', '.join(amenities[:3])}")

        if not reasons:
            reasons.append("matches the selected hotel preferences")

        return {
            "hotel_name": hotel.get("hotel_name", "Hotel"),
            "recommendation": "Best-value option" if predicted_price <= budget and rating >= 4.3 else "Worth considering",
            "reasons": reasons,
            "summary": f"{hotel.get('hotel_name', 'This hotel')} is recommended because it offers {', '.join(reasons)}.",
        }

    def generate_many(self, hotels: list[dict[str, Any]], preferences: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        return [self.generate(hotel, preferences) for hotel in hotels]
