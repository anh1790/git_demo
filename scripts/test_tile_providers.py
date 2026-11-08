import urllib.request
import os

headers = {'User-Agent': 'Mozilla/5.0'}
urls = {
    'osm': 'https://tile.openstreetmap.org/8/207/116.png',
    'carto_light': 'https://a.basemaps.cartocdn.com/light_all/8/207/116.png',
    'carto_nolabels': 'https://a.basemaps.cartocdn.com/light_nolabels/8/207/116.png',
    'carto_voyager': 'https://a.basemaps.cartocdn.com/rastertiles/voyager/8/207/116.png',
    'esri_gray': 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/8/116/207',
    'esri_topo': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/8/116/207'
}

os.makedirs('tmp_tiles', exist_ok=True)
for name, url in urls.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp, open(f'tmp_tiles/{name}.png', 'wb') as f:
            f.write(resp.read())
        size = os.path.getsize(f'tmp_tiles/{name}.png')
        print(f'{name}: OK ({size} bytes)')
    except Exception as e:
        print(f'{name}: ERROR {e}')
