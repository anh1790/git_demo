import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
js_path = os.path.join(ROOT, "js", "app.js")

with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# 1. Add state variables to App object if not present
if "hourlyHorizon: 24" not in js_content:
    js_content = js_content.replace(
        "showIslands: true,",
        "showIslands: true,\n  hourlyHorizon: 24,\n  dailyHorizon: 7,\n  favorites: ['VN_HN', 'VN_DN', 'VN_HCM'],\n  aiChatOpen: false,"
    )
    print("Added state variables to App object")

# 2. Add full extension methods
methods_code = '''
  // =========================================================================
  // AIRSENSE AI EXTENSIONS: FAVORITES, GEOLOCATION, 48H/10D HORIZONS, ALERTS, AI CHAT
  // =========================================================================

  // --- QUẢN LÝ ĐỊA ĐIỂM: YÊU THÍCH (FAVORITES / BOOKMARKS) ---
  initFavorites() {
    try {
      const saved = localStorage.getItem('airsense_favorites');
      if (saved) {
        this.favorites = JSON.parse(saved);
      }
    } catch (e) {
      this.favorites = ['VN_HN', 'VN_DN', 'VN_HCM'];
    }
    this.renderFavoritesChips();
    this.updateFavoriteStar();
  },

  toggleFavoriteCurrentProvince() {
    const provId = this.selectedProvinceId;
    const p = this.getSelectedProvince();
    const idx = this.favorites.indexOf(provId);
    if (idx !== -1) {
      this.favorites.splice(idx, 1);
      this.showToast(`Đã bỏ ${p.name} khỏi danh sách yêu thích.`);
    } else {
      this.favorites.push(provId);
      this.showToast(`⭐ Đã lưu ${p.name} vào danh sách địa điểm yêu thích!`);
    }
    try {
      localStorage.setItem('airsense_favorites', JSON.stringify(this.favorites));
    } catch (e) {}
    this.renderFavoritesChips();
    this.updateFavoriteStar();
  },

  updateFavoriteStar() {
    const btn = document.getElementById('btn-toggle-favorite');
    if (!btn) return;
    const isFav = this.favorites.includes(this.selectedProvinceId);
    if (isFav) {
      btn.classList.add('active');
      btn.innerHTML = '<i class="fa-solid fa-star"></i>';
      btn.title = 'Đã lưu trong mục yêu thích (Nhấn để hủy)';
    } else {
      btn.classList.remove('active');
      btn.innerHTML = '<i class="fa-regular fa-star"></i>';
      btn.title = 'Lưu vào danh sách yêu thích';
    }
  },

  renderFavoritesChips() {
    const container = document.getElementById('favorites-chips-container');
    if (!container) return;
    if (!this.favorites || this.favorites.length === 0) {
      container.innerHTML = '<span style="font-size:11.5px;color:var(--text-muted);"><i class="fa-regular fa-star"></i> Chưa có địa điểm yêu thích. Nhấn ngôi sao để lưu tỉnh thành thường xem.</span>';
      return;
    }

    container.innerHTML = `
      <span style="font-size:11.5px;font-weight:700;color:var(--text-muted);"><i class="fa-solid fa-star" style="color:#f59e0b;"></i> Yêu thích:</span>
      ${this.favorites.map(id => {
        const p = this.provinces.find(item => item.id === id);
        if (!p) return '';
        const isActive = (p.id === this.selectedProvinceId);
        return `
          <div class="fav-chip ${isActive ? 'active' : ''}" onclick="App.selectProvince('${p.id}')">
            <span>${p.name}</span>
            <small style="opacity:0.8;">${p.temp}°</small>
            <span class="remove-fav" onclick="event.stopPropagation(); App.removeFavorite('${p.id}')" title="Xóa">×</span>
          </div>
        `;
      }).join('')}
    `;
  },

  removeFavorite(provId) {
    this.favorites = this.favorites.filter(id => id !== provId);
    try {
      localStorage.setItem('airsense_favorites', JSON.stringify(this.favorites));
    } catch (e) {}
    this.renderFavoritesChips();
    this.updateFavoriteStar();
  },

  // --- QUẢN LÝ ĐỊA ĐIỂM: ĐỊNH VỊ GPS (GEOLOCATION) ---
  locateUserGPS() {
    if (!navigator.geolocation) {
      this.showToast('Trình duyệt của bạn không hỗ trợ định vị GPS.');
      return;
    }
    this.showToast('Đang quét tọa độ GPS vị trí thực tế của bạn...');
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const userLat = pos.coords.latitude;
        const userLon = pos.coords.longitude;
        const nearest = this.findNearestProvince(userLat, userLon);
        if (nearest) {
          this.selectProvince(nearest.p.id);
          this.showToast(`📍 Đã định vị thành công: Bạn đang ở gần ${nearest.p.name} (cách ${nearest.distKm.toFixed(1)} km)!`);
        }
      },
      (err) => {
        console.warn('GPS location note:', err);
        this.showToast('Không thể lấy tọa độ GPS (vui lòng cấp quyền vị trí trong trình duyệt).');
      },
      { timeout: 10000, enableHighAccuracy: true }
    );
  },

  locateUserOnMap() {
    if (!navigator.geolocation) {
      this.showToast('Trình duyệt của bạn không hỗ trợ định vị GPS.');
      return;
    }
    if (!this.map) {
      this.switchTab('tab-map');
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const userLat = pos.coords.latitude;
        const userLon = pos.coords.longitude;
        const nearest = this.findNearestProvince(userLat, userLon);
        if (this.map) {
          this.map.flyTo([userLat, userLon], 10, { animate: true, duration: 1.5 });
          const userIcon = L.divIcon({
            className: 'user-gps-pin',
            html: `
              <div style="background:#0284c7;width:20px;height:20px;border-radius:50%;border:3px solid #fff;box-shadow:0 0 0 6px rgba(2,132,199,0.35);animation:pulseSovereignty 1.5s infinite;"></div>
            `,
            iconSize: [20, 20],
            iconAnchor: [10, 10]
          });
          const gpsMarker = L.marker([userLat, userLon], { icon: userIcon }).addTo(this.map);
          gpsMarker.bindPopup(`
            <div style="font-family:'Plus Jakarta Sans',sans-serif;min-width:180px;">
              <h4 style="margin:0 0 4px;color:#0284c7;"><i class="fa-solid fa-location-crosshairs"></i> Vị trí của bạn</h4>
              <p style="font-size:12px;color:#64748b;margin:0 0 6px;">Tọa độ: ${userLat.toFixed(4)}°B, ${userLon.toFixed(4)}°Đ</p>
              <p style="font-size:12px;margin:0 0 8px;">Gần nhất: <strong>${nearest.p.name}</strong> (cách ${nearest.distKm.toFixed(1)} km)</p>
              <button style="width:100%;padding:5px;background:#0284c7;color:#fff;border:none;border-radius:5px;font-size:11.5px;font-weight:700;cursor:pointer;" onclick="App.selectProvince('${nearest.p.id}'); App.switchTab('tab-overview');">
                Xem thời tiết ${nearest.p.name}
              </button>
            </div>
          `).openPopup();
          this.mapMarkers.push(gpsMarker);
        }
        if (nearest) {
          this.showToast(`📍 Vị trí bản đồ: Bạn đang gần ${nearest.p.name} (cách ${nearest.distKm.toFixed(1)} km)`);
        }
      },
      (err) => {
        this.showToast('Vui lòng bật quyền truy cập vị trí trên trình duyệt để định vị.');
      }
    );
  },

  findNearestProvince(lat, lon) {
    if (!this.provinces || this.provinces.length === 0) return null;
    let minD = Infinity;
    let closest = this.provinces[0];
    this.provinces.forEach(p => {
      const d = this.calculateHaversineDistance(lat, lon, p.lat, p.lon);
      if (d < minD) {
        minD = d;
        closest = p;
      }
    });
    return { p: closest, distKm: minD };
  },

  calculateHaversineDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  },

  // --- DỰ BÁO THEO GIỜ (24H - 48H) ---
  setHourlyHorizon(h) {
    this.hourlyHorizon = h;
    document.querySelectorAll('.horizon-toggle-group .horizon-btn').forEach(b => {
      if (b.id === `btn-hourly-${h}`) b.classList.add('active');
      else if (b.id && b.id.startsWith('btn-hourly-')) b.classList.remove('active');
    });
    this.renderHourlyForecast();
  },

  // --- DỰ BÁO NHIỀU NGÀY (7 - 10 NGÀY) ---
  setDailyHorizon(d) {
    this.dailyHorizon = d;
    document.querySelectorAll('.horizon-toggle-group .horizon-btn').forEach(b => {
      if (b.id === `btn-daily-${d}`) b.classList.add('active');
      else if (b.id && b.id.startsWith('btn-daily-')) b.classList.remove('active');
    });
    this.renderDailyForecast();
  },

  // --- TRUNG TÂM CẢNH BÁO THỜI TIẾT & Ô NHIỄM (8 CẤP ĐỘ THIÊN TAI) ---
  generateWeatherAlerts(p) {
    const alerts = [];
    if (!p) return alerts;

    // 1. Mưa lớn diện rộng
    if (p.rain_prob >= 70 || (p.weather_text && p.weather_text.toLowerCase().includes('mưa rào'))) {
      alerts.push({
        id: 'heavy_rain',
        level: p.rain_prob >= 80 ? 'emergency' : 'warning',
        tag: 'Mưa lớn',
        title: `Cảnh báo mưa lớn diện rộng tại ${p.name}`,
        desc: `Xác suất mưa ${p.rain_prob}%, nguy cơ mưa dồn dập cục bộ gây ngập úng các tuyến đường trũng.`,
        action: 'Hạn chế đi qua vùng ngập sâu, mang theo áo mưa và che chắn đồ đạc cẩn thận.'
      });
    }

    // 2. Giông sét, lốc xoáy
    if (p.condition === 'thunderstorm' || (p.weather_text && p.weather_text.toLowerCase().includes('dông'))) {
      alerts.push({
        id: 'thunderstorm',
        level: 'emergency',
        tag: 'Giông sét',
        title: `Cảnh báo giông sét và gió giật mạnh`,
        desc: `Hiện tượng đối lưu nhiệt mạnh tạo ra mây dông tích điện, nguy cơ có sét đánh và gió giật cục bộ.`,
        action: 'Tìm nơi trú ẩn kiên cố, ngắt điện các thiết bị ngoài trời, tránh xa gốc cây cao và cột điện.'
      });
    }

    // 3. Gió mạnh / Bão / Áp thấp nhiệt đới
    if (p.wind_speed >= 7.0 || (p.region === 'Miền Trung' && p.wind_speed >= 6.0)) {
      const isSevere = p.wind_speed >= 10.8;
      alerts.push({
        id: 'typhoon',
        level: isSevere ? 'emergency' : 'warning',
        tag: isSevere ? 'Bão / Áp thấp' : 'Gió mạnh',
        title: `Cảnh báo gió mạnh trên đất liền và vùng ven biển`,
        desc: `Tốc độ gió đo được ${p.wind_speed} m/s hướng ${p.wind_dir}, sóng biển tăng cao tại vùng ven bờ.`,
        action: 'Gia cố mái nhà, biển hiệu; tàu thuyền vào nơi tránh trú an toàn, tuân thủ hướng dẫn cứu hộ.'
      });
    }

    // 4. Nắng nóng gay gắt / Bức xạ UV cao
    if (p.temp >= 34.0 || p.uv_index >= 7) {
      alerts.push({
        id: 'heatwave',
        level: p.temp >= 36.0 || p.uv_index >= 9 ? 'emergency' : 'warning',
        tag: 'Nắng nóng & UV',
        title: `Cảnh báo nắng nóng gay gắt – Chỉ số UV mức nguy hại`,
        desc: `Nhiệt độ ${p.temp}°C, cảm giác thực tế ${p.feels_like}°C, chỉ số tia cực tím UV ${p.uv_index || 8}.`,
        action: 'Uống đủ nước, che chắn da cẩn thận khi ra ngoài, tránh hoạt động cường độ cao giữa trưa (11h-15h).'
      });
    }

    // 5. Rét đậm, rét hại (Vùng núi & mùa đông)
    if (p.temp <= 15.0) {
      alerts.push({
        id: 'coldwave',
        level: p.temp <= 11.0 ? 'emergency' : 'warning',
        tag: 'Rét đậm',
        title: `Cảnh báo không khí lạnh và rét buốt diện rộng`,
        desc: `Nhiệt độ giảm sâu còn ${p.temp}°C, độ ẩm cao gây cảm giác buốt giá, sương muối vùng núi.`,
        action: 'Mặc ấm nhiều lớp, giữ ấm cổ và ngực cho người già và trẻ nhỏ, che chắn chuồng trại chăn nuôi.'
      });
    }

    // 6. Ngập lụt đô thị / Triều cường
    const urbanCities = ['VN_HCM', 'VN_CT', 'VN_HP', 'VN_HN', 'VN_DN'];
    if (urbanCities.includes(p.id) && (p.rain_prob >= 60 || (p.weather_text && p.weather_text.toLowerCase().includes('mưa')))) {
      alerts.push({
        id: 'urban_flood',
        level: 'warning',
        tag: 'Ngập úng đô thị',
        title: `Nguy cơ ngập úng cục bộ và triều cường tại ${p.name}`,
        desc: `Lượng mưa tích tụ kết hợp khả năng thoát nước chậm vào giờ cao điểm tại các lưu vực trũng thấp.`,
        action: 'Chủ động điều chỉnh lộ trình di chuyển, không cố vượt qua các điểm ngập nước sâu quá trục bánh xe.'
      });
    }

    // 7. Ô nhiễm không khí nguy hại (AQI / Bụi PM2.5)
    if (p.pm25 >= 50.0 || (p.pm25 * 1.8) >= 120) {
      const aqi = Math.round(p.pm25 * 1.8);
      alerts.push({
        id: 'pollution',
        level: aqi >= 150 ? 'emergency' : 'warning',
        tag: 'Ô nhiễm không khí',
        title: `Cảnh báo chất lượng không khí mức ${p.aqi_level || 'Kém'} (AQI ${aqi})`,
        desc: `Nồng độ bụi mịn PM2.5 đạt ${p.pm25} µg/m³ (vượt ngưỡng an toàn QCVN 05:2023).`,
        action: 'Đeo khẩu trang chuẩn N95/KF94 khi ra đường, bật máy lọc không khí trong nhà, hạn chế tập thể dục ngoài trời.'
      });
    }

    // 8. Sương mù và suy giảm tầm nhìn
    if (p.humidity >= 88 && (p.condition.includes('fog') || p.condition.includes('cloud') || p.visibility <= 5.0)) {
      alerts.push({
        id: 'fog',
        level: 'warning',
        tag: 'Sương mù',
        title: `Cảnh báo sương mù dày đặc và tầm nhìn hạn chế`,
        desc: `Độ ẩm không khí đạt ${p.humidity}%, sương mù làm giảm tầm nhìn xa xuống dưới 5.0 km vào sáng sớm.`,
        action: 'Bật đèn sương mù hoặc đèn chiếu gần khi lái xe, giữ khoảng cách an toàn và giảm tốc độ.'
      });
    }

    return alerts;
  },

  renderWeatherAlerts() {
    const p = this.getSelectedProvince();
    const alerts = this.generateWeatherAlerts(p);

    // 1. Cập nhật Banner cảnh báo trên cùng
    const banner = document.getElementById('weather-alert-banner');
    if (banner) {
      if (alerts.length > 0) {
        const topAlert = alerts[0];
        const isEmerg = topAlert.level === 'emergency';
        banner.className = `weather-alert-banner ${isEmerg ? 'alert-emergency' : 'alert-warning'}`;
        banner.style.display = 'flex';
        banner.innerHTML = `
          <div style="display:flex;align-items:center;gap:10px;">
            <i class="fa-solid ${isEmerg ? 'fa-triangle-exclamation' : 'fa-circle-exclamation'}" style="font-size:18px;"></i>
            <div>
              <div style="font-weight:800;font-size:13px;display:flex;align-items:center;gap:6px;">
                <span class="alert-tag" style="background:${isEmerg ? '#ef4444' : '#f59e0b'};color:#fff;">${topAlert.tag}</span>
                <span>${topAlert.title}</span>
              </div>
              <div style="font-size:11.5px;margin-top:2px;">${topAlert.desc}</div>
            </div>
          </div>
          <button style="padding:6px 12px;background:${isEmerg ? '#ef4444' : '#f59e0b'};color:#fff;border:none;border-radius:6px;font-weight:700;font-size:11px;cursor:pointer;white-space:nowrap;" onclick="App.switchTab('tab-weather')">
            Xem khuyến nghị <i class="fa-solid fa-arrow-right"></i>
          </button>
        `;
      } else {
        banner.className = 'weather-alert-banner alert-info';
        banner.style.display = 'flex';
        banner.innerHTML = `
          <div style="display:flex;align-items:center;gap:8px;">
            <i class="fa-solid fa-circle-check" style="font-size:16px;"></i>
            <span style="font-size:12.5px;font-weight:600;">Thời tiết và chất lượng không khí tại <strong>${p.name}</strong> hiện ở mức an toàn, thuận lợi cho các hoạt động thường ngày.</span>
          </div>
          <span style="font-size:11px;font-weight:700;color:var(--text-muted);"><i class="fa-solid fa-shield-heart"></i> AirSense Giám Sát 24/7</span>
        `;
      }
    }

    // 2. Cập nhật Trung tâm Cảnh báo trong Tab 2
    const alertsContainer = document.getElementById('weather-alerts-list-container');
    const alertsCityTitle = document.getElementById('alerts-city-title');
    const alertsBadge = document.getElementById('alerts-status-badge');

    if (alertsCityTitle) alertsCityTitle.innerText = p.name;
    if (alertsBadge) {
      alertsBadge.innerText = alerts.length > 0 ? `${alerts.length} Cảnh Báo Hoạt Động` : 'Thời Tiết Ổn Định';
      alertsBadge.style.background = alerts.length > 0 ? '#fee2e2' : '#dcfce7';
      alertsBadge.style.color = alerts.length > 0 ? '#991b1b' : '#166534';
    }

    if (alertsContainer) {
      if (alerts.length === 0) {
        alertsContainer.innerHTML = `
          <div style="padding:14px;background:var(--body-bg);border-radius:8px;border-left:4px solid #10b981;display:flex;align-items:center;gap:12px;">
            <i class="fa-solid fa-circle-check" style="color:#10b981;font-size:22px;"></i>
            <div>
              <h4 style="margin:0 0 4px;font-size:13.5px;color:#0f172a;">Không có cảnh báo thời tiết hay ô nhiễm nguy hại</h4>
              <p style="margin:0;font-size:12px;color:#64748b;">Mọi chỉ số nhiệt độ, độ ẩm, gió và bụi mịn PM2.5 tại ${p.name} đều nằm trong giới hạn an toàn theo quy chuẩn QCVN 05:2023.</p>
            </div>
          </div>
        `;
      } else {
        alertsContainer.innerHTML = alerts.map(a => {
          const isEmerg = a.level === 'emergency';
          return `
            <div class="alert-item-card" style="border-left-color:${isEmerg ? '#ef4444' : '#f59e0b'};">
              <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:4px;">
                <div style="display:flex;align-items:center;gap:6px;">
                  <span class="alert-tag" style="background:${isEmerg ? '#ef4444' : '#f59e0b'};color:#fff;">${a.tag}</span>
                  <strong style="font-size:13.5px;color:#0f172a;">${a.title}</strong>
                </div>
                <span style="font-size:11px;font-weight:700;color:${isEmerg ? '#ef4444' : '#f59e0b'};text-transform:uppercase;">${isEmerg ? 'Khẩn cấp' : 'Cảnh báo'}</span>
              </div>
              <p style="font-size:12px;color:#475569;margin:4px 0 6px;">${a.desc}</p>
              <div style="font-size:11.5px;background:rgba(255,255,255,0.7);padding:6px 10px;border-radius:5px;border:1px solid var(--border-color);color:#0f172a;">
                <i class="fa-solid fa-lightbulb" style="color:#f59e0b;"></i> <strong>Khuyến nghị an toàn:</strong> ${a.action}
              </div>
            </div>
          `;
        }).join('');
      }
    }
  },

  // --- TRỢ LÝ AI HỎI ĐÁP THỜI TIẾT & CHẤT LƯỢNG KHÔNG KHÍ ---
  toggleAiChat() {
    this.aiChatOpen = !this.aiChatOpen;
    const win = document.getElementById('ai-chat-window');
    if (win) {
      win.style.display = this.aiChatOpen ? 'flex' : 'none';
      if (this.aiChatOpen) {
        const input = document.getElementById('ai-chat-input');
        if (input) setTimeout(() => input.focus(), 100);
      }
    }
  },

  askAiSuggestion(queryText) {
    const input = document.getElementById('ai-chat-input');
    if (input) {
      input.value = queryText;
      this.submitAiUserChat();
    }
  },

  submitAiUserChat() {
    const input = document.getElementById('ai-chat-input');
    const body = document.getElementById('ai-chat-body');
    if (!input || !body) return;

    const query = input.value.trim();
    if (!query) return;

    // Hiển thị tin nhắn người dùng
    const userMsg = document.createElement('div');
    userMsg.className = 'ai-chat-msg user';
    userMsg.innerText = query;
    body.appendChild(userMsg);
    input.value = '';

    // Tạo phản hồi từ Trợ lý AI AirSense
    const p = this.getSelectedProvince();
    const reply = this.generateAiAssistantAnswer(query, p);

    const botMsg = document.createElement('div');
    botMsg.className = 'ai-chat-msg bot';
    botMsg.innerHTML = reply;
    body.appendChild(botMsg);

    body.scrollTop = body.scrollHeight;
  },

  generateAiAssistantAnswer(query, p) {
    const q = query.toLowerCase();
    const aqi = Math.round(p.pm25 * 1.8);
    const temp = p.temp;
    const feels = p.feels_like;
    const pop = p.rain_prob;

    // Hỏi về chạy bộ, thể dục, ra ngoài
    if (q.includes('chạy bộ') || q.includes('thể dục') || q.includes('đi chơi') || q.includes('ra ngoài')) {
      if (aqi <= 50 && pop < 30) {
        return `✅ <strong>Rất lý tưởng!</strong> Tại <strong>${p.name}</strong>, thời tiết hiện tại ${temp}°C, xác suất mưa chỉ ${pop}% và chất lượng không khí đạt chuẩn <strong>Tốt (AQI ${aqi})</strong>. Đây là điều kiện hoàn hảo để chạy bộ, tập thể dục hoặc tham quan ngoài trời!`;
      } else if (aqi > 100) {
        return `⚠️ <strong>Nên cân nhắc:</strong> Nồng độ bụi mịn PM2.5 tại <strong>${p.name}</strong> đang ở mức <strong>${p.pm25} µg/m³ (AQI ${aqi} - ${p.aqi_level})</strong>. Bạn nên tập thể dục trong phòng kín hoặc chuyển sang khung giờ sáng sớm, đeo khẩu trang N95 nếu phải ra đường lâu.`;
      } else if (pop >= 60) {
        return `🌧️ <strong>Khả năng có mưa cao (${pop}%):</strong> Tại <strong>${p.name}</strong> trời có thể có mưa rào (${p.weather_text}). Nếu chạy bộ ngoài trời, bạn nên chọn công viên có mái che hoặc chạy trong phòng gym để tránh ướt.`;
      } else {
        return `🌤️ <strong>Tương đối thuận lợi:</strong> Thời tiết tại <strong>${p.name}</strong> là ${temp}°C, AQI ${aqi} (Mức ${p.aqi_level}). Bạn hoàn toàn có thể chạy bộ hoặc đi dạo, uống đủ nước và theo dõi thời tiết nếu trời đổi gió.`;
      }
    }

    // Hỏi về mưa, dự báo mưa 24h - 48h
    if (q.includes('mưa') || q.includes('24h') || q.includes('48h')) {
      return `🌧️ <strong>Dự báo mưa tại ${p.name}:</strong> Hiện tại xác suất mưa là <strong>${pop}%</strong> (${p.weather_text}). Trong 24h - 48h tới, mô hình học máy AI dự báo xu hướng thời tiết dao động từ ${temp - 2}°C đến ${temp + 3}°C. Bạn có thể mở <strong>Tab Thời Tiết Chi Tiết</strong> và chuyển nút <strong>[48 Giờ (AI)]</strong> để xem biểu đồ từng giờ liên tục!`;
    }

    // Hỏi về PM2.5, AQI, ô nhiễm
    if (q.includes('pm2.5') || q.includes('aqi') || q.includes('ô nhiễm') || q.includes('bụi')) {
      return `💨 <strong>Chỉ số chất lượng không khí tại ${p.name}:</strong><br>
      • <strong>Chỉ số AQI:</strong> ${aqi} (${p.aqi_level})<br>
      • <strong>Bụi mịn PM2.5:</strong> ${p.pm25} µg/m³ (Ngưỡng QCVN: 50 µg/m³)<br>
      • <strong>Bụi PM10:</strong> ${p.pm10 || Math.round(p.pm25 * 1.5)} µg/m³<br>
      • <strong>Khí độc hại:</strong> NO2 ${p.no2 || 28} µg/m³, CO ${p.co || 0.8} mg/m³, O3 ${p.o3 || 45} µg/m³.<br>
      Khuyến cáo: ${p.health_advice || 'Theo dõi chất lượng không khí khi tham gia giao thông giờ cao điểm.'}`;
    }

    // Hỏi về cảnh báo, bão, ngập lụt, nắng nóng
    if (q.includes('cảnh báo') || q.includes('bão') || q.includes('ngập') || q.includes('nắng') || q.includes('rét')) {
      const alerts = this.generateWeatherAlerts(p);
      if (alerts.length === 0) {
        return `🛡️ Hiện tại tại <strong>${p.name}</strong> <strong>không có cảnh báo thiên tai khẩn cấp nào</strong>. Mọi chỉ số khí tượng và nồng độ chất ô nhiễm đều trong ngưỡng kiểm soát an toàn.`;
      } else {
        const list = alerts.map(a => `• <strong>${a.tag}:</strong> ${a.title} (${a.action})`).join('<br>');
        return `⚠️ <strong>Đang có ${alerts.length} cảnh báo tại ${p.name}:</strong><br>${list}`;
      }
    }

    // Hỏi về nguyên nhân ô nhiễm / giải thích AI
    if (q.includes('nguyên nhân') || q.includes('tại sao') || q.includes('giải thích')) {
      return `🔬 <strong>Phân tích nguyên nhân từ AI SHAP:</strong><br>
      Theo phân tích độ quan trọng đặc trưng (Feature Importance), nồng độ bụi PM2.5 tại <strong>${p.name}</strong> chịu ảnh hưởng lớn nhất từ:<br>
      1. <strong>Tốc độ & Hướng gió (${p.wind_speed} m/s ${p.wind_dir}):</strong> Gió nhẹ khiến bụi tích tụ không thể khuếch tán.<br>
      2. <strong>Độ ẩm tương đối (${p.humidity}%):</strong> Độ ẩm cao kết hợp nghịch nhiệt làm tăng sol khí thứ cấp.<br>
      3. <strong>Mật độ giao thông & Đô thị hóa:</strong> Khí thải phương tiện trong các khung giờ cao điểm.<br>
      Bạn có thể xem ma trận giải thích chi tiết trong <strong>Tab Giải Thích & Tối Ưu ML</strong>.`;
    }

    // Mặc định trả lời tổng quát
    return `🤖 <strong>Tổng quan tại ${p.name}:</strong> Nhiệt độ <strong>${temp}°C</strong> (cảm giác ${feels}°C), độ ẩm <strong>${p.humidity}%</strong>, mưa <strong>${pop}%</strong>, gió <strong>${p.wind_speed} m/s</strong>, AQI <strong>${aqi} (${p.aqi_level})</strong>.<br>Bạn có câu hỏi cụ thể nào về hoạt động ngoài trời, dự báo mưa hay cảnh báo thiên tai không?`;
  },
'''

if "initFavorites()" not in js_content:
    insert_point = js_content.find("  initMap() {")
    if insert_point != -1:
        js_content = js_content[:insert_point] + methods_code + "\n" + js_content[insert_point:]
        print("Inserted extension methods before initMap()")

# 3. Update init() to call initFavorites() and renderWeatherAlerts()
old_init_render = "    this.renderAll();"
new_init_render = "    this.initFavorites();\n    this.renderAll();"

if old_init_render in js_content and "this.initFavorites();" not in js_content:
    js_content = js_content.replace(old_init_render, new_init_render, 1)
    print("Added initFavorites() call in App.init()")

# 4. Update renderAll() to call updateFavoriteStar() and renderWeatherAlerts()
old_render_all_end = "    this.renderOutdoorTab();\n  },"
new_render_all_end = """    this.renderOutdoorTab();
    this.updateFavoriteStar();
    this.renderWeatherAlerts();
  },"""

if old_render_all_end in js_content:
    js_content = js_content.replace(old_render_all_end, new_render_all_end)
    print("Updated renderAll() to refresh favorites and alerts")

# 5. Update renderWeatherDetailTab() to support 48h and 10d
old_weather_detail_start = "    const dailyContainer = document.getElementById('weather-detail-daily');\n    if (dailyContainer) {\n      const days = ['Chủ Nhật', 'Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7'];\n      const todayIdx = new Date().getDay();\n      let dailyHtml = '';\n\n      for (let i = 0; i < 7; i++) {"
new_weather_detail_start = """    const dailyContainer = document.getElementById('weather-detail-daily');
    if (dailyContainer) {
      const days = ['Chủ Nhật', 'Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7'];
      const todayIdx = new Date().getDay();
      let dailyHtml = '';
      const limitDays = this.dailyHorizon || 7;

      for (let i = 0; i < limitDays; i++) {"""

if old_weather_detail_start in js_content:
    js_content = js_content.replace(old_weather_detail_start, new_weather_detail_start)
    print("Updated daily forecast loop to support dailyHorizon")

# Also update hourly forecast loop to support hourlyHorizon (24 or 48)
old_hourly_loop = "if (p.hourly_forecast_24h && p.hourly_forecast_24h.length >= 24) {\n      for (let i = 0; i < 24; i++) {"
new_hourly_loop = """const limitHours = this.hourlyHorizon || 24;
    const hourlyData = (limitHours > 24 && p.hourly_forecast_48h) ? p.hourly_forecast_48h : (p.hourly_forecast_24h || []);
    if (hourlyData && hourlyData.length > 0) {
      const count = Math.min(limitHours, hourlyData.length);
      for (let i = 0; i < count; i++) {"""

if old_hourly_loop in js_content:
    js_content = js_content.replace(old_hourly_loop, new_hourly_loop)
    print("Updated hourly forecast loop to support hourlyHorizon")

# Update updateMapMarkers to support clouds layer
old_map_layers = """      } else if (this.mapLayer === 'wind') {
        pinText = `${p.wind_speed}`;
        pinColor = '#0d9488';
      } else if (this.mapLayer === 'geopandas') {
        pinText = 'GIS';
        pinColor = '#0891b2';
      }"""

new_map_layers = """      } else if (this.mapLayer === 'wind') {
        pinText = `${p.wind_speed}`;
        pinColor = '#0d9488';
      } else if (this.mapLayer === 'clouds') {
        const cloudVal = p.cloud_cover || (p.rain_prob > 60 ? 85 : (p.condition.includes('cloud') ? 65 : 25));
        pinText = `${cloudVal}%`;
        pinColor = '#475569';
      } else if (this.mapLayer === 'geopandas') {
        pinText = 'GIS';
        pinColor = '#0891b2';
      }"""

if old_map_layers in js_content:
    js_content = js_content.replace(old_map_layers, new_map_layers)
    print("Updated map layer handling for clouds")

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print("Saved js/app.js successfully!")
