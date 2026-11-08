import urllib.request
import os
import math

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

headers = {'User-Agent': 'Mozilla/5.0'}
os.makedirs('tmp_tiles/ts_check', exist_ok=True)

for z in [6, 7, 8, 9, 10]:
    x, y = deg2num(8.647, 111.919, z)
    url = f'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp, open(f'tmp_tiles/ts_check/esri_ts_z{z}.jpg', 'wb') as f:
            f.write(resp.read())
        print(f'Zoom {z} ({x}, {y}): {os.path.getsize(f"tmp_tiles/ts_check/esri_ts_z{z}.jpg")} bytes')
    except Exception as e:
        print(f'Zoom {z}: {e}')
