# -*- coding: utf-8 -*-
import sys
import time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")

from backend.services.weather_sync import live_sync_service

print("=" * 80)
print("AIRSENSE AI - TIẾN TRÌNH ĐỒNG BỘ THỜI TIẾT THỰC TẾ 34 TỈNH & 101 TRẠM QUAN TRẮC")
print("=" * 80)

t0 = time.time()
print("\n>>> Đang kết nối Open-Meteo Weather API & Air Quality API thời gian thực...")
result = live_sync_service.sync_all_provinces_live()
elapsed_fetch = time.time() - t0

print(f">>> Thu thập thành công {result['provinces_count']} tỉnh thành & {result['stations_count']} trạm quan trắc ({elapsed_fetch:.2f}s)!")
print("\n>>> Đang lưu trữ và đồng bộ vào hệ thống (backend, frontend, static)...")
live_sync_service.persist_to_disk()

print(f"\nĐỒNG BỘ HOÀN TẤT VÀO LÚC: {result['sync_time']}")
print("=" * 80)
print(f"{'Mã':<8} {'Tỉnh / Thành':<22} {'Nhiệt độ':<10} {'Cảm giác':<10} {'Độ ẩm':<8} {'Mưa (mm)':<10} {'Gió':<14} {'PM2.5':<8} {'AQI':<6}")
print("-" * 100)

for p in result["provinces"]:
    print(f"{p['id']:<8} {p['name']:<22} {p['temp']:>4.1f}°C    {p['feels_like']:>4.1f}°C    {p['humidity']:>3}%    {p['rain_mm']:>4.1f}mm    {p['wind_speed']:>4.1f}m/s {p['wind_dir']:<7} {p['pm25']:>5.1f}   {round(p['pm25']*1.8):>4}")

print("=" * 100)
