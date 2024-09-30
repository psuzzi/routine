# File: init-backend/init-backend.py

import sys
from pathlib import Path

# Add the parent directory to sys.path to allow importing from utils
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.project_initializer import ProjectInitializer

# Config constants
CONFIG_FILE_PATH = 'init-app-config.yaml'

def main():

    initializer = ProjectInitializer(Path(__file__).resolve().parent, CONFIG_FILE_PATH, "Manage project structure")
    initializer.run()

if __name__ == "__main__":
    main()