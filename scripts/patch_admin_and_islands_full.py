import os
import sys

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

# 2. Define the complete islands data and helper methods
islands_code = '''  // =========================================================================
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

    // --- CÁC HẢI ĐẢO & HUYỆN ĐẢO TIỀN TIÊU VIỆT NAM ---
    {
      id: 'isl_phuquoc',
      name: 'Đảo Phú Quốc',
      group: 'Vùng biển Tây Nam',
      admin: 'Thành phố Phú Quốc, Tỉnh Kiên Giang',
      lat: 10.228,
      lon: 103.957,
      desc: 'Đảo lớn nhất Việt Nam, thành phố đảo đầu tiên với hệ sinh thái Vườn Quốc gia và du lịch biển đẳng cấp quốc tế.',
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
      desc: 'Huyện đảo tiền tiêu núi lửa cổ triệu năm, quê hương của Đội Hoàng Sa kiêm quản Trường Sa lừng danh.',
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

if "islandsData:" not in js_content:
    js_content = js_content.replace("  initMap() {", islands_code + "\n  initMap() {")
    print("Added islandsData and helper methods to js/app.js")

# 3. Replace updateMapMarkers() with the comprehensive, island-rich version
new_update_map_markers = '''  updateMapMarkers() {
    if (!this.map || typeof L === 'undefined') return;

    this.mapMarkers.forEach(m => this.map.removeLayer(m));
    this.mapMarkers = [];
    if (this.geoJsonDistrictsLayer) {
      this.map.removeLayer(this.geoJsonDistrictsLayer);
      this.geoJsonDistrictsLayer = null;
    }

    // 1. Lớp ranh giới hành chính GeoPandas
    if (this.mapLayer === 'geopandas') {
      this.renderGeoPandasLayer();
    }

    // 2. Lớp Quần đảo & Đảo Tiêu Biểu Việt Nam (Hiện rõ từng đảo có dấu)
    if (this.showIslands && this.islandsData) {
      this.islandsData.forEach(isl => {
        // Vòng thể hiện rạn san hô / phạm vi địa lý của đảo
        const reefCircle = L.circle([isl.lat, isl.lon], {
          radius: isl.radius || 8000,
          color: '#0284c7',
          weight: 1.5,
          opacity: 0.85,
          fillColor: '#38bdf8',
          fillOpacity: 0.22
        }).addTo(this.map);
        this.mapMarkers.push(reefCircle);

        const isMain = isl.isMainArchipelago;
        const islIcon = L.divIcon({
          className: 'island-pin-wrapper',
          html: `
            <div class="${isMain ? 'island-flag-pin' : 'island-item-pin'}" title="${isl.name} (${isl.admin})">
              <div class="${isMain ? 'flag-icon-circle' : 'island-icon-inner'}">
                <i class="fa-solid ${isMain ? 'fa-star' : 'fa-anchor'}"></i>
              </div>
            </div>
          `,
          iconSize: isMain ? [32, 32] : [24, 24],
          iconAnchor: isMain ? [16, 16] : [12, 12]
        });

        const islMarker = L.marker([isl.lat, isl.lon], { icon: islIcon, zIndexOffset: isMain ? 950 : 850 }).addTo(this.map);

        // Nhãn tiếng Việt có dấu cố định rõ ràng
        islMarker.bindTooltip(`<strong>${isl.name}</strong><br><small style="color:#fef08a;">${isl.admin}</small>`, {
          permanent: true,
          direction: 'top',
          className: isMain ? 'island-sovereignty-badge' : 'island-item-badge',
          offset: [0, isMain ? -14 : -10]
        });

        // Popup chi tiết
        islMarker.bindPopup(`
          <div style="font-family:'Plus Jakarta Sans',sans-serif;min-width:240px;line-height:1.5;">
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
              <i class="fa-solid fa-water" style="color:#0284c7;"></i>
              <h4 style="font-size:14px;font-weight:800;margin:0;color:#0f172a;">${isl.name}</h4>
            </div>
            <p style="font-size:11.5px;color:#475569;margin-bottom:8px;">
              <strong>Đơn vị hành chính:</strong> ${isl.admin}<br>
              <strong>Khu vực:</strong> ${isl.group} • <strong>Tọa độ:</strong> ${isl.lat}°B, ${isl.lon}°Đ<br>
              <em>${isl.desc}</em>
            </p>
            <div style="font-size:11.5px;background:#f8fafc;padding:8px;border-radius:6px;border:1px solid #e2e8f0;margin-bottom:8px;">
              <div><strong>Nhiệt độ biển:</strong> ${isl.temp}°C • <strong>Độ ẩm:</strong> ${isl.humidity}%</div>
              <div><strong>Gió biển:</strong> ${isl.wind} • <strong>Sóng biển:</strong> ${isl.wave}</div>
              <div><strong>Chất lượng không khí:</strong> AQI ${isl.aqi} (${isl.status})</div>
            </div>
            ${isl.provId ? `
            <button style="width:100%;padding:6px;background:#0284c7;color:#fff;border:none;border-radius:6px;font-weight:700;font-size:11.5px;cursor:pointer;" onclick="App.selectProvince('${isl.provId}'); App.switchTab('tab-overview');">
              Xem thời tiết ${isl.admin.split(',').pop().trim()}
            </button>
            ` : ''}
          </div>
        `);
        this.mapMarkers.push(islMarker);
      });
    }

    // 3. Điểm quan trắc 34 tỉnh thành Việt Nam & Nhãn hành chính tiếng Việt có dấu
    this.provinces.forEach(p => {
      let pinText = `${p.temp}°`;
      let pinColor = '#0284c7';

      if (this.mapLayer === 'aqi') {
        pinText = `${Math.round(p.pm25 * 1.8)}`;
        pinColor = p.color;
      } else if (this.mapLayer === 'rain') {
        pinText = `${p.rain_prob}%`;
        pinColor = p.rain_prob > 50 ? '#2563eb' : '#38bdf8';
      } else if (this.mapLayer === 'wind') {
        pinText = `${p.wind_speed}`;
        pinColor = '#0d9488';
      } else if (this.mapLayer === 'geopandas') {
        pinText = 'GIS';
        pinColor = '#0891b2';
      }

      const isCurrentProv = (p.id === this.selectedProvinceId);
      const customIcon = L.divIcon({
        className: 'custom-map-pin',
        html: `<div style="background:${pinColor};width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:12px;border:${isCurrentProv ? '3px solid #f59e0b' : '2px solid #fff'};box-shadow:${isCurrentProv ? '0 0 0 4px rgba(245,158,11,0.4), 0 3px 10px rgba(0,0,0,0.3)' : '0 3px 8px rgba(0,0,0,0.3)'};">${pinText}</div>`,
        iconSize: [36, 36],
        iconAnchor: [18, 18]
      });

      const marker = L.marker([p.lat, p.lon], { icon: customIcon }).addTo(this.map);

      // Hiển thị rõ tên đơn vị hành chính mới nhất tiếng Việt có dấu
      if (this.showAdminLabels) {
        const adminName = this.getOfficialAdminName(p);
        const isCapital = (p.id === 'VN_HN');
        marker.bindTooltip(`<strong>${adminName}</strong>`, {
          permanent: true,
          direction: 'bottom',
          className: isCapital ? 'admin-province-label admin-capital-label' : 'admin-province-label',
          offset: [0, 18]
        });
      }

      marker.bindPopup(`
        <div style="font-family:'Plus Jakarta Sans',sans-serif;min-width:190px;">
          <h4 style="font-size:14px;font-weight:800;margin-bottom:4px;color:#0f172a;">${this.getOfficialAdminName(p)}</h4>
          <p style="font-size:12px;color:#64748b;margin-bottom:8px;">${p.weather_text}</p>
          <div style="font-size:12px;display:flex;flex-direction:column;gap:3px;margin-bottom:10px;">
            <span><strong>Nhiệt độ:</strong> ${p.temp}°C (Cảm giác ${p.feels_like}°C)</span>
            <span><strong>Độ ẩm:</strong> ${p.humidity}% • <strong>Gió:</strong> ${p.wind_speed} m/s ${p.wind_dir}</span>
            <span><strong>Bụi mịn PM2.5:</strong> ${p.pm25} µg/m³ (AQI ${Math.round(p.pm25 * 1.8)})</span>
            <span><strong>Vùng địa lý:</strong> ${p.region}</span>
          </div>
          <button style="width:100%;padding:6px;background:#0284c7;color:#fff;border:none;border-radius:6px;font-weight:700;font-size:12px;cursor:pointer;" onclick="App.selectProvince('${p.id}'); App.switchTab('tab-overview');">
            Xem chi tiết địa phương
          </button>
        </div>
      `);
      this.mapMarkers.push(marker);
    });

    // 4. Hiển thị các trạm quan trắc chi tiết của tỉnh đang chọn
    const currProv = this.getSelectedProvince();
    const stations = this.getStationsForProvince(currProv.id);
    stations.forEach(s => {
      const sAqi = s.aqi || Math.round(s.pm25 * 1.8);
      const isSelected = (s.id === this.selectedStationId);
      const sIcon = L.divIcon({
        className: 'custom-station-pin',
        html: `<div style="background:${s.color || '#0d9488'};width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:10px;border:${isSelected ? '3px solid #f59e0b' : '2px solid #fff'};box-shadow:0 2px 6px rgba(0,0,0,0.4);">${sAqi}</div>`,
        iconSize: [26, 26],
        iconAnchor: [13, 13]
      });

      const sMarker = L.marker([s.lat, s.lon], { icon: sIcon }).addTo(this.map);
      sMarker.bindPopup(`
        <div style="font-family:'Plus Jakarta Sans',sans-serif;min-width:180px;">
          <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
            <i class="fa-solid fa-tower-broadcast" style="color:#0d9488;"></i>
            <h4 style="font-size:13px;font-weight:800;margin:0;color:#0f172a;">${s.name}</h4>
          </div>
          <span style="display:inline-block;padding:2px 6px;border-radius:4px;font-size:10px;font-weight:700;background:${s.color}20;color:${s.color};margin-bottom:6px;">${s.type}</span>
          <p style="font-size:11px;color:#64748b;margin-bottom:6px;">${s.address || currProv.name}</p>
          <div style="font-size:11px;display:flex;flex-direction:column;gap:2px;margin-bottom:8px;">
            <span><strong>AQI:</strong> ${sAqi} (${s.aqi_level || 'Trung bình'})</span>
            <span><strong>PM2.5:</strong> ${s.pm25} µg/m³ • <strong>Nhiệt độ:</strong> ${s.temp || currProv.temp}°C</span>
          </div>
          <button style="width:100%;padding:5px;background:#0d9488;color:#fff;border:none;border-radius:6px;font-weight:700;font-size:11px;cursor:pointer;" onclick="App.selectStation('${s.id}'); App.switchTab('tab-aiforecast');">
            Chọn trạm này & Dự báo AI
          </button>
        </div>
      `);
      this.mapMarkers.push(sMarker);
    });
  },'''

m_start = js_content.find("  updateMapMarkers() {")
m_end_anchor = "  // =========================================================================\n  // TAB 7: KHÁM PHÁ"
m_end = js_content.find(m_end_anchor)

if m_start != -1 and m_end != -1:
    js_content = js_content[:m_start] + new_update_map_markers + "\n\n" + js_content[m_end:]
    print("Successfully replaced updateMapMarkers in js/app.js")
else:
    print(f"Error: Could not locate bounds for updateMapMarkers (start: {m_start}, end: {m_end})")

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)
print("Saved js/app.js successfully!")

# 4. Update index.html to add toggle buttons
html_path = os.path.join(ROOT, "index.html")
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

old_toggles = """            <div class="map-layer-toggles">
              <button class="map-layer-btn active" onclick="App.setMapLayer('temp')">Nhiệt độ (°C)</button>
              <button class="map-layer-btn" onclick="App.setMapLayer('aqi')">Chất lượng không khí (AQI)</button>
              <button class="map-layer-btn" onclick="App.setMapLayer('rain')">Khả năng mưa (%)</button>
              <button class="map-layer-btn" onclick="App.setMapLayer('wind')">Tốc độ gió (m/s)</button>
              <button class="map-layer-btn" onclick="App.setMapLayer('geopandas')"><i class="fa-solid fa-draw-polygon"></i> Ranh giới GeoPandas</button>
            </div>"""

new_toggles = """            <div class="map-layer-toggles">
              <button class="map-layer-btn active" onclick="App.setMapLayer('temp')">Nhiệt độ (°C)</button>
              <button class="map-layer-btn" onclick="App.setMapLayer('aqi')">Chất lượng không khí (AQI)</button>
              <button class="map-layer-btn" onclick="App.setMapLayer('rain')">Khả năng mưa (%)</button>
              <button class="map-layer-btn" onclick="App.setMapLayer('wind')">Tốc độ gió (m/s)</button>
              <button class="map-layer-btn" onclick="App.setMapLayer('geopandas')"><i class="fa-solid fa-draw-polygon"></i> Ranh giới GeoPandas</button>
              <button class="map-layer-btn active" id="btn-toggle-admin-labels" onclick="App.toggleAdminLabels()"><i class="fa-solid fa-tags"></i> Tên Đơn Vị Hành Chính (Có Dấu)</button>
              <button class="map-layer-btn active" id="btn-toggle-islands" onclick="App.toggleIslandsLayer()"><i class="fa-solid fa-water"></i> Quần Đảo & Đảo Tiêu Biểu</button>
            </div>"""

if old_toggles in html_content:
    html_content = html_content.replace(old_toggles, new_toggles)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Updated index.html with island and admin layer toggle buttons!")
else:
    print("Warning: old_toggles not matched in index.html")

print("All patches completed successfully!")
