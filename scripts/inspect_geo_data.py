import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from backend.provinces_data import PROVINCES_34
import geopandas as gpd

print(f"=== KIỂM TRA 34 TỈNH THÀNH VIỆT NAM ({len(PROVINCES_34)} TỈNH) ===")
regions_count = {}
for i, p in enumerate(PROVINCES_34):
    r = p.get('region', 'Không rõ')
    regions_count[r] = regions_count.get(r, 0) + 1
    lat, lon = p.get('lat'), p.get('lon')
    # Validate Vietnam bounding box (mainland: 8.5 <= lat <= 23.5, 102.0 <= lon <= 109.8)
    valid_lat = (8.5 <= lat <= 23.5)
    valid_lon = (102.0 <= lon <= 109.8)
    status = "OK" if (valid_lat and valid_lon) else "CHECK"
    print(f"{i+1:2d}. [{p['id']}] {p['name']:<20} | Tỉnh: {p.get('province',''):<20} | Miền: {r:<10} | [{lat:6.3f}, {lon:7.3f}] -> {status}")

print("\nPhân bổ theo vùng miền:")
for r, c in regions_count.items():
    print(f" - {r}: {c} tỉnh/thành")

print("\n=== KIỂM TRA DỮ LIỆU GEOPANDAS (data/geo/) ===")
districts_gdf = gpd.read_file(os.path.join(ROOT, "data", "geo", "districts.geojson"))
stations_gdf = gpd.read_file(os.path.join(ROOT, "data", "geo", "stations.geojson"))

print(f"Districts GeoDataFrame: {len(districts_gdf)} features | CRS: {districts_gdf.crs}")
print(districts_gdf[['district_name', 'city', 'country']].to_string())

print(f"\nStations GeoDataFrame: {len(stations_gdf)} features | CRS: {stations_gdf.crs}")
print(stations_gdf[['station_id', 'station_name', 'district', 'station_type']].to_string())
