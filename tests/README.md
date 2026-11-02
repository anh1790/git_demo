# AirSense AI - Software Test Suite

Hệ thống kiểm thử tự động toàn diện dành cho nền tảng **AirSense AI - Smart Weather & Air Quality Experience**.

## 1. Cấu Trúc Bộ Kiểm Thử
```text
tests/
├── frontend/
│   ├── test_ui_dom.py               # Kiểm thử cấu trúc DOM, 7 tab, responsive, sovereignty
│   └── test_client_data_and_logic.py # Kiểm thử 34 tỉnh / 101 trạm, ngày/đêm, phân cấp AQI
├── backend/
│   ├── test_api_endpoints.py        # Kiểm thử 11 endpoint FastAPI (Health, Spatial, Forecast, Benchmark)
│   └── test_api_validation.py       # Kiểm thử biên (boundary), ngoại lệ (negative tests), Pydantic validation
├── integration/
│   └── test_fe_be_integration.py    # Kiểm thử tích hợp E2E dữ liệu FE <-> BE, offline fallback, tải 12 CCU
├── ai/
│   ├── test_model_pipeline.py       # Kiểm thử SHA-256 mô hình, Int8 vs FP32 parity, 48h autoregressive
│   ├── test_preprocessing.py        # Kiểm thử làm sạch dữ liệu, xử lý ngoại lai, trễ thời gian
│   └── test_geospatial.py           # Kiểm thử tính khoảng cách Haversine và nội suy không gian
├── fixtures/
│   └── test_payloads.json           # SHA-256 hash của 6 model và payloads mẫu
├── conftest.py                      # Cấu hình session-level fixtures, model warming, coroutine runner
└── README.md
```

## 2. Hướng Dẫn Thực Thi
Chạy toàn bộ bộ test với `pytest`:
```bash
pytest tests/ -v -p no:anyio
```

Chạy từng module riêng biệt:
```bash
# Frontend tests:
pytest tests/frontend/ -v -p no:anyio

# Backend tests:
pytest tests/backend/ -v -p no:anyio

# Integration tests:
pytest tests/integration/ -v -p no:anyio

# AI / ML tests:
pytest tests/ai/ -v -p no:anyio
```
