# -*- coding: utf-8 -*-
with open("js/app.js", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update renderHeroWeather to be aware of selected station
old_hero_start = """  renderHeroWeather(overrideCondition = null) {
    const p = this.getSelectedProvince();
    if (!p || !p.id) return;"""

new_hero_start = """  renderHeroWeather(overrideCondition = null) {
    const p = this.getSelectedProvince();
    if (!p || !p.id) return;
    const st = this.getSelectedStation();
    const activeTemp = (st && st.temp != null) ? st.temp : p.temp;
    const activePm25 = (st && st.pm25 != null) ? st.pm25 : p.pm25;
    const activeAqi = (st && st.aqi != null) ? st.aqi : Math.round(activePm25 * 1.8);
    const activeAqiLevel = (st && st.aqi_level) ? st.aqi_level : p.aqi_level;"""

code = code.replace(old_hero_start, new_hero_start, 1)

# In hero text updates:
old_hero_texts = """    const locEl = document.getElementById('hero-location-name');
    if (locEl) locEl.innerHTML = `<i class=\"fa-solid fa-location-dot\"></i> ${p.name} • ${p.type}`;

    const tempEl = document.getElementById('hero-temp-val');
    if (tempEl) tempEl.innerText = `${p.temp}°`;

    const feelsEl = document.getElementById('hero-feels-val');
    if (feelsEl) feelsEl.innerText = `Cảm giác như ${p.feels_like}°C`;

    const sumEl = document.getElementById('hero-summary-text');
    if (sumEl) sumEl.innerText = `Thời tiết tại ${p.name} hiện tại: ${p.weather_text}. ${p.outdoor_advice}`;

    const humEl = document.getElementById('hero-hum-val');
    if (humEl) humEl.innerText = `${p.humidity}%`;

    const windEl = document.getElementById('hero-wind-val');
    if (windEl) windEl.innerText = `${p.wind_speed} m/s ${p.wind_dir}`;

    const rainEl = document.getElementById('hero-rain-val');
    if (rainEl) rainEl.innerText = `${p.rain_prob}%`;

    const uvEl = document.getElementById('hero-uv-val');
    if (uvEl) uvEl.innerText = `${p.uv}`;

    const aqiEl = document.getElementById('hero-aqi-val');
    if (aqiEl) aqiEl.innerText = `${Math.round(p.pm25 * 1.8)} (${p.aqi_level})`;"""

new_hero_texts = """    const locEl = document.getElementById('hero-location-name');
    if (locEl) {
      locEl.innerHTML = st 
        ? `<i class=\"fa-solid fa-tower-broadcast\" style=\"color:var(--accent-teal);\"></i> ${st.name} • <span style=\"font-size:12px;opacity:0.85;\">${p.name}</span>`
        : `<i class=\"fa-solid fa-location-dot\"></i> ${p.name} • ${p.type}`;
    }

    const tempEl = document.getElementById('hero-temp-val');
    if (tempEl) tempEl.innerText = `${activeTemp}°`;

    const feelsEl = document.getElementById('hero-feels-val');
    if (feelsEl) feelsEl.innerText = `Cảm giác như ${Math.round((activeTemp + 0.8) * 10) / 10}°C`;

    const sumEl = document.getElementById('hero-summary-text');
    if (sumEl) {
      sumEl.innerText = st 
        ? `Số liệu đo đạc tại ${st.name} (${p.name}): PM2.5 là ${activePm25} µg/m³, AQI ${activeAqi} (${activeAqiLevel}). ${p.weather_text}.`
        : `Thời tiết tại ${p.name} hiện tại: ${p.weather_text}. ${p.outdoor_advice}`;
    }

    const humEl = document.getElementById('hero-hum-val');
    if (humEl) humEl.innerText = `${st && st.humidity != null ? st.humidity : p.humidity}%`;

    const windEl = document.getElementById('hero-wind-val');
    if (windEl) windEl.innerText = `${p.wind_speed} m/s ${p.wind_dir}`;

    const rainEl = document.getElementById('hero-rain-val');
    if (rainEl) rainEl.innerText = `${p.rain_prob}%`;

    const uvEl = document.getElementById('hero-uv-val');
    if (uvEl) uvEl.innerText = `${p.uv}`;

    const aqiEl = document.getElementById('hero-aqi-val');
    if (aqiEl) aqiEl.innerText = `${activeAqi} (${activeAqiLevel})`;"""

code = code.replace(old_hero_texts, new_hero_texts, 1)

# 2. Update renderAirQualityTab to render detailed stations
old_aqi_render = """  renderAirQualityTab() {
    const p = this.getSelectedProvince();
    const aqi = Math.round(p.pm25 * 1.8);

    document.getElementById('aqi-city-title').innerText = p.name;
    document.getElementById('aqi-main-val').innerText = aqi;
    document.getElementById('aqi-main-badge').innerText = `${p.aqi_level} (PM2.5: ${p.pm25} µg/m³)`;
    document.getElementById('aqi-main-badge').style.backgroundColor = `${p.color}20`;
    document.getElementById('aqi-main-badge').style.color = p.color;
    document.getElementById('aqi-health-advice').innerText = p.health_advice;"""

new_aqi_render = """  renderAirQualityTab() {
    const p = this.getSelectedProvince();
    const st = this.getSelectedStation();
    const activePm25 = (st && st.pm25 != null) ? st.pm25 : p.pm25;
    const aqi = (st && st.aqi != null) ? st.aqi : Math.round(activePm25 * 1.8);
    const aqiLevel = (st && st.aqi_level) ? st.aqi_level : p.aqi_level;
    const aqiColor = (st && st.color) ? st.color : p.color;

    const titleEl = document.getElementById('aqi-city-title');
    if (titleEl) {
      titleEl.innerText = st ? `${st.name} (${p.name})` : p.name;
    }
    const valEl = document.getElementById('aqi-main-val');
    if (valEl) valEl.innerText = aqi;

    const badgeEl = document.getElementById('aqi-main-badge');
    if (badgeEl) {
      badgeEl.innerText = `${aqiLevel} (PM2.5: ${activePm25} µg/m³)`;
      badgeEl.style.backgroundColor = `${aqiColor}20`;
      badgeEl.style.color = aqiColor;
    }
    const advEl = document.getElementById('aqi-health-advice');
    if (advEl) advEl.innerText = p.health_advice;"""

code = code.replace(old_aqi_render, new_aqi_render, 1)

# Also insert detailed stations cards rendering in renderAirQualityTab
target_after_pollutants = """    const ctxAqi = document.getElementById('compareAqiChart');"""

stations_grid_code = """    // Render danh sách các trạm quan trắc chi tiết của tỉnh hiện tại
    const stationsGrid = document.getElementById('province-stations-grid');
    const stationsProvTitle = document.getElementById('aqi-stations-province-name');
    if (stationsProvTitle) stationsProvTitle.innerText = p.name;

    const stations = this.getStationsForProvince(p.id);
    if (stationsGrid) {
      if (!stations || stations.length === 0) {
        stationsGrid.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:24px;color:var(--text-muted);">Đang tải dữ liệu mạng lưới trạm quan trắc của ${p.name}...</div>`;
      } else {
        stationsGrid.innerHTML = stations.map(s => {
          const isActive = (this.selectedStationId === s.id);
          const sAqi = s.aqi || Math.round(s.pm25 * 1.8);
          const sColor = s.color || '#f59e0b';
          const sLevel = s.aqi_level || 'Trung bình';
          return `
            <div class="station-detail-card ${isActive ? 'active-station' : ''}">
              <div>
                <div class="station-card-header">
                  <div>
                    <div class="station-card-title">${s.name}</div>
                    <span class="station-type-tag" style="color:${sColor}; background:${sColor}18;">${s.type}</span>
                  </div>
                  <span class="stat-badge" style="background:${sColor}20; color:${sColor}; font-size:11px; font-weight:800;">
                    AQI ${sAqi}
                  </span>
                </div>
                <div class="station-card-address">
                  <i class="fa-solid fa-location-dot" style="color:var(--primary);"></i> ${s.address || p.name}
                </div>
                <div class="station-card-metrics">
                  <div class="station-metric-item">
                    <span class="station-metric-label">Bụi PM2.5</span>
                    <span class="station-metric-val" style="color:${sColor};">${s.pm25} <small>µg/m³</small></span>
                  </div>
                  <div class="station-metric-item">
                    <span class="station-metric-label">Bụi PM10</span>
                    <span class="station-metric-val">${s.pm10 || Math.round(s.pm25 * 1.5)} <small>µg/m³</small></span>
                  </div>
                  <div class="station-metric-item">
                    <span class="station-metric-label">Nhiệt độ</span>
                    <span class="station-metric-val">${s.temp || p.temp}°C</span>
                  </div>
                </div>
                <div style="font-size:11px;color:var(--text-muted);display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
                  <span><i class="fa-solid fa-signal" style="color:#10b981;"></i> ${s.status || 'Hoạt động 24/7'}</span>
                  <span>Độ ẩm: <strong>${s.humidity || p.humidity}%</strong></span>
                </div>
              </div>
              <button class="station-select-btn" onclick="App.selectStation('${s.id}'); App.switchTab('tab-aiforecast');">
                <i class="fa-solid fa-wand-magic-sparkles"></i> ${isActive ? '✓ Đang chọn • Xem dự báo AI' : 'Chọn trạm này & Dự báo AI'}
              </button>
            </div>
          `;
        }).join('');
      }
    }

    const ctxAqi = document.getElementById('compareAqiChart');"""

if target_after_pollutants in code:
    code = code.replace(target_after_pollutants, stations_grid_code, 1)

with open("js/app.js", "w", encoding="utf-8") as f:
    f.write(code)

print("Step 3 applied successfully!")
