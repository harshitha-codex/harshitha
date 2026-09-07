from hotel_ai.eda import HotelEDA
from hotel_ai.insights import HotelInsightsEngine
from hotel_ai.price_anomaly import HotelPriceAnomalyDetector
from hotel_ai.price_prediction import HotelPricePredictor
from hotel_ai.recommender import HotelRecommendationEngine
from hotel_ai.sentiment_analysis import HotelSentimentAnalyzer
from hotel_ai.user_preference import UserPreferencePredictor


def test_recommendation_returns_ranked_hotels() -> None:
    engine = HotelRecommendationEngine()
    results = engine.recommend({"budget": 7000, "location": "Bangalore", "min_rating": 4.0}, top_n=3)
    assert len(results) == 3
    assert results[0]["overall_score"] >= results[-1]["overall_score"]


def test_price_prediction_returns_positive_value() -> None:
    result = HotelPricePredictor().predict({"location": "Bangalore", "rating": 4.6, "room_type": "Deluxe"})
    assert result["predicted_price"] > 0


def test_sentiment_and_insights() -> None:
    sentiment = HotelSentimentAnalyzer().classify("The hotel was clean and the staff was friendly")
    assert sentiment["label"] == "positive"
    explanation = HotelInsightsEngine().generate(
        {"hotel_name": "Test Hotel", "rating": 4.8, "price": 5000, "predicted_price": 4800, "sentiment": 0.9},
        {"budget": 6000},
    )
    assert explanation["recommendation"] == "Best-value option"


def test_anomaly_detection_covers_all_hotels() -> None:
    results = HotelPriceAnomalyDetector().detect()
    assert len(results) == 12
    assert "percentage_delta" in results[0]


def test_user_preference_prediction() -> None:
    result = UserPreferencePredictor().predict({"budget": 6000, "purpose": "business"})
    assert result["predicted_location"]
    assert result["predicted_room_type"]


def test_eda_summary() -> None:
    report = HotelEDA().generate_report()
    assert report["summary"]["total_hotels"] == 12
    assert report["insights"]
