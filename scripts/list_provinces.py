import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, ".")
from backend.provinces_data import PROVINCES_34

print(f"Total provinces: {len(PROVINCES_34)}")
for i, p in enumerate(PROVINCES_34):
    print(f"{i+1:2d}. {p['id']:<8} {p['name']:<25} ({p['lat']:.4f}, {p['lon']:.4f})")
