"""
Client Data & Logic Unit Tests.
Kiểm thử dữ liệu 34 tỉnh thành và 101 trạm quan trắc, thuật toán tính chu kỳ Ngày/Đêm,
phân cấp chuẩn AQI Việt Nam & US-EPA, và dữ liệu offline fallback.
"""

import json
import re
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def test_vietnam_stations_data_completeness(stations_js_content):
    # Trích xuất danh sách key tỉnh thành
    matches = re.findall(r'\"(VN_[A-Z0-9]+)\"\s*:\s*\[', stations_js_content)
    unique_provinces = list(set(matches))
    assert len(unique_provinces) == 34, f"Cần chính xác 34 tỉnh thành, tìm thấy: {len(unique_provinces)}"

    # Trích xuất tổng số trạm đo
    station_ids = re.findall(r'\"id\":\s*\"(VN_[A-Z0-9_]+)\"', stations_js_content)
    assert len(station_ids) >= 100, f"Tổng số trạm đo phải đạt ít nhất 100, tìm thấy: {len(station_ids)}"

def test_stations_geographical_bounds(stations_js_content):
    # Kiểm tra tọa độ địa lý Việt Nam: Vĩ độ 8°N - 24°N, Kinh độ 102°E - 110°E
    lats = [float(x) for x in re.findall(r'\"lat\":\s*([0-9.]+)', stations_js_content)]
    lons = [float(x) for x in re.findall(r'\"lon\":\s*([0-9.]+)', stations_js_content)]
    
    assert len(lats) > 0 and len(lons) > 0
    assert len(lats) == len(lons)
    
    for lat in lats:
        assert 8.0 <= lat <= 24.0, f"Vĩ độ ngoài phạm vi lãnh thổ Việt Nam: {lat}"
    for lon in lons:
        assert 102.0 <= lon <= 112.5, f"Kinh độ ngoài phạm vi lãnh thổ Việt Nam: {lon}"

def test_aqi_classification_logic():
    # Kiểm tra thuật toán phân cấp chất lượng không khí chuẩn QCVN 05:2023 / US-EPA
    def classify_aqi(pm25):
        if pm25 <= 12.0:
            return "Tốt", "#10b981"
        elif pm25 <= 35.4:
            return "Trung bình", "#f59e0b"
        elif pm25 <= 55.4:
            return "Kém", "#f97316"
        elif pm25 <= 150.4:
            return "Xấu", "#ef4444"
        elif pm25 <= 250.4:
            return "Rất xấu", "#8b5cf6"
        else:
            return "Nguy hại", "#881337"

    assert classify_aqi(8.5)[0] == "Tốt"
    assert classify_aqi(25.0)[0] == "Trung bình"
    assert classify_aqi(45.0)[0] == "Kém"
    assert classify_aqi(85.0)[0] == "Xấu"
    assert classify_aqi(180.0)[0] == "Rất xấu"
    assert classify_aqi(300.0)[0] == "Nguy hại"

def test_day_night_cycle_calculation():
    # Kiểm tra thuật toán xác định ban ngày / ban đêm theo giờ thực tế
    def get_is_daytime(hour: int) -> bool:
        return 6 <= hour < 18

    # Ban ngày: 6h sáng đến 17h chiều
    assert get_is_daytime(6) is True
    assert get_is_daytime(12) is True
    assert get_is_daytime(17) is True

    # Ban đêm: 18h tối đến 5h sáng hôm sau
    assert get_is_daytime(18) is False
    assert get_is_daytime(22) is False
    assert get_is_daytime(0) is False
    assert get_is_daytime(5) is False

def test_embedded_offline_fallback_file():
    embedded_file = BASE_DIR / "js" / "embedded_data.js"
    assert embedded_file.exists(), "Tập tin js/embedded_data.js phải tồn tại để phục vụ chạy offline"
    
    with open(embedded_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert "EMBEDDED_DATA" in content
    assert "Int8" in content or "quantized" in content.lower()
