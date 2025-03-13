import sys
from pathlib import Path


def pytest_configure(config):
    project_root = Path(__file__).resolve().parents[2]  # Adjust the number of parents
    src_path = project_root / "src"
    sys.path.append(str(src_path))
