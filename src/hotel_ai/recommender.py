from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from .data import Hotel
from .kaggle_loader import load_hotels_from_source


class HotelRecommendationEngine:
    def __init__(self, dataset_slug: str | None = None, dataset_path: str | None = None) -> None:
        self.hotels: List[Hotel] = load_hotels_from_source(
            dataset_slug=dataset_slug,
            dataset_path=dataset_path,
        )
        self.price_model = self._build_price_model()

    def _build_price_model(self) -> Pipeline:
        rows = []
        for hotel in self.hotels:
            for season in ["low", "normal", "peak"]:
                for guests in [1, 2, 4]:
                    season_factor = {"low": 0.82, "normal": 1.0, "peak": 1.18}[season]
                    guest_factor = {1: 0.92, 2: 1.0, 4: 1.16}[guests]
                    predicted = hotel.price * season_factor * guest_factor
                    rows.append(
                        {
                            "hotel_name": hotel.name,
                            "location": hotel.location,
                            "rating": hotel.rating,
                            "distance_km": hotel.distance_km,
                            "reviews": hotel.reviews,
                            "room_type": hotel.room_type,
                            "amenity_count": len(hotel.amenities),
                            "season": season,
                            "guests": guests,
                            "price": round(predicted, 2),
                        }
                    )

        df = pd.DataFrame(rows)
        features = ["location", "rating", "distance_km", "reviews", "room_type", "amenity_count", "season", "guests"]
        X = df[features]
        y = df["price"]

        preprocessor = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore"), ["location", "room_type", "season"]),
            ],
            remainder="passthrough",
        )

        model = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("regressor", RandomForestRegressor(n_estimators=200, random_state=42)),
            ]
        )
        model.fit(X, y)
        return model

    def predict_price(self, hotel: Hotel | str, guests: int = 2, season: str = "normal") -> float:
        if isinstance(hotel, str):
            hotel = next(item for item in self.hotels if item.name.lower() == hotel.lower())

        row = {
            "location": hotel.location,
            "rating": hotel.rating,
            "distance_km": hotel.distance_km,
            "reviews": hotel.reviews,
            "room_type": hotel.room_type,
            "amenity_count": len(hotel.amenities),
            "season": season,
            "guests": guests,
        }
        df = pd.DataFrame([row])
        price = float(self.price_model.predict(df)[0])
        return round(price, 2)

    def recommend(self, preferences: Dict[str, Any], top_n: int = 5) -> List[Dict[str, Any]]:
        budget = float(preferences.get("budget", 7000))
        min_rating = float(preferences.get("min_rating", 4.0))
        preferred_location = str(preferences.get("location", "Any")).strip().lower()
        preferred_amenities = {item.lower() for item in preferences.get("amenities", [])}
        room_type = str(preferences.get("room_type", "Any")).strip().lower()
        guests = int(preferences.get("guests", 2))
        season = str(preferences.get("season", "normal")).strip().lower()

        ranked = []
        for hotel in self.hotels:
            if hotel.rating < min_rating:
                continue
            if hotel.price > budget * 1.5:
                continue

            location_score = 1.0 if preferred_location in {"any", ""} or hotel.location.lower() == preferred_location else 0.6
            room_score = 1.0 if room_type in {"any", ""} or hotel.room_type.lower() == room_type.lower() else 0.7
            price_gap = abs(hotel.price - budget)
            price_score = max(0.0, 1.0 - (price_gap / max(budget, 1)))
            rating_score = hotel.rating / 5.0
            sentiment_score = hotel.sentiment
            amenity_match = 0.0
            if preferred_amenities:
                match_count = sum(1 for item in preferred_amenities if item in {a.lower() for a in hotel.amenities})
                amenity_match = match_count / len(preferred_amenities)
            else:
                amenity_match = 0.5

            composite = (
                0.32 * rating_score +
                0.18 * price_score +
                0.20 * sentiment_score +
                0.18 * amenity_match +
                0.07 * location_score +
                0.05 * room_score
            )

            if preferred_location not in {"any", ""} and hotel.location.lower() == preferred_location:
                composite += 0.05

            predicted_price = self.predict_price(hotel, guests=guests, season=season)
            price_delta = abs(predicted_price - budget)
            value_score = max(0.0, 1.0 - (price_delta / max(budget, 1)))

            final_score = round((composite * 0.8 + value_score * 0.2) * 100, 2)
            ranked.append(
                {
                    "hotel_name": hotel.name,
                    "location": hotel.location,
                    "rating": hotel.rating,
                    "price": hotel.price,
                    "predicted_price": predicted_price,
                    "reviews": hotel.reviews,
                    "room_type": hotel.room_type,
                    "amenities": hotel.amenities,
                    "overall_score": final_score,
                    "value_score": round(hotel.value_score, 1),
                    "sentiment": hotel.sentiment,
                }
            )

        ranked.sort(key=lambda item: item["overall_score"], reverse=True)
        return ranked[: max(1, top_n)]

    def generate_insights(self, recommendation: List[Dict[str, Any]]) -> List[str]:
        insights = []
        for hotel in recommendation:
            candidate = f"{hotel['hotel_name']} in {hotel['location']} offers a {hotel['rating']} star experience with a predicted price of INR {hotel['predicted_price']}."
            if hotel["sentiment"] >= 0.8:
                candidate += " Guest sentiment is very strong and the hotel is likely a high-value option."
            else:
                candidate += " Guest sentiment is moderate, so price and amenities should be reviewed before booking."
            insights.append(candidate)
        return insights
