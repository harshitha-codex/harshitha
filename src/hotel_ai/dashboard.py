from __future__ import annotations

import html

import streamlit as st

from .recommender import HotelRecommendationEngine
from .price_anomaly import HotelPriceAnomalyDetector
from .insights import HotelInsightsEngine


@st.cache_resource
def get_engine():
    return HotelRecommendationEngine()


def main() -> None:
    st.set_page_config(page_title="AI Hotel Recommendation", layout="wide")

    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1600&q=80");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-color: #ffffff;
            filter: none;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .title-box {
            background: #ffffff !important;
            border: 1px solid rgba(17, 24, 39, 0.12);
            border-radius: 16px;
            padding: 0.7rem 1.2rem;
            margin-bottom: 1rem;
            width: fit-content;
            max-width: 100%;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        }

        .title-box h1 {
            color: #000000 !important;
            margin: 0 !important;
            font-weight: 800 !important;
            opacity: 1 !important;
        }

        .hotel-card {
            background: #ffffff !important;
            color: #111827 !important;
            border: 1px solid rgba(17, 24, 39, 0.10);
            border-radius: 14px;
            padding: 20px 20px 18px 20px;
            margin-bottom: 1rem;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.10);
            opacity: 1 !important;
            display: block;
            width: 100%;
            position: relative;
            z-index: 2;
            filter: none !important;
            line-height: 1.6;
        }

        .hotel-card h3,
        .hotel-card p,
        .hotel-card li,
        .hotel-card ul,
        .stSubheader,
        .stDataFrame,
        .stTable,
        h1, h2, h3, p, li, label, .stSelectbox, .stSlider, .stMultiSelect {
            color: #111827 !important;
            opacity: 1 !important;
            filter: none !important;
            text-shadow: none !important;
            font-weight: 700 !important;
        }

        .hotel-card ul {
            margin: 0.5rem 0 0 1.1rem;
            padding-left: 1rem;
        }

        .stDataFrame {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            padding: 0.4rem;
        }

        div[data-testid="stSidebar"] > div:first-child {
            background: rgba(255, 255, 255, 0.78);
            border-right: 1px solid rgba(17, 24, 39, 0.12);
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: #ffffff !important;
            border: 1px solid rgba(17, 24, 39, 0.10) !important;
            border-radius: 14px !important;
            padding: 0.75rem 1rem 0.5rem 1rem !important;
            margin-bottom: 1rem !important;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.10) !important;
        }

        div[data-testid="stLayoutWrapper"] {
            background: #ffffff !important;
            border: 1px solid rgba(17, 24, 39, 0.10) !important;
            border-radius: 14px !important;
            padding: 0.75rem 1rem 0.5rem 1rem !important;
            margin-bottom: 1rem !important;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.10) !important;
        }

        div[data-testid="stMarkdownContainer"]:has(> ul > li),
        div[data-testid="stMarkdownContainer"]:has(> p > strong) {
            background: #ffffff !important;
            border: 1px solid rgba(17, 24, 39, 0.10) !important;
            border-radius: 14px !important;
            padding: 0.75rem 1rem 0.5rem 1rem !important;
            margin-bottom: 1rem !important;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.10) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.html(
        """
        <div class="title-box">
            <h1>AI Hotel Recommendation & Price Prediction</h1>
        </div>
        """
    )

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
        hotel_name = html.escape(str(hotel["hotel_name"]))
        location = html.escape(str(hotel["location"]))
        rating = html.escape(str(hotel["rating"]))
        price = html.escape(str(hotel["price"]))
        predicted_price = html.escape(str(hotel["predicted_price"]))
        overall_score = html.escape(str(hotel["overall_score"]))
        sentiment = html.escape(f"{hotel['sentiment']:.2f}")
        amenities = html.escape(", ".join(hotel["amenities"]))

        with st.container(border=True):
            st.markdown(
                f"""
                <div class="hotel-card">
                    <h3>{hotel_name} — {location}</h3>
                    <ul>
                        <li>Rating: {rating}</li>
                        <li>Price: INR {price}</li>
                        <li>Predicted price: INR {predicted_price}</li>
                        <li>Overall score: {overall_score}</li>
                        <li>Sentiment: {sentiment}</li>
                        <li>Amenities: {amenities}</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
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
        st.markdown(
            f"""
            <div class="hotel-card">
                <h3>{html.escape(str(insight))}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Why these hotels match")
    for explanation in HotelInsightsEngine().generate_many(recommendations, preferences):
        explanation_name = html.escape(str(explanation["hotel_name"]))
        explanation_summary = html.escape(str(explanation["summary"]))
        st.markdown(
            f"""
            <div class="hotel-card">
                <h3>{explanation_name}</h3>
                <p>{explanation_summary}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
