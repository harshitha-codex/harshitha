from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from .data import generate_sample_hotels


class UserPreferencePredictor:
    """Predict likely hotel location and room type from traveler preferences."""

    def __init__(self) -> None:
        self.hotels = generate_sample_hotels()
        self.location_model = self._train_model("location")
        self.room_model = self._train_model("room_type")

    def _training_frame(self) -> pd.DataFrame:
        rows: list[dict[str, Any]] = []
        purposes = ["business", "leisure", "family"]
        for hotel in self.hotels:
            for purpose in purposes:
                for budget_factor in (0.85, 1.0, 1.2):
                    budget = hotel.price * budget_factor
                    rows.append(
                        {
                            "budget": budget,
                            "preferred_rating": hotel.rating,
                            "review_count": hotel.reviews,
                            "distance_km": hotel.distance_km,
                            "stay_nights": 2 if purpose == "business" else 4,
                            "purpose": purpose,
                            "location": hotel.location,
                            "room_type": hotel.room_type,
                        }
                    )
        return pd.DataFrame(rows)

    def _train_model(self, target: str) -> Pipeline:
        frame = self._training_frame()
        features = [
            "budget",
            "preferred_rating",
            "review_count",
            "distance_km",
            "stay_nights",
            "purpose",
        ]
        categorical = ["purpose"]
        preprocessor = ColumnTransformer(
            [("categorical", OneHotEncoder(handle_unknown="ignore"), categorical)],
            remainder="passthrough",
        )
        model = Pipeline(
            [
                ("preprocessor", preprocessor),
                ("classifier", RandomForestClassifier(n_estimators=200, random_state=42)),
            ]
        )
        model.fit(frame[features], frame[target])
        return model

    def predict(self, preferences: dict[str, Any]) -> dict[str, Any]:
        row = {
            "budget": float(preferences.get("budget", 7000)),
            "preferred_rating": float(preferences.get("preferred_rating", 4.2)),
            "review_count": int(preferences.get("review_count", 1000)),
            "distance_km": float(preferences.get("distance_km", 4.0)),
            "stay_nights": int(preferences.get("stay_nights", 3)),
            "purpose": str(preferences.get("purpose", "leisure")).lower(),
        }
        frame = pd.DataFrame([row])
        location = str(self.location_model.predict(frame)[0])
        room_type = str(self.room_model.predict(frame)[0])
        location_confidence = float(max(self.location_model.predict_proba(frame)[0]))
        room_confidence = float(max(self.room_model.predict_proba(frame)[0]))
        return {
            "predicted_location": location,
            "location_confidence": round(location_confidence, 3),
            "predicted_room_type": room_type,
            "room_confidence": round(room_confidence, 3),
            "input": row,
        }
