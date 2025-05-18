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
from typing import List

app = FastAPI()

# Set ephemeris path
EPHE_PATH = "./ephe"
try:
    swe.set_ephe_path(EPHE_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to set ephemeris path {EPHE_PATH}: {str(e)}")

# Define zodiac signs in traditional order (0° = start of Aries)
SIGNS = [
    "Aries",  # 0° - 30°
    "Taurus",  # 30° - 60°
    "Gemini",  # 60° - 90°
    "Cancer",  # 90° - 120°
    "Leo",  # 120° - 150°
    "Virgo",  # 150° - 180°
    "Libra",  # 180° - 210°
    "Scorpio",  # 210° - 240°
    "Sagittarius",  # 240° - 270°
    "Capricorn",  # 270° - 300°
    "Aquarius",  # 300° - 330°
    "Pisces",  # 330° - 360°
]

# Define aspects with their angles and allowed orbs (tolerance)
ASPECTS = {
    # Major aspects
    "conjunction": {"angle": 0, "orb": 8},  # Same position
    "opposition": {"angle": 180, "orb": 8},  # Opposite positions
    "trine": {"angle": 120, "orb": 7},  # 4 signs apart (harmonious)
    "square": {"angle": 90, "orb": 7},  # 3 signs apart (tense)
    "sextile": {"angle": 60, "orb": 6},  # 2 signs apart (harmonious)
    # Minor aspects
    "quincunx": {"angle": 150, "orb": 5},  # 5 signs apart (adjustment)
    "semi-sextile": {"angle": 30, "orb": 3},  # 1 sign apart (mild)
    "semi-square": {"angle": 45, "orb": 3},  # 1.5 signs apart (mild tension)
    "sesquiquadrate": {"angle": 135, "orb": 3},  # 4.5 signs apart (tension)
    "quintile": {"angle": 72, "orb": 2},  # Creative aspect (360° ÷ 5)
    "bi-quintile": {"angle": 144, "orb": 2},  # Creative aspect (360° ÷ 5 × 2)
}

# House system codes for Swiss Ephemeris library
# The byte values match the character codes required by the C library
HOUSE_SYSTEM_CODES = {
    "placidus": b"P",  # Most commonly used in Western astrology
    "koch": b"K",  # Koch house system
    "equal": b"E",  # Equal house system (equal 30° houses)
    "whole_sign": b"W",  # Whole sign houses (each sign = one house)
    "porphyry": b"O",  # Porphyry house system
    "regiomontanus": b"R",  # Regiomontanus house system
    "campanus": b"C",  # Campanus house system
    # Add more as needed
}


class BirthData(BaseModel):
    """
    Birth data required for astrological calculations.

    Attributes:
        utc_birth_datetime: Birth date and time in ISO 8601 UTC format
        birth_lat: Birth latitude in decimal degrees (positive for North, negative for South)
        birth_lon: Birth longitude in decimal degrees (positive for East, negative for West)
    """

    utc_birth_datetime: str  # Format: 2025-05-15T04:06:36Z
    birth_lat: float  # Latitude in decimal degrees (e.g., 40.7128)
    birth_lon: float  # Longitude in decimal degrees (e.g., -74.0060)


class Planet(BaseModel):
    """
    Represents a planet in an astrological chart.

    Attributes:
        planet: Planet name (Sun, Moon, Mercury, etc.)
        sign: Zodiac sign the planet is in
        degree: Position within sign in degrees (0-30)
        house: House number (1-12) the planet is in
        speed: Movement speed in degrees per day (negative for retrograde motion)
    """

    planet: str
    sign: str
    degree: float
    house: int
    speed: float  # Degrees per day, negative means retrograde


class House(BaseModel):
    """
    Represents an astrological house cusp.

    Attributes:
        sign: Zodiac sign at the house cusp
        degree: Position within sign in degrees (0-30)
        house: House number (1-12)
    """

    sign: str
    degree: float
    house: int


class Aspect(BaseModel):
    """
    Represents an aspect (angular relationship) between two planets.

    Attributes:
        type: Aspect type (conjunction, opposition, trine, etc.)
        planets: List of two planet names forming the aspect
        angle: The exact angle between planets in degrees
        orb: Difference between exact aspect angle and actual angle
    """

    type: str
    planets: list[str]
    angle: float  # The exact angle between planets
    orb: float  # How far from exact the aspect is


class NatalChart(BaseModel):
    """
    Complete natal chart with planets, houses, and aspects.

    Attributes:
        planets: List of planets with their positions
        houses: List of house cusps
        aspects: List of aspects between planets
    """

    planets: list[Planet]
    houses: list[House]
    aspects: list[Aspect]


def zodiac_sign(degree: float) -> str:
    """
    Convert an absolute ecliptic longitude (0-360°) to its corresponding zodiac sign.

    Args:
        degree: Absolute ecliptic longitude in degrees (0-360°)

    Returns:
        str: Name of the zodiac sign (Aries, Taurus, etc.)

    Notes:
        Each sign spans 30° starting from 0° Aries. The degree is divided by 30
        and the integer result is used as an index into the SIGNS array.
    """
    return SIGNS[int(degree // 30)]


def house_number(degree: float, cusps: list[float]) -> int:
    """
    Determine which house a planet belongs to based on its ecliptic longitude.

    Args:
        degree: Planet's ecliptic longitude (0-360)
        cusps: List of house cusps from SwissEphemeris (indices 0-11 represent houses 1-12)

    Returns:
        House number (1-12)

    Raises:
        ValueError: If house cannot be determined
    """
    # Check for valid house cusps array
    if len(cusps) < 12:
        raise ValueError(
            f"Invalid house cusps array: expected at least 12 values, got {len(cusps)}"
        )

    # Check each house - house numbers in astrology are 1-based (not 0-based)
    for i in range(
        12
    ):  # Houses 0-11 in the array (representing houses 1-12 in astrology)
        next_house = (i + 1) % 12  # Wrap around from 11 to 0

        # Get the cusps for current and next house
        cusp_current = cusps[i]
        cusp_next = cusps[next_house]

        # Handle houses that cross over 0° Aries (360°→0°)
        if cusp_next < cusp_current:  # House spans 0°
            # Planet is in this house if it's after current cusp OR before next cusp
            if degree >= cusp_current or degree < cusp_next:
                return i + 1  # Convert to 1-based house number for astrology
        else:
            # Standard case: planet is in house if between current cusp and next cusp
            if degree >= cusp_current and degree < cusp_next:
                return i + 1  # Convert to 1-based house number for astrology

    # If we get here, there's an error in the house calculation
    raise ValueError(
        f"Failed to determine house for planet at {degree}°. House cusps: {[round(cusps[i], 2) for i in range(12)]}"
    )


def planet_name(id: int) -> str:
    """
    Convert a Swiss Ephemeris planet ID to its common name.

    Args:
        id: Swiss Ephemeris planet ID constant (e.g., swe.SUN, swe.MOON)

    Returns:
        str: Common name of the planet or "Unknown" if not found

    Notes:
        This function supports the 10 classical planets used in Western astrology:
        Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, and Pluto.
    """
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
    """
    Calculate all valid astrological aspects between planets in a chart.

    Args:
        planets: List of Planet objects with position information

    Returns:
        list[Aspect]: List of astrological aspects between planets

    Notes:
        - Converts planet positions from sign+degree to absolute longitude (0-360°)
        - Calculates the smallest angle between any two planets
        - Compares each angle to defined aspect angles (conjunction, trine, etc.)
        - Includes the aspect if it's within the allowed orb (tolerance)
        - Only considers each unique pair of planets once
        - When multiple aspects are possible for a pair, takes the first valid one
    """
    aspects = []
    for i, p1 in enumerate(planets):
        for p2 in planets[i + 1 :]:  # Only consider each pair once
            # Convert from sign+degree to absolute longitude (0-360°)
            lon1 = p1.degree + SIGNS.index(p1.sign) * 30
            lon2 = p2.degree + SIGNS.index(p2.sign) * 30

            # Calculate smallest angle between planets (always ≤ 180°)
            angle = abs(lon1 - lon2)
            angle = min(angle, 360 - angle)

            # Check each possible aspect type
            for aspect_name, aspect_data in ASPECTS.items():
                target_angle = aspect_data["angle"]
                orb = aspect_data["orb"]

                # If within orb tolerance, record the aspect
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
                    break  # Only record the first valid aspect for this planet pair
    return aspects


@app.get("/health")
async def health_check():
    """
    Check if the API and Swiss Ephemeris library are operational.

    This endpoint performs basic health checks:
    1. Tests Julian Day calculation functionality
    2. Verifies the ephemeris files are accessible

    Returns:
        JSON with status information and version details

    Raises:
        HTTPException with 500 status code if any check fails
    """
    try:
        # Verify pyswisseph is operational with a simple Julian Day calculation
        test_jd = swe.julday(2025, 5, 15, 13.9)  # Sample date calculation
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
    """
    Provide basic API documentation and licensing information.

    Returns:
        JSON with API description, source repository URL, and license information
    """
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
    """
    Calculate a natal astrological chart based on birth date, time, and location.

    This endpoint performs the following calculations:
    1. Converts UTC datetime to Julian Day
    2. Calculates house cusps for requested house systems
    3. Calculates planet positions, signs, and houses
    4. Determines aspects between planets
    5. Returns complete chart data for each requested house system

    Args:
        data: Birth data (datetime, latitude, longitude)
        house_systems: List of house systems to calculate (placidus, koch, etc.)

    Returns:
        JSON with natal chart data organized by house system

    Raises:
        HTTPException: On invalid input (400) or calculation error (500)
    """
    try:
        # Convert ISO datetime string to Python datetime, ensuring proper timezone handling
        utc_dt = datetime.fromisoformat(data.utc_birth_datetime.replace("Z", "+00:00"))

        # Calculate Julian Day number from datetime components
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
            # Add "placidus" to house_systems and reprocess to avoid code duplication
            house_systems = ["placidus"]
            code = HOUSE_SYSTEM_CODES.get("placidus")
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
