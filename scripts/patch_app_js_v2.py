import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. State additions
old_state = """const App = {
  currentTab: 'tab-overview',
  provinces: [],
  selectedProvinceId: 'VN_HN',
  selectedStationId: null,
  selectedRegion: 'all',
  compareProvinceIds: ['VN_HN', 'VN_DN', 'VN_HCM'],
  compareHorizon: 'now',
  activeActivity: 'all',"""

new_state = """const App = {
  currentTab: 'tab-overview',
  provinces: [],
  selectedProvinceId: 'VN_HN',
  selectedStationId: null,
  selectedRegion: 'all',
  outdoorRegion: 'all',
  searchFilterProvId: null,
  timeScrubMode: 'now',
  compareProvinceIds: ['VN_HN', 'VN_DN', 'VN_HCM'],
  compareHorizon: 'now',
  activeActivity: 'all',"""

if old_state in code:
    code = code.replace(old_state, new_state)
    print("1. Patched state additions")

# 2. Add periodic day/night timer in init()
old_init = """    this.renderAll();
    
    // Auto-resize leaflet map on tab switch
    window.addEventListener('resize', () => {
      if (this.map && this.currentTab === 'tab-map') {
        this.map.invalidateSize();
      }
    });
  },"""

new_init = """    this.renderAll();
    
    // Auto-resize leaflet map on tab switch
    window.addEventListener('resize', () => {
      if (this.map && this.currentTab === 'tab-map') {
        this.map.invalidateSize();
      }
    });

    // Chu kỳ tự động kiểm tra giờ thực tế để cập nhật ngày/đêm và thời tiết
    setInterval(() => {
      if (this.timeScrubMode === 'now') {
        this.renderHeroWeather();
      }
    }, 30000);
  },"""

if old_init in code:
    code = code.replace(old_init, new_init)
    print("2. Patched init()")

# 3. Search and Single Province Isolation
old_search_start = """  // 5. Thanh tìm kiếm 34 tỉnh thành và 101 trạm đo với Auto-complete
  setupLocationSearch() {"""

old_search_end = """    document.addEventListener('click', (e) => {
      if (!input.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.style.display = 'none';
      }
    });
  },"""

pos1 = code.find(old_search_start)
if pos1 != -1:
    pos2 = code.find(old_search_end, pos1)
    if pos2 != -1:
        new_search_block = """  // 5. Thanh tìm kiếm 34 tỉnh thành và 101 trạm đo với Auto-complete & Cách ly 1 tỉnh duy nhất
  setupLocationSearch() {
    const input = document.getElementById('input-location-search');
    const dropdown = document.getElementById('search-results-dropdown');
    if (!input || !dropdown) return;

    input.addEventListener('input', (e) => {
      const q = e.target.value.trim().toLowerCase();
      if (!q) {
        dropdown.style.display = 'none';
        if (this.searchFilterProvId) {
          this.clearProvinceSearch();
        }
        return;
      }

      // Lọc danh sách tỉnh không bị lặp
      const provMatches = this.provinces.filter(p => 
        p.name.toLowerCase().includes(q) ||
        p.province.toLowerCase().includes(q) ||
        p.region.toLowerCase().includes(q)
      );

      // Tìm kiếm trạm đo chi tiết
      const stationMatches = [];
      this.provinces.forEach(p => {
        const sts = this.getStationsForProvince(p.id);
        sts.forEach(s => {
          if (s.name.toLowerCase().includes(q) || s.type.toLowerCase().includes(q) || (s.address && s.address.toLowerCase().includes(q))) {
            stationMatches.push({ ...s, parent_prov_id: p.id, parent_prov_name: p.name });
          }
        });
      });

      if (provMatches.length === 0 && stationMatches.length === 0) {
        dropdown.innerHTML = '<div style="padding:12px;color:var(--text-muted);font-size:13px;text-align:center;">Không tìm thấy địa phương hoặc trạm quan trắc phù hợp</div>';
        dropdown.style.display = 'block';
        return;
      }

      let html = '';
      if (provMatches.length > 0) {
        html += '<div style="padding:6px 12px;font-size:11px;font-weight:800;color:var(--primary);background:var(--body-bg);">TỈNH / THÀNH PHỐ</div>';
        html += provMatches.slice(0, 5).map(p => `
          <div class="search-result-item" onclick="App.selectProvinceFromSearch('${p.id}');">
            <div>
              <div class="item-title"><i class="fa-solid fa-location-dot" style="color:var(--primary);font-size:12px;"></i> ${p.name}</div>
              <div class="item-sub">${p.type} • ${p.region} • ${p.weather_text}</div>
            </div>
            <span class="stat-badge" style="background:${p.color}20; color:${p.color};">${p.temp}°C • AQI ${Math.round(p.pm25 * 1.8)}</span>
          </div>
        `).join('');
      }

      if (stationMatches.length > 0) {
        html += '<div style="padding:6px 12px;font-size:11px;font-weight:800;color:var(--accent-teal);background:var(--body-bg);border-top:1px solid var(--border-color);">TRẠM QUAN TRẮC CHI TIẾT</div>';
        html += stationMatches.slice(0, 5).map(s => `
          <div class="search-result-item" onclick="App.selectProvinceFromSearch('${s.parent_prov_id}'); App.selectStation('${s.id}');">
            <div>
              <div class="item-title"><i class="fa-solid fa-tower-broadcast" style="color:var(--accent-teal);font-size:12px;"></i> ${s.name}</div>
              <div class="item-sub">${s.parent_prov_name} • ${s.type}</div>
            </div>
            <span class="stat-badge" style="background:${s.color}20; color:${s.color};">PM2.5: ${s.pm25} • AQI ${s.aqi}</span>
          </div>
        `).join('');
      }

      dropdown.innerHTML = html;
      dropdown.style.display = 'block';
    });

    // Bấm Enter: Chọn ngay tỉnh phù hợp nhất và hiển thị duy nhất tỉnh đó
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        const q = input.value.trim().toLowerCase();
        if (!q) return;
        const match = this.provinces.find(p => p.name.toLowerCase().includes(q) || p.province.toLowerCase().includes(q)) || this.provinces[0];
        if (match) {
          this.selectProvinceFromSearch(match.id);
        }
      }
    });

    document.addEventListener('click', (e) => {
      if (!input.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.style.display = 'none';
      }
    });
  },

  selectProvinceFromSearch(provId) {
    const p = this.getProvinceById(provId);
    if (!p) return;
    this.searchFilterProvId = provId;
    const input = document.getElementById('input-location-search');
    const dropdown = document.getElementById('search-results-dropdown');
    if (input) input.value = p.name;
    if (dropdown) dropdown.style.display = 'none';

    // Hiển thị DUY NHẤT 1 tỉnh tại thanh địa phương
    this.renderSingleProvincePill(p);
    this.selectProvince(provId);
  },

  renderSingleProvincePill(p) {
    const container = document.getElementById('province-pills-container');
    if (!container) return;
    container.innerHTML = `
      <span class="pills-label"><i class="fa-solid fa-magnifying-glass" style="color:var(--primary);"></i> Kết quả tìm kiếm (1 tỉnh duy nhất):</span>
      <button class="district-pill active" onclick="App.selectProvince('${p.id}')">
        <i class="fa-solid fa-location-dot" style="color:var(--accent-teal);"></i> ${p.name}
      </button>
      <button class="district-pill btn-clear-search" onclick="App.clearProvinceSearch()">
        <i class="fa-solid fa-xmark"></i> Hiện tất cả 34 tỉnh
      </button>
    `;
  },

  clearProvinceSearch() {
    this.searchFilterProvId = null;
    const input = document.getElementById('input-location-search');
    if (input) input.value = '';
    const dropdown = document.getElementById('search-results-dropdown');
    if (dropdown) dropdown.style.display = 'none';
    this.filterByRegion(this.selectedRegion || 'all');
  },"""
        code = code[:pos1] + new_search_block + code[pos2 + len(old_search_end):]
        print("3. Patched setupLocationSearch & single province search")

# 4. Update filterByRegion to reset search filter
old_filter_reg = """  filterByRegion(region) {
    this.selectedRegion = region;"""

new_filter_reg = """  filterByRegion(region) {
    this.selectedRegion = region;
    this.searchFilterProvId = null;"""

if old_filter_reg in code:
    code = code.replace(old_filter_reg, new_filter_reg, 1)
    print("4. Patched filterByRegion")

# 5. Full sync in selectProvince(provId)
old_select_prov = """  selectProvince(provId) {
    this.selectedProvinceId = provId;
    this.selectedStationId = null;

    const select = document.getElementById('select-province-dropdown');
    if (select) select.value = provId;

    document.querySelectorAll('#province-pills-container .district-pill').forEach(btn => {
      const p = this.getProvinceById(provId);
      if (p && btn.innerText.trim() === p.name.trim()) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    this.renderStationPills();
    this.renderAll();
    this.showToast(`Đã chuyển sang theo dõi: ${this.getSelectedProvince().name}`);
  },"""

new_select_prov = """  selectProvince(provId) {
    this.selectedProvinceId = provId;
    this.selectedStationId = null;

    const select = document.getElementById('select-province-dropdown');
    if (select) select.value = provId;

    // Cập nhật trạng thái active của nút tỉnh
    document.querySelectorAll('#province-pills-container .district-pill').forEach(btn => {
      const p = this.getProvinceById(provId);
      if (p && btn.innerText.includes(p.name)) {
        btn.classList.add('active');
      } else if (!btn.classList.contains('btn-clear-search')) {
        btn.classList.remove('active');
      }
    });

    // Đồng bộ vào mảng so sánh tỉnh nếu chưa có (đưa lên đầu)
    if (!this.compareProvinceIds.includes(provId)) {
      this.compareProvinceIds.unshift(provId);
      if (this.compareProvinceIds.length > 5) {
        this.compareProvinceIds.pop();
      }
    }

    this.renderStationPills();
    this.renderAll();

    // Đồng bộ bản đồ: bay tới tọa độ tỉnh đã chọn
    if (this.map) {
      const p = this.getSelectedProvince();
      if (p && p.lat && p.lon) {
        this.map.flyTo([p.lat, p.lon], 9, { duration: 0.8 });
      }
    }

    this.showToast(`Đã chuyển sang theo dõi: ${this.getSelectedProvince().name}`);
  },"""

if old_select_prov in code:
    code = code.replace(old_select_prov, new_select_prov)
    print("5. Patched selectProvince for complete tab synchronization")

# 6. Update renderAll() so all tabs are kept in sync
old_render_all = """  renderAll() {
    this.renderHeroWeather();
    this.renderStatCards();
    this.renderOverviewLeaderboards();
    this.renderOverviewHourly();
    this.renderOverviewOutdoorPreview();
    this.renderWeatherDetailTab();
    if (this.currentTab === 'tab-compare') this.renderCompareTab();
    if (this.currentTab === 'tab-airquality') this.renderAirQualityTab();
    if (this.currentTab === 'tab-aiforecast') this.renderForecastTab();
    if (this.currentTab === 'tab-outdoor') this.renderOutdoorTab();
    if (this.map && this.currentTab === 'tab-map') this.updateMapMarkers();
  },"""

new_render_all = """  renderAll() {
    this.renderHeroWeather();
    this.renderStatCards();
    this.renderOverviewLeaderboards();
    this.renderOverviewHourly();
    this.renderOverviewOutdoorPreview();
    this.renderWeatherDetailTab();
    this.renderCompareTab();
    this.renderAirQualityTab();
    this.renderForecastTab();
    this.renderOutdoorTab();
    if (this.map) this.updateMapMarkers();
  },"""

if old_render_all in code:
    code = code.replace(old_render_all, new_render_all)
    print("6. Patched renderAll()")

# 7. Day / Night & Weather auto calculation
old_hero_fn_start = """  renderHeroWeather(overrideCondition = null) {"""
old_hero_fn_end = """  scrubTimeOfDay(period) {
    document.querySelectorAll('.time-scrub-btn').forEach(btn => btn.classList.remove('active'));
    event.currentTarget.classList.add('active');

    if (period === 'now') {
      this.renderHeroWeather();
    } else if (period === 'noon') {
      this.renderHeroWeather('sunny');
    } else if (period === 'sunset') {
      this.renderHeroWeather('sunset');
    } else if (period === 'night') {
      this.renderHeroWeather('night');
    }
  },"""

pos3 = code.find(old_hero_fn_start)
if pos3 != -1:
    pos4 = code.find(old_hero_fn_end, pos3)
    if pos4 != -1:
        new_hero_block = """  getEffectiveWeatherCondition(baseCondition) {
    if (this.timeScrubMode && this.timeScrubMode !== 'now') {
      return this.timeScrubMode;
    }

    // Tự động nhận diện chu kỳ Ngày / Hoàng hôn / Đêm theo ngày giờ thực tế của hệ thống
    const now = new Date();
    const hr = now.getHours();
    const min = now.getMinutes();

    // 06:00 - 16:59: Ban ngày (Day)
    // 17:00 - 18:29: Hoàng hôn (Sunset / Dusk)
    // 18:30 - 05:59: Ban đêm (Night)
    const isNight = (hr >= 18 && min >= 30) || (hr > 18) || (hr < 6);
    const isSunset = (hr === 17) || (hr === 18 && min < 30);

    const cond = baseCondition || 'sunny';

    if (isNight) {
      if (cond === 'thunderstorm') return 'night_thunderstorm';
      if (cond === 'heavy_rain' || cond === 'light_rain') return 'night_rain';
      if (cond === 'foggy') return 'night_foggy';
      return 'night';
    } else if (isSunset) {
      if (cond === 'heavy_rain' || cond === 'light_rain') return 'sunset_rain';
      if (cond === 'thunderstorm') return 'thunderstorm';
      return 'sunset';
    } else {
      return cond;
    }
  },

  renderHeroWeather() {
    const p = this.getSelectedProvince();
    if (!p || !p.id) return;
    const st = this.getSelectedStation();
    const activeTemp = (st && st.temp != null) ? st.temp : p.temp;
    const activePm25 = (st && st.pm25 != null) ? st.pm25 : p.pm25;
    const activeAqi = (st && st.aqi != null) ? st.aqi : Math.round(activePm25 * 1.8);
    const activeAqiLevel = (st && st.aqi_level) ? st.aqi_level : p.aqi_level;

    const condition = this.getEffectiveWeatherCondition(p.condition);
    const heroCard = document.getElementById('dynamic-weather-hero');
    if (!heroCard) return;

    heroCard.className = 'weather-stage';
    heroCard.classList.add(`weather-${condition.replace('_', '-')}`);

    const sunEl = document.getElementById('hero-sun');
    const cloud1 = document.getElementById('hero-cloud-1');
    const cloud2 = document.getElementById('hero-cloud-2');
    const rainStream = document.getElementById('hero-rain-stream');
    const lightning = document.getElementById('hero-lightning-flash');
    const fogLayer = document.getElementById('hero-fog-layer');
    const moonEl = document.getElementById('hero-moon');
    const starField = document.getElementById('hero-star-field');

    if (sunEl) sunEl.style.display = 'none';
    if (cloud1) cloud1.style.display = 'none';
    if (cloud2) cloud2.style.display = 'none';
    if (rainStream) rainStream.style.display = 'none';
    if (lightning) lightning.style.display = 'none';
    if (fogLayer) fogLayer.style.display = 'none';
    if (moonEl) moonEl.style.display = 'none';
    if (starField) starField.style.display = 'none';

    if (condition === 'sunny') {
      if (sunEl) { sunEl.style.display = 'block'; sunEl.style.background = 'radial-gradient(circle, #fef08a 20%, #f59e0b 80%)'; }
    } else if (condition === 'partly_cloudy') {
      if (sunEl) { sunEl.style.display = 'block'; sunEl.style.background = 'radial-gradient(circle, #fef08a 20%, #f59e0b 80%)'; }
      if (cloud1) cloud1.style.display = 'block';
    } else if (condition === 'cloudy' || condition === 'overcast') {
      if (cloud1) cloud1.style.display = 'block';
      if (cloud2) cloud2.style.display = 'block';
    } else if (condition === 'light_rain') {
      if (cloud1) cloud1.style.display = 'block';
      if (rainStream) rainStream.style.display = 'block';
    } else if (condition === 'heavy_rain') {
      if (cloud1) cloud1.style.display = 'block';
      if (cloud2) cloud2.style.display = 'block';
      if (rainStream) rainStream.style.display = 'block';
    } else if (condition === 'thunderstorm') {
      if (cloud1) cloud1.style.display = 'block';
      if (cloud2) cloud2.style.display = 'block';
      if (rainStream) rainStream.style.display = 'block';
      if (lightning) lightning.style.display = 'block';
    } else if (condition === 'foggy') {
      if (fogLayer) fogLayer.style.display = 'block';
      if (cloud1) cloud1.style.display = 'block';
    } else if (condition === 'night') {
      if (moonEl) moonEl.style.display = 'block';
      if (starField) starField.style.display = 'block';
    } else if (condition === 'night_rain') {
      if (moonEl) moonEl.style.display = 'block';
      if (starField) starField.style.display = 'block';
      if (cloud1) cloud1.style.display = 'block';
      if (rainStream) rainStream.style.display = 'block';
    } else if (condition === 'night_thunderstorm') {
      if (starField) starField.style.display = 'block';
      if (cloud1) cloud1.style.display = 'block';
      if (cloud2) cloud2.style.display = 'block';
      if (rainStream) rainStream.style.display = 'block';
      if (lightning) lightning.style.display = 'block';
    } else if (condition === 'night_foggy') {
      if (fogLayer) fogLayer.style.display = 'block';
      if (moonEl) moonEl.style.display = 'block';
    } else if (condition === 'sunset') {
      if (sunEl) {
        sunEl.style.display = 'block';
        sunEl.style.background = 'radial-gradient(circle, #fde047 20%, #ea580c 80%)';
      }
      if (cloud1) cloud1.style.display = 'block';
    } else if (condition === 'sunset_rain') {
      if (sunEl) {
        sunEl.style.display = 'block';
        sunEl.style.background = 'radial-gradient(circle, #fde047 20%, #ea580c 80%)';
      }
      if (cloud1) cloud1.style.display = 'block';
      if (rainStream) rainStream.style.display = 'block';
    }

    const aqi = Math.round(activePm25 * 1.8);
    const condIcon = this.getConditionIcon(condition);

    // Đồng hồ thời gian thực tế
    const now = new Date();
    const hr = now.getHours();
    const timeStr = `${String(hr).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    const periodLabel = (hr >= 18 || hr < 6) ? 'Ban đêm' : (hr >= 17 ? 'Hoàng hôn' : 'Ban ngày');

    document.getElementById('hero-location-name').innerHTML = `<i class="fa-solid fa-location-dot"></i> ${p.name} • ${p.type}`;
    document.getElementById('hero-cond-badge').innerHTML = `${condIcon} ${p.weather_text} <span style="opacity:0.85;font-size:11px;margin-left:4px;">(${timeStr} • ${periodLabel})</span>`;
    document.getElementById('hero-temp-val').innerText = `${activeTemp}°`;
    document.getElementById('hero-feels-val').innerText = `Cảm giác như ${Math.round((activeTemp + 1.2)*10)/10}°C`;
    document.getElementById('hero-summary-text').innerText = `Thời tiết tại ${p.name}: ${p.weather_text}. ${p.outdoor_advice}`;
    document.getElementById('hero-hum-val').innerText = `${p.humidity}%`;
    document.getElementById('hero-wind-val').innerText = `${p.wind_speed} m/s ${p.wind_dir}`;
    document.getElementById('hero-rain-val').innerText = `${p.rain_prob}% (${p.rain_mm}mm)`;
    document.getElementById('hero-uv-val').innerText = `${p.uv} (${this.getUvText(p.uv)})`;
    document.getElementById('hero-aqi-val').innerText = `${aqi} (${activeAqiLevel})`;
  },

  scrubTimeOfDay(period) {
    this.timeScrubMode = period;
    document.querySelectorAll('.time-scrub-btn').forEach(btn => btn.classList.remove('active'));
    if (typeof event !== 'undefined' && event && event.currentTarget) {
      event.currentTarget.classList.add('active');
    } else {
      const btn = document.getElementById(`btn-scrub-${period}`);
      if (btn) btn.classList.add('active');
    }

    this.renderHeroWeather();
  },"""
        code = code[:pos3] + new_hero_block + code[pos4 + len(old_hero_fn_end):]
        print("7. Patched Hero weather auto day/night cycle")

# 8. Leaflet Map Hoàng Sa & Trường Sa sovereignty
old_map_start = """  // =========================================================================
  // TAB 6: BẢN ĐỒ THỜI TIẾT TƯƠNG TÁC (LEAFLET 34 PROVINCES)
  // =========================================================================
  initMap() {"""

old_map_end = """      this.mapMarkers.push(sMarker);
    });
  },"""

pos5 = code.find(old_map_start)
if pos5 != -1:
    pos6 = code.find(old_map_end, pos5)
    if pos6 != -1:
        new_map_block = """  // =========================================================================
  // TAB 6: BẢN ĐỒ THỜI TIẾT TƯƠNG TÁC (LEAFLET 34 PROVINCES & HOÀNG SA, TRƯỜNG SA)
  // =========================================================================
  initMap() {
    const mapContainer = document.getElementById('weather-leaflet-map');
    if (!mapContainer || typeof L === 'undefined') return;

    if (!this.map) {
      // Khởi tạo bản đồ bao trọn vẹn lãnh thổ Việt Nam, Hoàng Sa & Trường Sa
      this.map = L.map('weather-leaflet-map').setView([15.5, 108.5], 6);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors | Bản đồ Khí tượng Việt Nam'
      }).addTo(this.map);

      // Thêm bảng khẳng định chủ quyền Hoàng Sa & Trường Sa vĩnh viễn ở góc bản đồ
      const SovereigntyControl = L.Control.extend({
        options: { position: 'bottomleft' },
        onAdd: function() {
          const div = L.DomUtil.create('div', 'map-sovereignty-box');
          div.innerHTML = `
            <div style="font-weight:800;color:#dc2626;margin-bottom:3px;display:flex;align-items:center;gap:6px;">
              <i class="fa-solid fa-flag"></i> CHỦ QUYỀN BIỂN ĐẢO VIỆT NAM
            </div>
            <div>Khẳng định chủ quyền toàn vẹn lãnh thổ đối với <strong>Quần đảo Hoàng Sa</strong> (TP. Đà Nẵng) và <strong>Quần đảo Trường Sa</strong> (Tỉnh Khánh Hòa).</div>
          `;
          return div;
        }
      });
      new SovereigntyControl().addTo(this.map);
    }

    this.map.invalidateSize();
    this.updateMapMarkers();
  },

  setMapLayer(layerType) {
    this.mapLayer = layerType;
    document.querySelectorAll('.map-layer-btn').forEach(btn => btn.classList.remove('active'));
    if (typeof event !== 'undefined' && event && event.currentTarget) {
      event.currentTarget.classList.add('active');
    }
    this.updateMapMarkers();
  },

  updateMapMarkers() {
    if (!this.map || typeof L === 'undefined') return;

    this.mapMarkers.forEach(m => this.map.removeLayer(m));
    this.mapMarkers = [];

    // 1. Nhãn Biển Đông Việt Nam
    const seaMarker = L.marker([12.8, 113.8], {
      icon: L.divIcon({
        className: 'sea-label-div',
        html: '<div class="sea-label-badge">BIỂN ĐÔNG (VIỆT NAM)</div>',
        iconSize: [240, 30],
        iconAnchor: [120, 15]
      }),
      interactive: false
    }).addTo(this.map);
    this.mapMarkers.push(seaMarker);

    // 2. Marker & Tooltip Chủ quyền Quần đảo Hoàng Sa (TP. Đà Nẵng, Việt Nam)
    const hsIcon = L.divIcon({
      className: 'island-flag-pin',
      html: `
        <div class="island-flag-pin" title="Quần đảo Hoàng Sa (TP. Đà Nẵng, Việt Nam)">
          <div class="flag-icon-circle"><i class="fa-solid fa-star"></i></div>
        </div>
      `,
      iconSize: [34, 34],
      iconAnchor: [17, 17]
    });
    const hsMarker = L.marker([16.536, 112.025], { icon: hsIcon, zIndexOffset: 1000 }).addTo(this.map);
    hsMarker.bindTooltip('🇻🇳 <strong>QUẦN ĐẢO HOÀNG SA</strong><br><small style="color:#fef08a;">(TP. Đà Nẵng, Việt Nam)</small>', {
      permanent: true,
      direction: 'top',
      className: 'island-sovereignty-badge',
      offset: [0, -12]
    });
    hsMarker.bindPopup(`
      <div style="font-family:'Plus Jakarta Sans',sans-serif;min-width:240px;line-height:1.5;">
        <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
          <span style="font-size:16px;">🇻🇳</span>
          <h4 style="font-size:14px;font-weight:800;margin:0;color:#dc2626;">QUẦN ĐẢO HOÀNG SA</h4>
        </div>
        <p style="font-size:11.5px;color:#475569;margin-bottom:8px;">
          <strong>Đơn vị hành chính:</strong> Huyện Hoàng Sa, Thành phố Đà Nẵng, Việt Nam<br>
          <strong>Cơ sở quan trắc:</strong> Trạm Khí tượng Hải văn Hoàng Sa
        </p>
        <div style="font-size:11.5px;background:#f8fafc;padding:8px;border-radius:6px;border:1px solid #e2e8f0;margin-bottom:8px;">
          <div><strong>Nhiệt độ biển:</strong> 28.5°C • <strong>Độ ẩm:</strong> 82%</div>
          <div><strong>Gió:</strong> Đông Bắc 6.5 m/s (Cấp 4) • <strong>Sóng:</strong> 1.2 m</div>
          <div><strong>Chất lượng không khí:</strong> AQI 18 (Rất trong lành)</div>
        </div>
        <div style="font-size:11px;color:#15803d;font-weight:700;margin-bottom:10px;">
          <i class="fa-solid fa-shield-halved"></i> Lãnh thổ thiêng liêng không thể tách rời của Việt Nam
        </div>
        <button style="width:100%;padding:6px;background:#0284c7;color:#fff;border:none;border-radius:6px;font-weight:700;font-size:11.5px;cursor:pointer;" onclick="App.selectProvince('VN_DN'); App.switchTab('tab-overview');">
          Xem thời tiết TP. Đà Nẵng
        </button>
      </div>
    `);
    this.mapMarkers.push(hsMarker);

    // 3. Marker & Tooltip Chủ quyền Quần đảo Trường Sa (Tỉnh Khánh Hòa, Việt Nam)
    const tsIcon = L.divIcon({
      className: 'island-flag-pin',
      html: `
        <div class="island-flag-pin" title="Quần đảo Trường Sa (Tỉnh Khánh Hòa, Việt Nam)">
          <div class="flag-icon-circle"><i class="fa-solid fa-star"></i></div>
        </div>
      `,
      iconSize: [34, 34],
      iconAnchor: [17, 17]
    });
    const tsMarker = L.marker([8.647, 111.919], { icon: tsIcon, zIndexOffset: 1000 }).addTo(this.map);
    tsMarker.bindTooltip('🇻🇳 <strong>QUẦN ĐẢO TRƯỜNG SA</strong><br><small style="color:#fef08a;">(Tỉnh Khánh Hòa, Việt Nam)</small>', {
      permanent: true,
      direction: 'top',
      className: 'island-sovereignty-badge',
      offset: [0, -12]
    });
    tsMarker.bindPopup(`
      <div style="font-family:'Plus Jakarta Sans',sans-serif;min-width:240px;line-height:1.5;">
        <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
          <span style="font-size:16px;">🇻🇳</span>
          <h4 style="font-size:14px;font-weight:800;margin:0;color:#dc2626;">QUẦN ĐẢO TRƯỜNG SA</h4>
        </div>
        <p style="font-size:11.5px;color:#475569;margin-bottom:8px;">
          <strong>Đơn vị hành chính:</strong> Huyện Trường Sa, Tỉnh Khánh Hòa, Việt Nam<br>
          <strong>Cơ sở quan trắc:</strong> Trạm Khí tượng Hải văn Đảo Trường Sa Lớn
        </p>
        <div style="font-size:11.5px;background:#f8fafc;padding:8px;border-radius:6px;border:1px solid #e2e8f0;margin-bottom:8px;">
          <div><strong>Nhiệt độ biển:</strong> 29.2°C • <strong>Độ ẩm:</strong> 85%</div>
          <div><strong>Gió:</strong> Đông Nam 5.2 m/s (Cấp 3) • <strong>Sóng:</strong> 1.0 m</div>
          <div><strong>Chất lượng không khí:</strong> AQI 15 (Tuyệt hảo)</div>
        </div>
        <div style="font-size:11px;color:#15803d;font-weight:700;margin-bottom:10px;">
          <i class="fa-solid fa-shield-halved"></i> Chủ quyền toàn vẹn và bất khả xâm phạm của Việt Nam
        </div>
        <button style="width:100%;padding:6px;background:#0284c7;color:#fff;border:none;border-radius:6px;font-weight:700;font-size:11.5px;cursor:pointer;" onclick="App.selectProvince('VN_KH'); App.switchTab('tab-overview');">
          Xem thời tiết Tỉnh Khánh Hòa
        </button>
      </div>
    `);
    this.mapMarkers.push(tsMarker);

    // 4. Các marker 34 tỉnh thành
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
      }

      const isCurrentProv = (p.id === this.selectedProvinceId);
      const customIcon = L.divIcon({
        className: 'custom-map-pin',
        html: `<div style="background:${pinColor};width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:12px;border:${isCurrentProv ? '3px solid #f59e0b' : '2px solid #fff'};box-shadow:${isCurrentProv ? '0 0 0 4px rgba(245,158,11,0.4), 0 3px 10px rgba(0,0,0,0.3)' : '0 3px 8px rgba(0,0,0,0.3)'};">${pinText}</div>`,
        iconSize: [36, 36],
        iconAnchor: [18, 18]
      });

      const marker = L.marker([p.lat, p.lon], { icon: customIcon }).addTo(this.map);
      marker.bindPopup(`
        <div style="font-family:'Plus Jakarta Sans',sans-serif;min-width:180px;">
          <h4 style="font-size:14px;font-weight:800;margin-bottom:4px;color:#0f172a;">${p.name}</h4>
          <p style="font-size:12px;color:#64748b;margin-bottom:8px;">${p.weather_text}</p>
          <div style="font-size:12px;display:flex;flex-direction:column;gap:3px;margin-bottom:10px;">
            <span><strong>Nhiệt độ:</strong> ${p.temp}°C (Cảm giác ${p.feels_like}°C)</span>
            <span><strong>Độ ẩm:</strong> ${p.humidity}% • <strong>Gió:</strong> ${p.wind_speed}m/s</span>
            <span><strong>Bụi PM2.5:</strong> ${p.pm25} µg/m³ (AQI ${Math.round(p.pm25 * 1.8)})</span>
          </div>
          <button style="width:100%;padding:6px;background:#0284c7;color:#fff;border:none;border-radius:6px;font-weight:700;font-size:12px;cursor:pointer;" onclick="App.selectProvince('${p.id}'); App.switchTab('tab-overview');">
            Xem chi tiết địa phương
          </button>
        </div>
      `);
      this.mapMarkers.push(marker);
    });

    // 5. Hiển thị các trạm quan trắc chi tiết của tỉnh đang chọn
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
  },"""
        code = code[:pos5] + new_map_block + code[pos6 + len(old_map_end):]
        print("8. Patched Map markers with Hoang Sa & Truong Sa sovereignty")

# 9. Tab 7 Outdoor Tab Region Filter
old_outdoor_start = """  // =========================================================================
  // TAB 7: KHÁM PHÁ – ĐI CHƠI (SMART OUTDOOR RECOMMENDER)
  // =========================================================================
  renderOutdoorTab() {"""

old_outdoor_end = """    return `
      <div class="outdoor-card" onclick="App.selectProvince('${p.id}');">
        <div>
          <div class="outdoor-card-top">
            <div>
              <div class="outdoor-city-title">${p.name}</div>
              <div class="outdoor-region-tag">${p.type} • ${p.region}</div>
            </div>
            <div class="outdoor-score-badge ${scoreClass}">${score}</div>
          </div>
          <div style="font-size:12px;font-weight:700;color:var(--accent-teal);margin-top:4px;">${scoreLabel}</div>
          <p style="font-size:12px;color:var(--text-muted);margin:8px 0;">${p.weather_text} • ${p.temp}°C</p>
          <div style="font-size:12px;color:var(--text-secondary);line-height:1.5;margin-bottom:12px;">
            <strong>Khung giờ vàng:</strong> ${p.best_time}<br>
            <strong>Lời khuyên:</strong> ${p.outdoor_advice}
          </div>
        </div>
        <div style="display:flex;gap:6px;flex-wrap:wrap;">
          ${(p.outdoor_activities || []).map(act => `<span class="activity-pill-tag">${act}</span>`).join('')}
        </div>
      </div>
    `;
  },"""

pos7 = code.find(old_outdoor_start)
if pos7 != -1:
    pos8 = code.find(old_outdoor_end, pos7)
    if pos8 != -1:
        new_outdoor_block = """  // =========================================================================
  // TAB 7: KHÁM PHÁ – ĐI CHƠI (SMART OUTDOOR RECOMMENDER THEO MIỀN CHUẨN XÁC)
  // =========================================================================
  filterOutdoorRegion(reg) {
    this.outdoorRegion = reg;
    document.querySelectorAll('.outdoor-region-filter-row .district-pill').forEach(btn => {
      const txt = btn.innerText.toLowerCase();
      const match = (reg === 'all')
        ? txt.includes('tất cả')
        : (reg === 'Miền Trung' ? (txt.includes('miền trung') && !txt.includes('tây nguyên')) : txt.includes(reg.toLowerCase()));
      if (match) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
    this.renderOutdoorTab();
  },

  renderOutdoorTab() {
    const grid = document.getElementById('outdoor-full-grid');
    if (!grid) return;

    let filtered = [...this.provinces];

    // Lọc theo Vùng miền chuẩn xác
    if (this.outdoorRegion && this.outdoorRegion !== 'all') {
      if (this.outdoorRegion === 'Tây Nguyên') {
        filtered = filtered.filter(p => p.region.includes('Tây Nguyên'));
      } else if (this.outdoorRegion === 'Miền Trung') {
        filtered = filtered.filter(p => p.region.includes('Miền Trung') && !p.region.includes('Tây Nguyên'));
      } else {
        filtered = filtered.filter(p => p.region.includes(this.outdoorRegion));
      }
    }

    // Lọc theo Hoạt động
    if (this.activeActivity !== 'all') {
      const actMap = {
        walk: 'Đi dạo',
        run: 'Chạy bộ',
        cycling: 'Đạp xe',
        picnic: 'Picnic',
        travel: 'Du lịch',
        beach: 'Đi biển',
        hiking: 'Leo núi',
        sports: 'Thể thao'
      };
      const keyword = actMap[this.activeActivity];
      filtered = filtered.filter(p => p.outdoor_activities && p.outdoor_activities.some(a => a.includes(keyword)));
    }

    filtered.sort((a, b) => b.outdoor_score - a.outdoor_score);

    if (filtered.length === 0) {
      grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:40px;color:var(--text-muted);"><i class="fa-solid fa-triangle-exclamation"></i> Không có địa phương nào phù hợp với bộ lọc đã chọn.</div>';
      return;
    }

    grid.innerHTML = filtered.map(p => this.createOutdoorCardHtml(p)).join('');
  },

  filterActivity(actKey) {
    this.activeActivity = actKey;
    document.querySelectorAll('.activity-filter-btn').forEach(btn => btn.classList.remove('active'));
    if (typeof event !== 'undefined' && event && event.currentTarget) {
      event.currentTarget.classList.add('active');
    }
    this.renderOutdoorTab();
  },

  createOutdoorCardHtml(p) {
    const score = p.outdoor_score;
    const scoreClass = score >= 90 ? 'outdoor-score-90' : (score >= 80 ? 'outdoor-score-80' : (score >= 70 ? 'outdoor-score-70' : 'outdoor-score-60'));
    const scoreLabel = score >= 90 ? 'Rất lý tưởng' : (score >= 80 ? 'Thuận lợi' : (score >= 70 ? 'Vừa phải' : 'Nên cân nhắc'));
    const isSelected = (p.id === this.selectedProvinceId);

    return `
      <div class="outdoor-card ${isSelected ? 'selected-outdoor-card' : ''}" id="outdoor-card-${p.id}" onclick="App.selectProvince('${p.id}');">
        <div>
          <div class="outdoor-card-top">
            <div>
              <div class="outdoor-city-title">
                ${isSelected ? '<i class="fa-solid fa-location-dot" style="color:var(--primary);margin-right:4px;"></i>' : ''}${p.name}
              </div>
              <div class="outdoor-region-tag">${p.type} • ${p.region}</div>
            </div>
            <div class="outdoor-score-badge ${scoreClass}">${score}</div>
          </div>
          <div style="font-size:12px;font-weight:700;color:var(--accent-teal);margin-top:4px;">${scoreLabel}</div>
          <p style="font-size:12px;color:var(--text-muted);margin:8px 0;">${p.weather_text} • ${p.temp}°C • AQI ${Math.round(p.pm25 * 1.8)}</p>
          <div style="font-size:12px;color:var(--text-secondary);line-height:1.5;margin-bottom:12px;">
            <strong>Khung giờ vàng:</strong> ${p.best_time}<br>
            <strong>Lời khuyên:</strong> ${p.outdoor_advice}
          </div>
        </div>
        <div style="display:flex;gap:6px;flex-wrap:wrap;">
          ${(p.outdoor_activities || []).map(act => `<span class="activity-pill-tag">${act}</span>`).join('')}
        </div>
      </div>
    `;
  },"""
        code = code[:pos7] + new_outdoor_block + code[pos8 + len(old_outdoor_end):]
        print("9. Patched Outdoor tab with region filtering")

# 10. Update Geopandas modal for sovereignty
old_geo_modal = """    } else if (type === 'geopandas') {
      title.innerHTML = '<i class="fa-solid fa-draw-polygon" style="color:#0d9488;"></i> Hạ Tầng GIS & Xử Lý Không Gian GeoPandas';
      body.innerHTML = `
        <div style="line-height:1.7;">
          <h4 style="color:#0d9488;font-size:15px;margin-bottom:8px;">1. Kiến trúc Địa không gian Toàn Quốc</h4>
          <p style="margin-bottom:12px;">Hệ thống ứng dụng thư viện <code>GeoPandas</code> và <code>Shapely</code> để chuyển đổi dữ liệu tọa độ WGS84 (EPSG:4326) sang hệ tọa độ phẳng UTM VN-2000 (EPSG:3405/3406) nhằm tính toán khoảng cách và nội suy không gian chính xác.</p>
          
          <h4 style="color:#0d9488;font-size:15px;margin-bottom:8px;">2. Phương pháp Nội suy IDW & Kriging</h4>
          <p style="margin-bottom:12px;">Các điểm trạm đo đạc của 34 tỉnh/thành phố được xây dựng thành lưới raster độ phân giải cao thông qua thuật toán Trọng số nghịch đảo khoảng cách (Inverse Distance Weighting - IDW). Điều này cho phép ước lượng trường nồng độ bụi và nhiệt độ tại bất kỳ vị trí địa lý nào không có trạm vật lý.</p>
          
          <div style="background:var(--body-bg);padding:12px;border-radius:8px;border-left:4px solid #0d9488;">
            <strong>Quy mô mạng lưới:</strong> 34 Tỉnh/Thành phố trực thuộc Trung ương & Cấp tỉnh bao phủ trọn vẹn 3 miền Bắc, Trung, Nam và Tây Nguyên.
          </div>
        </div>
      `;
    }"""

new_geo_modal = """    } else if (type === 'geopandas') {
      title.innerHTML = '<i class="fa-solid fa-draw-polygon" style="color:#0d9488;"></i> Hạ Tầng GIS & Bản Đồ Không Gian Việt Nam (GeoPandas)';
      body.innerHTML = `
        <div style="line-height:1.7;">
          <h4 style="color:#0d9488;font-size:15px;margin-bottom:8px;">1. Quy Chuẩn Bản Đồ Hành Chính Số Quốc Gia</h4>
          <p style="margin-bottom:12px;">Hệ thống tuân thủ nghiêm ngặt quy chuẩn bản đồ hành chính không gian số của <strong>Cục Đo đạc, Bản đồ và Thông tin địa lý Việt Nam (Bộ Tài nguyên & Môi trường)</strong>. Dữ liệu địa không gian bao trùm trọn vẹn toàn bộ chủ quyền lãnh thổ Việt Nam bao gồm phần đất liền (34 tỉnh/thành phố trọng điểm), vùng trời, vùng biển, thềm lục địa và hai quần đảo <strong>Hoàng Sa (thuộc Thành phố Đà Nẵng)</strong> và <strong>Trường Sa (thuộc Tỉnh Khánh Hòa)</strong>.</p>
          
          <h4 style="color:#0d9488;font-size:15px;margin-bottom:8px;">2. Xử Lý Tọa Độ WGS84 & Phép Chiếu VN-2000</h4>
          <p style="margin-bottom:12px;">Hệ thống ứng dụng thư viện <code>GeoPandas</code> và <code>Shapely</code> để chuyển đổi dữ liệu tọa độ địa lý WGS84 (EPSG:4326) sang hệ tọa độ phẳng UTM VN-2000 (EPSG:3405/3406) nhằm tính toán khoảng cách và nội suy không gian chính xác theo lưới kinh vĩ độ Việt Nam.</p>
          
          <h4 style="color:#0d9488;font-size:15px;margin-bottom:8px;">3. Phương Pháp Nội Suy IDW & Kriging Không Gian</h4>
          <p style="margin-bottom:12px;">101 điểm trạm quan trắc chi tiết trên toàn quốc được xây dựng thành lưới raster độ phân giải cao thông qua thuật toán Trọng số nghịch đảo khoảng cách (Inverse Distance Weighting - IDW). Điều này cho phép ước lượng trường nồng độ bụi PM2.5, nhiệt độ và trường gió tại bất kỳ tọa độ địa lý nào trên toàn lãnh thổ và vùng biển Việt Nam.</p>

          <div style="background:var(--body-bg);padding:12px;border-radius:8px;border-left:4px solid #0d9488;">
            <strong>Khẳng định Chủ quyền:</strong> Toàn bộ hai quần đảo Hoàng Sa và Trường Sa cùng vùng biển đặc quyền kinh tế 200 hải lý thuộc chủ quyền thiêng liêng và bất khả xâm phạm của Nước Cộng hòa Xã hội Chủ nghĩa Việt Nam.
          </div>
        </div>
      `;
    }"""

if old_geo_modal in code:
    code = code.replace(old_geo_modal, new_geo_modal)
    print("10. Patched Geopandas modal")

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("SUCCESS: All 10 patches applied to js/app.js!")
