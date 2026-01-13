import os

# Absolute path of project root (portal)
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
SUMMARY_DIR = os.path.join(PROJECT_ROOT, "summary")
