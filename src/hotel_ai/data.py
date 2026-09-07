from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import List


@dataclass
class Hotel:
    name: str
    location: str
    rating: float
    price: float
    reviews: int
    room_type: str
    amenities: list[str] = field(default_factory=list)
    distance_km: float = 0.0
    sentiment: float = 0.0
    occupancy: float = 0.0
    value_score: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)


def generate_sample_hotels() -> List[Hotel]:
    return [
        Hotel(
            name="Azure Heights",
            location="Bangalore",
            rating=4.8,
            price=6500,
            reviews=2100,
            room_type="Deluxe",
            amenities=["wifi", "breakfast", "parking", "pool"],
            distance_km=2.1,
            sentiment=0.88,
            occupancy=0.82,
            value_score=90,
        ),
        Hotel(
            name="City Nest Suites",
            location="Bangalore",
            rating=4.4,
            price=4800,
            reviews=1450,
            room_type="Standard",
            amenities=["wifi", "breakfast", "parking"],
            distance_km=3.7,
            sentiment=0.76,
            occupancy=0.71,
            value_score=78,
        ),
        Hotel(
            name="Green Valley Inn",
            location="Hyderabad",
            rating=4.6,
            price=5600,
            reviews=1700,
            room_type="Deluxe",
            amenities=["wifi", "breakfast", "gym"],
            distance_km=4.1,
            sentiment=0.83,
            occupancy=0.75,
            value_score=86,
        ),
        Hotel(
            name="Harbor View Stay",
            location="Mumbai",
            rating=4.9,
            price=8200,
            reviews=2600,
            room_type="Premium",
            amenities=["wifi", "breakfast", "pool", "spa"],
            distance_km=1.4,
            sentiment=0.92,
            occupancy=0.88,
            value_score=94,
        ),
        Hotel(
            name="Sunset Residency",
            location="Mumbai",
            rating=4.2,
            price=4300,
            reviews=980,
            room_type="Standard",
            amenities=["wifi", "parking"],
            distance_km=6.2,
            sentiment=0.69,
            occupancy=0.62,
            value_score=72,
        ),
        Hotel(
            name="Royal Comfort",
            location="Delhi",
            rating=4.7,
            price=7100,
            reviews=1880,
            room_type="Executive",
            amenities=["wifi", "breakfast", "parking", "gym"],
            distance_km=2.8,
            sentiment=0.87,
            occupancy=0.79,
            value_score=89,
        ),
        Hotel(
            name="Metro Pearl",
            location="Delhi",
            rating=4.1,
            price=3900,
            reviews=1050,
            room_type="Standard",
            amenities=["wifi", "parking"],
            distance_km=7.5,
            sentiment=0.63,
            occupancy=0.58,
            value_score=70,
        ),
        Hotel(
            name="Crown Grand",
            location="Chennai",
            rating=4.5,
            price=5400,
            reviews=1600,
            room_type="Deluxe",
            amenities=["wifi", "breakfast", "pool", "parking"],
            distance_km=3.6,
            sentiment=0.81,
            occupancy=0.74,
            value_score=85,
        ),
        Hotel(
            name="Lakeview Horizon",
            location="Pune",
            rating=4.3,
            price=4700,
            reviews=1190,
            room_type="Superior",
            amenities=["wifi", "breakfast", "gym"],
            distance_km=5.4,
            sentiment=0.74,
            occupancy=0.68,
            value_score=77,
        ),
        Hotel(
            name="Hill Crest Lodge",
            location="Pune",
            rating=4.6,
            price=6100,
            reviews=1550,
            room_type="Executive",
            amenities=["wifi", "breakfast", "parking", "pool"],
            distance_km=4.5,
            sentiment=0.85,
            occupancy=0.78,
            value_score=88,
        ),
        Hotel(
            name="Golden Palm Retreat",
            location="Goa",
            rating=4.9,
            price=9600,
            reviews=2400,
            room_type="Premium",
            amenities=["wifi", "breakfast", "pool", "spa", "parking"],
            distance_km=1.8,
            sentiment=0.94,
            occupancy=0.9,
            value_score=96,
        ),
        Hotel(
            name="Coastal Breeze",
            location="Goa",
            rating=4.1,
            price=4200,
            reviews=820,
            room_type="Standard",
            amenities=["wifi", "parking"],
            distance_km=8.0,
            sentiment=0.60,
            occupancy=0.56,
            value_score=68,
        ),
    ]
