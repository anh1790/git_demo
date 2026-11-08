import urllib.request
import os

headers = {'User-Agent': 'Mozilla/5.0'}
url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/8/116/207'
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp, open('tmp_tiles/esri_imagery_hs.jpg', 'wb') as f:
        f.write(resp.read())
    print('Imagery OK:', os.path.getsize('tmp_tiles/esri_imagery_hs.jpg'))
except Exception as e:
    print('Imagery error:', e)
