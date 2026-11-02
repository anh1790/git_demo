# -*- coding: utf-8 -*-
"""
Script to generate rich detailed stations for all 34 provinces of Vietnam
and embed them into embedded_data.js, stations_data.js, and backend/provinces_data.py
"""
import json
import os

STATIONS_CONFIG = {
    # Miền Bắc (15)
    "VN_HN": [
        {"id": "VN_HN_01", "name": "Trạm Ba Đình - Trung tâm Hành chính", "type": "Đô thị / Hành chính", "address": "Số 1 Hoàng Hoa Thám, P. Ba Đình", "lat": 21.0342, "lon": 105.8360, "pm25": 38.5, "pm10": 58.2, "aqi": 69, "temp": 22.4, "humidity": 72, "wind": 3.2},
        {"id": "VN_HN_02", "name": "Trạm Hoàn Kiếm - Phố Cổ", "type": "Dân cư / Thương mại", "address": "Số 2 Hàng Trống, P. Hàng Trống", "lat": 21.0289, "lon": 105.8524, "pm25": 42.1, "pm10": 63.5, "aqi": 74, "temp": 22.8, "humidity": 71, "wind": 2.8},
        {"id": "VN_HN_03", "name": "Trạm Cầu Giấy - Giao thông", "type": "Giao thông huyết mạch", "address": "Đường Cầu Giấy, P. Dịch Vọng", "lat": 21.0365, "lon": 105.7952, "pm25": 48.0, "pm10": 72.8, "aqi": 82, "temp": 23.1, "humidity": 69, "wind": 3.5},
        {"id": "VN_HN_04", "name": "Trạm Sóc Sơn - Nền Sinh thái Ngoại ô", "type": "Trạm nền sinh thái", "address": "Xã Nam Sơn, H. Sóc Sơn", "lat": 21.3120, "lon": 105.8450, "pm25": 22.0, "pm10": 34.0, "aqi": 45, "temp": 21.5, "humidity": 75, "wind": 3.0}
    ],
    "VN_HP": [
        {"id": "VN_HP_01", "name": "Trạm Tam Bạc - Q. Hồng Bàng", "type": "Đô thị / Trung tâm", "address": "Đường Tam Bạc, P. Phan Bội Châu", "lat": 20.8601, "lon": 106.6782, "pm25": 32.0, "pm10": 51.5, "aqi": 65, "temp": 23.0, "humidity": 78, "wind": 4.5},
        {"id": "VN_HP_02", "name": "Trạm KCN Đình Vũ - Cảng biển", "type": "Công nghiệp / Cảng", "address": "Bán đảo Đình Vũ, Q. Hải An", "lat": 20.8415, "lon": 106.7582, "pm25": 41.5, "pm10": 64.2, "aqi": 76, "temp": 23.5, "humidity": 76, "wind": 4.8},
        {"id": "VN_HP_03", "name": "Trạm Đồ Sơn - Sinh thái Ven biển", "type": "Sinh thái biển", "address": "Khu 2 Đồ Sơn, Q. Đồ Sơn", "lat": 20.7125, "lon": 106.7891, "pm25": 16.2, "pm10": 26.5, "aqi": 40, "temp": 22.8, "humidity": 80, "wind": 5.2}
    ],
    "VN_CB": [
        {"id": "VN_CB_01", "name": "Trạm Trung tâm TP Cao Bằng", "type": "Đô thị", "address": "Đường Kim Đồng, P. Hợp Giang", "lat": 22.6680, "lon": 106.2550, "pm25": 15.0, "pm10": 24.5, "aqi": 38, "temp": 17.5, "humidity": 84, "wind": 2.0},
        {"id": "VN_CB_02", "name": "Trạm Thác Bản Giốc - Trùng Khánh", "type": "Sinh thái du lịch", "address": "Xã Đàm Thủy, H. Trùng Khánh", "lat": 22.8540, "lon": 106.7230, "pm25": 9.5, "pm10": 15.2, "aqi": 26, "temp": 16.0, "humidity": 88, "wind": 1.8}
    ],
    "VN_TQ": [
        {"id": "VN_TQ_01", "name": "Trạm Trung tâm TP Tuyên Quang", "type": "Đô thị", "address": "Đường Tân Trào, P. Phan Thiết", "lat": 21.8240, "lon": 105.2170, "pm25": 22.1, "pm10": 35.4, "aqi": 52, "temp": 21.0, "humidity": 76, "wind": 2.2},
        {"id": "VN_TQ_02", "name": "Trạm Hồ Sinh thái Na Hang", "type": "Trạm nền sinh thái", "address": "Thị trấn Na Hang, H. Na Hang", "lat": 22.3480, "lon": 105.3850, "pm25": 12.0, "pm10": 19.5, "aqi": 32, "temp": 19.5, "humidity": 82, "wind": 2.0}
    ],
    "VN_DB": [
        {"id": "VN_DB_01", "name": "Trạm Di tích TP Điện Biên Phủ", "type": "Đô thị / Văn hóa", "address": "Đường Võ Nguyên Giáp, P. Mường Thanh", "lat": 21.3880, "lon": 103.0210, "pm25": 18.4, "pm10": 29.8, "aqi": 46, "temp": 20.5, "humidity": 68, "wind": 2.5},
        {"id": "VN_DB_02", "name": "Trạm Cửa khẩu Tây Trang", "type": "Giao thông biên giới", "address": "Xã Na Ư, H. Điện Biên", "lat": 21.2150, "lon": 102.9150, "pm25": 11.5, "pm10": 18.5, "aqi": 30, "temp": 19.8, "humidity": 72, "wind": 2.2}
    ],
    "VN_LC": [
        {"id": "VN_LC_01", "name": "Trạm Quảng trường TP Lai Châu", "type": "Đô thị", "address": "Đường Trần Phú, P. Tân Phong", "lat": 22.3980, "lon": 103.4610, "pm25": 12.0, "pm10": 19.5, "aqi": 32, "temp": 16.2, "humidity": 86, "wind": 2.1},
        {"id": "VN_LC_02", "name": "Trạm Đèo Ô Quy Hồ", "type": "Trạm nền núi cao", "address": "Đèo Ô Quy Hồ, H. Tam Đường", "lat": 22.3550, "lon": 103.7780, "pm25": 7.8, "pm10": 12.6, "aqi": 22, "temp": 12.5, "humidity": 92, "wind": 3.8}
    ],
    "VN_SL": [
        {"id": "VN_SL_01", "name": "Trạm Trung tâm TP Sơn La", "type": "Đô thị", "address": "Đường Tô Hiệu, P. Chiềng Lề", "lat": 21.3300, "lon": 103.9180, "pm25": 14.5, "pm10": 23.2, "aqi": 37, "temp": 18.5, "humidity": 70, "wind": 2.6},
        {"id": "VN_SL_02", "name": "Trạm Cao nguyên Mộc Châu", "type": "Sinh thái nông nghiệp", "address": "Thị trấn Nông trường Mộc Châu", "lat": 20.8420, "lon": 104.6540, "pm25": 9.2, "pm10": 14.8, "aqi": 25, "temp": 16.8, "humidity": 76, "wind": 2.8}
    ],
    "VN_LCAI": [
        {"id": "VN_LCAI_01", "name": "Trạm TP Lào Cai - Cửa khẩu", "type": "Đô thị biên giới", "address": "Đường Hoàng Liên, P. Cốc Lếu", "lat": 22.4890, "lon": 103.9680, "pm25": 16.5, "pm10": 26.2, "aqi": 42, "temp": 17.2, "humidity": 82, "wind": 2.5},
        {"id": "VN_LCAI_02", "name": "Trạm Sa Pa - Đỉnh Fansipan", "type": "Sinh thái núi cao", "address": "Thị xã Sa Pa", "lat": 22.3360, "lon": 103.8440, "pm25": 8.2, "pm10": 13.5, "aqi": 24, "temp": 12.0, "humidity": 90, "wind": 3.2}
    ],
    "VN_TN": [
        {"id": "VN_TN_01", "name": "Trạm Trung tâm TP Thái Nguyên", "type": "Đô thị", "address": "Đường Lương Ngọc Quyến, P. Quang Trung", "lat": 21.5960, "lon": 105.8450, "pm25": 36.8, "pm10": 58.4, "aqi": 68, "temp": 22.0, "humidity": 75, "wind": 2.8},
        {"id": "VN_TN_02", "name": "Trạm KCN Yên Bình (Samsung)", "type": "Công nghiệp", "address": "Phường Đồng Tiến, TX. Phổ Yên", "lat": 21.4320, "lon": 105.8850, "pm25": 44.5, "pm10": 68.5, "aqi": 78, "temp": 22.8, "humidity": 73, "wind": 3.0},
        {"id": "VN_TN_03", "name": "Trạm Sinh thái Hồ Núi Cốc", "type": "Trạm nền sinh thái", "address": "Xã Tân Thái, H. Đại Từ", "lat": 21.6020, "lon": 105.7150, "pm25": 18.0, "pm10": 28.5, "aqi": 44, "temp": 21.2, "humidity": 78, "wind": 2.5}
    ],
    "VN_LS": [
        {"id": "VN_LS_01", "name": "Trạm TP Lạng Sơn - Tam Thanh", "type": "Đô thị", "address": "Đường Lê Lợi, P. Vĩnh Trại", "lat": 21.8550, "lon": 106.7600, "pm25": 20.5, "pm10": 33.2, "aqi": 49, "temp": 18.0, "humidity": 78, "wind": 3.4},
        {"id": "VN_LS_02", "name": "Trạm Cửa khẩu Quốc tế Hữu Nghị", "type": "Giao thông biên giới", "address": "Thị trấn Đồng Đăng, H. Cao Lộc", "lat": 21.9850, "lon": 106.7120, "pm25": 28.5, "pm10": 44.5, "aqi": 58, "temp": 17.5, "humidity": 80, "wind": 3.6},
        {"id": "VN_LS_03", "name": "Trạm Khí tượng Đỉnh Mẫu Sơn", "type": "Trạm nền núi cao", "address": "Khu du lịch Mẫu Sơn, H. Lộc Bình", "lat": 21.8480, "lon": 106.9150, "pm25": 9.8, "pm10": 15.8, "aqi": 26, "temp": 13.5, "humidity": 88, "wind": 4.2}
    ],
    "VN_QN": [
        {"id": "VN_QN_01", "name": "Trạm Bãi Cháy - Hạ Long", "type": "Đô thị du lịch ven biển", "address": "Đường Hạ Long, P. Bãi Cháy", "lat": 20.9580, "lon": 107.0350, "pm25": 23.0, "pm10": 38.0, "aqi": 54, "temp": 24.5, "humidity": 74, "wind": 4.6},
        {"id": "VN_QN_02", "name": "Trạm Cẩm Phả - Vùng khai thác", "type": "Công nghiệp khai khoáng", "address": "Đường Trần Phú, P. Cẩm Thành", "lat": 21.0180, "lon": 107.2880, "pm25": 38.0, "pm10": 62.5, "aqi": 72, "temp": 24.0, "humidity": 76, "wind": 4.2},
        {"id": "VN_QN_03", "name": "Trạm Vân Đồn - Sân bay & Đảo", "type": "Sinh thái biển đảo", "address": "Huyện Vân Đồn", "lat": 21.1250, "lon": 107.4120, "pm25": 14.5, "pm10": 23.5, "aqi": 36, "temp": 23.8, "humidity": 78, "wind": 5.0}
    ],
    "VN_BN": [
        {"id": "VN_BN_01", "name": "Trạm TP Bắc Ninh - Đền Đô", "type": "Đô thị văn hóa", "address": "Đường Ngô Gia Tự, P. Tiền An", "lat": 21.1890, "lon": 106.0720, "pm25": 41.2, "pm10": 65.2, "aqi": 73, "temp": 22.0, "humidity": 76, "wind": 2.8},
        {"id": "VN_BN_02", "name": "Trạm KCN Quế Võ", "type": "Công nghiệp", "address": "KCN Quế Võ, TX. Quế Võ", "lat": 21.1620, "lon": 106.1450, "pm25": 49.5, "pm10": 76.5, "aqi": 84, "temp": 22.6, "humidity": 74, "wind": 3.0},
        {"id": "VN_BN_03", "name": "Trạm KCN Yên Phong", "type": "Công nghiệp công nghệ cao", "address": "KCN Yên Phong, H. Yên Phong", "lat": 21.2250, "lon": 105.9850, "pm25": 45.0, "pm10": 70.0, "aqi": 79, "temp": 22.4, "humidity": 75, "wind": 2.9}
    ],
    "VN_PT": [
        {"id": "VN_PT_01", "name": "Trạm TP Việt Trì - Trung tâm", "type": "Đô thị", "address": "Đường Hùng Vương, P. Gia Cẩm", "lat": 21.3180, "lon": 105.4120, "pm25": 25.4, "pm10": 40.8, "aqi": 56, "temp": 22.5, "humidity": 73, "wind": 2.6},
        {"id": "VN_PT_02", "name": "Trạm Khu Di tích Đền Hùng", "type": "Trạm nền văn hóa lịch sử", "address": "Khu di tích lịch sử Đền Hùng", "lat": 21.3780, "lon": 105.3350, "pm25": 16.5, "pm10": 26.5, "aqi": 41, "temp": 22.0, "humidity": 76, "wind": 2.5},
        {"id": "VN_PT_03", "name": "Trạm KCN Thụy Vân", "type": "Công nghiệp", "address": "KCN Thụy Vân, TP. Việt Trì", "lat": 21.3450, "lon": 105.3780, "pm25": 36.8, "pm10": 58.0, "aqi": 67, "temp": 23.0, "humidity": 72, "wind": 2.8}
    ],
    "VN_HY": [
        {"id": "VN_HY_01", "name": "Trạm TP Hưng Yên - Phố Hiến", "type": "Đô thị cổ", "address": "Đường Bãi Sậy, P. Quang Trung", "lat": 20.6480, "lon": 106.0530, "pm25": 34.0, "pm10": 53.6, "aqi": 64, "temp": 23.0, "humidity": 76, "wind": 3.1},
        {"id": "VN_HY_02", "name": "Trạm KCN Phố Nối A", "type": "Công nghiệp", "address": "Huyện Văn Lâm & Mỹ Hào", "lat": 20.9350, "lon": 106.0350, "pm25": 44.2, "pm10": 69.5, "aqi": 77, "temp": 23.5, "humidity": 74, "wind": 3.2},
        {"id": "VN_HY_03", "name": "Trạm Sinh thái Ecopark", "type": "Đô thị sinh thái", "address": "Khu đô thị Ecopark, Văn Giang", "lat": 20.9650, "lon": 105.9320, "pm25": 21.5, "pm10": 34.5, "aqi": 50, "temp": 22.7, "humidity": 77, "wind": 3.0}
    ],
    "VN_NB": [
        {"id": "VN_NB_01", "name": "Trạm Trung tâm TP Ninh Bình", "type": "Đô thị", "address": "Đường Lê Thái Tổ, P. Đông Thành", "lat": 20.2550, "lon": 105.9780, "pm25": 21.8, "pm10": 36.0, "aqi": 51, "temp": 23.5, "humidity": 72, "wind": 3.3},
        {"id": "VN_NB_02", "name": "Trạm Di sản Tràng An - Tam Cốc", "type": "Trạm nền di sản thiên nhiên", "address": "Quần thể danh thắng Tràng An", "lat": 20.2580, "lon": 105.9080, "pm25": 13.5, "pm10": 21.5, "aqi": 34, "temp": 23.0, "humidity": 75, "wind": 3.0},
        {"id": "VN_NB_03", "name": "Trạm KCN Gián Khẩu", "type": "Công nghiệp", "address": "Huyện Gia Viễn", "lat": 20.3250, "lon": 105.9120, "pm25": 33.5, "pm10": 52.8, "aqi": 63, "temp": 23.8, "humidity": 71, "wind": 3.4}
    ],

    # Miền Trung (8)
    "VN_TH": [
        {"id": "VN_TH_01", "name": "Trạm Trung tâm TP Thanh Hóa", "type": "Đô thị", "address": "Đường Trần Phú, P. Điện Biên", "lat": 19.8120, "lon": 105.7820, "pm25": 27.6, "pm10": 43.5, "aqi": 59, "temp": 23.8, "humidity": 79, "wind": 3.5},
        {"id": "VN_TH_02", "name": "Trạm Du lịch Biển Sầm Sơn", "type": "Ven biển", "address": "Đường Hồ Xuân Hương, TP. Sầm Sơn", "lat": 19.7450, "lon": 105.9050, "pm25": 18.2, "pm10": 29.5, "aqi": 43, "temp": 24.2, "humidity": 82, "wind": 4.2},
        {"id": "VN_TH_03", "name": "Trạm KKT Nghi Sơn", "type": "Công nghiệp nặng & Lọc dầu", "address": "Khu kinh tế Nghi Sơn, TX. Nghi Sơn", "lat": 19.3450, "lon": 105.7850, "pm25": 43.0, "pm10": 67.5, "aqi": 75, "temp": 24.5, "humidity": 77, "wind": 4.0}
    ],
    "VN_NA": [
        {"id": "VN_NA_01", "name": "Trạm Trung tâm TP Vinh", "type": "Đô thị", "address": "Đường Lê Mao, P. Lê Mao", "lat": 18.6750, "lon": 105.6840, "pm25": 26.2, "pm10": 41.5, "aqi": 57, "temp": 23.2, "humidity": 81, "wind": 3.6},
        {"id": "VN_NA_02", "name": "Trạm Quê Bác - Nam Đàn", "type": "Trạm nền văn hóa", "address": "Khu di tích Kim Liên, H. Nam Đàn", "lat": 18.6850, "lon": 105.5450, "pm25": 15.8, "pm10": 25.0, "aqi": 38, "temp": 23.0, "humidity": 83, "wind": 3.2},
        {"id": "VN_NA_03", "name": "Trạm Thị xã Biển Cửa Lò", "type": "Ven biển", "address": "Đường Bình Minh, TX. Cửa Lò", "lat": 18.8050, "lon": 105.7250, "pm25": 19.4, "pm10": 30.8, "aqi": 45, "temp": 23.5, "humidity": 84, "wind": 4.0}
    ],
    "VN_HT": [
        {"id": "VN_HT_01", "name": "Trạm Trung tâm TP Hà Tĩnh", "type": "Đô thị", "address": "Đường Phan Đình Phùng, P. Bắc Hà", "lat": 18.3450, "lon": 105.9080, "pm25": 22.0, "pm10": 35.8, "aqi": 52, "temp": 23.0, "humidity": 82, "wind": 3.4},
        {"id": "VN_HT_02", "name": "Trạm KKT Vũng Áng - Formosa", "type": "Công nghiệp nặng", "address": "Khu kinh tế Vũng Áng, TX. Kỳ Anh", "lat": 18.0650, "lon": 106.3850, "pm25": 39.5, "pm10": 62.0, "aqi": 71, "temp": 23.6, "humidity": 80, "wind": 4.5},
        {"id": "VN_HT_03", "name": "Trạm Khu Di tích Ngã ba Đồng Lộc", "type": "Trạm nền lịch sử", "address": "Huyện Can Lộc", "lat": 18.4250, "lon": 105.7520, "pm25": 14.0, "pm10": 22.5, "aqi": 35, "temp": 22.6, "humidity": 85, "wind": 3.0}
    ],
    "VN_QT": [
        {"id": "VN_QT_01", "name": "Trạm TP Đông Hà", "type": "Đô thị", "address": "Đường Hùng Vương, P. 1", "lat": 16.8220, "lon": 107.0980, "pm25": 18.0, "pm10": 28.5, "aqi": 44, "temp": 24.2, "humidity": 84, "wind": 3.1},
        {"id": "VN_QT_02", "name": "Trạm TX Quảng Trị - Thành Cổ", "type": "Văn hóa di tích", "address": "Đường Hai Bà Trưng, P. 2", "lat": 16.7480, "lon": 107.1850, "pm25": 15.2, "pm10": 24.0, "aqi": 38, "temp": 24.0, "humidity": 85, "wind": 2.8},
        {"id": "VN_QT_03", "name": "Trạm Cửa khẩu Quốc tế Lao Bảo", "type": "Giao thông biên giới", "address": "Thị trấn Lao Bảo, H. Hướng Hóa", "lat": 16.6150, "lon": 106.5920, "pm25": 12.0, "pm10": 19.2, "aqi": 31, "temp": 22.8, "humidity": 80, "wind": 3.5}
    ],
    "VN_HUE": [
        {"id": "VN_HUE_01", "name": "Trạm Đại Nội - Trung tâm Cố Đô", "type": "Đô thị di sản", "address": "Đường Đoàn Thị Điểm, P. Thuận Thành", "lat": 16.4690, "lon": 107.5780, "pm25": 16.2, "pm10": 26.8, "aqi": 42, "temp": 24.0, "humidity": 85, "wind": 2.8},
        {"id": "VN_HUE_02", "name": "Trạm Phố đi bộ Nguyễn Đình Chiểu", "type": "Du lịch ven sông Hương", "address": "Bờ sông Hương, P. Vĩnh Ninh", "lat": 16.4620, "lon": 107.5890, "pm25": 17.5, "pm10": 28.0, "aqi": 44, "temp": 24.1, "humidity": 84, "wind": 2.6},
        {"id": "VN_HUE_03", "name": "Trạm KCN Phú Bài & Sân bay", "type": "Giao thông công nghiệp", "address": "TX. Hương Thủy", "lat": 16.3980, "lon": 107.6980, "pm25": 24.8, "pm10": 39.5, "aqi": 54, "temp": 24.5, "humidity": 82, "wind": 3.2}
    ],
    "VN_DN": [
        {"id": "VN_DN_01", "name": "Trạm Hải Châu - Cầu Rồng", "type": "Đô thị trung tâm", "address": "Đường Bạch Đằng, Q. Hải Châu", "lat": 16.0620, "lon": 108.2230, "pm25": 14.5, "pm10": 24.0, "aqi": 38, "temp": 27.5, "humidity": 70, "wind": 4.2},
        {"id": "VN_DN_02", "name": "Trạm Bán đảo Sinh thái Sơn Trà", "type": "Trạm nền sinh thái rừng biển", "address": "Bán đảo Sơn Trà, Q. Sơn Trà", "lat": 16.1150, "lon": 108.2750, "pm25": 8.2, "pm10": 13.5, "aqi": 22, "temp": 25.8, "humidity": 76, "wind": 4.8},
        {"id": "VN_DN_03", "name": "Trạm KCN Hòa Khánh - Liên Chiểu", "type": "Công nghiệp", "address": "KCN Hòa Khánh, Q. Liên Chiểu", "lat": 16.0720, "lon": 108.1450, "pm25": 23.5, "pm10": 38.2, "aqi": 53, "temp": 27.8, "humidity": 68, "wind": 3.8},
        {"id": "VN_DN_04", "name": "Trạm Bãi biển Mỹ Khê", "type": "Du lịch ven biển", "address": "Đường Võ Nguyên Giáp, Q. Ngũ Hành Sơn", "lat": 16.0480, "lon": 108.2450, "pm25": 11.0, "pm10": 18.0, "aqi": 29, "temp": 27.2, "humidity": 72, "wind": 4.5}
    ],
    "VN_QNG": [
        {"id": "VN_QNG_01", "name": "Trạm Trung tâm TP Quảng Ngãi", "type": "Đô thị", "address": "Đường Quang Trung, P. Lê Hồng Phong", "lat": 15.1220, "lon": 108.7950, "pm25": 15.5, "pm10": 25.2, "aqi": 39, "temp": 27.0, "humidity": 73, "wind": 3.8},
        {"id": "VN_QNG_02", "name": "Trạm KKT Dung Quất - Lọc dầu", "type": "Công nghiệp nặng & Lọc dầu", "address": "Khu kinh tế Dung Quất, H. Bình Sơn", "lat": 15.4120, "lon": 108.7850, "pm25": 31.0, "pm10": 49.5, "aqi": 61, "temp": 27.5, "humidity": 71, "wind": 4.2},
        {"id": "VN_QNG_03", "name": "Trạm Đảo Sinh thái Lý Sơn", "type": "Sinh thái biển đảo", "address": "Huyện đảo Lý Sơn", "lat": 15.3780, "lon": 109.1250, "pm25": 8.5, "pm10": 13.8, "aqi": 23, "temp": 26.5, "humidity": 76, "wind": 5.2}
    ],
    "VN_KH": [
        {"id": "VN_KH_01", "name": "Trạm Bờ biển Trần Phú - Nha Trang", "type": "Đô thị du lịch", "address": "Đường Trần Phú, TP. Nha Trang", "lat": 12.2420, "lon": 109.1980, "pm25": 12.4, "pm10": 20.8, "aqi": 34, "temp": 28.2, "humidity": 70, "wind": 4.8},
        {"id": "VN_KH_02", "name": "Trạm Bán đảo Cam Ranh & Sân bay", "type": "Giao thông ven vịnh", "address": "TP. Cam Ranh", "lat": 11.9950, "lon": 109.1350, "pm25": 10.8, "pm10": 17.5, "aqi": 30, "temp": 28.5, "humidity": 68, "wind": 5.0},
        {"id": "VN_KH_03", "name": "Trạm Đảo Hòn Tre - Vinpearl", "type": "Sinh thái đảo", "address": "Vịnh Nha Trang", "lat": 12.2150, "lon": 109.2550, "pm25": 7.5, "pm10": 12.2, "aqi": 20, "temp": 27.6, "humidity": 73, "wind": 4.6}
    ],

    # Tây Nguyên (3)
    "VN_GL": [
        {"id": "VN_GL_01", "name": "Trạm Pleiku - Quảng trường Đại Đoàn Kết", "type": "Đô thị cao nguyên", "address": "Đường Trần Hưng Đạo, P. Tây Sơn", "lat": 13.9850, "lon": 108.0050, "pm25": 11.5, "pm10": 18.2, "aqi": 31, "temp": 22.8, "humidity": 65, "wind": 3.5},
        {"id": "VN_GL_02", "name": "Trạm Thắng cảnh Biển Hồ (Tơ Nưng)", "type": "Trạm nền sinh thái hồ", "address": "Xã Biển Hồ, TP. Pleiku", "lat": 14.0480, "lon": 108.0020, "pm25": 7.2, "pm10": 11.5, "aqi": 19, "temp": 21.5, "humidity": 70, "wind": 3.8},
        {"id": "VN_GL_03", "name": "Trạm Rừng Quốc gia Kon Ka Kinh", "type": "Trạm nền rừng đặc dụng", "address": "Huyện Mang Yang", "lat": 14.3150, "lon": 108.3850, "pm25": 5.8, "pm10": 9.2, "aqi": 16, "temp": 19.8, "humidity": 75, "wind": 3.0}
    ],
    "VN_DLAK": [
        {"id": "VN_DLAK_01", "name": "Trạm Buôn Ma Thuột - Thủ phủ Cà phê", "type": "Đô thị", "address": "Đường Lê Duẩn, P. Tân Thành", "lat": 12.6710, "lon": 108.0480, "pm25": 13.8, "pm10": 22.0, "aqi": 36, "temp": 24.5, "humidity": 67, "wind": 3.2},
        {"id": "VN_DLAK_02", "name": "Trạm Sinh thái Hồ Lắk", "type": "Sinh thái hồ nước", "address": "Thị trấn Liên Sơn, H. Lắk", "lat": 12.4150, "lon": 108.1850, "pm25": 8.6, "pm10": 13.8, "aqi": 23, "temp": 23.8, "humidity": 72, "wind": 2.8},
        {"id": "VN_DLAK_03", "name": "Trạm KCN Hòa Phú", "type": "Công nghiệp", "address": "Xã Hòa Phú, TP. Buôn Ma Thuột", "lat": 12.5850, "lon": 107.9550, "pm25": 22.5, "pm10": 36.0, "aqi": 52, "temp": 25.2, "humidity": 64, "wind": 3.0}
    ],
    "VN_LD": [
        {"id": "VN_LD_01", "name": "Trạm Hồ Xuân Hương - Đà Lạt", "type": "Đô thị ngàn hoa", "address": "Đường Trần Quốc Toản, P. 1, TP. Đà Lạt", "lat": 11.9440, "lon": 108.4480, "pm25": 8.5, "pm10": 14.8, "aqi": 23, "temp": 17.0, "humidity": 82, "wind": 2.2},
        {"id": "VN_LD_02", "name": "Trạm Đèo Prenn - Rừng thông", "type": "Trạm nền sinh thái rừng thông", "address": "Đèo Prenn, TP. Đà Lạt", "lat": 11.8950, "lon": 108.4420, "pm25": 6.2, "pm10": 10.2, "aqi": 17, "temp": 16.2, "humidity": 86, "wind": 2.5},
        {"id": "VN_LD_03", "name": "Trạm TP Bảo Lộc - Vùng Đồi Chè", "type": "Đô thị cao nguyên trà", "address": "Đường Lê Hồng Phong, TP. Bảo Lộc", "lat": 11.5450, "lon": 107.8050, "pm25": 10.4, "pm10": 16.8, "aqi": 27, "temp": 21.0, "humidity": 78, "wind": 2.6}
    ],

    # Miền Nam (8)
    "VN_HCM": [
        {"id": "VN_HCM_01", "name": "Trạm Bến Nghé - Quận 1", "type": "Đô thị trung tâm hành chính", "address": "Đường Nguyễn Huệ, P. Bến Nghé, Q. 1", "lat": 10.7750, "lon": 106.7040, "pm25": 31.5, "pm10": 51.0, "aqi": 68, "temp": 31.5, "humidity": 66, "wind": 3.0},
        {"id": "VN_HCM_02", "name": "Trạm Ngã tư Hàng Xanh - Bình Thạnh", "type": "Giao thông mật độ cao", "address": "Ngã tư Hàng Xanh, Q. Bình Thạnh", "lat": 10.8020, "lon": 106.7120, "pm25": 44.0, "pm10": 68.5, "aqi": 78, "temp": 32.2, "humidity": 63, "wind": 3.2},
        {"id": "VN_HCM_03", "name": "Trạm TP Thủ Đức - KCNC", "type": "Đô thị sáng tạo công nghệ", "address": "Đường D1, Khu CNC, TP. Thủ Đức", "lat": 10.8540, "lon": 106.7950, "pm25": 27.5, "pm10": 44.2, "aqi": 60, "temp": 31.8, "humidity": 65, "wind": 3.0},
        {"id": "VN_HCM_04", "name": "Trạm KCN Tân Bình - Bình Chánh", "type": "Công nghiệp", "address": "KCN Tân Bình & Bình Chánh", "lat": 10.8120, "lon": 106.6250, "pm25": 41.8, "pm10": 65.0, "aqi": 75, "temp": 32.5, "humidity": 62, "wind": 2.8},
        {"id": "VN_HCM_05", "name": "Trạm Sinh thái Cần Giờ", "type": "Trạm nền sinh thái rừng ngập mặn", "address": "Xã Long Hòa, H. Cần Giờ", "lat": 10.4150, "lon": 106.9150, "pm25": 12.8, "pm10": 20.5, "aqi": 32, "temp": 29.8, "humidity": 75, "wind": 4.5}
    ],
    "VN_DNAI": [
        {"id": "VN_DNAI_01", "name": "Trạm TP Biên Hòa - Trung tâm", "type": "Đô thị", "address": "Đường 30/4, P. Thanh Bình", "lat": 10.9590, "lon": 106.8390, "pm25": 34.2, "pm10": 54.6, "aqi": 70, "temp": 31.0, "humidity": 68, "wind": 2.9},
        {"id": "VN_DNAI_02", "name": "Trạm KCN Biên Hòa 2 & Amata", "type": "Công nghiệp", "address": "KCN Biên Hòa 2, TP. Biên Hòa", "lat": 10.9250, "lon": 106.8850, "pm25": 46.5, "pm10": 72.8, "aqi": 82, "temp": 32.0, "humidity": 65, "wind": 3.1},
        {"id": "VN_DNAI_03", "name": "Trạm Vườn Quốc gia Cát Tiên", "type": "Trạm nền rừng nhiệt đới", "address": "Huyện Tân Phú", "lat": 11.4250, "lon": 107.4150, "pm25": 11.0, "pm10": 17.5, "aqi": 28, "temp": 27.5, "humidity": 78, "wind": 2.4}
    ],
    "VN_TNINH": [
        {"id": "VN_TNINH_01", "name": "Trạm TP Tây Ninh - Trung tâm Đô thị", "type": "Đô thị", "address": "Đường 30/4, P. 3, TP. Tây Ninh", "lat": 11.3120, "lon": 106.0990, "pm25": 23.5, "pm10": 38.2, "aqi": 58, "temp": 32.0, "humidity": 62, "wind": 2.9},
        {"id": "VN_TNINH_02", "name": "Trạm Đỉnh Núi Bà Đen - Khí tượng Cao nguyên", "type": "Trạm nền khí hậu núi cao", "address": "Khu du lịch Quốc gia Núi Bà Đen", "lat": 11.3850, "lon": 106.1680, "pm25": 11.2, "pm10": 18.0, "aqi": 35, "temp": 25.4, "humidity": 74, "wind": 4.2},
        {"id": "VN_TNINH_03", "name": "Trạm KCN Trảng Bàng - Cửa khẩu Mộc Bài", "type": "Công nghiệp & Giao thông", "address": "KCN Trảng Bàng, TX. Trảng Bàng", "lat": 11.0350, "lon": 106.3550, "pm25": 31.0, "pm10": 49.5, "aqi": 68, "temp": 32.5, "humidity": 60, "wind": 3.2},
        {"id": "VN_TNINH_04", "name": "Trạm Tòa Thánh Tây Ninh - Tâm linh", "type": "Văn hóa du lịch", "address": "Phường Hiệp Ninh, TP. Tây Ninh", "lat": 11.3050, "lon": 106.1350, "pm25": 18.5, "pm10": 29.8, "aqi": 47, "temp": 31.8, "humidity": 64, "wind": 2.8}
    ],
    "VN_CT": [
        {"id": "VN_CT_01", "name": "Trạm Bến Ninh Kiều - Trung tâm", "type": "Đô thị sông nước", "address": "Đường Hai Bà Trưng, P. Tân An, Q. Ninh Kiều", "lat": 10.0350, "lon": 105.7890, "pm25": 21.4, "pm10": 36.8, "aqi": 52, "temp": 30.2, "humidity": 72, "wind": 2.8},
        {"id": "VN_CT_02", "name": "Trạm KCN Trà Nóc & Cảng Cần Thơ", "type": "Công nghiệp cảng", "address": "KCN Trà Nóc 1, Q. Bình Thủy", "lat": 10.0850, "lon": 105.7250, "pm25": 29.8, "pm10": 47.5, "aqi": 64, "temp": 30.8, "humidity": 70, "wind": 3.1},
        {"id": "VN_CT_03", "name": "Trạm Chợ Nổi Cái Răng", "type": "Nông nghiệp du lịch sinh thái", "address": "Quận Cái Răng", "lat": 10.0050, "lon": 105.7450, "pm25": 15.5, "pm10": 24.8, "aqi": 42, "temp": 29.8, "humidity": 75, "wind": 2.6}
    ],
    "VN_DT": [
        {"id": "VN_DT_01", "name": "Trạm TP Cao Lãnh - Trung tâm", "type": "Đô thị", "address": "Đường Lý Thường Kiệt, P. 1", "lat": 10.4590, "lon": 105.6350, "pm25": 19.8, "pm10": 32.5, "aqi": 49, "temp": 30.5, "humidity": 73, "wind": 2.6},
        {"id": "VN_DT_02", "name": "Trạm Làng Hoa Sa Đéc", "type": "Nông nghiệp hoa kiểng", "address": "Xã Tân Quy Đông, TP. Sa Đéc", "lat": 10.3150, "lon": 105.7550, "pm25": 14.2, "pm10": 23.0, "aqi": 38, "temp": 30.2, "humidity": 74, "wind": 2.5},
        {"id": "VN_DT_03", "name": "Trạm Vườn Quốc gia Tràm Chim", "type": "Trạm nền ngập nước", "address": "Thị trấn Tràm Chim, H. Tam Nông", "lat": 10.7150, "lon": 105.5150, "pm25": 9.8, "pm10": 16.0, "aqi": 26, "temp": 29.5, "humidity": 78, "wind": 2.4}
    ],
    "VN_VL": [
        {"id": "VN_VL_01", "name": "Trạm Trung tâm TP Vĩnh Long", "type": "Đô thị", "address": "Đường Trưng Nữ Vương, P. 1", "lat": 10.2550, "lon": 105.9750, "pm25": 20.2, "pm10": 33.6, "aqi": 50, "temp": 30.0, "humidity": 74, "wind": 2.7},
        {"id": "VN_VL_02", "name": "Trạm Cù lao An Bình - Miệt vườn", "type": "Sinh thái sông nước", "address": "Huyện Long Hồ", "lat": 10.2850, "lon": 105.9850, "pm25": 13.0, "pm10": 21.2, "aqi": 35, "temp": 29.5, "humidity": 76, "wind": 2.5},
        {"id": "VN_VL_03", "name": "Trạm KCN Hòa Phú", "type": "Công nghiệp", "address": "Xã Hòa Phú, H. Long Hồ", "lat": 10.1850, "lon": 105.9550, "pm25": 28.5, "pm10": 45.2, "aqi": 62, "temp": 30.6, "humidity": 72, "wind": 2.9}
    ],
    "VN_AG": [
        {"id": "VN_AG_01", "name": "Trạm TP Long Xuyên - Trung tâm", "type": "Đô thị", "address": "Đường Hà Hoàng Hổ, P. Mỹ Xuyên", "lat": 10.3850, "lon": 105.4200, "pm25": 18.6, "pm10": 30.5, "aqi": 48, "temp": 31.0, "humidity": 71, "wind": 2.8},
        {"id": "VN_AG_02", "name": "Trạm TP Châu Đốc - Núi Sam", "type": "Du lịch tâm linh biên giới", "address": "Phường Núi Sam, TP. Châu Đốc", "lat": 10.6850, "lon": 105.1550, "pm25": 15.0, "pm10": 24.5, "aqi": 40, "temp": 30.8, "humidity": 72, "wind": 2.9},
        {"id": "VN_AG_03", "name": "Trạm Rừng Tràm Trà Sư", "type": "Trạm nền sinh thái rừng ngập phèn", "address": "Xã Văn Giáo, TX. Tịnh Biên", "lat": 10.5120, "lon": 105.0520, "pm25": 9.2, "pm10": 15.0, "aqi": 25, "temp": 29.6, "humidity": 76, "wind": 2.6}
    ],
    "VN_CM": [
        {"id": "VN_CM_01", "name": "Trạm Trung tâm TP Cà Mau", "type": "Đô thị", "address": "Đường Hùng Vương, P. 5", "lat": 9.1800, "lon": 105.1550, "pm25": 14.0, "pm10": 23.5, "aqi": 42, "temp": 29.5, "humidity": 78, "wind": 4.5},
        {"id": "VN_CM_02", "name": "Trạm Cột Mốc Tọa Độ Đất Mũi", "type": "Trạm nền sinh thái cực Nam", "address": "Xã Đất Mũi, H. Ngọc Hiển", "lat": 8.6150, "lon": 104.7250, "pm25": 8.4, "pm10": 13.8, "aqi": 22, "temp": 28.5, "humidity": 82, "wind": 5.2},
        {"id": "VN_CM_03", "name": "Trạm KCN Khí - Điện - Đạm Cà Mau", "type": "Công nghiệp năng lượng", "address": "Xã Khánh An, H. U Minh", "lat": 9.2850, "lon": 105.0150, "pm25": 26.5, "pm10": 42.0, "aqi": 58, "temp": 30.0, "humidity": 76, "wind": 4.2}
    ]
}

def aqi_category(aqi):
    if aqi <= 50:
        return ("Tốt", "#10b981")
    elif aqi <= 100:
        return ("Trung bình", "#f59e0b")
    elif aqi <= 150:
        return ("Kém (Nhạy cảm)", "#f97316")
    elif aqi <= 200:
        return ("Xấu (Có hại)", "#ef4444")
    else:
        return ("Rất xấu / Nguy hại", "#7c3aed")

# Build enriched stations
for prov_id, st_list in STATIONS_CONFIG.items():
    for s in st_list:
        lvl, col = aqi_category(s["aqi"])
        s["aqi_level"] = lvl
        s["color"] = col
        s["status"] = "Đang hoạt động 24/7"
        s["province_id"] = prov_id

# 1. Write js/stations_data.js
stations_js_content = f"// Detailed Monitoring Stations for All 34 Provinces of Vietnam\nwindow.VIETNAM_STATIONS_DATA = {json.dumps(STATIONS_CONFIG, ensure_ascii=False, indent=2)};\n"
with open("js/stations_data.js", "w", encoding="utf-8") as f:
    f.write(stations_js_content)
print(f"Generated js/stations_data.js with {len(STATIONS_CONFIG)} provinces.")

# 2. Update js/embedded_data.js with stations
with open("js/embedded_data.js", "r", encoding="utf-8") as f:
    embed_text = f.read()

s_idx = embed_text.find("latest: [")
e_idx = embed_text.find("history:", s_idx)
e_bracket = embed_text.rfind("]", s_idx, e_idx)
provinces_list = json.loads(embed_text[s_idx + len("latest: "):e_bracket + 1])

for p in provinces_list:
    pid = p.get("id")
    if pid in STATIONS_CONFIG:
        p["stations"] = STATIONS_CONFIG[pid]
    else:
        p["stations"] = []

new_latest_json = json.dumps(provinces_list, ensure_ascii=False)
new_embed_text = embed_text[:s_idx + len("latest: ")] + new_latest_json + embed_text[e_bracket + 1:]

with open("js/embedded_data.js", "w", encoding="utf-8") as f:
    f.write(new_embed_text)
print("Updated js/embedded_data.js with province stations.")

# 3. Update backend/provinces_data.py with clean UTF-8
py_backend_content = f'''# -*- coding: utf-8 -*-
"""
Master 34 Provinces and 101 Monitoring Stations for Backend Service
"""

PROVINCES_34 = {json.dumps(provinces_list, ensure_ascii=False, indent=2)}

STATIONS_CONFIG = {json.dumps(STATIONS_CONFIG, ensure_ascii=False, indent=2)}
'''

with open("backend/provinces_data.py", "w", encoding="utf-8") as f:
    f.write(py_backend_content)
print("Updated backend/provinces_data.py successfully!")

# 4. Update backend/routes/air_quality.py to handle detailed stations
with open("backend/routes/air_quality.py", "r", encoding="utf-8") as f:
    route_code = f.read()

if "STATIONS_CONFIG" not in route_code:
    route_code = route_code.replace(
        "from backend.provinces_data import PROVINCES_34",
        "from backend.provinces_data import PROVINCES_34, STATIONS_CONFIG"
    )

old_lookup = '''        # Tra cứu thông tin từ 34 tỉnh thành
        matched = next((p for p in PROVINCES_34 if p["id"] == req.station_id or p["name"].lower() == req.station_id.lower()), None)
        if not matched:
            matched = PROVINCES_34[0] # Hà Nội mặc định
            
        # Tạo chuỗi dữ liệu 48h thực tế cho trạm để làm đầu vào cho mô hình
        records = []
        base_pm = matched["pm25"]
        base_temp = matched["temp"]
        base_hum = matched["humidity"]
        base_wind = matched["wind_speed"]
        now = pd.Timestamp.now()
        
        for i in range(48, 0, -1):
            ts = now - pd.Timedelta(hours=i)
            jitter_pm = round(max(4.0, base_pm + np.sin(i / 3.8) * 4.5), 2)
            records.append({
                "timestamp": ts,
                "station_id": matched["id"],
                "station_name": f"Trạm {matched['name']}",
                "district": matched["name"],
                "pm25": jitter_pm,
                "temperature": base_temp + np.sin(i / 4.0) * 2.0,
                "humidity": np.clip(base_hum + np.cos(i / 3.0) * 6.0, 30.0, 95.0),
                "wind_speed": base_wind,
                "pm10": round(jitter_pm * 1.45, 2),
                "no2": matched.get("no2", 20.0),
                "co": matched.get("co", 0.8),
                "o3": matched.get("o3", 25.0),
                "so2": matched.get("so2", 6.0),
                "dist_center_km": 3.5,
                "elevation_m": 15.0
            })
        recent_history = pd.DataFrame(records)'''

new_lookup = '''        # Tra cứu thông tin từ 101 trạm chi tiết hoặc 34 tỉnh thành
        matched_st = None
        matched_prov = None
        for pid, st_list in STATIONS_CONFIG.items():
            for s in st_list:
                if s["id"] == req.station_id:
                    matched_st = s
                    matched_prov = next((p for p in PROVINCES_34 if p["id"] == pid), None)
                    break
            if matched_st:
                break
        
        if matched_st:
            base_pm = matched_st["pm25"]
            base_temp = matched_st["temp"]
            base_hum = matched_st["humidity"]
            base_wind = matched_st.get("wind", 3.0)
            station_name = matched_st["name"]
            district_name = matched_prov["name"] if matched_prov else matched_st["name"]
            station_id_val = matched_st["id"]
        else:
            matched = next((p for p in PROVINCES_34 if p["id"] == req.station_id or p["name"].lower() == req.station_id.lower()), None)
            if not matched:
                matched = PROVINCES_34[0] # Hà Nội mặc định
            base_pm = matched["pm25"]
            base_temp = matched["temp"]
            base_hum = matched["humidity"]
            base_wind = matched["wind_speed"]
            station_name = f"Trạm {matched['name']}"
            district_name = matched["name"]
            station_id_val = matched["id"]
            
        # Tạo chuỗi dữ liệu 48h thực tế cho trạm để làm đầu vào cho mô hình
        records = []
        now = pd.Timestamp.now()
        
        for i in range(48, 0, -1):
            ts = now - pd.Timedelta(hours=i)
            jitter_pm = round(max(4.0, base_pm + np.sin(i / 3.8) * 4.5), 2)
            records.append({
                "timestamp": ts,
                "station_id": station_id_val,
                "station_name": station_name,
                "district": district_name,
                "pm25": jitter_pm,
                "temperature": base_temp + np.sin(i / 4.0) * 2.0,
                "humidity": np.clip(base_hum + np.cos(i / 3.0) * 6.0, 30.0, 95.0),
                "wind_speed": base_wind,
                "pm10": round(jitter_pm * 1.45, 2),
                "no2": 20.0,
                "co": 0.8,
                "o3": 25.0,
                "so2": 6.0,
                "dist_center_km": 3.5,
                "elevation_m": 15.0
            })
        recent_history = pd.DataFrame(records)'''

route_code_normalized = route_code.replace("\r\n", "\n")
old_lookup_normalized = old_lookup.replace("\r\n", "\n")
new_lookup_normalized = new_lookup.replace("\r\n", "\n")

if old_lookup_normalized in route_code_normalized:
    route_code_normalized = route_code_normalized.replace(old_lookup_normalized, new_lookup_normalized)
    with open("backend/routes/air_quality.py", "w", encoding="utf-8") as f:
        f.write(route_code_normalized)
    print("Updated backend/routes/air_quality.py with detailed station lookup!")
else:
    print("Lookup snippet already updated or pattern adjusted.")


