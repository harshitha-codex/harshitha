from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from .preprocessing import HotelPreprocessor


class HotelPricePredictor:
    def __init__(self) -> None:
        self.preprocessor = HotelPreprocessor()
        self.model = self._train_model()

    def _train_model(self) -> Pipeline:
        df = self.preprocessor.fit_transform()
        if df.empty:
            raise ValueError("No hotel data available for training.")

        feature_columns = [
            "location",
            "rating",
            "distance_km",
            "reviews",
            "room_type",
            "amenity_count",
            "sentiment",
            "value_score",
        ]

        X = df[feature_columns]
        y = df["price"]

        pre = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore"), ["location", "room_type"]),
            ],
            remainder="passthrough",
        )

        model = Pipeline(
            steps=[
                ("preprocessor", pre),
                ("regressor", RandomForestRegressor(n_estimators=300, random_state=42)),
            ]
        )
        model.fit(X, y)
        return model

    def predict(self, record: dict[str, Any]) -> dict[str, Any]:
        row = {
            "location": record.get("location", "Bangalore"),
            "rating": float(record.get("rating", 4.2)),
            "distance_km": float(record.get("distance_km", 3.0)),
            "reviews": int(record.get("reviews", 1000)),
            "room_type": record.get("room_type", "Deluxe"),
            "amenity_count": int(record.get("amenity_count", 3)),
            "sentiment": float(record.get("sentiment", 0.8)),
            "value_score": float(record.get("value_score", 80)),
        }

        df = pd.DataFrame([row])
        prediction = float(self.model.predict(df)[0])
        return {
            "predicted_price": round(prediction, 2),
            "currency": "INR",
            "input": row,
        }
