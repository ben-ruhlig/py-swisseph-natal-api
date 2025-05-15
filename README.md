# Astrology API

> **!IMPORTANT: Not Production Ready**. 
> This application is in active development.

A FastAPI-based Python API for calculating natal charts using the Swiss Ephemeris via pyswisseph. This API is designed to compute astrological data (planetary positions, house cusps, and aspects) for living humans, using the seas_18.se1 ephemeris file covering years 1800–2400.

## Features
* Calculates natal charts with planets, houses, and aspects (currently square aspects).
* Supports Placidus house system and Western astrology.
* Includes health check and documentation endpoints for monitoring and compliance.

## Endpoints
`GET /health`

* Description: Checks the API’s operational status and pyswisseph functionality.
* **Response:**
```json
{
  "status": "healthy",
  "message": "API is operational",
  "pyswisseph_version": "2.10.03",
  "timestamp": "2025-05-15T14:36:00.123456+08:00",
  "source": "https://github.com/ben-ruhlig/py-swisseph-natal-api"
}
```
* Error: Returns 500 with details if the API or pyswisseph fails (e.g., missing ephemeris files).

`GET /docs`

* Description: Provides API documentation and licensing information.
* **Response:**
```json
{
  "message": "Astrology API using pyswisseph",
  "source": "https://github.com/yourusername/astro-api",
  "license": "AGPL-3.0"
}
```

`POST /natal-chart`

* Description: Calculates a natal chart based on birth details.
* See [docs/natal-chart-calc.md](docs/natal-chart-calc.md) for full request/response specification and calculation details.

## Ephemeris Files
This API includes only the `seas_18.se1` ephemeris file, which covers planetary positions from 1800 to 2400. This is sufficient for natal charts of living humans, as it spans modern birth dates. The file is stored in the `./ephe/` directory and must be downloaded separately (see Setup).

Additional ephemeris files (e.g., for ancient or future dates) are available from Astrodienst but are not included, as this API focuses on contemporary astrology.

## Setup
### Prerequisites
* Python >=3.13
* Ephemeris file: `seas_18.se1` (download from ftp://ftp.astro.ch/pub/swisseph/ephe/)
Linux server (e.g., Ubuntu 22.04) for deployment

**Installation**

1. Clone the Repository:
```bash
git clone https://github.com/ben-ruhlig/py-swisseph-natal-api
cd py-swisseph-natal-api
```

2. Install Dependencies:
```bash
uv add fastapi uvicorn pyswisseph pytz geopy
```

3. Set Up Ephemeris Files:
* Download `seas_18.se1` from one of the dowload links shown at https://www.astro.com/swisseph/swedownload_e.htm.
* Place the downloaded file in `./ephe/`
```bash
chown -R youruser:youruser /app/ephe
chmod -R 700 /app/ephe
```

4. Run the API:
```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

Test Endpoints:
* Health check:
```bash
curl http://localhost:8000/health`
```

* Natal chart:
> TODO: This will change
```bash
curl -X POST http://localhost:8000/natal-chart \
-H "Content-Type: application/json" \
-d '{"birth_date":"1995-08-23","birth_time":"14:30","birth_place":"New York, NY"}'
```

### Deployment
> TODO: Validate all the deployment steps
* Systemd:
```bash
sudo nano /etc/systemd/system/py-swisseph-natal-api.service
```

```ini
[Unit]
Description=Python Astrology API
After=network.target

[Service]
User=youruser
WorkingDirectory=/app/astro-app/python-api
ExecStart=/usr/bin/env python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable py-swisseph-natal-api
sudo systemctl start py-swisseph-natal-api
```

* Docker:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn pyswisseph pytz geopy
COPY ephe/ ephe/
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
```
```bash
docker build -t py-swisseph-natal-api .
docker run -d -p 127.0.0.1:8000:8000 -v /app/ephe:/app/ephe py-swisseph-natal-api
```



## License
This project is licensed under the GNU Affero General Public License (AGPL-3.0). See the LICENSE file for details.

This software incorporates the Swiss Ephemeris library:Copyright (C) 1997 - 2021 Astrodienst AG, Switzerland. All rights reserved.Authors: Dieter Koch and Alois TreindlSee https://www.astro.com/swisseph/ for details.

## Source Code
Source code is available at: https://github.com/ben-ruhlig/py-swisseph-natal-api
As required by AGPL-3.0, the source code is publicly accessible for users interacting with the API, even for `localhost` access.


## Notes
* Time Zone Handling: The API currently assumes UTC time provided.
* Geocoding: Assumes location is provided as a valid geocode.

## Contributing
Contributions are welcome! Please fork the repository, create a branch, and submit a pull request. Ensure changes comply with AGPL-3.0.

## Contact
For issues or questions, open an issue on GitHub.
