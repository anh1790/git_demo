import sys
import json
import urllib.request
import time
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, ".")
from backend.provinces_data import PROVINCES_34

lats = ",".join(f"{p['lat']:.4f}" for p in PROVINCES_34)
lons = ",".join(f"{p['lon']:.4f}" for p in PROVINCES_34)

# 1. Fetch real-time weather
weather_url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={lats}&longitude={lons}&"
    f"current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m,uv_index&"
    f"hourly=temperature_2m,relative_humidity_2m,precipitation_probability,weather_code&"
    f"timezone=Asia%2FBangkok&forecast_days=2"
)

print("Fetching real-time weather for 34 provinces from Open-Meteo...")
req = urllib.request.Request(weather_url, headers={"User-Agent": "Mozilla/5.0 AirSense-LiveSync"})
with urllib.request.urlopen(req, timeout=15) as resp:
    weather_data = json.loads(resp.read().decode('utf-8'))

if not isinstance(weather_data, list):
    weather_data = [weather_data]

print(f"Successfully received real-time weather observations for {len(weather_data)} locations!")

# 2. Fetch real-time air quality
air_url = (
    f"https://air-quality-api.open-meteo.com/v1/air-quality?"
    f"latitude={lats}&longitude={lons}&"
    f"current=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi&"
    f"timezone=Asia%2FBangkok"
)

print("Fetching real-time air quality for 34 provinces from Open-Meteo Air Quality...")
req_air = urllib.request.Request(air_url, headers={"User-Agent": "Mozilla/5.0 AirSense-LiveSync"})
with urllib.request.urlopen(req_air, timeout=15) as resp:
    air_data = json.loads(resp.read().decode('utf-8'))

if not isinstance(air_data, list):
    air_data = [air_data]

print(f"Successfully received real-time air quality observations for {len(air_data)} locations!")

# Display a sample of results
print("\n--- SAMPLE REAL-TIME OBSERVATIONS (LIVE) ---")
for i in [0, 1, 2, 3, 4, 27]: # HN, HP, Hue, DN, HCM, Lam Dong (Da Lat)
    p = PROVINCES_34[i]
    w = weather_data[i].get("current", {})
    a = air_data[i].get("current", {})
    print(f"[{p['id']}] {p['name']}: {w.get('temperature_2m')}°C, Độ ẩm {w.get('relative_humidity_2m')}%, Mưa {w.get('rain')}mm, Gió {w.get('wind_speed_10m')}m/s, PM2.5: {a.get('pm2_5')}µg/m³, AQI: {a.get('us_aqi')} (Observed: {w.get('time')})")
