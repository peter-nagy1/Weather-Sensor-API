# Weather Sensors API

A proof-of-concept for an app that collects and queries weather data from sensors via REST API.

---
## Features

- Receives new metric values from sensors (i.e. temperature, humidity, wind speed, etc.).
- Allows querying sensor data from sensors, with metrics and statistics, from a date range.
    - Example query: Give me the average temperature and humidity for sensor 1 in the last week.

---
## Installation and Setup

```bash
# Clone repo
git clone https://github.com/<a>/<b>.git
cd <b>

# Install requirements
pip install -r requirements.txt

# Run
uvicorn main:app --reload
```

The app will start on: http://127.0.0.1:8000

## Example Usage

### 1. Adding sensor data

```bash
curl -X POST "http://127.0.0.1:8000/sensors/1/data" \
     -H "Content-Type: application/json" \
     -d '{"metric":"temperature","value":20,"timestamp":"2025-10-02T10:00:00"}'
```

### 2. Query sensor data

```bash
curl "http://127.0.0.1:8000/query?sensors=1&metrics=temperature&statistic=avg&date_range=10"
```

---
## Notes
- I Used FASTAPI since it's ideal for PoC, it has built-in validation (Pydantic) and automatic API docs generation.
- I Used SQLite for simplicity since it's file-based (no server, authentication needed) and portable. Also the schemas and models developed using SQLAlchemy are easily transferable to MySQL or PostgreSQL.
- SQLAlchemy was used as our ORM to avoid having to write raw SQL. Also helps with cleaniness.
- To support scalability and readability, I structured the app by separating the schemas, models and routers instead of having them all in `main.py`.
- Sensors and metrics are not validated against a fixed list of available sensors and metrics inside the database. If a sensor or metric is queried which has no data in the database, then the query will simply be empty instead of returning an exception.
