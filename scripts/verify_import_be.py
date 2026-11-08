# -*- coding: utf-8 -*-
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

try:
    import backend.app
    print("SUCCESS: backend.app imported without error!")
except Exception as e:
    print("FAILED:", e)
    sys.exit(1)
