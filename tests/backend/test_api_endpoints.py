"""
Backend API Endpoints Unit & Integration Tests.
Kiểm thử toàn bộ các endpoint xử lý dữ liệu của FastAPI:
Health, Stations, Regions GeoJSON, Latest Air Quality, History,
Forecast AI (RF, NN, Baseline cho 34 tỉnh), Optimization Benchmark,
Concurrency Test (12 & 20 CCU), Evaluation Metrics, Explainability.
"""

import pytest
from backend.routes import health, spatial, air_quality, evaluation
from backend.schemas import ForecastRequest

def run_coro(coro):
    try:
        coro.send(None)
    except StopIteration as e:
        return e.value

def test_endpoint_health(app_state):
    res = run_coro(health.get_health())
    # Kiểm tra cấu trúc phản hồi
    assert res["status"] == "healthy"
    assert res["memory_mb"] > 0
    assert res["uptime_seconds"] >= 0
    assert res["stations_count"] == 8
    assert res["districts_count"] == 8
    assert "Random_Forest" in res["models_loaded"]

def test_endpoint_stations_list(app_state):
    stations = run_coro(spatial.list_stations())
    assert len(stations) == 8
    first = stations[0]
    assert "station_id" in first
    assert "station_name" in first
    assert "latitude" in first and "longitude" in first
    assert "dist_center_km" in first
    assert first["dist_center_km"] >= 0.0

def test_endpoint_regions_geojson(app_state):
    geojson = run_coro(spatial.get_geojson_regions())
    assert geojson["type"] == "FeatureCollection"
    assert len(geojson["features"]) == 8
    for feat in geojson["features"]:
        assert feat["type"] == "Feature"
        props = feat["properties"]
        assert "district_name" in props
        assert "pm25" in props
        assert "aqi_level" in props
        assert "color" in props

def test_endpoint_latest_air_quality(app_state):
    latest = run_coro(air_quality.get_latest_observations())
    assert len(latest) == 8
    for obs in latest:
        assert obs["pm25"] > 0
        assert obs["pm10"] > 0
        assert "aqi_level" in obs
        assert "timestamp" in obs

def test_endpoint_history(app_state):
    history = run_coro(air_quality.get_station_history(station_id="VN_HN_01", hours=24))
    assert history["station_id"] == "VN_HN_01"
    assert "records" in history
    assert len(history["records"]) <= 24
    if len(history["records"]) > 0:
        first_rec = history["records"][0]
        assert "value" in first_rec or "pm25" in first_rec
        assert "timestamp" in first_rec

def test_endpoint_forecast_random_forest(app_state):
    req = ForecastRequest(
        station_id="VN_HN_01",
        pollutant="pm25",
        model_name="Random_Forest",
        horizon_hours=6
    )
    res = run_coro(air_quality.forecast_air_quality(req))
    assert res["station_id"] == "VN_HN_01"
    assert res["model_used"] == "Random_Forest"
    assert len(res["forecast_steps"]) == 6
    assert res["forecast_steps"][0].step_ahead == 1
    assert res["forecast_steps"][0].pm25_predicted > 0
    assert "Backend AI Engine" in res["disclaimer"]

def test_endpoint_forecast_neural_network(app_state):
    req = ForecastRequest(
        station_id="VN_HN_02",
        pollutant="pm25",
        model_name="Neural_Network",
        horizon_hours=12
    )
    res = run_coro(air_quality.forecast_air_quality(req))
    assert res["station_id"] == "VN_HN_02"
    assert res["model_used"] == "Neural_Network"
    assert len(res["forecast_steps"]) == 12

def test_endpoint_forecast_baseline(app_state):
    req = ForecastRequest(
        station_id="VN_HN_03",
        pollutant="pm25",
        model_name="Baseline_Persistence",
        horizon_hours=24
    )
    res = run_coro(air_quality.forecast_air_quality(req))
    assert res["station_id"] == "VN_HN_03"
    assert res["model_used"] == "Baseline_Persistence"
    assert len(res["forecast_steps"]) == 24

def test_endpoint_forecast_provinces_support(app_state):
    # Kiểm thử dự báo cho các tỉnh thành ngoài Hà Nội (TP.HCM, Tây Ninh, Đà Nẵng)
    test_provinces = ["VN_HCM", "VN_TN", "VN_DN"]
    for prov_id in test_provinces:
        req = ForecastRequest(
            station_id=prov_id,
            pollutant="pm25",
            model_name="Random_Forest",
            horizon_hours=6
        )
        res = run_coro(air_quality.forecast_air_quality(req))
        assert res["station_id"] == prov_id
        assert len(res["forecast_steps"]) == 6

def test_endpoint_optimization_experiment(app_state):
    opt = run_coro(air_quality.run_optimization_experiment())
    assert opt["status"] == "success"
    assert "Post-Training Quantization" in opt["experiment_name"]
    assert "models_comparison" in opt
    comp = opt["models_comparison"]
    assert "Random_Forest" in comp
    assert comp["Random_Forest"]["improvements"]["size_reduction_pct"] >= 60.0

def test_endpoint_concurrency_benchmark_12_ccu(app_state):
    bench = run_coro(air_quality.run_concurrency_load_test(concurrent_requests=12))
    assert bench["status"] == "success"
    assert bench["concurrency_level"] == 12
    assert bench["error_rate_pct"] == 0.0
    assert bench["response_time_ms"]["p95"] < 150.0

def test_endpoint_concurrency_benchmark_20_ccu(app_state):
    bench = run_coro(air_quality.run_concurrency_load_test(concurrent_requests=20))
    assert bench["status"] == "success"
    assert bench["concurrency_level"] == 20
    assert bench["error_rate_pct"] == 0.0

def test_endpoint_model_evaluation(app_state):
    metrics = run_coro(evaluation.get_model_evaluation())
    assert "Random_Forest" in metrics
    assert "Neural_Network" in metrics
    assert "Baseline_Persistence" in metrics
    rf_metrics = metrics["Random_Forest"]
    assert rf_metrics["r2"] > 0.5
    assert rf_metrics["mae"] < 10.0
    assert rf_metrics["rmse"] < 15.0

def test_endpoint_model_explainability(app_state):
    explain = run_coro(evaluation.get_model_explanation())
    assert "problem_definition" in explain
    assert "preprocessing_pipeline" in explain
    assert "models_comparison" in explain
    assert len(explain["preprocessing_pipeline"]) >= 5
