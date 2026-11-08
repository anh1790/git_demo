# -*- coding: utf-8 -*-
"""
AI Chatbot & Intelligent Meteorological Assistant Routes:
- POST /api/ai/chat: Điểm vào xử lý câu hỏi tự nhiên đa lượt, độc lập địa điểm,
  phân tích bão, thiên tai, chỉ số không khí AQI và dự báo thời tiết 48h/7d.
- GET /api/ai/typhoon/live: Dữ liệu theo dõi bão và xoáy thuận nhiệt đới NCHMF.
- GET /api/ai/disasters/live: Tổng hợp cảnh báo 8 loại hình thiên tai toàn quốc.
- GET /api/ai/provinces/all: Danh mục 63 tỉnh thành & tọa độ phục vụ đối soát địa lý.
"""

from fastapi import APIRouter, HTTPException
from backend.schemas import ChatRequest, ChatResponse
from backend.services.ai_engine import (
    ai_engine,
    VIETNAM_PROVINCES_CATALOG,
    INTERNATIONAL_CITIES
)

router = APIRouter(prefix="/api/ai", tags=["AI Chatbot & Assistant"])

@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(request: ChatRequest):
    """
    Xử lý câu hỏi người dùng với Trợ lý AI AirSense.
    Hỗ trợ nhận diện độc lập 63 tỉnh thành, hội thoại đa lượt và truy xuất dữ liệu quan trắc.
    """
    try:
        result = ai_engine.process_chat(
            message=request.message,
            session_id=request.session_id,
            selected_prov_id=request.province_id
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý câu hỏi AI: {str(e)}")

@router.get("/typhoon/live")
async def get_live_typhoon_status():
    """Lấy dữ liệu theo dõi bão, áp thấp và xoáy thuận nhiệt đới mới nhất."""
    res = ai_engine.generate_typhoon_report(
        province_data={"name": "Khu vực Biển Đông"},
        query_text="theo dõi bão mới nhất"
    )
    return {
        "status": "success",
        "data": res
    }

@router.get("/disasters/live")
async def get_live_disasters():
    """Tổng hợp bản tin cảnh báo thiên tai và rủi ro khí hậu các vùng trọng điểm."""
    res = ai_engine.generate_disaster_report(
        province_data={"name": "Toàn quốc", "temp": 28.0, "rain_prob": 65, "rain_mm": 15.0},
        query_text="cảnh báo thiên tai"
    )
    return {
        "status": "success",
        "data": res
    }

@router.get("/provinces/all")
async def list_all_provinces():
    """Trả về danh mục toàn bộ 63 tỉnh thành và các quần đảo của Việt Nam."""
    items = []
    for pid, data in VIETNAM_PROVINCES_CATALOG.items():
        items.append({
            "id": pid,
            "name": data["name"],
            "region": data["region"],
            "type": data["type"],
            "lat": data["lat"],
            "lon": data["lon"]
        })
    return {
        "total": len(items),
        "provinces": items
    }
