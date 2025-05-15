from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import swisseph as swe
from datetime import datetime
import pytz

app = FastAPI()

# Set ephemeris path (adjust to your ephemeris directory)
swe.set_ephe_path("./ephe")


class BirthData(BaseModel):
    birth_date: str  # Format: YYYY-MM-DD
    birth_time: str  # Format: HH:MM
    birth_place: str  # City name (for geocoding)


class Planet(BaseModel):
    planet: str
    sign: str
    degree: float
    house: int


class House(BaseModel):
    sign: str
    degree: float
    house: int


class Aspect(BaseModel):
    type: str
    planets: list[str]


class NatalChart(BaseModel):
    planets: list[Planet]
    houses: list[House]
    aspects: list[Aspect]


def zodiac_sign(degree: float) -> str:
    signs = [
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
    return signs[int(degree // 30)]


def house_number(degree: float, cusps: list[float]) -> int:
    for i in range(1, 13):
        if degree >= cusps[i] and degree < cusps[(i % 12) + 1]:
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
            angle = abs(
                (p1.degree + signs.index(p1.sign) * 30)
                - (p2.degree + signs.index(p2.sign) * 30)
            )
            if angle > 180:
                angle = 360 - angle
            if abs(angle - 90) < 5:  # Square aspect with 5-degree orb
                aspects.append(Aspect(type="square", planets=[p1.planet, p2.planet]))
    return aspects


@app.post("/natal-chart", response_model=NatalChart)
async def calculate_natal_chart(data: BirthData):
    try:
        # Parse date and time
        dt = datetime.strptime(f"{data.birth_date} {data.birth_time}", "%Y-%m-%d %H:%M")
        dt = pytz.timezone("America/New_York").localize(dt)  # Adjust timezone
        utc_dt = dt.astimezone(pytz.UTC)

        # Calculate Julian Day
        jd = swe.julday(
            utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60
        )

        # Hardcoded coordinates for New York, NY (use geocoding in production)
        lat, lon = 40.7128, -74.0060

        # Calculate house cusps (Placidus)
        cusps, ascmc = swe.houses(jd, lat, lon, b"P")

        # Calculate planet positions
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
        planets = []
        for pid in planet_ids:
            xx, _ = swe.calc_ut(jd, pid, swe.FLG_SPEED)
            sign = zodiac_sign(xx[0])
            house = house_number(xx[0], cusps)
            planets.append(
                Planet(
                    planet=planet_name(pid), sign=sign, degree=xx[0] % 30, house=house
                )
            )

        # Calculate houses
        houses = [
            House(sign=zodiac_sign(cusps[i]), degree=cusps[i] % 30, house=i)
            for i in range(1, 13)
        ]

        # Calculate aspects
        aspects = calculate_aspects(planets)

        return NatalChart(planets=planets, houses=houses, aspects=aspects)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
