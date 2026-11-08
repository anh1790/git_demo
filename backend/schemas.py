"""
Pydantic Schemas xác thực đầu vào và định nghĩa cấu trúc phản hồi API.
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str = Field(..., json_schema_extra={"example": "healthy"})
    uptime_seconds: float
    cpu_percent: float
    memory_mb: float
    models_loaded: list[str]
    stations_count: int
    districts_count: int

class StationInfo(BaseModel):
    station_id: str
    station_name: str
    district: str
    latitude: float
    longitude: float
    station_type: str
    elevation_m: float
    dist_center_km: float

class LatestObservation(BaseModel):
    station_id: str
    station_name: str
    district: str
    latitude: float
    longitude: float
    timestamp: str
    pm25: float
    pm10: float
    no2: float
    co: float
    o3: float
    so2: float
    temperature: float
    humidity: float
    wind_speed: float
    aqi_level: str
    aqi_code: str
    color: str

class ForecastRequest(BaseModel):
    station_id: str = Field("VN_HN", description="Mã trạm quan trắc (ví dụ: VN_HN, VN_DN, VN_HCM)")
    pollutant: str = Field("pm25", description="Chỉ số dự báo (mặc định: pm25)")
    model_name: str = Field("Random_Forest", description="Mô hình AI sử dụng (Baseline, Random_Forest, Neural_Network, Random_Forest_Quantized, Neural_Network_Quantized)")
    horizon_hours: int = Field(48, ge=1, le=48, description="Số giờ cần dự báo (1 đến 48 giờ)")

class ForecastStepResult(BaseModel):
    step_ahead: int
    forecast_time: str
    pm25_predicted: float
    lower_bound: float
    upper_bound: float
    unit: str
    aqi_level: str
    aqi_code: str
    color: str
    health_advice: str

class ForecastResponse(BaseModel):
    station_id: str
    station_name: str
    district: str
    model_used: str
    horizon_hours: int
    current_timestamp: str
    current_pm25: float
    forecast_steps: list[ForecastStepResult]
    disclaimer: str = "Kết quả dự báo từ mô hình AI phục vụ học tập và nghiên cứu, không thay thế trạm đo quốc gia."

class ModelEvaluationItem(BaseModel):
    model_name: str
    model_type: str
    description: str
    mae: float
    rmse: float
    r2: float
    train_time_sec: float
    inference_latency_ms: float
    test_samples: int
    epochs_trained: Optional[int] = None
    top_features: Optional[list[dict]] = None


class ChatMessage(BaseModel):
    role: str = Field(..., description="Vai trò: user, assistant, system")
    content: str = Field(..., description="Nội dung tin nhắn")

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Câu hỏi của người dùng")
    session_id: Optional[str] = Field(None, description="Mã phiên trò chuyện đa lượt")
    province_id: Optional[str] = Field(None, description="Mã tỉnh đang chọn trên giao diện (nếu có)")
    history: Optional[list[ChatMessage]] = Field(default_factory=list, description="Lịch sử hội thoại trước đó")

class ChatResponse(BaseModel):
    reply: str = Field(..., description="Nội dung trả lời từ Trợ lý AI AirSense")
    session_id: str = Field(..., description="Mã phiên trò chuyện ghi nhớ ngữ cảnh")
    province_id: Optional[str] = Field(None, description="Mã định danh tỉnh thành đang trao đổi")
    province_name: Optional[str] = Field(None, description="Tên tỉnh thành đang trao đổi")
    grounded: Optional[dict] = Field(None, description="Dữ liệu quan trắc thực tế trích xuất")
    suggested_followups: list[str] = Field(default_factory=list, description="Các câu hỏi gợi ý tiếp nối")
    model_used: str = Field(..., description="Bộ máy AI đã phân tích câu trả lời")
    timestamp: str = Field(..., description="Thời điểm tạo phản hồi")
