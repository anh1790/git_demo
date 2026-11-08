import sys
import json
import urllib.request
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, ".")
from backend.provinces_data import PROVINCES_34

lats = ",".join(f"{p['lat']:.4f}" for p in PROVINCES_34)
lons = ",".join(f"{p['lon']:.4f}" for p in PROVINCES_34)

# 1. Fetch live weather
weather_url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={lats}&longitude={lons}&"
    f"current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m,uv_index&"
    f"timezone=Asia%2FBangkok"
)

req_w = urllib.request.Request(weather_url, headers={"User-Agent": "Mozilla/5.0 AirSense-LiveSync"})
with urllib.request.urlopen(req_w, timeout=20) as resp:
    weather_data = json.loads(resp.read().decode('utf-8'))

if not isinstance(weather_data, list):
    weather_data = [weather_data]

# 2. Fetch live air quality
air_url = (
    f"https://air-quality-api.open-meteo.com/v1/air-quality?"
    f"latitude={lats}&longitude={lons}&"
    f"current=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi&"
    f"timezone=Asia%2FBangkok"
)

req_a = urllib.request.Request(air_url, headers={"User-Agent": "Mozilla/5.0 AirSense-LiveSync"})
with urllib.request.urlopen(req_a, timeout=20) as resp:
    air_data = json.loads(resp.read().decode('utf-8'))

if not isinstance(air_data, list):
    air_data = [air_data]

print(f"{'#':<3} {'Mã':<8} {'Tỉnh / Thành':<22} {'Nhiệt độ':<9} {'Độ ẩm':<7} {'Mưa':<7} {'Gió':<14} {'PM2.5':<8} {'AQI':<6}")
print("-" * 90)

for i, p in enumerate(PROVINCES_34):
    w = weather_data[i].get("current", {})
    a = air_data[i].get("current", {})
    temp = w.get("temperature_2m", 25.0)
    hum = w.get("relative_humidity_2m", 70)
    rain = w.get("rain", 0.0)
    wind_spd = w.get("wind_speed_10m", 3.0)
    wind_deg = w.get("wind_direction_10m", 90)
    pm25 = a.get("pm2_5", 15.0)
    aqi = a.get("us_aqi", 50)
    print(f"{i+1:<3} {p['id']:<8} {p['name']:<22} {temp:>4.1f}°C   {hum:>3}%   {rain:>4.1f}mm {wind_spd:>4.1f}m/s      {pm25:>5.1f}   {aqi:>4}")
