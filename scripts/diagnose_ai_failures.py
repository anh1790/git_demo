# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.services.ai_engine import ai_engine
from scripts.test_50_ai_scenarios import SCENARIOS

failed_ids = ["TC02", "TC06", "TC08", "TC14", "TC16", "TC22", "TC30", "TC33", "TC34", "TC39", "TC40", "TC41", "TC42", "TC43", "TC44", "TC45", "TC47", "TC48"]

for sc in SCENARIOS:
    if sc["id"] in failed_ids:
        res = ai_engine.process_chat(sc["query"], sc["session"], sc["ui_prov"])
        print(f"=== {sc['id']}: {sc['query']} ===")
        print(f"PID: {res.get('province_id')} (Expected: {sc['expected_prov_id']})")
        print(f"REPLY snippet: {res.get('reply')[:180]}...")
        kw_missing = [kw for kw in sc["expected_keywords"] if kw.lower() not in res.get('reply', '').lower()]
        print(f"Missing KW: {kw_missing}")
        print()
