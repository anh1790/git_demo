import urllib.request
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# Esri layers
# 1. World_Topo_Map: Clean topographical map, standard international cartography
# 2. World_Street_Map: Clean road & street map
# 3. Canvas/World_Light_Gray_Base: Clean minimalist base
# 4. Ocean/World_Ocean_Base: Bathymetric ocean base

layers = {
    'esri_topo_vn': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/7/58/103',
    'esri_street_vn': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/7/58/103',
    'esri_street_hanoi': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/8/110/203',
    'esri_topo_hanoi': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/8/110/203'
}

for name, url in layers.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp, open(f'tmp_tiles/{name}.png', 'wb') as f:
            f.write(resp.read())
        print(f'{name}: OK ({os.path.getsize(f"tmp_tiles/{name}.png")} bytes)')
    except Exception as e:
        print(f'{name}: {e}')
