from __future__ import annotations

from typing import Any

import numpy as np

from .data import Hotel
from .recommender import HotelRecommendationEngine


class HotelPriceAnomalyDetector:
    """Compare observed hotel prices with model-estimated expected prices."""

    def __init__(self, engine: HotelRecommendationEngine | None = None) -> None:
        self.engine = engine or HotelRecommendationEngine()

    def analyze_hotel(self, hotel: Hotel, guests: int = 2, season: str = "normal") -> dict[str, Any]:
        expected_price = self.engine.predict_price(hotel, guests=guests, season=season)
        difference = round(hotel.price - expected_price, 2)
        percentage_delta = round((difference / expected_price) * 100, 2) if expected_price else 0.0

        if percentage_delta >= 20:
            label = "high_price_anomaly"
        elif percentage_delta <= -20:
            label = "low_price_anomaly"
        else:
            label = "normal"

        return {
            "hotel_name": hotel.name,
            "location": hotel.location,
            "observed_price": round(hotel.price, 2),
            "expected_price": expected_price,
            "difference": difference,
            "percentage_delta": percentage_delta,
            "label": label,
        }

    def detect(self, guests: int = 2, season: str = "normal") -> list[dict[str, Any]]:
        results = [self.analyze_hotel(hotel, guests=guests, season=season) for hotel in self.engine.hotels]
        deltas = np.array([item["percentage_delta"] for item in results], dtype=float)
        mean_delta = float(deltas.mean()) if len(deltas) else 0.0
        standard_deviation = float(deltas.std()) if len(deltas) else 0.0

        for item in results:
            item["z_score"] = round(
                (item["percentage_delta"] - mean_delta) / standard_deviation,
                3,
            ) if standard_deviation else 0.0

        return sorted(results, key=lambda item: abs(item["percentage_delta"]), reverse=True)
