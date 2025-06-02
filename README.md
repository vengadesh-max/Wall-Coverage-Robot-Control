# Wall Coverage Robot Control System

This project implements a backend and frontend for an autonomous wall-finishing robot control system.

## Setup

1. **Install Dependencies**

   Make sure you have Python 3.7+ installed.
   
   Clone repository : https://github.com/vengadesh-max/Wall-Coverage-Robot-Control.git

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

   ![Screenshot (1766)](https://github.com/user-attachments/assets/0d126e1a-084e-4858-8e8f-8efddd7e5b5c)


To stop both servers, press `Ctrl+C` in the terminal where you ran the `run.py` script.
