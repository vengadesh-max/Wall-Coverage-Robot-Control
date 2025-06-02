import subprocess
import sys


def install_requirements():
    print("Installing backend dependencies...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"]
    )


if __name__ == "__main__":
    install_requirements()
