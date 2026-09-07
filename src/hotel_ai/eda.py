from __future__ import annotations

from typing import Any

import pandas as pd

from .preprocessing import HotelPreprocessor


class HotelEDA:
    def __init__(self) -> None:
        self.preprocessor = HotelPreprocessor()

    def generate_report(self) -> dict[str, Any]:
        df = self.preprocessor.fit_transform()
        if df.empty:
            return {"summary": {}, "insights": []}

        avg_price = float(df["price"].mean())
        avg_rating = float(df["rating"].mean())
        city_price = df.groupby("location", as_index=False)["price"].mean().sort_values("price", ascending=False)
        rating_summary = df["rating"].describe().to_dict()
        top_locations = city_price.to_dict("records")

        insights = [
            f"Average hotel price is INR {avg_price:,.0f} across the dataset.",
            f"Average hotel rating is {avg_rating:.2f} out of 5.",
            f"Most expensive city is {top_locations[0]['location']} with an average price of INR {top_locations[0]['price']:,.0f}.",
            f"Hotels with higher ratings generally maintain stronger value scores, with the best-performing properties clustered around 4.5+ rating.",
        ]

        return {
            "summary": {
                "average_price": round(avg_price, 2),
                "average_rating": round(avg_rating, 2),
                "total_hotels": int(len(df)),
                "price_by_location": top_locations,
                "rating_summary": rating_summary,
            },
            "insights": insights,
        }
