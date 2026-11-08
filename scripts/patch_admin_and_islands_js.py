import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
js_path = os.path.join(ROOT, "js", "app.js")

with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# 1. Add state variables to App object if not present
if "showAdminLabels: true" not in js_content:
    js_content = js_content.replace(
        "mapLayer: 'temp',",
        "mapLayer: 'temp',\n  showAdminLabels: true,\n  showIslands: true,"
    )
    print("Added showAdminLabels & showIslands state variables to App object")

# 2. Add islandsData and helper methods right before initMap()
islands_and_methods = '''  // =========================================================================
  // DỮ LIỆU ĐỊA LÝ CÁC QUẦN ĐẢO & ĐẢO TIÊU BIỂU VIỆT NAM (100% TIẾNG VIỆT CÓ DẤU)
  // =========================================================================
  islandsData: [
    // --- QUẦN ĐẢO HOÀNG SA (Huyện Hoàng Sa, TP. Đà Nẵng) ---
    {
      id: 'hs_main',
      name: 'Đảo Hoàng Sa',
      group: 'Quần đảo Hoàng Sa',
      admin: 'Huyện Hoàng Sa, TP. Đà Nẵng',
      lat: 16.533,
      lon: 111.605,
      isMainArchipelago: true,
      desc: 'Đảo chính trung tâm của Quần đảo Hoàng Sa, nơi đặt Trạm Khí tượng Hải văn Hoàng Sa (thành lập từ năm 1938).',
      radius: 9000,
      temp: 28.5,
      humidity: 82,
      wind: 'Đông Bắc 6.5 m/s (Cấp 4)',
      wave: '1.2 m',
      aqi: 18,
      status: 'Tốt',
      provId: 'VN_DN'
    },
    {
      id: 'hs_phulam',
      name: 'Đảo Phú Lâm',
      group: 'Quần đảo Hoàng Sa',
      admin: 'Huyện Hoàng Sa, TP. Đà Nẵng',
      lat: 16.834,
      lon: 112.336,
      desc: 'Đảo có diện tích tự nhiên lớn nhất nhóm đảo An Vĩnh thuộc Quần đảo Hoàng Sa.',
      radius: 10000,
      temp: 28.8,
      humidity: 80,
      wind: 'Đông Bắc 6.0 m/s',
      wave: '1.1 m',
      aqi: 16,
      status: 'Tốt',
      provId: 'VN_DN'
    },
    {
      id: 'hs_triton',
      name: 'Đảo Tri Tôn',
      group: 'Quần đảo Hoàng Sa',
      admin: 'Huyện Hoàng Sa, TP. Đà Nẵng',
      lat: 15.790,
      lon: 111.203,
      desc: 'Đảo ở vị trí cực tây nam của Quần đảo Hoàng Sa, gần đất liền miền Trung Việt Nam nhất.',
      radius: 7500,
      temp: 29.0,
      humidity: 81,
      wind: 'Đông 5.8 m/s',
      wave: '1.0 m',
      aqi: 15,
      status: 'Tốt',
      provId: 'VN_DN'
    },
    {
      id: 'hs_linhcon',
      name: 'Đảo Linh Côn',
      group: 'Quần đảo Hoàng Sa',
      admin: 'Huyện Hoàng Sa, TP. Đà Nẵng',
      lat: 16.667,
      lon: 112.733,
      desc: 'Đảo san hô ở cực đông của Quần đảo Hoàng Sa, bao bọc bởi đầm phá nước nông và rạn san hô trù phú.',
      radius: 9000,
      temp: 28.3,
      humidity: 83,
      wind: 'Đông Bắc 6.8 m/s',
      wave: '1.3 m',
      aqi: 17,
      status: 'Tốt',
      provId: 'VN_DN'
    },
    {
      id: 'hs_quanghoa',
      name: 'Đảo Quang Hòa',
      group: 'Quần đảo Hoàng Sa',
      admin: 'Huyện Hoàng Sa, TP. Đà Nẵng',
      lat: 16.452,
      lon: 111.710,
      desc: 'Đảo san hô lớn thuộc nhóm đảo Lưỡi Liềm của Quần đảo Hoàng Sa.',
      radius: 7500,
      temp: 28.6,
      humidity: 82,
      wind: 'Đông Bắc 6.2 m/s',
      wave: '1.2 m',
      aqi: 18,
      status: 'Tốt',
      provId: 'VN_DN'
    },
    {
      id: 'hs_cay',
      name: 'Đảo Cây',
      group: 'Quần đảo Hoàng Sa',
      admin: 'Huyện Hoàng Sa, TP. Đà Nẵng',
      lat: 16.890,
      lon: 112.270,
      desc: 'Đảo cát và rạn san hô xanh tươi thuộc nhóm đảo An Vĩnh của Quần đảo Hoàng Sa.',
      radius: 7000,
      temp: 28.7,
      humidity: 81,
      wind: 'Đông 6.0 m/s',
      wave: '1.1 m',
      aqi: 15,
      status: 'Tốt',
      provId: 'VN_DN'
    },

    // --- QUẦN ĐẢO TRƯỜNG SA (Huyện Trường Sa, Tỉnh Khánh Hòa) ---
    {
      id: 'ts_lon',
      name: 'Đảo Trường Sa Lớn',
      group: 'Quần đảo Trường Sa',
      admin: 'Thị trấn Trường Sa, Huyện Trường Sa, Tỉnh Khánh Hòa',
      lat: 8.644,
      lon: 111.921,
      isMainArchipelago: true,
      desc: 'Thủ phủ hành chính Thị trấn Trường Sa, có Trạm Khí tượng Hải văn Đảo Trường Sa Lớn, trạm y tế và âu tàu kiên cố.',
      radius: 9000,
      temp: 29.2,
      humidity: 85,
      wind: 'Đông Nam 5.2 m/s (Cấp 3)',
      wave: '1.0 m',
      aqi: 15,
      status: 'Tốt',
      provId: 'VN_KH'
    },
    {
      id: 'ts_songtutay',
      name: 'Đảo Song Tử Tây',
      group: 'Quần đảo Trường Sa',
      admin: 'Xã Song Tử Tây, Huyện Trường Sa, Tỉnh Khánh Hòa',
      lat: 11.428,
      lon: 114.331,
      desc: 'Cụm đảo cực bắc của Quần đảo Trường Sa, có ngọn hải đăng Song Tử Tây cao 36m và thảm thực vật phong phú.',
      radius: 8000,
      temp: 28.9,
      humidity: 83,
      wind: 'Đông Bắc 6.0 m/s',
      wave: '1.2 m',
      aqi: 14,
      status: 'Tốt',
      provId: 'VN_KH'
    },
    {
      id: 'ts_sinhton',
      name: 'Đảo Sinh Tồn',
      group: 'Quần đảo Trường Sa',
      admin: 'Xã Sinh Tồn, Huyện Trường Sa, Tỉnh Khánh Hòa',
      lat: 9.885,
      lon: 114.321,
      desc: 'Đảo kiên cố thuộc cụm đảo Sinh Tồn, có cụm dân cư xã Sinh Tồn và trạm quan trắc khí tượng bề mặt.',
      radius: 7500,
      temp: 29.1,
      humidity: 84,
      wind: 'Đông 5.5 m/s',
      wave: '1.1 m',
      aqi: 16,
      status: 'Tốt',
      provId: 'VN_KH'
    },
    {
      id: 'ts_namyet',
      name: 'Đảo Nam Yết',
      group: 'Quần đảo Trường Sa',
      admin: 'Huyện Trường Sa, Tỉnh Khánh Hòa',
      lat: 10.182,
      lon: 114.364,
      desc: 'Đảo trung tâm của cụm Nam Yết, nổi tiếng với vườn dừa và các loài cây phong ba, bàng vuông cổ thụ.',
      radius: 8500,
      temp: 29.0,
      humidity: 82,
      wind: 'Đông 5.0 m/s',
      wave: '1.0 m',
      aqi: 15,
      status: 'Tốt',
      provId: 'VN_KH'
    },
    {
      id: 'ts_sonca',
      name: 'Đảo Sơn Ca',
      group: 'Quần đảo Trường Sa',
      admin: 'Huyện Trường Sa, Tỉnh Khánh Hòa',
      lat: 10.377,
      lon: 114.478,
      desc: 'Đảo san hô cát trắng và rạn san hô viền bao quanh, môi trường sinh thái biển nguyên sơ.',
      radius: 7000,
      temp: 28.8,
      humidity: 83,
      wind: 'Đông Bắc 5.4 m/s',
      wave: '1.1 m',
      aqi: 14,
      status: 'Tốt',
      provId: 'VN_KH'
    },
    {
      id: 'ts_phanvinh',
      name: 'Đảo Phan Vinh',
      group: 'Quần đảo Trường Sa',
      admin: 'Huyện Trường Sa, Tỉnh Khánh Hòa',
      lat: 8.967,
      lon: 113.469,
      desc: 'Đảo mang tên Anh hùng LLVTND Nguyễn Phan Vinh, điểm tựa cứu hộ cứu nạn cho ngư dân trên Biển Đông.',
      radius: 8000,
      temp: 29.3,
      humidity: 84,
      wind: 'Đông 5.6 m/s',
      wave: '1.0 m',
      aqi: 15,
      status: 'Tốt',
      provId: 'VN_KH'
    },
    {
      id: 'ts_anbang',
      name: 'Đảo An Bang',
      group: 'Quần đảo Trường Sa',
      admin: 'Huyện Trường Sa, Tỉnh Khánh Hòa',
      lat: 7.891,
      lon: 112.919,
      desc: 'Đảo san hô nằm ở phía nam Quần đảo Trường Sa, đặc trưng với bờ cát dịch chuyển theo mùa gió.',
      radius: 7000,
      temp: 29.5,
      humidity: 86,
      wind: 'Đông Nam 5.8 m/s',
      wave: '1.2 m',
      aqi: 13,
      status: 'Tốt',
      provId: 'VN_KH'
    },
    {
      id: 'ts_thuyenchai',
      name: 'Đá Thuyền Chài',
      group: 'Quần đảo Trường Sa',
      admin: 'Huyện Trường Sa, Tỉnh Khánh Hòa',
      lat: 8.167,
      lon: 114.817,
      desc: 'Rạn san hô vòng dài hơn 30 km, có hồ nước sâu kín gió là điểm tránh bão an toàn cho tàu thuyền.',
      radius: 12000,
      temp: 29.4,
      humidity: 85,
      wind: 'Đông 6.0 m/s',
      wave: '1.2 m',
      aqi: 12,
      status: 'Tốt',
      provId: 'VN_KH'
    },

    // --- CÁC HẢI ĐẢO & HUYỆN ĐẢO TIỀN TIÊU DỌC BỜ BIỂN VIỆT NAM ---
    {
      id: 'isl_phuquoc',
      name: 'Đảo Phú Quốc',
      group: 'Vùng biển Tây Nam',
      admin: 'Thành phố Phú Quốc, Tỉnh Kiên Giang',
      lat: 10.228,
      lon: 103.957,
      desc: 'Đảo lớn nhất Việt Nam, thành phố đảo đầu tiên với hệ sinh thái Vườn Quốc gia và du lịch biển tầm vóc quốc tế.',
      radius: 18000,
      temp: 29.8,
      humidity: 78,
      wind: 'Tây Nam 4.0 m/s',
      wave: '0.8 m',
      aqi: 22,
      status: 'Tốt',
      provId: 'VN_KG'
    },
    {
      id: 'isl_condao',
      name: 'Quần đảo Côn Đảo',
      group: 'Vùng biển Đông Nam Bộ',
      admin: 'Huyện Côn Đảo, Tỉnh Bà Rịa - Vũng Tàu',
      lat: 8.683,
      lon: 106.608,
      desc: 'Quần đảo gồm 16 hòn đảo lớn nhỏ, có Vườn Quốc gia Côn Đảo bảo tồn đa dạng sinh học biển quý hiếm.',
      radius: 12000,
      temp: 28.6,
      humidity: 80,
      wind: 'Đông Bắc 5.0 m/s',
      wave: '1.0 m',
      aqi: 19,
      status: 'Tốt',
      provId: 'VN_VT'
    },
    {
      id: 'isl_lyson',
      name: 'Huyện đảo Lý Sơn',
      group: 'Duyên hải Nam Trung Bộ',
      admin: 'Huyện đảo Lý Sơn, Tỉnh Quảng Ngãi',
      lat: 15.378,
      lon: 109.117,
      desc: 'Huyện đảo tiền tiêu núi lửa cổ triệu năm, quê hương của Hải đội Hoàng Sa kiêm quản Trường Sa lừng danh.',
      radius: 7000,
      temp: 27.5,
      humidity: 82,
      wind: 'Đông Bắc 5.5 m/s',
      wave: '1.1 m',
      aqi: 20,
      status: 'Tốt',
      provId: 'VN_QNG'
    },
    {
      id: 'isl_phuquy',
      name: 'Huyện đảo Phú Quý',
      group: 'Nam Trung Bộ',
      admin: 'Huyện đảo Phú Quý, Tỉnh Bình Thuận',
      lat: 10.528,
      lon: 108.940,
      desc: 'Huyện đảo cách Phan Thiết 56 hải lý, trung tâm hậu cần khai thác hải sản và năng lượng gió sạch.',
      radius: 8000,
      temp: 28.2,
      humidity: 79,
      wind: 'Đông Bắc 6.2 m/s',
      wave: '1.2 m',
      aqi: 18,
      status: 'Tốt',
      provId: 'VN_NT'
    },
    {
      id: 'isl_catba',
      name: 'Đảo Cát Bà & Vịnh Lan Hạ',
      group: 'Vịnh Bắc Bộ',
      admin: 'Huyện Cát Hải, Thành phố Hải Phòng',
      lat: 20.728,
      lon: 107.045,
      desc: 'Di sản Thiên nhiên Thế giới UNESCO (Quần đảo Cát Bà - Vịnh Hạ Long), khu dự trữ sinh quyển thế giới.',
      radius: 11000,
      temp: 23.5,
      humidity: 75,
      wind: 'Đông Bắc 4.2 m/s',
      wave: '0.6 m',
      aqi: 35,
      status: 'Tốt',
      provId: 'VN_HP'
    },
    {
      id: 'isl_bachlongvi',
      name: 'Huyện đảo Bạch Long Vĩ',
      group: 'Vịnh Bắc Bộ',
      admin: 'Huyện đảo Bạch Long Vĩ, Thành phố Hải Phòng',
      lat: 20.133,
      lon: 107.724,
      desc: 'Đảo xa bờ nhất trong Vịnh Bắc Bộ, có Trạm Khí tượng Hải văn Bạch Long Vĩ kiểm soát thời tiết biển bắc.',
      radius: 6500,
      temp: 22.8,
      humidity: 78,
      wind: 'Đông Bắc 7.0 m/s (Cấp 4-5)',
      wave: '1.4 m',
      aqi: 24,
      status: 'Tốt',
      provId: 'VN_HP'
    },
    {
      id: 'isl_coto',
      name: 'Huyện đảo Cô Tô',
      group: 'Vùng biển Đông Bắc',
      admin: 'Huyện đảo Cô Tô, Tỉnh Quảng Ninh',
      lat: 20.975,
      lon: 107.765,
      desc: 'Huyện đảo tiền tiêu vùng biển đông bắc, bãi biển Hồng Vàn, Vàn Chảy và ngọn hải đăng Cô Tô lịch sử.',
      radius: 8000,
      temp: 22.2,
      humidity: 76,
      wind: 'Đông Bắc 5.8 m/s',
      wave: '1.0 m',
      aqi: 26,
      status: 'Tốt',
      provId: 'VN_QN'
    },
    {
      id: 'isl_conco',
      name: 'Huyện đảo Cồn Cỏ',
      group: 'Bắc Trung Bộ',
      admin: 'Huyện đảo Cồn Cỏ, Tỉnh Quảng Trị',
      lat: 17.159,
      lon: 107.337,
      desc: 'Đảo tiền tiêu anh hùng án ngữ eo biển miền Trung, đài vọng cảnh và khu bảo tồn sinh thái biển Cồn Cỏ.',
      radius: 5000,
      temp: 25.4,
      humidity: 83,
      wind: 'Đông Bắc 5.2 m/s',
      wave: '0.9 m',
      aqi: 21,
      status: 'Tốt',
      provId: 'VN_HUE'
    },
    {
      id: 'isl_culaocham',
      name: 'Cù Lao Chàm',
      group: 'Duyên hải Miền Trung',
      admin: 'Xã đảo Tân Hiệp, TP. Hội An, Tỉnh Quảng Nam',
      lat: 15.955,
      lon: 108.513,
      desc: 'Khu dự trữ sinh quyển thế giới UNESCO với 8 hòn đảo nhỏ, hệ sinh thái rạn san hô biển nguyên sơ tuyệt đẹp.',
      radius: 6000,
      temp: 26.8,
      humidity: 81,
      wind: 'Đông 4.5 m/s',
      wave: '0.8 m',
      aqi: 20,
      status: 'Tốt',
      provId: 'VN_QNA'
    }
  ],

  // Hàm chuẩn hóa tên đơn vị hành chính chính thống Việt Nam (có dấu đầy đủ)
  getOfficialAdminName(p) {
    if (!p) return '';
    const name = (p.name || p.province || '').trim();
    if (name.includes('Hà Nội')) return 'Thủ đô Hà Nội';
    if (name.includes('Hồ Chí Minh')) return 'Thành phố Hồ Chí Minh';
    if (name.includes('Đà Nẵng')) return 'Thành phố Đà Nẵng';
    if (name.includes('Hải Phòng')) return 'Thành phố Hải Phòng';
    if (name.includes('Cần Thơ')) return 'Thành phố Cần Thơ';
    if (name.startsWith('TP.')) return name.replace('TP.', 'Thành phố');
    if (!name.startsWith('Tỉnh') && !name.startsWith('Thành phố') && !name.startsWith('Thủ đô')) {
      return `Tỉnh ${name}`;
    }
    return name;
  },

  // Bật/tắt lớp nhãn đơn vị hành chính tiếng Việt có dấu
  toggleAdminLabels() {
    this.showAdminLabels = !this.showAdminLabels;
    const btn = document.getElementById('btn-toggle-admin-labels');
    if (btn) {
      btn.classList.toggle('active', this.showAdminLabels);
    }
    this.updateMapMarkers();
  },

  // Bật/tắt lớp hiển thị các quần đảo & đảo tiêu biểu Việt Nam
  toggleIslandsLayer() {
    this.showIslands = !this.showIslands;
    const btn = document.getElementById('btn-toggle-islands');
    if (btn) {
      btn.classList.toggle('active', this.showIslands);
    }
    this.updateMapMarkers();
  },

'''

target_init_map = "  initMap() {"
if "islandsData:" not in js_content and target_init_map in js_content:
    js_content = js_content.replace(target_init_map, islands_and_methods + target_init_map)
    print("Added islandsData and helper methods before initMap()")

# 3. Replace updateMapMarkers() with the comprehensive version
old_update_markers_start = "  updateMapMarkers() {"
# Find where updateMapMarkers ends (at the next method or end of loop)
# Let's locate the entire updateMapMarkers function
start_pos = js_content.find("  updateMapMarkers() {")
end_pos = js_content.find("  // -------------------------------------------------------------------------", start_pos)
if end_pos == -1:
    end_pos = js_content.find("  // =========================================================================", start_pos)

print("start_pos:", start_pos, "end_pos:", end_pos)
'''
'''
