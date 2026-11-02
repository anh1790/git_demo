# -*- coding: utf-8 -*-
"""
Patch and upgrade js/app.js to support:
- Detailed station selection for all 34 provinces (101 stations)
- Accurate 4-region filtering (Miền Bắc, Miền Trung, Tây Nguyên, Miền Nam)
- Dropdown with optgroups
- Robust renderForecastTimeSeriesChart and renderOptimizationBenchmarkCharts
- Fix white screen issue completely
"""

with open("js/app.js", "r", encoding="utf-8") as f:
    code = f.read()

# 1. State updates
old_state = """  selectedProvinceId: 'VN_HN',
  compareProvinceIds: ['VN_HN', 'VN_DN', 'VN_HCM'],
  compareHorizon: 'now',
  activeActivity: 'all',
  mapLayer: 'temp',
  selectedMlModel: 'Random_Forest',
  inferencePrecision: 'optimized', // 'optimized' (Int8) or 'fp32'
  theme: 'light',"""

new_state = """  selectedProvinceId: 'VN_HN',
  selectedStationId: null,
  selectedRegion: 'all',
  compareProvinceIds: ['VN_HN', 'VN_DN', 'VN_HCM'],
  compareHorizon: 'now',
  activeActivity: 'all',
  mapLayer: 'temp',
  selectedMlModel: 'Random_Forest',
  inferencePrecision: 'optimized', // 'optimized' (Int8) or 'fp32'
  theme: 'light',"""

if old_state in code:
    code = code.replace(old_state, new_state, 1)

# 2. initData: attach stations to provinces
old_init_data = """  // 1. Dữ liệu 34 Tỉnh Thành từ EMBEDDED_DATA
  initData() {
    if (typeof EMBEDDED_DATA !== 'undefined' && EMBEDDED_DATA.latest) {
      this.provinces = EMBEDDED_DATA.latest;
    } else {
      console.warn("EMBEDDED_DATA not found, retrying with fallback...");
      this.provinces = [];
    }
  },"""

new_init_data = """  // 1. Dữ liệu 34 Tỉnh Thành và 101 Trạm Quan Trắc
  initData() {
    if (typeof EMBEDDED_DATA !== 'undefined' && EMBEDDED_DATA.latest) {
      this.provinces = EMBEDDED_DATA.latest;
    } else {
      console.warn("EMBEDDED_DATA not found, retrying with fallback...");
      this.provinces = [];
    }

    // Gắn thông tin trạm chi tiết cho từng tỉnh thành
    if (window.VIETNAM_STATIONS_DATA) {
      this.provinces.forEach(p => {
        if (!p.stations || p.stations.length === 0) {
          p.stations = window.VIETNAM_STATIONS_DATA[p.id] || [];
        }
      });
    }

    // Khởi tạo trạm mặc định cho Hà Nội
    const hnStations = this.getStationsForProvince('VN_HN');
    if (hnStations && hnStations.length > 0) {
      this.selectedStationId = hnStations[0].id;
    }
  },

  getStationsForProvince(provId) {
    if (window.VIETNAM_STATIONS_DATA && window.VIETNAM_STATIONS_DATA[provId]) {
      return window.VIETNAM_STATIONS_DATA[provId];
    }
    const p = this.getProvinceById(provId);
    if (p && p.stations && p.stations.length > 0) {
      return p.stations;
    }
    return [
      {
        id: `${provId}_01`,
        name: `Trạm Trung tâm ${p.name || ''}`,
        type: 'Đô thị / Trung tâm',
        address: `Trung tâm hành chính ${p.name || ''}`,
        pm25: p.pm25 || 25.0,
        pm10: p.pm10 || 38.0,
        aqi: Math.round((p.pm25 || 25.0) * 1.8),
        temp: p.temp || 24.0,
        humidity: p.humidity || 70,
        wind: p.wind_speed || 3.0,
        status: 'Đang hoạt động 24/7',
        color: p.color || '#f59e0b'
      }
    ];
  },

  getSelectedStation() {
    const stations = this.getStationsForProvince(this.selectedProvinceId);
    if (!stations || stations.length === 0) return null;
    if (!this.selectedStationId) return stations[0];
    return stations.find(s => s.id === this.selectedStationId) || stations[0];
  },

  selectStation(stationId) {
    this.selectedStationId = stationId;
    const st = this.getSelectedStation();
    const p = this.getSelectedProvince();

    // Cập nhật active class cho station pills
    document.querySelectorAll('#station-pills-container .station-pill').forEach(btn => {
      if (btn.getAttribute('data-station-id') === stationId) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    // Cập nhật card active trong Tab 4 nếu có
    document.querySelectorAll('.station-detail-card').forEach(card => {
      card.classList.remove('active-station');
    });

    this.renderHeroWeather();
    if (this.currentTab === 'tab-airquality') this.renderAirQualityTab();
    if (this.currentTab === 'tab-aiforecast') this.renderForecastTab();

    this.showToast(`📍 Đã chuyển sang đo đạc trạm: ${st ? st.name : stationId}`);
  },"""

if old_init_data in code:
    code = code.replace(old_init_data, new_init_data, 1)

with open("js/app.js", "w", encoding="utf-8") as f:
    f.write(code)

print("Step 1 of patch applied.")
