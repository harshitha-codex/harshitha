from __future__ import annotations

import os
from importlib import import_module
from pathlib import Path
from typing import Any

import pandas as pd

from .data import Hotel, generate_sample_hotels


def _load_kaggle_csv(dataset_slug: str | None = None, dataset_path: str | None = None) -> pd.DataFrame | None:
    dataset_slug = dataset_slug or os.getenv("KAGGLE_DATASET_SLUG")
    dataset_path = dataset_path or os.getenv("KAGGLE_DATASET_PATH")

    if dataset_path and Path(dataset_path).exists():
        try:
            return pd.read_csv(dataset_path)
        except (OSError, pd.errors.ParserError):
            return None

    if not dataset_slug:
        return None

    try:
        kaggle_module = import_module("kaggle.api.kaggle_api_extended")
        kaggle_api = kaggle_module.KaggleApi()
    except ImportError:
        return None

    try:
        kaggle_api.authenticate()
        if dataset_slug:
            target_dir = Path("data") / "kaggle"
            target_dir.mkdir(parents=True, exist_ok=True)
            kaggle_api.dataset_download_files(dataset_slug, path=str(target_dir), unzip=True)
            files = list(target_dir.glob("*.csv"))
            if files:
                return pd.read_csv(files[0])
    except Exception:
        return None

    return None


def _coerce_hotel_rows(frame: pd.DataFrame) -> list[Hotel]:
    rename_map = {
        "hotel_name": "name",
        "hotel": "name",
        "name": "name",
        "city": "location",
        "location": "location",
        "price": "price",
        "avg_price": "price",
        "rating": "rating",
        "stars": "rating",
        "review_count": "reviews",
        "reviews": "reviews",
        "room_type": "room_type",
        "room": "room_type",
        "amenities": "amenities",
        "distance": "distance_km",
        "distance_from_city_center": "distance_km",
        "sentiment": "sentiment",
        "sentiment_score": "sentiment",
        "value_score": "value_score",
    }

    cleaned = frame.copy()
    cleaned = cleaned.rename(columns={key: value for key, value in rename_map.items() if key in cleaned.columns})

    if "amenities" in cleaned.columns:
        cleaned["amenities"] = cleaned["amenities"].apply(lambda value: str(value).split("|") if isinstance(value, str) else [])
    else:
        cleaned["amenities"] = [[] for _ in range(len(cleaned))]

    normalized = []
    for _, row in cleaned.iterrows():
        hotel_name = str(row.get("name") or "Hotel")
        location = str(row.get("location") or "Unknown")
        rating = float(row.get("rating") or 4.0)
        price = float(row.get("price") or 0.0)
        reviews = int(row.get("reviews") or 0)
        room_type = str(row.get("room_type") or "Standard")
        amenities = row.get("amenities")
        if not isinstance(amenities, list):
            amenities = []
        distance_km = float(row.get("distance_km") or 0.0)
        sentiment = float(row.get("sentiment") or 0.7)
        value_score = float(row.get("value_score") or ((rating * 20) + (sentiment * 50)))

        normalized.append(
            Hotel(
                name=hotel_name,
                location=location,
                rating=rating,
                price=price,
                reviews=reviews,
                room_type=room_type,
                amenities=[str(item).lower() for item in amenities],
                distance_km=distance_km,
                sentiment=sentiment,
                value_score=value_score,
            )
        )

    return normalized


def load_hotels_from_source(dataset_slug: str | None = None, dataset_path: str | None = None) -> list[Hotel]:
    frame = _load_kaggle_csv(dataset_slug=dataset_slug, dataset_path=dataset_path)
    if frame is None or frame.empty:
        return generate_sample_hotels()
    return _coerce_hotel_rows(frame)


def load_hotel_dataframe(dataset_slug: str | None = None, dataset_path: str | None = None) -> pd.DataFrame:
    hotels = load_hotels_from_source(dataset_slug=dataset_slug, dataset_path=dataset_path)
    rows = [hotel.to_dict() for hotel in hotels]
    return pd.DataFrame(rows)
