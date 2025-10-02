from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import SensorDataIn
from models import SensorData
from db import get_db

router = APIRouter()

# Define the /add endpoint
@router.post("/{sensor_id}/data")
async def add_sensor_data(sensor_id: int, data: SensorDataIn, db: Session = Depends(get_db)):
    """
    Endpoint to add sensor data.
    
    Parameters:
        - sensor_id: ID of the sensor.
        - data: Sensor data payload.
        - db: Database session (injected).

    Returns:
        - The created SensorData record.
    """

    record = SensorData(
        sensor_id = sensor_id,
        metric = data.metric,
        value = data.value,
        timestamp = data.timestamp,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
