from __future__ import annotations

import streamlit as st

from .recommender import HotelRecommendationEngine
from .price_anomaly import HotelPriceAnomalyDetector
from .insights import HotelInsightsEngine


@st.cache_resource
def get_engine():
    return HotelRecommendationEngine()


def main() -> None:
    st.set_page_config(page_title="AI Hotel Recommendation", layout="wide")
    st.title("AI Hotel Recommendation & Price Prediction")

    engine = get_engine()

    with st.sidebar:
        st.header("User preferences")
        budget = st.slider("Budget (INR)", 2000, 20000, 7000, 500)
        min_rating = st.slider("Minimum rating", 3.0, 5.0, 4.0, 0.1)
        location = st.selectbox("Preferred city", ["Any", *sorted({hotel.location for hotel in engine.hotels})])
        room_type = st.selectbox("Room type", ["Any", *sorted({hotel.room_type for hotel in engine.hotels})])
        guests = st.slider("Guests", 1, 6, 2)
        season = st.selectbox("Season", ["low", "normal", "peak"])
        amenities = st.multiselect(
            "Amenities",
            sorted({amenity for hotel in engine.hotels for amenity in hotel.amenities}),
        )

    preferences = {
        "budget": budget,
        "min_rating": min_rating,
        "location": location,
        "room_type": room_type,
        "guests": guests,
        "season": season,
        "amenities": amenities,
    }

    recommendations = engine.recommend(preferences, top_n=5)

    st.subheader("Top hotel matches")
    for hotel in recommendations:
        with st.container():
            st.markdown(
                f"### {hotel['hotel_name']} — {hotel['location']}"
                f"\n- Rating: {hotel['rating']}\n- Price: INR {hotel['price']}\n- Predicted price: INR {hotel['predicted_price']}\n- Overall score: {hotel['overall_score']}\n- Sentiment: {hotel['sentiment']:.2f}\n- Amenities: {', '.join(hotel['amenities'])}"
            )

    st.subheader("Hotel table")
    hotel_table = [
        {
            "Hotel": item["hotel_name"],
            "Location": item["location"],
            "Rating": item["rating"],
            "Price": item["price"],
            "Predicted Price": item["predicted_price"],
            "Score": item["overall_score"],
        }
        for item in recommendations
    ]
    st.dataframe(hotel_table, use_container_width=True)

    st.subheader("AI-generated insights")
    for insight in engine.generate_insights(recommendations):
        st.write("- " + insight)

    st.subheader("Why these hotels match")
    for explanation in HotelInsightsEngine().generate_many(recommendations, preferences):
        st.write(f"**{explanation['hotel_name']}**: {explanation['summary']}")

    st.subheader("Price anomaly watch")
    anomaly_rows = HotelPriceAnomalyDetector(engine).detect(guests=guests, season=season)[:5]
    anomaly_table = [
        {
            "Hotel": item["hotel_name"],
            "Observed Price": item["observed_price"],
            "Expected Price": item["expected_price"],
            "Difference (%)": item["percentage_delta"],
            "Status": item["label"],
        }
        for item in anomaly_rows
    ]
    st.dataframe(anomaly_table, use_container_width=True)


if __name__ == "__main__":
    main()
