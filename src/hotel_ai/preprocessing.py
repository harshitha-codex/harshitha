from __future__ import annotations

from typing import Any

import pandas as pd

from .kaggle_loader import load_hotel_dataframe


class HotelPreprocessor:
    def __init__(self) -> None:
        self.df: pd.DataFrame | None = None

    def fit_transform(self, dataset_slug: str | None = None, dataset_path: str | None = None) -> pd.DataFrame:
        df = load_hotel_dataframe(dataset_slug=dataset_slug, dataset_path=dataset_path)
        cleaned = df.copy()

        if cleaned.empty:
            return cleaned

        if "amenities" in cleaned.columns:
            cleaned["amenities"] = cleaned["amenities"].apply(
                lambda value: value if isinstance(value, list) else str(value).split("|") if isinstance(value, str) and value else []
            )
        else:
            cleaned["amenities"] = [[] for _ in range(len(cleaned))]

        cleaned["amenities_hash"] = cleaned["amenities"].apply(lambda value: tuple(sorted(str(item).lower() for item in value)))
        cleaned = cleaned.drop_duplicates(subset=[col for col in cleaned.columns if col != "amenities"]).reset_index(drop=True)
        cleaned = cleaned.drop(columns=["amenities_hash"])

        cleaned["name"] = cleaned["name"].fillna("Unnamed Hotel")
        cleaned["location"] = cleaned["location"].fillna("Unknown")
        cleaned["room_type"] = cleaned["room_type"].fillna("Standard")
        cleaned["price"] = pd.to_numeric(cleaned["price"], errors="coerce").fillna(0)
        cleaned["rating"] = pd.to_numeric(cleaned["rating"], errors="coerce").fillna(4.0)
        cleaned["reviews"] = pd.to_numeric(cleaned["reviews"], errors="coerce").fillna(0)
        cleaned["distance_km"] = pd.to_numeric(cleaned["distance_km"], errors="coerce").fillna(5.0)
        cleaned["sentiment"] = pd.to_numeric(cleaned["sentiment"], errors="coerce").fillna(0.7)
        cleaned["value_score"] = pd.to_numeric(cleaned["value_score"], errors="coerce").fillna(cleaned["rating"] * 20)

        cleaned["amenity_count"] = cleaned["amenities"].apply(len)
        cleaned["price_band"] = pd.cut(
            cleaned["price"],
            bins=[0, 4000, 7000, 10000, float("inf")],
            labels=["budget", "mid", "premium", "luxury"],
            right=False,
        )
        cleaned["review_quality"] = cleaned["reviews"].apply(lambda x: "high" if x > 1500 else "medium" if x > 500 else "low")
        cleaned["rating_bucket"] = cleaned["rating"].apply(lambda x: "excellent" if x >= 4.5 else "good" if x >= 4.0 else "basic")

        self.df = cleaned
        return cleaned

    def get_feature_table(self) -> pd.DataFrame:
        if self.df is None:
            return self.fit_transform()
        return self.df
