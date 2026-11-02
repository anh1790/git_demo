"""
Frontend & Backend Integration Tests.
Kiểm thử tính tương thích dữ liệu và toàn vẹn luồng giữa Giao diện (Frontend)
và Máy chủ (Backend): Khớp danh sách trạm & tỉnh thành, luồng dự báo E2E,
và cơ chế chịu lỗi offline fallback.
"""

import re
import json
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent.parent

from backend.routes.air_quality import forecast_air_quality, run_concurrency_load_test
from backend.schemas import ForecastRequest
from backend.provinces_data import PROVINCES_34

def run_coro(coro):
    try:
        coro.send(None)
    except StopIteration as e:
        return e.value

def test_province_ids_alignment_fe_and_be(stations_js_content):
    # Lấy danh sách ID tỉnh thành từ frontend stations_data.js
    fe_province_ids = set(re.findall(r'\"(VN_[A-Z0-9]+)\"\s*:\s*\[', stations_js_content))
    
    # Lấy danh sách ID tỉnh thành từ backend provinces_data.py
    be_province_ids = set(p["id"] for p in PROVINCES_34)

    assert len(fe_province_ids) == 34
    assert len(be_province_ids) == 34
    assert fe_province_ids == be_province_ids, "Danh sách mã 34 tỉnh thành giữa Frontend và Backend phải trùng khớp 100%"

def test_primary_stations_alignment(stations_js_content, app_state):
    # 8 trạm quan trắc gốc của Hà Nội trong backend
    be_station_ids = set(app_state.stations_df["station_id"].tolist())
    assert len(be_station_ids) == 8

    # 8 trạm này phải có mặt trong stations_data.js
    for sid in be_station_ids:
        assert f'"{sid}"' in stations_js_content, f"Trạm {sid} của Backend thiếu trong Frontend stations_data.js"

def test_end_to_end_forecast_flow(app_state):
    # Mô phỏng luồng Frontend chọn tỉnh -> gửi request -> Backend AI chạy -> trả kết quả cho biểu đồ
    selected_province = "VN_TN" # Tây Ninh
    req = ForecastRequest(
        station_id=selected_province,
        pollutant="pm25",
        model_name="Random_Forest",
        horizon_hours=24
    )
    res = run_coro(forecast_air_quality(req))
    
    # Xác minh dữ liệu đầu ra phù hợp định dạng Chart.js của Frontend
    assert res["station_id"] == selected_province
    assert len(res["forecast_steps"]) == 24
    
    chart_labels = [s.forecast_time for s in res["forecast_steps"]]
    chart_values = [s.pm25_predicted for s in res["forecast_steps"]]
    chart_lower = [s.lower_bound for s in res["forecast_steps"]]
    chart_upper = [s.upper_bound for s in res["forecast_steps"]]

    assert len(chart_labels) == 24
    assert len(chart_values) == 24
    assert all(val > 0 for val in chart_values)
    assert all(chart_lower[i] <= chart_values[i] <= chart_upper[i] for i in range(24))

def test_offline_fallback_compatibility():
    # Kiểm tra cơ chế tự thích ứng khi mất kết nối backend
    embedded_file = BASE_DIR / "js" / "embedded_data.js"
    assert embedded_file.exists()
    
    with open(embedded_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Kiểm tra các cấu trúc hỗ trợ chạy độc lập client-side
    assert "Int8" in content or "quantized" in content.lower()
    assert "random_forest" in content.lower() or "rf" in content.lower()

def test_concurrency_load_integration(app_state):
    # Kiểm thử tích hợp tải đồng thời phục vụ người dùng
    res = run_coro(run_concurrency_load_test(concurrent_requests=12))
    assert res["status"] == "success"
    assert res["error_rate_pct"] == 0.0
    assert res["successful_requests"] == 12
