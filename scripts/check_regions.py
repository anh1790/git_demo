import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.append('.')
from backend.provinces_data import PROVINCES_34

regions = {}
for p in PROVINCES_34:
    reg = p.get('region', 'Chưa rõ')
    regions.setdefault(reg, []).append((p['id'], p['name']))

for r, items in regions.items():
    print(f"=== {r} ({len(items)}) ===")
    for pid, name in items:
        print(f"  {pid}: {name}")
