# AI Hotel Recommendation & Price Prediction System

This project contains a compact end-to-end hotel recommender built around the concepts described in the AI hotel capstone brief: hotel data generation, exploratory analysis, price prediction, recommendation scoring, and a simple interactive dashboard.

## Project modules

- `src/hotel_ai/data.py` creates a synthetic hotel dataset
- `src/hotel_ai/recommender.py` implements the recommendation engine and price predictor
- `src/hotel_ai/api.py` exposes REST endpoints with FastAPI
- `src/hotel_ai/dashboard.py` provides a Streamlit UI
- `app.py` is the entry point for the dashboard

## Quick start

1. Create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install the project in editable mode so imports work correctly:
   ```bash
   pip install -e .
   ```
4. Run the dashboard:
   ```bash
   streamlit run app.py
   ```
5. Run the API:
   ```bash
   uvicorn hotel_ai.api:app --reload
   ```

## Loading a real Kaggle dataset

This project supports Kaggle hotel data automatically.

### Option 1: download via Kaggle API

1. Create a Kaggle API token from your Kaggle account.
2. Place it in `~/.kaggle/kaggle.json`.
3. Run:
   ```bash
   export KAGGLE_DATASET_SLUG=your-kaggle-dataset-slug
   ```
   or pass the file path directly:
   ```bash
   export KAGGLE_DATASET_PATH=./data/hotel_data.csv
   ```
4. Start the app as usual. The loader will prefer the Kaggle dataset and fall back to the built-in sample data when no dataset is available.

### Option 2: use a local CSV

Put a CSV in your project and set `KAGGLE_DATASET_PATH` to its path.

## Module 4: Data preprocessing & feature engineering

The project now includes a preprocessing pipeline to clean, normalize, and engineer hotel features before model training.

```python
from hotel_ai.preprocessing import HotelPreprocessor

preprocessor = HotelPreprocessor()
prepared = preprocessor.fit_transform()
print(prepared.head())
```

This module does the following:
- removes duplicate records
- fills missing values
- normalizes numeric fields
- converts amenity strings into lists
- creates derived features like price band and review quality
- prepares a model-ready feature table

## Module 5: Hotel data exploratory analysis

The EDA module calculates summary statistics and produces practical insights for price, rating, review, and location trends.

```python
from hotel_ai.eda import HotelEDA

eda = HotelEDA()
report = eda.generate_report()
print(report)
```

Included analysis:
- average hotel price by city
- rating distribution summary
- top cities by average price
- price vs rating trend summary
- value-potential insights

## Module 6: Hotel price prediction using machine learning

This module trains a regression model to estimate hotel pricing using features such as city, rating, distance, reviews, and room type.

```python
from hotel_ai.price_prediction import HotelPricePredictor

predictor = HotelPricePredictor()
result = predictor.predict({
    "location": "Bangalore",
    "rating": 4.6,
    "distance_km": 2.5,
    "reviews": 1800,
    "room_type": "Deluxe",
    "amenity_count": 4,
})
print(result)
```

This model is useful for the capstone requirement of hotel price prediction and can be extended with XGBoost or a stronger regressor on real Kaggle data.

## Module 7: Hotel review sentiment analysis using NLP

This module performs sentiment analysis on hotel review text with a keyword-based NLP approach that classifies reviews as positive, neutral, or negative.

```python
from hotel_ai.sentiment_analysis import HotelSentimentAnalyzer

review = "The rooms were clean, staff was friendly, and breakfast was excellent."
analyzer = HotelSentimentAnalyzer()
print(analyzer.classify(review))
```

This satisfies the capstone requirement for sentiment analysis and can be upgraded to transformer-based models on real review data.

## Module 8: Personalized hotel ranking engine

The ranking engine combines rating, price fit, sentiment, and amenity match into a final weighted score used to rank hotel recommendations.

```python
from hotel_ai.ranking import HotelRankingEngine

ranking = HotelRankingEngine()
print(ranking.rank_hotels([{
    "hotel_name": "Azure Heights",
    "rating": 4.8,
    "price": 6500,
    "sentiment": 0.88,
    "amenities": ["wifi", "breakfast", "pool"],
    "budget": 7000,
}]))
```

This stage is used to prioritize the top hotel options after recommendation scoring.

## Module 10: User preference and booking prediction

The user preference predictor estimates a traveler's likely city and room type from budget, rating preference, trip purpose, stay length, review history, and distance preference.

```python
from hotel_ai.user_preference import UserPreferencePredictor

predictor = UserPreferencePredictor()
print(predictor.predict({
   "budget": 6000,
   "preferred_rating": 4.5,
   "purpose": "business",
   "stay_nights": 2,
}))
```

The matching API endpoint is `POST /predict-preferences`.

## Module 11: Hotel value and price anomaly detection

The anomaly detector compares each observed hotel price with its model-estimated expected price and reports unusually high or low values, percentage differences, and z-scores.

```python
from hotel_ai.price_anomaly import HotelPriceAnomalyDetector

detector = HotelPriceAnomalyDetector()
print(detector.detect()[:3])
```

The API endpoint is `POST /detect-price-anomalies`.

## Modules 12-14: AI insights, API, deployment, and monitoring

The final modules now include a human-readable insights engine, recommendation event monitoring, and Docker deployment files.

Run the dashboard directly with Streamlit or build it with Docker:

```bash
docker compose up --build
```

Useful monitoring endpoint:

- GET `/monitoring`

The API recommendation response includes both scored recommendations and explanations for why each hotel matched.

## API sample

- GET `/health`
- GET `/hotels`
- POST `/recommend`
- POST `/predict-price`
- POST `/predict-preferences`
- POST `/detect-price-anomalies`

## Notes

The dataset is intentionally synthetic and generated in code so the project is runnable without downloading external data sources.
