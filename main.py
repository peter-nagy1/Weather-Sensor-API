from fastapi import FastAPI
from routers import sensors, query
from db import engine
from models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Weather Sensors API")

app.include_router(sensors.router, prefix="/sensors", tags=["Sensors"])
app.include_router(query.router, prefix="/query", tags=["Query"])

@app.get("/")
async def root():
    return {"message": "Weather Sensors API is running."}