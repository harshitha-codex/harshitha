from __future__ import annotations

from typing import Any, Dict, List

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .recommender import HotelRecommendationEngine
from .price_anomaly import HotelPriceAnomalyDetector
from .insights import HotelInsightsEngine
from .monitoring import RecommendationMonitor
from .user_preference import UserPreferencePredictor

app = FastAPI(title="AI Hotel Recommendation API")
engine = HotelRecommendationEngine()
preference_predictor = UserPreferencePredictor()
anomaly_detector = HotelPriceAnomalyDetector(engine)
insights_engine = HotelInsightsEngine()
monitor = RecommendationMonitor()


class RecommendRequest(BaseModel):
    budget: float = Field(default=7000, gt=0)
    min_rating: float = Field(default=4.0, ge=0, le=5)
    location: str = "Any"
    amenities: List[str] = []
    room_type: str = "Any"
    guests: int = 2
    season: str = "normal"


class PriceRequest(BaseModel):
    hotel_name: str
    guests: int = 2
    season: str = "normal"


class PreferenceRequest(BaseModel):
    budget: float = Field(default=7000, gt=0)
    preferred_rating: float = Field(default=4.2, ge=0, le=5)
    review_count: int = Field(default=1000, ge=0)
    distance_km: float = Field(default=4.0, ge=0)
    stay_nights: int = Field(default=3, ge=1)
    purpose: str = "leisure"


class AnomalyRequest(BaseModel):
    guests: int = Field(default=2, ge=1)
    season: str = "normal"


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/hotels")
def list_hotels() -> List[Dict[str, Any]]:
    return [hotel.to_dict() for hotel in engine.hotels]


@app.post("/recommend")
def recommend(request: RecommendRequest) -> Dict[str, Any]:
    recommendations = engine.recommend(request.model_dump(), top_n=5)
    monitor.record("recommendation_request", {"count": len(recommendations)})
    return {
        "recommendations": recommendations,
        "insights": engine.generate_insights(recommendations),
        "explanations": insights_engine.generate_many(recommendations, request.model_dump()),
    }


@app.post("/predict-price")
def predict_price(request: PriceRequest) -> Dict[str, Any]:
    hotel = next((item for item in engine.hotels if item.name.lower() == request.hotel_name.lower()), None)
    if hotel is None:
        return {"error": "Hotel not found"}
    return {
        "hotel_name": hotel.name,
        "predicted_price": engine.predict_price(hotel, guests=request.guests, season=request.season),
    }


@app.post("/predict-preferences")
def predict_preferences(request: PreferenceRequest) -> Dict[str, Any]:
    return preference_predictor.predict(request.model_dump())


@app.post("/detect-price-anomalies")
def detect_price_anomalies(request: AnomalyRequest) -> Dict[str, Any]:
    results = anomaly_detector.detect(guests=request.guests, season=request.season)
    monitor.record("anomaly_scan", {"count": len(results)})
    return {"anomalies": results, "count": len(results)}


@app.get("/monitoring")
def monitoring_summary() -> Dict[str, Any]:
    return monitor.summary()
