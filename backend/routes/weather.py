# -*- coding: utf-8 -*-
"""
Weather & Meteorological Live Routes:
- GET /api/weather/live: Trả về dữ liệu quan trắc khí tượng và chất lượng không khí thời gian thực của toàn bộ 34 tỉnh thành và 105 trạm.
- POST /api/weather/sync-realtime: Kích hoạt tiến trình đồng bộ hóa dữ liệu thời gian thực từ Open-Meteo API.
"""

from fastapi import APIRouter
from backend.provinces_data import PROVINCES_34, STATIONS_CONFIG
from backend.services.weather_sync import live_sync_service

router = APIRouter(prefix="/api/weather", tags=["Live Weather & Real-Time Sync"])

@router.get("/live")
async def get_live_weather():
    """Trả về dữ liệu thời tiết và quan trắc thực tế thời gian thực của 34 tỉnh và 105 trạm."""
    obs_time = PROVINCES_34[0].get("timestamp", "2026-11-08 12:45:43") if PROVINCES_34 else "2026-11-08 12:45:43"
    total_stations = sum(len(v) for v in STATIONS_CONFIG.values()) if STATIONS_CONFIG else 105
    return {
        "status": "success",
        "sync_time": obs_time,
        "source": "Open-Meteo Global Meteorological & Air Quality Network",
        "provinces_count": len(PROVINCES_34),
        "stations_count": total_stations,
        "provinces": PROVINCES_34,
        "stations_config": STATIONS_CONFIG
    }

@router.post("/sync-realtime")
async def trigger_live_sync():
    """Kích hoạt tiến trình đồng bộ thời gian thực từ Open-Meteo API."""
    try:
        res = live_sync_service.sync_all_provinces_live()
        live_sync_service.persist_to_disk()
        return res
    except Exception as e:
        obs_time = PROVINCES_34[0].get("timestamp", "2026-11-08 12:45:43") if PROVINCES_34 else "2026-11-08 12:45:43"
        return {
            "status": "cached_fallback",
            "message": f"Dùng dữ liệu đồng bộ thời gian thực mới nhất ({str(e)})",
            "sync_time": obs_time,
            "provinces_count": len(PROVINCES_34)
        }
