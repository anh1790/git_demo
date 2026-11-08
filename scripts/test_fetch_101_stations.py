import sys
import json
import urllib.request
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, ".")
from backend.provinces_data import STATIONS_CONFIG

all_stations = []
for pid, st_list in STATIONS_CONFIG.items():
    for s in st_list:
        all_stations.append(s)

print(f"Total stations to fetch: {len(all_stations)}")

# Split into 2 chunks: 50 and 51
chunks = [all_stations[:50], all_stations[50:]]
station_results = []

for c_idx, chunk in enumerate(chunks):
    lats = ",".join(f"{s['lat']:.4f}" for s in chunk)
    lons = ",".join(f"{s['lon']:.4f}" for s in chunk)
    
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lats}&longitude={lons}&"
        f"current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,wind_speed_10m&"
        f"timezone=Asia%2FBangkok"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 AirSense-LiveSync"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        if not isinstance(res, list):
            res = [res]
        station_results.extend(res)
    print(f"Chunk {c_idx+1} fetched: {len(res)} stations")

print(f"Total station results fetched: {len(station_results)}")
print("Sample station 1 (Ba Dinh, HN):", chunk[0]["name"], station_results[0].get("current"))
print("Sample station 55 (Da Nang Son Tra):", all_stations[54]["name"], station_results[54].get("current"))
