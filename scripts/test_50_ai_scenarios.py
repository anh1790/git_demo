# -*- coding: utf-8 -*-
"""
Bộ kiểm thử toàn diện 50 Kịch bản thực tế cho AI Chatbot - AIRSENSE AI
Tuân thủ đầy đủ 11 nhóm tiêu chí theo yêu cầu:
1. Địa điểm độc lập (không bị UI ghi đè)
2. Hội thoại đa lượt & nhớ ngữ cảnh liên tiếp
3. Tên viết tắt, không dấu, lỗi chính tả
4. Địa danh trùng / dễ nhầm
5. Thời tiết hiện tại, 24h, 48h, 7-10 ngày
6. Bão: vị trí tâm, cấp gió Beaufort, quỹ đạo 72h, kịch bản đổ bộ
7. Thiên tai: lũ quét, sạt lở, ngập úng, dông sét, nắng nóng (QĐ 18/2021/QĐ-TTg)
8. Chất lượng không khí: AQI, PM2.5, PM10, khí độc (QCVN 05:2023)
9. So sánh liên tỉnh (2-3 địa phương)
10. Tư vấn du lịch, dã ngoại, thể thao ngoài trời
11. Kiến thức khí quyển, nghịch nhiệt & câu hỏi ngoài lề
"""

import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.services.ai_engine import ai_engine, session_manager

SCENARIOS = [
    # --- NHÓM 1: ĐỊA ĐIỂM ĐỘC LẬP (UI dropdown là VN_HN nhưng hỏi nơi khác) ---
    {
        "id": "TC01", "group": "1. Độc lập địa điểm",
        "query": "Thời tiết ở Hải Phòng hôm nay thế nào?",
        "ui_prov": "VN_HN", "session": "sess_tc01",
        "expected_prov_id": "VN_HP", "expected_keywords": ["Hải Phòng"]
    },
    {
        "id": "TC02", "group": "1. Độc lập địa điểm",
        "query": "Nhiệt độ hiện tại tại Đà Nẵng là bao nhiêu độ?",
        "ui_prov": "VN_HN", "session": "sess_tc02",
        "expected_prov_id": "VN_DN", "expected_keywords": ["Đà Nẵng", "°C"]
    },
    {
        "id": "TC03", "group": "1. Độc lập địa điểm",
        "query": "Cần Thơ hôm nay trời có nắng không?",
        "ui_prov": "VN_HN", "session": "sess_tc03",
        "expected_prov_id": "VN_CT", "expected_keywords": ["Cần Thơ"]
    },
    {
        "id": "TC04", "group": "1. Độc lập địa điểm",
        "query": "Thời tiết tại Thừa Thiên Huế ra sao?",
        "ui_prov": "VN_HCM", "session": "sess_tc04",
        "expected_prov_id": "VN_HUE", "expected_keywords": ["Huế"]
    },
    {
        "id": "TC05", "group": "1. Độc lập địa điểm",
        "query": "Hôm nay trời có mưa không? (Không nêu tỉnh -> dùng mặc định)",
        "ui_prov": "VN_QN", "session": "sess_tc05",
        "expected_prov_id": "VN_QN", "expected_keywords": ["Quảng Ninh"]
    },

    # --- NHÓM 2: HỘI THOẠI ĐA LƯỢT & NHỚ NGỮ CẢNH LIÊN TIẾP ---
    {
        "id": "TC06", "group": "2. Đa lượt & Ngữ cảnh",
        "query": "Thời tiết ở Đà Lạt hôm nay thế nào?",
        "ui_prov": "VN_HN", "session": "sess_multiturn_1",
        "expected_prov_id": "VN_LD", "expected_keywords": ["Lâm Đồng", "Đà Lạt"]
    },
    {
        "id": "TC07", "group": "2. Đa lượt & Ngữ cảnh",
        "query": "Thế ngày mai có mưa không?",
        "ui_prov": "VN_HN", "session": "sess_multiturn_1",
        "expected_prov_id": "VN_LD", "expected_keywords": ["Lâm Đồng", "mưa"]
    },
    {
        "id": "TC08", "group": "2. Đa lượt & Ngữ cảnh",
        "query": "Chỉ số PM2.5 ở đó bao nhiêu?",
        "ui_prov": "VN_HN", "session": "sess_multiturn_1",
        "expected_prov_id": "VN_LD", "expected_keywords": ["PM2.5", "AQI"]
    },
    {
        "id": "TC09", "group": "2. Đa lượt & Ngữ cảnh",
        "query": "Thế còn Hải Phòng thì sao?",
        "ui_prov": "VN_HN", "session": "sess_multiturn_1",
        "expected_prov_id": "VN_HP", "expected_keywords": ["Hải Phòng"]
    },
    {
        "id": "TC10", "group": "2. Đa lượt & Ngữ cảnh",
        "query": "Bão có ảnh hưởng đến đây không?",
        "ui_prov": "VN_HN", "session": "sess_multiturn_1",
        "expected_prov_id": "VN_HP", "expected_keywords": ["Hải Phòng", "bão"]
    },

    # --- NHÓM 3: VIẾT TẮT, KHÔNG DẤU, LỖI CHÍNH TẢ ---
    {
        "id": "TC11", "group": "3. Tên viết tắt / Không dấu",
        "query": "tphcm nhiet do bao nhieu?",
        "ui_prov": "VN_HN", "session": "sess_tc11",
        "expected_prov_id": "VN_HCM", "expected_keywords": ["Hồ Chí Minh"]
    },
    {
        "id": "TC12", "group": "3. Tên viết tắt / Không dấu",
        "query": "thoi tiet sg hom nay co mua ko",
        "ui_prov": "VN_HN", "session": "sess_tc12",
        "expected_prov_id": "VN_HCM", "expected_keywords": ["Hồ Chí Minh"]
    },
    {
        "id": "TC13", "group": "3. Tên viết tắt / Không dấu",
        "query": "thoi tiet hn gio the nao",
        "ui_prov": "VN_HCM", "session": "sess_tc13",
        "expected_prov_id": "VN_HN", "expected_keywords": ["Hà Nội"]
    },
    {
        "id": "TC14", "group": "3. Tên viết tắt / Không dấu",
        "query": "da nag hom nay nang hay mua",
        "ui_prov": "VN_HN", "session": "sess_tc14",
        "expected_prov_id": "VN_DN", "expected_keywords": ["Đà Nẵng"]
    },
    {
        "id": "TC15", "group": "3. Tên viết tắt / Không dấu",
        "query": "o vung tau co gio lon khong",
        "ui_prov": "VN_HN", "session": "sess_tc15",
        "expected_prov_id": "VN_VT", "expected_keywords": ["Vũng Tàu"]
    },

    # --- NHÓM 4: ĐỊA DANH BIỂN ĐẢO & TRÙNG / DỄ NHẦM ---
    {
        "id": "TC16", "group": "4. Biển đảo & Phân biệt",
        "query": "Thời tiết và sóng gió tại Quần đảo Hoàng Sa hiện tại ra sao?",
        "ui_prov": "VN_HN", "session": "sess_tc16",
        "expected_prov_id": "VN_HS", "expected_keywords": ["Hoàng Sa", "sóng"]
    },
    {
        "id": "TC17", "group": "4. Biển đảo & Phân biệt",
        "query": "Tình hình biển tại Quần đảo Trường Sa thế nào?",
        "ui_prov": "VN_HN", "session": "sess_tc17",
        "expected_prov_id": "VN_TS", "expected_keywords": ["Trường Sa"]
    },
    {
        "id": "TC18", "group": "4. Biển đảo & Phân biệt",
        "query": "Thời tiết tại đảo Phú Quốc hôm nay?",
        "ui_prov": "VN_HN", "session": "sess_tc18",
        "expected_prov_id": "VN_KG", "expected_keywords": ["Kiên Giang"]
    },
    {
        "id": "TC19", "group": "4. Biển đảo & Phân biệt",
        "query": "Chất lượng không khí tại Côn Đảo ra sao?",
        "ui_prov": "VN_HN", "session": "sess_tc19",
        "expected_prov_id": "VN_VT", "expected_keywords": ["Vũng Tàu"]
    },
    {
        "id": "TC20", "group": "4. Biển đảo & Phân biệt",
        "query": "Thời tiết tại Bắc Giang hôm nay thế nào?",
        "ui_prov": "VN_HN", "session": "sess_tc20",
        "expected_prov_id": "VN_BG", "expected_keywords": ["Bắc Giang"]
    },
    {
        "id": "TC21", "group": "4. Biển đảo & Phân biệt",
        "query": "Thời tiết tại Bắc Ninh hôm nay có gì khác?",
        "ui_prov": "VN_HN", "session": "sess_tc21",
        "expected_prov_id": "VN_BN", "expected_keywords": ["Bắc Ninh"]
    },

    # --- NHÓM 5: THỜI TIẾT CHI TIẾT & CHỈ SỐ KHÍ TƯỢNG (HIỆN TẠI, 24H, 48H, 7-10 NGÀY) ---
    {
        "id": "TC22", "group": "5. Thời tiết chi tiết",
        "query": "Nhiệt độ, độ ẩm và tốc độ gió tại Hà Nội hiện tại là bao nhiêu?",
        "ui_prov": "VN_HN", "session": "sess_tc22",
        "expected_prov_id": "VN_HN", "expected_keywords": ["Hà Nội", "Nhiệt độ quan trắc", "Độ ẩm", "Gió"]
    },
    {
        "id": "TC23", "group": "5. Thời tiết chi tiết",
        "query": "Dự báo thời tiết 24 giờ tới tại TP. Hồ Chí Minh?",
        "ui_prov": "VN_HCM", "session": "sess_tc23",
        "expected_prov_id": "VN_HCM", "expected_keywords": ["Hồ Chí Minh", "24 GIỜ TỚI"]
    },
    {
        "id": "TC24", "group": "5. Thời tiết chi tiết",
        "query": "Dự báo thời tiết 48 giờ tới tại Đà Nẵng có mưa không?",
        "ui_prov": "VN_DN", "session": "sess_tc24",
        "expected_prov_id": "VN_DN", "expected_keywords": ["Đà Nẵng", "48 GIỜ TỚI", "mưa"]
    },
    {
        "id": "TC25", "group": "5. Thời tiết chi tiết",
        "query": "Xu hướng thời tiết 7–10 ngày tới tại Sa Pa Lào Cai?",
        "ui_prov": "VN_LC", "session": "sess_tc25",
        "expected_prov_id": "VN_LC", "expected_keywords": ["Lào Cai", "7–10 NGÀY"]
    },
    {
        "id": "TC26", "group": "5. Thời tiết chi tiết",
        "query": "Chỉ số bức xạ tia cực tím UV hôm nay tại Nha Trang Khánh Hòa?",
        "ui_prov": "VN_KH", "session": "sess_tc26",
        "expected_prov_id": "VN_KH", "expected_keywords": ["Khánh Hòa", "UV"]
    },

    # --- NHÓM 6: THEO DÕI VÀ DỰ BÁO BÃO CHUẨN NCHMF ---
    {
        "id": "TC27", "group": "6. Theo dõi bão NCHMF",
        "query": "Hiện tại trên Biển Đông có cơn bão nào đang hoạt động không?",
        "ui_prov": "VN_HN", "session": "sess_tc27",
        "expected_prov_id": "VN_HN", "expected_keywords": ["BẢN TIN THEO DÕI BÃO", "Biển Đông"]
    },
    {
        "id": "TC28", "group": "6. Theo dõi bão NCHMF",
        "query": "Vị trí tâm bão và hướng di chuyển hiện tại được dự báo ra sao?",
        "ui_prov": "VN_DN", "session": "sess_tc28",
        "expected_prov_id": "VN_DN", "expected_keywords": ["tâm theo dõi", "Tây Tây Bắc"]
    },
    {
        "id": "TC29", "group": "6. Theo dõi bão NCHMF",
        "query": "Sức gió của bão đạt cấp mấy theo thang Beaufort?",
        "ui_prov": "VN_HN", "session": "sess_tc29",
        "expected_prov_id": "VN_HN", "expected_keywords": ["Beaufort", "giật cấp"]
    },
    {
        "id": "TC30", "group": "6. Theo dõi bão NCHMF",
        "query": "Quỹ đạo dự báo bão trong 24h, 48h, 72h tới như thế nào?",
        "ui_prov": "VN_HP", "session": "sess_tc30",
        "expected_prov_id": "VN_HP", "expected_keywords": ["24 giờ tới", "48 giờ tới", "72 giờ tới"]
    },
    {
        "id": "TC31", "group": "6. Theo dõi bão NCHMF",
        "query": "Khả năng đổ bộ của bão vào đất liền các tỉnh ven biển ra sao?",
        "ui_prov": "VN_QN", "session": "sess_tc31",
        "expected_prov_id": "VN_QN", "expected_keywords": ["Quảng Ninh", "tàu thuyền"]
    },

    # --- NHÓM 7: CẢNH BÁO THIÊN TAI (8 NHÓM, CẤP ĐỘ RỦI RO QĐ 18/2021/QĐ-TTg) ---
    {
        "id": "TC32", "group": "7. Cảnh báo thiên tai",
        "query": "Có cảnh báo lũ quét hay sạt lở đất tại Lào Cai không?",
        "ui_prov": "VN_LC", "session": "sess_tc32",
        "expected_prov_id": "VN_LC", "expected_keywords": ["Lào Cai", "THIÊN TAI", "sạt lở"]
    },
    {
        "id": "TC33", "group": "7. Cảnh báo thiên tai",
        "query": "Tình hình cảnh báo ngập lụt đô thị tại Hà Nội ra sao?",
        "ui_prov": "VN_HN", "session": "sess_tc33",
        "expected_prov_id": "VN_HN", "expected_keywords": ["Hà Nội", "Ngập lụt", "Cấp 1"]
    },
    {
        "id": "TC34", "group": "7. Cảnh báo thiên tai",
        "query": "Khu vực miền núi phía Bắc có nguy cơ sương muối hay rét đậm không?",
        "ui_prov": "VN_LC", "session": "sess_tc34",
        "expected_prov_id": "VN_LC", "expected_keywords": ["Cảnh báo", "rét"]
    },
    {
        "id": "TC35", "group": "7. Cảnh báo thiên tai",
        "query": "Có cảnh báo dông sét, lốc xoáy nguy hiểm tại Quảng Ninh không?",
        "ui_prov": "VN_QN", "session": "sess_tc35",
        "expected_prov_id": "VN_QN", "expected_keywords": ["Quảng Ninh", "Cảnh báo"]
    },
    {
        "id": "TC36", "group": "7. Cảnh báo thiên tai",
        "query": "Cấp độ rủi ro thiên tai hiện nay được tính theo quyết định nào?",
        "ui_prov": "VN_HN", "session": "sess_tc36",
        "expected_prov_id": "VN_HN", "expected_keywords": ["18/2021/QĐ-TTg", "PCTT"]
    },

    # --- NHÓM 8: CHẤT LƯỢNG KHÔNG KHÍ & TIÊU CHUẨN QCVN 05:2023 ---
    {
        "id": "TC37", "group": "8. Chất lượng không khí",
        "query": "Chỉ số AQI và nồng độ bụi mịn PM2.5 tại Hà Nội hôm nay thế nào?",
        "ui_prov": "VN_HN", "session": "sess_tc37",
        "expected_prov_id": "VN_HN", "expected_keywords": ["Hà Nội", "AQI", "PM2.5", "QCVN 05:2023"]
    },
    {
        "id": "TC38", "group": "8. Chất lượng không khí",
        "query": "Nồng độ bụi PM10 tại TP. Hồ Chí Minh có đạt tiêu chuẩn không?",
        "ui_prov": "VN_HCM", "session": "sess_tc38",
        "expected_prov_id": "VN_HCM", "expected_keywords": ["Hồ Chí Minh", "PM10"]
    },
    {
        "id": "TC39", "group": "8. Chất lượng không khí",
        "query": "Các khí độc hại NO2, CO, SO2, O3 tại Đà Nẵng ở mức nào?",
        "ui_prov": "VN_DN", "session": "sess_tc39",
        "expected_prov_id": "VN_DN", "expected_keywords": ["Đà Nẵng", "NO₂", "CO", "O₃"]
    },
    {
        "id": "TC40", "group": "8. Chất lượng không khí",
        "query": "Quy chuẩn QCVN 05:2023 quy định giới hạn bụi PM2.5 là bao nhiêu?",
        "ui_prov": "VN_HN", "session": "sess_tc40",
        "expected_prov_id": "VN_HN", "expected_keywords": ["50 µg/m³", "QCVN 05:2023"]
    },

    # --- NHÓM 9: SO SÁNH THỜI TIẾT & AQI LIÊN TỈNH ---
    {
        "id": "TC41", "group": "9. So sánh liên tỉnh",
        "query": "So sánh thời tiết và chất lượng không khí giữa Hà Nội và TP. Hồ Chí Minh",
        "ui_prov": "VN_HN", "session": "sess_tc41",
        "expected_prov_id": "VN_HN", "expected_keywords": ["Hà Nội", "Hồ Chí Minh", "BẢNG SO SÁNH"]
    },
    {
        "id": "TC42", "group": "9. So sánh liên tỉnh",
        "query": "Thời tiết ở Đà Nẵng và Hải Phòng nơi nào mát hơn?",
        "ui_prov": "VN_HN", "session": "sess_tc42",
        "expected_prov_id": "VN_DN", "expected_keywords": ["Đà Nẵng", "Hải Phòng", "SO SÁNH"]
    },
    {
        "id": "TC43", "group": "9. So sánh liên tỉnh",
        "query": "So sánh AQI giữa Hà Nội, Cần Thơ và Đà Lạt",
        "ui_prov": "VN_HN", "session": "sess_tc43",
        "expected_prov_id": "VN_HN", "expected_keywords": ["Hà Nội", "Cần Thơ", "SO SÁNH"]
    },

    # --- NHÓM 10: TƯ VẤN DU LỊCH, DÃ NGOẠI & THỂ THAO NGOÀI TRỜI ---
    {
        "id": "TC44", "group": "10. Du lịch & Dã ngoại",
        "query": "Sáng nay ở Hà Nội có nên chạy bộ ngoài trời quanh Hồ Gươm không?",
        "ui_prov": "VN_HN", "session": "sess_tc44",
        "expected_prov_id": "VN_HN", "expected_keywords": ["Hà Nội", "Outdoor Score", "chạy bộ"]
    },
    {
        "id": "TC45", "group": "10. Du lịch & Dã ngoại",
        "query": "Khung giờ vàng nào thích hợp đi dạo ngắm cảnh ở Đà Lạt?",
        "ui_prov": "VN_LD", "session": "sess_tc45",
        "expected_prov_id": "VN_LD", "expected_keywords": ["Lâm Đồng", "Khung giờ vàng"]
    },
    {
        "id": "TC46", "group": "10. Du lịch & Dã ngoại",
        "query": "Đi du lịch Vũng Tàu hôm nay cần mang theo trang bị gì?",
        "ui_prov": "VN_VT", "session": "sess_tc46",
        "expected_prov_id": "VN_VT", "expected_keywords": ["Vũng Tàu", "Trang bị"]
    },

    # --- NHÓM 11: KIẾN THỨC KHÍ TƯỢNG, ĐỊA DANH QUỐC TẾ & CHÀO HỎI ---
    {
        "id": "TC47", "group": "11. Kiến thức & Quốc tế",
        "query": "Hiện tượng nghịch nhiệt khí quyển là gì và tại sao làm ô nhiễm tăng cao?",
        "ui_prov": "VN_HN", "session": "sess_tc47",
        "expected_prov_id": "VN_HN", "expected_keywords": ["NGHỊCH NHIỆT", "đối lưu", "nắp vung"]
    },
    {
        "id": "TC48", "group": "11. Kiến thức & Quốc tế",
        "query": "El Niño và La Niña tác động thế nào đến hạn hán và mưa bão ở Việt Nam?",
        "ui_prov": "VN_HN", "session": "sess_tc48",
        "expected_prov_id": "VN_HN", "expected_keywords": ["EL NIÑO", "LA NIÑA", "hạn hán"]
    },
    {
        "id": "TC49", "group": "11. Kiến thức & Quốc tế",
        "query": "Thời tiết ở Tokyo Nhật Bản hiện tại thế nào?",
        "ui_prov": "VN_HN", "session": "sess_tc49",
        "expected_prov_id": "INTL", "expected_keywords": ["Tokyo", "QUỐC TẾ"]
    },
    {
        "id": "TC50", "group": "11. Kiến thức & Quốc tế",
        "query": "Xin chào! Bạn là ai và AirSense AI có thể làm được những gì?",
        "ui_prov": "VN_HN", "session": "sess_tc50",
        "expected_prov_id": "VN_HN", "expected_keywords": ["Trợ lý AI AirSense", "Thời tiết thực tế", "QCVN 05:2023"]
    }
]

def run_50_test_suite():
    print("=" * 80)
    print("BẮT ĐẦU CHẠY BỘ KIỂM THỬ TOÀN DIỆN 50 KỊCH BẢN THỰC TẾ CHO TRỢ LÝ AI AIRSENSE")
    print(f"Thời gian bắt đầu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    passed_count = 0
    failed_count = 0
    results_summary = []

    for tc in SCENARIOS:
        tc_id = tc["id"]
        group = tc["group"]
        query = tc["query"]
        ui_prov = tc["ui_prov"]
        sess_id = tc["session"]
        exp_pid = tc["expected_prov_id"]
        exp_kw = tc["expected_keywords"]

        # Gọi engine xử lý
        res = ai_engine.process_chat(
            message=query,
            session_id=sess_id,
            selected_prov_id=ui_prov
        )

        reply = res.get("reply", "")
        ret_pid = res.get("province_id", "")
        ret_name = res.get("province_name", "")

        # Kiểm tra điều kiện:
        # 1. Độc lập địa điểm (nếu câu hỏi có địa điểm, không bị ui_prov ghi đè)
        loc_ok = (ret_pid == exp_pid) or (exp_pid == "INTL" and ret_pid == "INTL")
        
        # 2. Chứa các từ khóa cốt lõi
        kw_missing = [kw for kw in exp_kw if kw.lower() not in reply.lower()]
        kw_ok = len(kw_missing) == 0

        is_passed = loc_ok and kw_ok

        if is_passed:
            passed_count += 1
            status_str = "PASS [✓]"
        else:
            failed_count += 1
            status_str = f"FAIL [✗] (loc_ok={loc_ok}, missing_kw={kw_missing})"

        print(f"[{tc_id}] {group:26} | Câu hỏi: {query[:38]:38} | {status_str}")
        results_summary.append({
            "id": tc_id,
            "group": group,
            "query": query,
            "passed": is_passed,
            "expected_pid": exp_pid,
            "actual_pid": ret_pid,
            "missing_keywords": kw_missing
        })

    print("=" * 80)
    print(f"KẾT QUẢ TỔNG HỢP: {passed_count}/{len(SCENARIOS)} KỊCH BẢN ĐẠT ({passed_count/len(SCENARIOS)*100:.1f}%)")
    if failed_count > 0:
        print(f"Số kịch bản chưa đạt: {failed_count}")
    else:
        print("TẤT CẢ 50 KỊCH BẢN ĐỀU VƯỢT QUA XUẤT SẮC!")
    print("=" * 80)

    return passed_count, failed_count, results_summary

if __name__ == "__main__":
    p, f, _ = run_50_test_suite()
    if f > 0:
        sys.exit(1)
