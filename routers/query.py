from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from models import SensorData
from db import get_db
from typing import List, Optional
from sqlalchemy import func
from datetime import datetime, timedelta

router = APIRouter()

# Define the /query endpoint
@router.get("/")
async def query_sensor_data(
    sensors: Optional[List[int]] = Query(None), 
    metrics: Optional[List[str]] = Query(None),
    statistic: str = Query(..., pattern="^(min|max|avg|sum)$"),
    date_range: Optional[int] = Query(1, description="Number of days (1-30) from today"),
    db: Session = Depends(get_db)):
    """
    Endpoint to query sensor data based on sensor IDs.

    Parameters:
        - sensors: Optional list of sensor IDs. If not provided, returns data for all sensors.
        - metrics: Optional list of metrics. If not provided, returns all metrics.
        - statistic: Required statistic to compute (min, max, avg, or sum).
        - date_range: Optional number of days (1-30) from today. Defaults to 1 day.
        - db: Database session (injected).

    Returns:
        - List of sensor data with computed statistics.
    """

    query = db.query(
        SensorData.sensor_id,
        SensorData.metric,
        getattr(func, statistic)(SensorData.value).label("result")
    )

    if sensors:
        query = query.filter(SensorData.sensor_id.in_(sensors))

    if metrics:
        query = query.filter(SensorData.metric.in_(metrics))

    if 1 <= date_range <= 30:
        start_date = datetime.now() - timedelta(days=date_range)
        query = query.filter(SensorData.timestamp >= start_date)
    else:
        raise HTTPException(status_code=400, detail="date_range must be between 1 and 30")
    
    query = query.group_by(SensorData.sensor_id, SensorData.metric)

    results = query.all()

    # Convert to list of dicts
    output = []
    for row in results:
        output.append({
            "sensor_id": row.sensor_id,
            "metric": row.metric,
            statistic: row.result
        })

    return output