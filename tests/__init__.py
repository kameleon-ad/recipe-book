# tests/__init__.py

import os
import sys

from app import create_app
from config import TestConfig

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = create_app(TestConfig)
