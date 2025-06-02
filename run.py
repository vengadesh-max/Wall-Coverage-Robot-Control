import subprocess
import sys
import webbrowser
import time
import os
from threading import Thread
import pathlib
import shutil


def ensure_frontend_directory():
    # Get absolute paths
    current_dir = pathlib.Path.cwd()
    frontend_dir = current_dir / "frontend"

    print(f"Current directory: {current_dir}")
    print(f"Frontend directory path: {frontend_dir}")
    print(f"Frontend directory exists: {frontend_dir.exists()}")

    if not frontend_dir.exists():
        print(f"Creating frontend directory at {frontend_dir}")
        try:
            frontend_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created frontend directory: {frontend_dir.exists()}")
        except Exception as e:
            print(f"Error creating frontend directory: {e}")
            return False

    # Ensure index.html exists
    index_path = frontend_dir / "index.html"
    print(f"Index.html path: {index_path}")
    print(f"Index.html exists: {index_path.exists()}")

    if not index_path.exists():
        print("Error: index.html not found in frontend directory!")
        return False

    return True


def run_backend():
    print("Starting backend server...")
    current_dir = pathlib.Path.cwd()
    backend_dir = current_dir / "backend"

    print(f"Current directory: {current_dir}")
    print(f"Backend directory path: {backend_dir}")
    print(f"Backend directory exists: {backend_dir.exists()}")

    if not backend_dir.exists():
        print("Error: Backend directory not found!")
        return

    try:
        os.chdir(backend_dir)
        print(f"Changed to backend directory: {os.getcwd()}")
        subprocess.run(
            [sys.executable, "-m", "uvicorn", "main:app", "--reload", "--port", "8000"]
        )
    except Exception as e:
        print(f"Error running backend server: {e}")


def run_frontend(original_dir):
    print("Starting frontend server...")
    frontend_dir = original_dir / "frontend"

    print(f"Original directory: {original_dir}")
    print(f"Frontend directory path: {frontend_dir}")
    print(f"Frontend directory exists: {frontend_dir.exists()}")

    if not frontend_dir.exists():
        print("Error: Frontend directory not found!")
        return

    print(f"Frontend directory contents: {list(frontend_dir.iterdir())}")

    index_path = frontend_dir / "index.html"
    print(f"Index.html path: {index_path}")
    print(f"Index.html exists: {index_path.exists()}")

    if not index_path.exists():
        print("Error: index.html not found in frontend directory!")
        return

    try:
        os.chdir(frontend_dir)
        print(f"Changed to frontend directory: {os.getcwd()}")
        subprocess.run([sys.executable, "-m", "http.server", "3000"])
    except Exception as e:
        print(f"Error running frontend server: {e}")


if __name__ == "__main__":
    # Store the original directory
    original_dir = pathlib.Path.cwd()
    print(f"Original directory: {original_dir}")

    # Ensure frontend directory exists with index.html
    if not ensure_frontend_directory():
        print("Failed to set up frontend directory. Exiting...")
        sys.exit(1)

    # Start backend server in a separate thread
    backend_thread = Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()

    # Wait a moment for the backend to start
    time.sleep(2)

    # Start frontend server in a separate thread
    frontend_thread = Thread(target=run_frontend, args=(original_dir,))
    frontend_thread.daemon = True
    frontend_thread.start()

    # Wait a moment for the frontend to start
    time.sleep(2)

    # Open the browser
    webbrowser.open("http://localhost:3000")

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        os.chdir(original_dir)
        sys.exit(0)
