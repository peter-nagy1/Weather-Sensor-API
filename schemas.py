from pydantic import BaseModel
from datetime import datetime

# Schemas
class SensorDataIn(BaseModel):
    metric: str
    value: float
    timestamp: datetime
