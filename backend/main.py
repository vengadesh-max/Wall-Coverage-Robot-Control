import logging
from fastapi import FastAPI, HTTPException
from databases import Database
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    Float,
    select,
    delete,
)
import time
from typing import List, Tuple, Dict, Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from coverage_planner import plan_rectangular_wall

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///./trajectory.db"

database = Database(DATABASE_URL)
metadata = MetaData()

trajectories = Table(
    "trajectories",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("x", Float),
    Column("y", Float),
    Column("timestamp", Float),
)


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

metadata.create_all(engine)

app = FastAPI(title="Wall Coverage Robot API")

# Configure CORS
origins = [
    "http://localhost:3000",  # Example frontend origin
    "http://localhost:8000",  # Allow requests from the same origin as the backend
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request validation
class ObstacleBase(BaseModel):
    type: str = Field(..., description="Type of obstacle: 'rectangle' or 'circle'")
    x: float = Field(..., description="X coordinate of the obstacle")
    y: float = Field(..., description="Y coordinate of the obstacle")


class RectangleObstacle(ObstacleBase):
    type: str = "rectangle"
    width: float = Field(..., description="Width of the rectangle")
    height: float = Field(..., description="Height of the rectangle")


class CircleObstacle(ObstacleBase):
    type: str = "circle"
    radius: float = Field(..., description="Radius of the circle")


class CoverageRequest(BaseModel):
    width: float = Field(..., gt=0, description="Width of the wall in meters")
    height: float = Field(..., gt=0, description="Height of the wall in meters")
    step_size: float = Field(
        ..., gt=0, description="Step size between coverage points in meters"
    )
    obstacles: Optional[List[Dict]] = Field(
        default=None, description="List of obstacles"
    )
    optimize: bool = Field(default=True, description="Whether to optimize the path")


@app.on_event("startup")
async def startup():
    await database.connect()
    logger.info("Database connected.")


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    logger.info("Database disconnected.")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/trajectory/")
async def create_trajectory(x: float, y: float, timestamp: float):
    query = trajectories.insert().values(x=x, y=y, timestamp=timestamp)
    last_record_id = await database.execute(query)
    logger.info(
        f"Inserted trajectory point: id={last_record_id}, x={x}, y={y}, timestamp={timestamp}"
    )
    return {"id": last_record_id}


@app.get("/trajectory/")
async def get_trajectories():
    query = select(trajectories)
    results = await database.fetch_all(query)
    logger.info(f"Retrieved {len(results)} trajectory points.")
    return results


@app.delete("/trajectory/")
async def delete_all_trajectories():
    start_time = time.time()
    logger.info("Starting deletion of all trajectory points.")

    query = delete(trajectories)
    await database.execute(query)

    end_time = time.time()
    logger.info(
        f"Finished deleting all trajectory points in {end_time - start_time:.4f} seconds."
    )

    return {"message": "All trajectory points deleted successfully."}


@app.post("/plan/rectangular/")
async def plan_and_store_rectangular_trajectory(request: CoverageRequest):
    start_time = time.time()
    logger.info(
        f"Starting rectangular coverage planning for wall {request.width}x{request.height} "
        f"with step size {request.step_size} and {len(request.obstacles) if request.obstacles else 0} obstacles"
    )

    try:
        trajectory_points = plan_rectangular_wall(
            request.width,
            request.height,
            request.step_size,
            request.obstacles,
            request.optimize,
        )

        logger.info(
            f"Generated {len(trajectory_points)} trajectory points. Storing in database..."
        )

        # Store trajectory points in the database
        values_to_insert = [
            {"x": point[0], "y": point[1], "timestamp": time.time()}
            for point in trajectory_points
        ]

        if values_to_insert:
            query = trajectories.insert()
            await database.execute_many(query=query, values=values_to_insert)

        end_time = time.time()
        logger.info(
            f"Finished storing {len(trajectory_points)} trajectory points in {end_time - start_time:.4f} seconds."
        )

        return {
            "message": "Trajectory planned and stored successfully",
            "points_generated": len(trajectory_points),
            "obstacles_processed": len(request.obstacles) if request.obstacles else 0,
            "execution_time": end_time - start_time,
        }
    except Exception as e:
        logger.error("Error planning trajectory:", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
