# Wall Coverage Robot Control System

This project implements a backend and frontend for an autonomous wall-finishing robot control system. It includes coverage planning, data management, visualization, and testing.

## Project Structure

- `backend/`: FastAPI application and database
- `frontend/`: HTML/CSS/JavaScript for visualization
- `tests/`: API tests
- `run.py`: Script to run both backend and frontend
- `install_dependencies.py`: Script to install project dependencies

## Setup

1. **Install Dependencies**

   Make sure you have Python 3.7+ installed.

   Run the dependency installation script from the project root:

   ```bash
   python install_dependencies.py
   ```

   This will install the necessary packages for the backend.

## Running the Application

To start both the backend and the frontend servers, run the `run.py` script from the project root:

```bash
python run.py
```

This script will:

1. Start the FastAPI backend server on `http://localhost:8000`.
2. Start the frontend server using Python's built-in `http.server` on `http://localhost:3000`.
3. Open your default web browser to `http://localhost:3000`.

To stop both servers, press `Ctrl+C` in the terminal where you ran the `run.py` script.

## Using the Frontend UI

Once the application is running and you have opened `http://localhost:3000` in your browser:

1.  **Configure Wall and Step Size:** Enter the desired wall width, height, and step size in the input fields on the left panel.
2.  **Add Obstacles:**
    - Select the obstacle type (Rectangle or Circle).
    - Enter the position (X, Y) and dimensions (Width/Height for Rectangle, Radius for Circle).
    - Click the "Add Obstacle" button. Added obstacles will appear in the list.
    - You can remove obstacles using the "Remove" button next to each obstacle.
3.  **Optimize Path:** Check or uncheck the "Optimize Path" checkbox to enable or disable path optimization.
4.  **Plan Trajectory:** Click the "Plan Trajectory" button to send the configuration and obstacles to the backend and generate the trajectory.
5.  **Visualize and Playback:**
    - The planned trajectory and obstacles will be displayed on the canvas in the right panel.
    - Use the "Play", "Pause", and "Reset" buttons to control the trajectory playback.
    - Adjust the playback speed using the speed slider.

## API Endpoints

The backend provides the following API endpoints:

- `GET /`: Basic endpoint to check if the backend is running.
- `POST /trajectory/`: Add a single trajectory point.
- `GET /trajectory/`: Retrieve all stored trajectory points.
- `DELETE /trajectory/`: Delete all stored trajectory points.
- `POST /plan/rectangular/`: Plan and store a rectangular coverage trajectory with optional obstacles and optimization.

## Running Tests

To run the backend API tests using pytest, navigate to the `backend` directory and run:

```bash
cd backend
pytest ../tests
```

## Notes

- The backend uses FastAPI and SQLite for data storage.
- The frontend uses HTML5 Canvas for visualization.
- CORS is configured to allow communication between the frontend and backend.
