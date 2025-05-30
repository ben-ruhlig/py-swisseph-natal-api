# TODO
- Add geocode functionality to lookup from the correct timezone (or make it a requirement to call this api w/UTC)
- Test api endpoints (mostly natal)


{
  "utc_birth_datetime": "1991-10-08T14:06:00Z",
  "birth_lat": 34.2257282,
  "birth_lon": -77.9447107
}


cusps
288.75561529918446, 1
332.70551065447086, 2
13.378664835476926, 3
43.24209034066223, 4
66.12343094909227, 5
86.53049165539608, 6
108.75561529918446, 7
152.7055106544708, 8
193.3786648354769, 9
223.24209034066226, 10
246.12343094909227, 11
266.5304916553961 12


ascmc
288.75561529918446 1
223.24209034066226 2
220.78919900183266 3
144.50427527253285 4
308.36699434989305 5
321.1998364120339 6
280.2669986532352 7
141.199836412033 8


## Test Example

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

Google would have been `curl "https://maps.googleapis.com/maps/api/geocode/json?address=Wilmington,+North+Carolina,+USA&key=YOUR_API_KEY"`


### SwissEph Response

```json
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