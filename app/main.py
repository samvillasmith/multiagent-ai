import subprocess
import threading
import time
import os
import sys

from dotenv import load_dotenv

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

load_dotenv()

def run_backend():
    try:
        logger.info("Starting backend server")
        subprocess.run(["uvicorn", "app.backend.api:app", "--host", "127.0.0.1", "--port", "9999"], check=True)
    except subprocess.CalledProcessError as e:
        error = CustomException("Backend server failed to start", e)
        logger.error(str(error))
        raise error
    except Exception as e:
        error = CustomException("Unexpected error in backend", e)
        logger.error(str(error))
        raise error

def run_frontend():
    try:
        logger.info("Starting frontend UI")
        # Get the absolute path to the ui.py file
        ui_path = os.path.join(os.path.dirname(__file__), "frontend", "ui.py")
        
        # Set PYTHONPATH to include the project root
        env = os.environ.copy()
        project_root = os.path.dirname(os.path.dirname(__file__))  # Go up from app/ to Multiagent/
        env['PYTHONPATH'] = project_root
        
        subprocess.run(["streamlit", "run", ui_path], check=True, env=env)
    except subprocess.CalledProcessError as e:
        error = CustomException("Frontend UI failed to start", e)
        logger.error(str(error))
        raise error
    except Exception as e:
        error = CustomException("Unexpected error in frontend", e)
        logger.error(str(error))
        raise error

if __name__ == "__main__":
    try:
        threading.Thread(target=run_backend, daemon=True).start()
        time.sleep(5)  # Wait for backend to start
        run_frontend()
    except CustomException as e:
        logger.exception(f"Critical error in main application: {str(e)}")
    except Exception as e:
        error = CustomException("Unexpected critical error", e)
        logger.exception(str(error))