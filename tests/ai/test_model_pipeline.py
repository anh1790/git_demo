"""
AI & Machine Learning Pipeline Unit Tests.
Kiểm thử tính toàn vẹn tệp mô hình (SHA-256 Checksum), đối sánh lượng tử hóa Int8 vs FP32,
thuật toán hồi quy đa bước 48h không rò rỉ dữ liệu, và kiểm soát cận tin cậy.
"""

import hashlib
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def test_model_files_sha256_integrity(test_fixtures):
    # Kiểm tra tính toàn vẹn chống giả mạo của 6 tệp mô hình AI
    models_dir = BASE_DIR / "models"
    expected_models = test_fixtures["models"]

    for filename, info in expected_models.items():
        file_path = models_dir / filename
        assert file_path.exists(), f"Tệp mô hình {filename} không tồn tại!"
        actual_size = file_path.stat().st_size
        assert actual_size == info["size_bytes"], f"Kích thước tệp {filename} không khớp!"
        
        hasher = hashlib.sha256()
        hasher.update(file_path.read_bytes())
        actual_hash = hasher.hexdigest()
        assert actual_hash == info["sha256"], f"SHA-256 hash của {filename} không khớp!"

def test_quantization_parity_random_forest(app_state):
    # Đối sánh sai số giữa Random Forest gốc (FP32) và đã lượng tử hóa (Int8)
    engine = app_state.engine
    sample_data = app_state.history_df.tail(48).copy()

    pred_fp32 = engine.forecast_multistep(sample_data, model_name="Random_Forest", horizon_hours=24)
    pred_int8 = engine.forecast_multistep(sample_data, model_name="Random_Forest_Quantized", horizon_hours=24)

    vals_fp32 = np.array([p["pm25_predicted"] for p in pred_fp32])
    vals_int8 = np.array([p["pm25_predicted"] for p in pred_int8])

    mae_diff = np.mean(np.abs(vals_fp32 - vals_int8))
    # Sai số giữa FP32 và Int8 phải cực nhỏ (<= 0.1 ug/m3)
    assert mae_diff <= 0.1, f"Sai số lượng tử hóa quá lớn: MAE = {mae_diff}"

def test_quantization_parity_neural_network(app_state):
    # Đối sánh sai số giữa Neural Network (MLP) FP32 và Int8 trên bước suy luận trực tiếp
    engine = app_state.engine
    sample_data = app_state.history_df.tail(48).copy()

    pred_fp32 = engine.forecast_multistep(sample_data, model_name="Neural_Network", horizon_hours=1)
    pred_int8 = engine.forecast_multistep(sample_data, model_name="Neural_Network_Quantized", horizon_hours=1)

    diff_1step = abs(pred_fp32[0]["pm25_predicted"] - pred_int8[0]["pm25_predicted"])
    assert diff_1step <= 1.0, f"Sai số MLP lượng tử hóa bước 1 quá lớn: {diff_1step}"

    # Kiểm tra tương quan xu hướng 24 bước
    pred_fp32_24 = engine.forecast_multistep(sample_data, model_name="Neural_Network", horizon_hours=24)
    pred_int8_24 = engine.forecast_multistep(sample_data, model_name="Neural_Network_Quantized", horizon_hours=24)
    v1 = np.array([p["pm25_predicted"] for p in pred_fp32_24])
    v2 = np.array([p["pm25_predicted"] for p in pred_int8_24])
    corr = np.corrcoef(v1, v2)[0, 1]
    assert corr > 0.95, f"Tương quan xu hướng suy luận bị lệch sau lượng tử hóa: r = {corr}"

def test_autoregressive_multistep_horizon_48(app_state):
    # Kiểm thử dự báo đa bước tới 48 giờ liên tục
    engine = app_state.engine
    sample_data = app_state.history_df.tail(48).copy()

    steps = engine.forecast_multistep(sample_data, model_name="Random_Forest", horizon_hours=48)
    assert len(steps) == 48

    for i, s in enumerate(steps):
        assert s["step_ahead"] == i + 1
        assert not np.isnan(s["pm25_predicted"])
        assert s["pm25_predicted"] > 0
        assert s["lower_bound"] <= s["pm25_predicted"] <= s["upper_bound"]
        assert s["lower_bound"] >= 0.0, "Cận dưới vật lý của nồng độ bụi mịn phải >= 0"

def test_baseline_persistence_step(app_state):
    # Mô hình Baseline phải lấy đúng giá trị t-1 cho bước t
    engine = app_state.engine
    sample_data = app_state.history_df.tail(48).copy()
    last_val = float(sample_data.iloc[-1]["pm25"])

    steps = engine.forecast_multistep(sample_data, model_name="Baseline", horizon_hours=6)
    assert len(steps) == 6
    # Bước đầu tiên của Baseline phải xấp xỉ giá trị cuối cùng của lịch sử
    assert abs(steps[0]["pm25_predicted"] - last_val) < 1.0

def test_inference_latency_budget(app_state):
    # Độ trễ suy luận cho 48 bước thời gian phải < 5000ms trên CPU tiêu chuẩn
    import time
    engine = app_state.engine
    sample_data = app_state.history_df.tail(48).copy()

    t0 = time.perf_counter()
    steps = engine.forecast_multistep(sample_data, model_name="Random_Forest", horizon_hours=48)
    latency_ms = (time.perf_counter() - t0) * 1000

    assert len(steps) == 48
    assert latency_ms < 5000.0, f"Độ trễ suy luận quá cao: {latency_ms:.2f}ms"
