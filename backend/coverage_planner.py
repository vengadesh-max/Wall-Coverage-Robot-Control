import math
from typing import List, Tuple, Union, Dict
import numpy as np
from dataclasses import dataclass


@dataclass
class Obstacle:
    type: str  # 'rectangle' or 'circle'
    x: float
    y: float
    width: float  # For rectangle
    height: float  # For rectangle
    radius: float = 0.0  # For circle


def is_point_in_obstacle(x: float, y: float, obstacle: Obstacle) -> bool:
    """
    Checks if a point (x, y) is inside an obstacle.
    """
    if obstacle.type == "rectangle":
        return (
            obstacle.x <= x <= obstacle.x + obstacle.width
            and obstacle.y <= y <= obstacle.y + obstacle.height
        )
    elif obstacle.type == "circle":
        distance = math.sqrt((x - obstacle.x) ** 2 + (y - obstacle.y) ** 2)
        return distance <= obstacle.radius
    return False


def optimize_path(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    Optimize the path using a simple nearest neighbor algorithm.
    """
    if not points:
        return points

    unvisited = points.copy()
    optimized = [unvisited.pop(0)]  # Start with the first point

    while unvisited:
        current = optimized[-1]
        # Find the nearest unvisited point
        nearest_idx = min(
            range(len(unvisited)),
            key=lambda i: math.sqrt(
                (current[0] - unvisited[i][0]) ** 2
                + (current[1] - unvisited[i][1]) ** 2
            ),
        )
        optimized.append(unvisited.pop(nearest_idx))

    return optimized


def plan_rectangular_wall(
    width: float,
    height: float,
    step_size: float,
    obstacles: List[Dict] = None,
    optimize: bool = True,
) -> List[Tuple[float, float]]:
    """
    Generates an optimized coverage path for a rectangular wall, avoiding obstacles.
    Args:
        width: Wall width in meters
        height: Wall height in meters
        step_size: Distance between coverage points in meters
        obstacles: List of obstacle dictionaries with type, position, and dimensions
        optimize: Whether to optimize the path for minimum travel distance
    """
    if obstacles is None:
        obstacles = []

    # Convert obstacle dictionaries to Obstacle objects
    obstacle_objects = []
    for obs in obstacles:
        if obs["type"] == "rectangle":
            obstacle_objects.append(
                Obstacle(
                    type="rectangle",
                    x=obs["x"],
                    y=obs["y"],
                    width=obs["width"],
                    height=obs["height"],
                )
            )
        elif obs["type"] == "circle":
            obstacle_objects.append(
                Obstacle(type="circle", x=obs["x"], y=obs["y"], radius=obs["radius"])
            )

    trajectory = []
    y = 0.0
    direction = 1  # 1 for moving right, -1 for moving left

    while y <= height:
        if direction == 1:
            # Move right
            x = 0.0
            while x <= width:
                # Check if the current point is inside any obstacle
                is_obstacle_point = any(
                    is_point_in_obstacle(x, y, obs) for obs in obstacle_objects
                )

                if not is_obstacle_point:
                    trajectory.append((x, y))

                x += step_size

            # Ensure the endpoint is included if it's exactly on the boundary
            if (width - (x - step_size)) < step_size:
                is_obstacle_point = any(
                    is_point_in_obstacle(width, y, obs) for obs in obstacle_objects
                )
                if not is_obstacle_point:
                    trajectory.append((width, y))
        else:
            # Move left
            x = width
            while x >= 0.0:
                is_obstacle_point = any(
                    is_point_in_obstacle(x, y, obs) for obs in obstacle_objects
                )

                if not is_obstacle_point:
                    trajectory.append((x, y))

                x -= step_size

            if (x + step_size) - 0.0 < step_size:
                is_obstacle_point = any(
                    is_point_in_obstacle(0.0, y, obs) for obs in obstacle_objects
                )
                if not is_obstacle_point:
                    trajectory.append((0.0, y))

        y += step_size
        direction *= -1

    # Ensure the last row is covered
    if (height - (y - step_size)) < step_size:
        y = height
        if direction == -1:
            x = 0.0
            while x <= width:
                is_obstacle_point = any(
                    is_point_in_obstacle(x, y, obs) for obs in obstacle_objects
                )
                if not is_obstacle_point:
                    trajectory.append((x, y))
                x += step_size
        else:
            x = width
            while x >= 0.0:
                is_obstacle_point = any(
                    is_point_in_obstacle(x, y, obs) for obs in obstacle_objects
                )
                if not is_obstacle_point:
                    trajectory.append((x, y))
                x -= step_size

    # Optimize the path if requested
    if optimize and trajectory:
        trajectory = optimize_path(trajectory)

    return trajectory


if __name__ == "__main__":
    # Example usage with mixed obstacles
    wall_width = 5.0
    wall_height = 5.0
    robot_step_size = 0.25

    obstacles = [
        {"type": "rectangle", "x": 1.0, "y": 1.0, "width": 0.5, "height": 0.5},
        {"type": "circle", "x": 3.0, "y": 3.0, "radius": 0.3},
    ]

    planned_path = plan_rectangular_wall(
        wall_width, wall_height, robot_step_size, obstacles, optimize=True
    )

    print(
        f"Generated {len(planned_path)} trajectory points (with obstacle avoidance and optimization)."
    )
    print("First 10 points:", planned_path[:10])
    print("Last 10 points:", planned_path[-10:])
