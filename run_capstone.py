from __future__ import annotations

from hotel_ai.eda import HotelEDA
from hotel_ai.insights import HotelInsightsEngine
from hotel_ai.price_anomaly import HotelPriceAnomalyDetector
from hotel_ai.price_prediction import HotelPricePredictor
from hotel_ai.recommender import HotelRecommendationEngine
from hotel_ai.sentiment_analysis import HotelSentimentAnalyzer
from hotel_ai.user_preference import UserPreferencePredictor


def main() -> None:
    preferences = {
        "budget": 7000,
        "location": "Bangalore",
        "min_rating": 4.0,
        "purpose": "leisure",
        "guests": 2,
    }

    engine = HotelRecommendationEngine()
    recommendations = engine.recommend(preferences, top_n=5)
    report = HotelEDA().generate_report()
    price = HotelPricePredictor().predict(
        {
            "location": "Bangalore",
            "rating": 4.6,
            "distance_km": 2.5,
            "reviews": 1800,
            "room_type": "Deluxe",
            "amenity_count": 4,
        }
    )
    sentiment = HotelSentimentAnalyzer().classify("The rooms were clean and the staff was extremely helpful.")
    preference = UserPreferencePredictor().predict(preferences)
    anomalies = HotelPriceAnomalyDetector(engine).detect()[:3]
    explanations = HotelInsightsEngine().generate_many(recommendations, preferences)

    print("AI HOTEL CAPSTONE REPORT")
    print(f"Hotels analyzed: {report['summary']['total_hotels']}")
    print(f"Top recommendation: {recommendations[0]['hotel_name']}")
    print(f"Predicted sample price: INR {price['predicted_price']}")
    print(f"Review sentiment: {sentiment['label']} ({sentiment['confidence']})")
    print(f"Predicted traveler destination: {preference['predicted_location']}")
    print(f"Largest price variance: {anomalies[0]['hotel_name']} ({anomalies[0]['percentage_delta']}%)")
    print(f"Generated explanations: {len(explanations)}")
    print("CAPSTONE RUN OK")


if __name__ == "__main__":
    main()
