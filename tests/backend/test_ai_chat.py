# -*- coding: utf-8 -*-
"""
AirSense AI Chatbot Backend Unit Tests.
Kiểm thử các chức năng cốt lõi:
- Độc lập địa danh (không phụ thuộc tỉnh mặc định trên giao diện)
- Hội thoại đa lượt (multi-turn context memory)
- Theo dõi bão theo chuẩn NCHMF (tọa độ, cấp gió Beaufort, quỹ đạo)
- Cảnh báo thiên tai (8 nhóm, cấp độ rủi ro QĐ 18/2021/QĐ-TTg)
- Đánh giá chất lượng không khí & chuẩn QCVN 05:2023
- So sánh thời tiết liên tỉnh
- Nhận diện không dấu, viết tắt, địa danh quốc tế
"""

import pytest
from backend.routes import ai_chat
from backend.schemas import ChatRequest

def run_coro(coro):
    try:
        coro.send(None)
    except StopIteration as e:
        return e.value

def test_ai_chat_location_independence():
    """Kiểm tra: Nếu câu hỏi hỏi về Hải Phòng nhưng selected_province_id là VN_HN (Hà Nội),
    AI bắt buộc phải trả lời về Hải Phòng, không bị Hà Nội đè."""
    req = ChatRequest(
        message="Thời tiết ở Hải Phòng hôm nay thế nào?",
        session_id="test_sess_01",
        province_id="VN_HN"
    )
    res = run_coro(ai_chat.chat_with_assistant(req))
    assert res.province_id == "VN_HP"
    assert "Hải Phòng" in res.province_name
    assert "Hải Phòng" in res.reply

def test_ai_chat_multi_turn_context_memory():
    """Kiểm tra hội thoại đa lượt: câu đầu hỏi về Đà Nẵng, câu sau hỏi tiếp 'Thế ngày mai có mưa không?'
    AI phải ghi nhớ đang trao đổi về Đà Nẵng."""
    req1 = ChatRequest(
        message="Thời tiết ở Đà Nẵng hiện tại ra sao?",
        session_id="test_sess_multiturn",
        province_id="VN_HN"
    )
    res1 = run_coro(ai_chat.chat_with_assistant(req1))
    assert res1.province_id == "VN_DN"

    req2 = ChatRequest(
        message="Thế ngày mai có mưa không?",
        session_id="test_sess_multiturn",
        province_id="VN_HN"
    )
    res2 = run_coro(ai_chat.chat_with_assistant(req2))
    assert res2.province_id == "VN_DN"
    assert "Đà Nẵng" in res2.reply
    assert "ngày mai" in res2.reply.lower() or "24 giờ" in res2.reply.lower()

def test_ai_chat_typhoon_tracking():
    """Kiểm tra bản tin theo dõi bão chuẩn NCHMF: tâm bão, cấp gió Beaufort, hướng di chuyển."""
    req = ChatRequest(
        message="Hiện tại bão số mấy đang hoạt động trên Biển Đông, tâm bão ở đâu và sức gió cấp bao nhiêu?",
        session_id="test_sess_typhoon",
        province_id="VN_HN"
    )
    res = run_coro(ai_chat.chat_with_assistant(req))
    assert "BẢN TIN THEO DÕI BÃO" in res.reply or "bão" in res.reply.lower()
    assert "Beaufort" in res.reply or "cấp" in res.reply.lower()
    assert "NCHMF" in res.reply or "Khí tượng Thủy văn Quốc gia" in res.reply

def test_ai_chat_disaster_alert():
    """Kiểm tra cảnh báo thiên tai và cấp độ rủi ro theo QĐ 18/2021/QĐ-TTg."""
    req = ChatRequest(
        message="Có cảnh báo lũ quét hay ngập úng nguy hiểm nào tại Lào Cai không?",
        session_id="test_sess_disaster",
        province_id="VN_HN"
    )
    res = run_coro(ai_chat.chat_with_assistant(req))
    assert res.province_id == "VN_LC"
    assert "THIÊN TAI" in res.reply or "Cảnh báo" in res.reply
    assert "18/2021" in res.reply or "Khuyến cáo" in res.reply

def test_ai_chat_air_quality_qcvn():
    """Kiểm tra thông số chất lượng không khí và chuẩn QCVN 05:2023."""
    req = ChatRequest(
        message="Chỉ số bụi mịn PM2.5 và AQI tại Hà Nội có vượt quy chuẩn không?",
        session_id="test_sess_aqi",
        province_id="VN_HN"
    )
    res = run_coro(ai_chat.chat_with_assistant(req))
    assert "PM2.5" in res.reply
    assert "QCVN 05:2023" in res.reply
    assert "AQI" in res.reply

def test_ai_chat_multi_province_comparison():
    """Kiểm tra so sánh thời tiết giữa 2 địa phương."""
    req = ChatRequest(
        message="So sánh thời tiết và chất lượng không khí giữa Hà Nội và Sài Gòn",
        session_id="test_sess_compare",
        province_id="VN_HN"
    )
    res = run_coro(ai_chat.chat_with_assistant(req))
    assert "SO SÁNH" in res.reply
    assert "Hà Nội" in res.reply
    assert "TP. Hồ Chí Minh" in res.reply or "Sài Gòn" in res.reply

def test_ai_chat_aliases_and_unaccented():
    """Kiểm tra nhận diện địa danh viết tắt hoặc không dấu (tphcm, da lat, hoang sa, truong sa)."""
    # 1. tphcm
    req1 = ChatRequest(message="tphcm nhiet do bao nhieu?", session_id="test_alias_1")
    res1 = run_coro(ai_chat.chat_with_assistant(req1))
    assert res1.province_id == "VN_HCM"

    # 2. da lat
    req2 = ChatRequest(message="thoi tiet da lat the nao?", session_id="test_alias_2")
    res2 = run_coro(ai_chat.chat_with_assistant(req2))
    assert res2.province_id == "VN_LD"

    # 3. hoang sa
    req3 = ChatRequest(message="tinh hinh song gio o hoang sa ra sao?", session_id="test_alias_3")
    res3 = run_coro(ai_chat.chat_with_assistant(req3))
    assert res3.province_id == "VN_HS"
    assert "Hoàng Sa" in res3.province_name

def test_ai_chat_international_city():
    """Kiểm tra nhận diện thành phố quốc tế."""
    req = ChatRequest(message="Thời tiết ở Tokyo hiện tại thế nào?", session_id="test_intl")
    res = run_coro(ai_chat.chat_with_assistant(req))
    assert "Tokyo" in res.reply

def test_ai_chat_endpoints_routes():
    """Kiểm tra các endpoint bổ trợ: /typhoon/live, /disasters/live, /provinces/all."""
    typhoon_res = run_coro(ai_chat.get_live_typhoon_status())
    assert typhoon_res["status"] == "success"
    assert "data" in typhoon_res

    disaster_res = run_coro(ai_chat.get_live_disasters())
    assert disaster_res["status"] == "success"

    provs_res = run_coro(ai_chat.list_all_provinces())
    assert provs_res["total"] >= 63
