"""
Pytest configuration.

This file explicitly sets the Backend directory as the Python package root
so that imports using the `app.*` namespace resolve correctly during tests.

This does NOT affect production runtime.
"""

import sys
from pathlib import Path

# Resolve repo root
REPO_ROOT = Path(__file__).resolve().parents[1]

# Add Backend/ to PYTHONPATH for tests
BACKEND_PATH = REPO_ROOT / "Backend"

if str(BACKEND_PATH) not in sys.path:
    sys.path.insert(0, str(BACKEND_PATH))
