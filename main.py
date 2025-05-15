"""
Astrology API
Copyright (C) 2025 Your Name

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

This software incorporates the Swiss Ephemeris library.
Copyright (C) 1997 - 2021 Astrodienst AG, Switzerland. All rights reserved.
See https://www.astro.com/swisseph/ for details.
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import swisseph as swe
from datetime import datetime
import pytz
import os
from typing import List, Dict

app = FastAPI()

# Set ephemeris path
EPHE_PATH = "./ephe"
try:
    swe.set_ephe_path(EPHE_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to set ephemeris path {EPHE_PATH}: {str(e)}")

# Define zodiac signs
SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

# Define aspects with their angles and orbs
ASPECTS = {
    "conjunction": {"angle": 0, "orb": 8},
    "opposition": {"angle": 180, "orb": 8},
    "trine": {"angle": 120, "orb": 7},
    "square": {"angle": 90, "orb": 7},
    "sextile": {"angle": 60, "orb": 6},
    "quincunx": {"angle": 150, "orb": 5},
    "semi-sextile": {"angle": 30, "orb": 3},
    "semi-square": {"angle": 45, "orb": 3},
    "sesquiquadrate": {"angle": 135, "orb": 3},
    "quintile": {"angle": 72, "orb": 2},
    "bi-quintile": {"angle": 144, "orb": 2},
}

HOUSE_SYSTEM_CODES = {
    "placidus": b"P",
    "koch": b"K",
    "equal": b"E",
    "whole_sign": b"W",
    "porphyry": b"O",
    "regiomontanus": b"R",
    "campanus": b"C",
    # Add more as needed
}


class BirthData(BaseModel):
    utc_birth_datetime: str  # Format: 2025-05-15T04:06:36Z
    birth_lat: float  # Latitude in decimal degrees (e.g.,  )
    birth_lon: float  # Longitude in decimal degrees (e.g., -74.0060)


class Planet(BaseModel):
    planet: str
    sign: str
    degree: float
    house: int
    speed: float  # Degrees per day, negative means retrograde


class House(BaseModel):
    sign: str
    degree: float
    house: int


class Aspect(BaseModel):
    type: str
    planets: list[str]
    angle: float  # The exact angle between planets
    orb: float  # How far from exact the aspect is


class NatalChart(BaseModel):
    planets: list[Planet]
    houses: list[House]
    aspects: list[Aspect]


def zodiac_sign(degree: float) -> str:
    return SIGNS[int(degree // 30)]


def house_number(degree: float, cusps: list[float]) -> int:
    for i in range(12):
        if degree >= cusps[i] and degree < cusps[(i % 12)]:
            return i
    return 12


def planet_name(id: int) -> str:
    names = {
        swe.SUN: "Sun",
        swe.MOON: "Moon",
        swe.MERCURY: "Mercury",
        swe.VENUS: "Venus",
        swe.MARS: "Mars",
        swe.JUPITER: "Jupiter",
        swe.SATURN: "Saturn",
        swe.URANUS: "Uranus",
        swe.NEPTUNE: "Neptune",
        swe.PLUTO: "Pluto",
    }
    return names.get(id, "Unknown")


def calculate_aspects(planets: list[Planet]) -> list[Aspect]:
    aspects = []
    for i, p1 in enumerate(planets):
        for p2 in planets[i + 1 :]:
            lon1 = p1.degree + SIGNS.index(p1.sign) * 30
            lon2 = p2.degree + SIGNS.index(p2.sign) * 30
            angle = abs(lon1 - lon2)
            angle = min(angle, 360 - angle)
            for aspect_name, aspect_data in ASPECTS.items():
                target_angle = aspect_data["angle"]
                orb = aspect_data["orb"]
                if abs(angle - target_angle) <= orb:
                    exact_orb = abs(angle - target_angle)
                    aspects.append(
                        Aspect(
                            type=aspect_name,
                            planets=[p1.planet, p2.planet],
                            angle=round(angle, 2),
                            orb=round(exact_orb, 2),
                        )
                    )
                    break
    return aspects


@app.get("/health")
async def health_check():
    try:
        # Verify pyswisseph is operational with a simple Julian Day calculation
        test_jd = swe.julday(2025, 5, 15, 13.9)  # Today, ~01:54 PM +08
        if test_jd < 0:
            raise Exception("Julian Day calculation failed")

        # Verify ephemeris path
        if not os.path.exists(EPHE_PATH):
            raise Exception(f"Ephemeris path {EPHE_PATH} does not exist")

        return {
            "status": "healthy",
            "message": "API is operational",
            "pyswisseph_version": swe.version,
            "timestamp": datetime.now(pytz.UTC).isoformat(),
            "source": "https://github.com/ben-ruhlig/py-swisseph-natal-api",  # AGPL compliance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@app.get("/docs")
async def docs():
    return {
        "message": "Astrology API using pyswisseph",
        "source": "https://github.com/ben-ruhlig/py-swisseph-natal-api",
        "license": "AGPL-3.0",
    }


# Refer to detailed documentation for this endpoint: ./docs/natal-chart-calculation.md
@app.post("/natal-chart")
async def calculate_natal_chart(
    data: BirthData,
    house_systems: List[str] = Query(
        default=["placidus"],
        description="Comma-separated list of house systems (e.g. placidus,koch,equal)",
    ),
):
    try:
        utc_dt = datetime.fromisoformat(data.utc_birth_datetime.replace("Z", "+00:00"))
        jd = swe.julday(
            utc_dt.year,
            utc_dt.month,
            utc_dt.day,
            utc_dt.hour + utc_dt.minute / 60 + utc_dt.second / 3600,
        )
        lat, lon = data.birth_lat, data.birth_lon

        planet_ids = [
            swe.SUN,
            swe.MOON,
            swe.MERCURY,
            swe.VENUS,
            swe.MARS,
            swe.JUPITER,
            swe.SATURN,
            swe.URANUS,
            swe.NEPTUNE,
            swe.PLUTO,
        ]

        systems_result = {}

        for sys in house_systems:
            code = HOUSE_SYSTEM_CODES.get(sys.lower())
            if not code:
                continue
            cusps, ascmc = swe.houses(jd, lat, lon, code)
            houses = [
                House(sign=zodiac_sign(cusps[i]), degree=cusps[i] % 30, house=(i + 1))
                for i in range(12)
            ]
            planets = []
            for pid in planet_ids:
                xx, _ = swe.calc_ut(jd, pid, swe.FLG_SPEED)
                sign = zodiac_sign(xx[0])
                house = house_number(xx[0], cusps)
                planets.append(
                    Planet(
                        planet=planet_name(pid),
                        sign=sign,
                        degree=xx[0] % 30,
                        house=house,
                        speed=xx[3],
                    )
                )
            aspects = calculate_aspects(planets)
            systems_result[sys.lower()] = {
                "houses": houses,
                "planets": planets,
                "aspects": aspects,
            }

        # Default to placidus if no valid system was requested
        if not systems_result:
            cusps, ascmc = swe.houses(jd, lat, lon, b"P")
            houses = [
                House(sign=zodiac_sign(cusps[i]), degree=cusps[i] % 30, house=(i + 1))
                for i in range(12)
            ]
            planets = []
            for pid in planet_ids:
                xx, _ = swe.calc_ut(jd, pid, swe.FLG_SPEED)
                sign = zodiac_sign(xx[0])
                house = house_number(xx[0], cusps)
                planets.append(
                    Planet(
                        planet=planet_name(pid),
                        sign=sign,
                        degree=xx[0] % 30,
                        house=house,
                        speed=xx[3],
                    )
                )
            aspects = calculate_aspects(planets)
            systems_result["placidus"] = {
                "houses": houses,
                "planets": planets,
                "aspects": aspects,
            }

        return {"systems": systems_result}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
