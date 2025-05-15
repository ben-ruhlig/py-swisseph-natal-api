# Natal Chart Calculation API Documentation

## Example workflow from the Caller
The caller will need to obtain geocoordinates. Let's take these coordinates as an example.

**Request**
`curl "https://nominatim.openstreetmap.org/search?q=Wilmington,+North+Carolina,+USA&format=json"`

**Response**
```json
[
  {
    "place_id":318494519,
    "licence":"Data © OpenStreetMap contributors,ODbL 1.0. http://osm.org/copyright",
    "osm_type":"relation",
    "osm_id":179032,
    "lat":"34.2257282",
    "lon":"-77.9447107",
    "class":"boundary",
    "type":"administrative",
    "place_rank":16,
    "importance":0.5924398226722164,
    "addresstype":"city",
    "name":"Wilmington",
    "display_name":"Wilmington, New Hanover County, North Carolina, United States",
    "boundingbox":["34.1472460","34.2670260","-77.9569950","-77.7868490"]
  }
]%
```

Google api would have been `curl "https://maps.googleapis.com/maps/api/geocode/json?address=Wilmington,+North+Carolina,+USA&key=YOUR_API_KEY"`


## Application Endpoint

`POST /natal-chart`

---

## Request Body
Note that house_systems can be specified as a comma delimited list placidus,koch,etc. If not query is provided, default is placidus.
```
/natal-chart?house_systems=placidus%2Ckoch
```

```json
{
  "utc_birth_datetime": "1991-10-08T14:06:00Z",
  "birth_lat": 34.2257282,
  "birth_lon": -77.9447107
}
```
- `utc_birth_datetime`: ISO 8601 UTC datetime string (e.g., "2025-05-15T04:06:36Z")
- `birth_lat`: Latitude in decimal degrees (positive for N, negative for S)
- `birth_lon`: Longitude in decimal degrees (positive for E, negative for W)

---

## Response Body

```
{
  "systems": {
    "placidus": {
      "houses": [
        {
          "sign": "Scorpio",
          "degree": 20.11398037426585,
          "house": 1
        },
        {
          "sign": "Sagittarius",
          "degree": 19.92778320110841,
          "house": 2
        },
        {
          "sign": "Capricorn",
          "degree": 23.25734735000833,
          "house": 3
        },
        {
          "sign": "Aquarius",
          "degree": 28.09384448267309,
          "house": 4
        },
        {
          "sign": "Aries",
          "degree": 0.26250299880575767,
          "house": 5
        },
        {
          "sign": "Aries",
          "degree": 27.38072451665272,
          "house": 6
        },
        {
          "sign": "Taurus",
          "degree": 20.11398037426585,
          "house": 7
        },
        {
          "sign": "Gemini",
          "degree": 19.92778320110841,
          "house": 8
        },
        {
          "sign": "Cancer",
          "degree": 23.25734735000833,
          "house": 9
        },
        {
          "sign": "Leo",
          "degree": 28.09384448267309,
          "house": 10
        },
        {
          "sign": "Libra",
          "degree": 0.26250299880572925,
          "house": 11
        },
        {
          "sign": "Libra",
          "degree": 27.38072451665272,
          "house": 12
        }
      ],
      "planets": [
        {
          "planet": "Sun",
          "sign": "Libra",
          "degree": 14.797585762072657,
          "house": 12,
          "speed": 0.9875628226953123
        },
        {
          "planet": "Moon",
          "sign": "Libra",
          "degree": 23.389115320985212,
          "house": 12,
          "speed": 13.415744955453373
        },
        {
          "planet": "Mercury",
          "sign": "Libra",
          "degree": 18.43519106446169,
          "house": 12,
          "speed": 1.6970160863555142
        },
        {
          "planet": "Venus",
          "sign": "Virgo",
          "degree": 1.185951013388916,
          "house": 12,
          "speed": 0.7120972257995012
        },
        {
          "planet": "Mars",
          "sign": "Libra",
          "degree": 24.478325125732113,
          "house": 12,
          "speed": 0.6696885167509263
        },
        {
          "planet": "Jupiter",
          "sign": "Virgo",
          "degree": 5.348207697213354,
          "house": 12,
          "speed": 0.1910602170789698
        },
        {
          "planet": "Saturn",
          "sign": "Aquarius",
          "degree": 0.20307854072359532,
          "house": 12,
          "speed": 0.005770032981705093
        },
        {
          "planet": "Uranus",
          "sign": "Capricorn",
          "degree": 9.99239568204598,
          "house": 12,
          "speed": 0.016308031145025242
        },
        {
          "planet": "Neptune",
          "sign": "Capricorn",
          "degree": 14.030213312885621,
          "house": 12,
          "speed": 0.006818064434473395
        },
        {
          "planet": "Pluto",
          "sign": "Scorpio",
          "degree": 18.92403550885203,
          "house": 12,
          "speed": 0.03475185655860378
        }
      ],
      "aspects": [
        {
          "type": "conjunction",
          "planets": [
            "Sun",
            "Mercury"
          ],
          "angle": 3.64,
          "orb": 3.64
        },
        {
          "type": "semi-square",
          "planets": [
            "Sun",
            "Venus"
          ],
          "angle": 43.61,
          "orb": 1.39
        },
        {
          "type": "square",
          "planets": [
            "Sun",
            "Uranus"
          ],
          "angle": 85.19,
          "orb": 4.81
        },
        {
          "type": "square",
          "planets": [
            "Sun",
            "Neptune"
          ],
          "angle": 89.23,
          "orb": 0.77
        },
        {
          "type": "conjunction",
          "planets": [
            "Moon",
            "Mercury"
          ],
          "angle": 4.95,
          "orb": 4.95
        },
        {
          "type": "conjunction",
          "planets": [
            "Moon",
            "Mars"
          ],
          "angle": 1.09,
          "orb": 1.09
        },
        {
          "type": "square",
          "planets": [
            "Moon",
            "Saturn"
          ],
          "angle": 96.81,
          "orb": 6.81
        },
        {
          "type": "semi-square",
          "planets": [
            "Mercury",
            "Venus"
          ],
          "angle": 47.25,
          "orb": 2.25
        },
        {
          "type": "conjunction",
          "planets": [
            "Mercury",
            "Mars"
          ],
          "angle": 6.04,
          "orb": 6.04
        },
        {
          "type": "semi-square",
          "planets": [
            "Mercury",
            "Jupiter"
          ],
          "angle": 43.09,
          "orb": 1.91
        },
        {
          "type": "square",
          "planets": [
            "Mercury",
            "Neptune"
          ],
          "angle": 85.6,
          "orb": 4.4
        },
        {
          "type": "semi-sextile",
          "planets": [
            "Mercury",
            "Pluto"
          ],
          "angle": 30.49,
          "orb": 0.49
        },
        {
          "type": "conjunction",
          "planets": [
            "Venus",
            "Jupiter"
          ],
          "angle": 4.16,
          "orb": 4.16
        },
        {
          "type": "quincunx",
          "planets": [
            "Venus",
            "Saturn"
          ],
          "angle": 149.02,
          "orb": 0.98
        },
        {
          "type": "sesquiquadrate",
          "planets": [
            "Venus",
            "Neptune"
          ],
          "angle": 132.84,
          "orb": 2.16
        },
        {
          "type": "square",
          "planets": [
            "Mars",
            "Saturn"
          ],
          "angle": 95.72,
          "orb": 5.72
        },
        {
          "type": "bi-quintile",
          "planets": [
            "Jupiter",
            "Saturn"
          ],
          "angle": 144.85,
          "orb": 0.85
        },
        {
          "type": "trine",
          "planets": [
            "Jupiter",
            "Uranus"
          ],
          "angle": 124.64,
          "orb": 4.64
        },
        {
          "type": "quintile",
          "planets": [
            "Jupiter",
            "Pluto"
          ],
          "angle": 73.58,
          "orb": 1.58
        },
        {
          "type": "quintile",
          "planets": [
            "Saturn",
            "Pluto"
          ],
          "angle": 71.28,
          "orb": 0.72
        },
        {
          "type": "conjunction",
          "planets": [
            "Uranus",
            "Neptune"
          ],
          "angle": 4.04,
          "orb": 4.04
        },
        {
          "type": "sextile",
          "planets": [
            "Neptune",
            "Pluto"
          ],
          "angle": 55.11,
          "orb": 4.89
        }
      ]
    }
  }
}
```

---

## Calculation Details & Assumptions

- **Time**: The API expects UTC time in ISO 8601 format. No timezone conversion is performed.
- **Location**: Latitude and longitude must be provided as decimal degrees. No geocoding is performed.
- **Ephemeris**: Swiss Ephemeris (pyswisseph) is used for all astronomical calculations. The ephemeris file must be present in the `./ephe/` directory.
- **Julian Day**: The UTC datetime is converted to Julian Day for all calculations.
- **House System**: Placidus house system is default if none is explicitely provided.
- **Planets**: The 10 classical planets are calculated: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto.
- **Planet Data**: Each planet includes its name, sign, degree within sign, house, and speed (degrees/day; negative means retrograde).
- **Houses**: Each house includes the sign and degree of its cusp (start) and the house number (1-12).
- **Aspects**: All major aspects are calculated between planet pairs:
    - Conjunction (0° ±8°), Opposition (180° ±8°), Trine (120° ±7°), Square (90° ±7°), Sextile (60° ±6°), Quincunx (150° ±5°), Semi-sextile (30° ±3°), Semi-square (45° ±3°), Sesquiquadrate (135° ±3°), Quintile (72° ±2°), Bi-quintile (144° ±2°)
    - Each aspect includes the type, the two planets, the exact angle, and the orb (difference from exact).
- **Aspect Calculation**: For each unique planet pair, the shortest angle between them is compared to all aspect angles. If within orb, the aspect is included.
- **Error Handling**: Invalid input or calculation errors return HTTP 400/500 with details.

---

## Astrological Concepts Explained

### Planets
- Represent core energies, drives, and archetypes in the chart.
- Example: Sun (identity), Moon (emotions), Mercury (mind), Venus (love), Mars (action), etc.

### Zodiac Signs
- The 12 signs (Aries, Taurus, ..., Pisces) represent modes of expression for planets and houses.
- Each sign covers 30° of the 360° zodiac.

### Houses
- The sky is divided into 12 houses, each representing a life area (e.g., self, money, communication, home, etc.).
- The house a planet falls in shows where its energy is most active.
- House cusps are the starting points of each house, calculated using the Placidus system.

### Aspects
- Aspects are angular relationships between planets, showing how their energies interact.
- Major aspects:
    - **Conjunction (0°)**: Planets act together, blending energies.
    - **Opposition (180°)**: Tension, polarity, or balance between planets.
    - **Trine (120°)**: Harmony, ease, talents.
    - **Square (90°)**: Challenge, friction, dynamic growth.
    - **Sextile (60°)**: Opportunity, cooperation.
    - **Quincunx (150°)**: Adjustment, awkwardness.
    - **Semi-sextile (30°)**: Subtle connection.
    - **Semi-square (45°)**: Minor tension.
    - **Sesquiquadrate (135°)**: Minor challenge.
    - **Quintile (72°), Bi-quintile (144°)**: Creative or unique connections.
- Each aspect is defined by its angle and an allowable "orb" (tolerance).

### Example Calculation Flow
1. Parse UTC datetime and coordinates from request.
2. Convert datetime to Julian Day.
3. Calculate house cusps using Placidus system.
4. Calculate planet positions (longitude, sign, degree, house, speed).
5. Calculate all aspects between planet pairs.
6. Return planets, houses, and aspects in the response.

---

## Notes
- The API does not perform geocoding or timezone conversion; all data must be provided in the correct format.
- Only the 10 classical planets are included; asteroids and other points are not calculated.
- The Placidus house system is standard for Western astrology, but other systems are not currently supported.
- The orb values for aspects are based on common astrological practice but can be adjusted in the code if needed.
