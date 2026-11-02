"""
Backend API Validation & Negative Tests.
Kiểm thử kiểm tra ràng buộc đầu vào (boundary & negative testing),
xử lý ngoại lệ, và xác thực schema Pydantic.
"""

import pytest
from pydantic import ValidationError
from backend.schemas import ForecastRequest
from backend.routes.air_quality import forecast_air_quality, get_station_history
from fastapi import HTTPException

def run_coro(coro):
    try:
        coro.send(None)
    except StopIteration as e:
        return e.value

def test_validation_horizon_hours_below_minimum():
    # horizon_hours = 0 phải bị Pydantic chặn (ge=1)
    with pytest.raises(ValidationError) as exc_info:
        ForecastRequest(station_id="VN_HN_01", horizon_hours=0)
    assert "greater than or equal to 1" in str(exc_info.value)

def test_validation_horizon_hours_negative():
    # horizon_hours < 0 phải bị chặn
    with pytest.raises(ValidationError) as exc_info:
        ForecastRequest(station_id="VN_HN_01", horizon_hours=-10)
    assert "greater than or equal to 1" in str(exc_info.value)

def test_validation_horizon_hours_exceed_maximum():
    # horizon_hours > 48 phải bị Pydantic chặn (le=48)
    with pytest.raises(ValidationError) as exc_info:
        ForecastRequest(station_id="VN_HN_01", horizon_hours=49)
    assert "less than or equal to 48" in str(exc_info.value)

def test_validation_horizon_hours_valid_boundaries():
    # Biên dưới 1 giờ
    req_min = ForecastRequest(station_id="VN_HN_01", horizon_hours=1)
    assert req_min.horizon_hours == 1

    # Biên trên 48 giờ
    req_max = ForecastRequest(station_id="VN_HN_01", horizon_hours=48)
    assert req_max.horizon_hours == 48

def test_validation_invalid_model_name_fallback_or_handling(app_state):
    # Khi truyền mô hình không tồn tại, hệ thống phải xử lý an toàn (fallback về mô hình mặc định hoặc xử lý graceful)
    req = ForecastRequest(station_id="VN_HN_01", model_name="Non_Existent_Model_123", horizon_hours=6)
    res = run_coro(forecast_air_quality(req))
    assert res is not None
    assert len(res["forecast_steps"]) == 6

def test_validation_unknown_station_id_fallback(app_state):
    # Khi truyền trạm lạ không nằm trong database, hệ thống tự động fallback sang dữ liệu mặc định chuẩn
    req = ForecastRequest(station_id="UNKNOWN_STATION_999", model_name="Random_Forest", horizon_hours=6)
    res = run_coro(forecast_air_quality(req))
    assert res is not None
    assert len(res["forecast_steps"]) == 6
    assert res["forecast_steps"][0].pm25_predicted > 0

def test_validation_history_hours_graceful(app_state):
    # Kiểm thử endpoint history với số giờ 24
    res = run_coro(get_station_history(station_id="VN_HN", hours=24))
    assert "records" in res
    assert len(res["records"]) <= 24
