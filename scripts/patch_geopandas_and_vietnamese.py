import os
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 1. Update districts.geojson and districts.json with "country": "Việt Nam"
geo_files = [
    os.path.join(ROOT, "data", "geo", "districts.geojson"),
    os.path.join(ROOT, "data", "districts.json"),
    os.path.join(ROOT, "static", "data", "districts.json"),
    os.path.join(ROOT, "dist", "data", "districts.json")
]

for gfile in geo_files:
    if os.path.exists(gfile):
        with open(gfile, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace('"country": "Vietnam"', '"country": "Việt Nam"')
        with open(gfile, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated country in: {os.path.relpath(gfile, ROOT)}")

# 2. Update js/app.js:
# - Map bounds & center focused on Vietnam mainland
# - Remove arbitrary open sea text marker
# - Add GeoPandas GeoJSON polygon layer support
# - Translate any remaining chart English strings to 100% Vietnamese
js_file = os.path.join(ROOT, "js", "app.js")
with open(js_file, "r", encoding="utf-8") as f:
    js_content = f.read()

# Replace initMap
old_init_map = """  initMap() {
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
  },"""

new_init_map = """  initMap() {
    const mapContainer = document.getElementById('weather-leaflet-map');
    if (!mapContainer || typeof L === 'undefined') return;

    if (!this.map) {
      // Khởi tạo bản đồ tập trung chính xác vào phạm vi lãnh thổ đất liền Việt Nam
      this.map = L.map('weather-leaflet-map', {
        minZoom: 5,
        maxZoom: 15
      }).setView([16.0, 107.0], 6);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors | Bản đồ Khí tượng & Quan trắc Việt Nam'
      }).addTo(this.map);

      // Bảng thông tin ghi chú địa lý hành chính Việt Nam
      const SovereigntyControl = L.Control.extend({
        options: { position: 'bottomleft' },
        onAdd: function() {
          const div = L.DomUtil.create('div', 'map-sovereignty-box');
          div.innerHTML = `
            <div style="font-weight:800;color:#0284c7;margin-bottom:3px;display:flex;align-items:center;gap:6px;">
              <i class="fa-solid fa-map-location-dot"></i> ĐỊA LÝ & HÀNH CHÍNH VIỆT NAM
            </div>
            <div style="font-size:11.5px;line-height:1.45;">Mạng lưới trạm khí tượng quốc gia trên phạm vi đất liền Việt Nam. Ghi nhận <strong>Quần đảo Hoàng Sa</strong> (thuộc TP. Đà Nẵng) và <strong>Quần đảo Trường Sa</strong> (thuộc Tỉnh Khánh Hòa). Không tự ý xác định đường ranh giới trên biển khi chưa có nguồn pháp lý xác thực.</div>
          `;
          return div;
        }
      });
      new SovereigntyControl().addTo(this.map);
    }

    this.map.invalidateSize();
    this.updateMapMarkers();
  },"""

if old_init_map in js_content:
    js_content = js_content.replace(old_init_map, new_init_map)
    print("Replaced initMap in js_content")

# Now update updateMapMarkers in js_content:
# - Remove floating seaMarker ([12.8, 113.8])
# - Add GeoPandas layer handling
old_markers_start = "  updateMapMarkers() {"
old_markers_end = "    // 5. Hiển thị các trạm quan trắc chi tiết của tỉnh đang chọn"

m_start = js_content.find(old_markers_start)
m_end = js_content.find(old_markers_end)

if m_start != -1 and m_end != -1:
    new_markers_code = """  updateMapMarkers() {
    if (!this.map || typeof L === 'undefined') return;

    this.mapMarkers.forEach(m => this.map.removeLayer(m));
    this.mapMarkers = [];
    if (this.geoJsonDistrictsLayer) {
      this.map.removeLayer(this.geoJsonDistrictsLayer);
      this.geoJsonDistrictsLayer = null;
    }

    // 1. Lớp ranh giới hành chính GeoPandas (Hiển thị khi chọn lớp GeoPandas hoặc xem thủ đô Hà Nội)
    if (this.mapLayer === 'geopandas') {
      this.renderGeoPandasLayer();
    }

    // 2. Điểm quan trắc hành chính Quần đảo Hoàng Sa (Huyện Hoàng Sa, TP. Đà Nẵng)
    const hsIcon = L.divIcon({
      className: 'island-flag-pin',
      html: `
        <div class="island-flag-pin" title="Quần đảo Hoàng Sa (TP. Đà Nẵng, Việt Nam)">
          <div class="flag-icon-circle"><i class="fa-solid fa-star"></i></div>
        </div>
      `,
      iconSize: [32, 32],
      iconAnchor: [16, 16]
    });
    const hsMarker = L.marker([16.536, 112.025], { icon: hsIcon, zIndexOffset: 900 }).addTo(this.map);
    hsMarker.bindTooltip('<strong>QUẦN ĐẢO HOÀNG SA</strong><br><small style="color:#fef08a;">(TP. Đà Nẵng, Việt Nam)</small>', {
      permanent: false,
      direction: 'top',
      className: 'island-sovereignty-badge',
      offset: [0, -10]
    });
    hsMarker.bindPopup(`
      <div style="font-family:'Plus Jakarta Sans',sans-serif;min-width:240px;line-height:1.5;">
        <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
          <i class="fa-solid fa-circle-dot" style="color:#0284c7;"></i>
          <h4 style="font-size:14px;font-weight:800;margin:0;color:#0f172a;">QUẦN ĐẢO HOÀNG SA</h4>
        </div>
        <p style="font-size:11.5px;color:#475569;margin-bottom:8px;">
          <strong>Đơn vị hành chính:</strong> Huyện Hoàng Sa, Thành phố Đà Nẵng, Việt Nam<br>
          <strong>Cơ sở quan trắc:</strong> Trạm Khí tượng Hải văn Hoàng Sa
        </p>
        <div style="font-size:11.5px;background:#f8fafc;padding:8px;border-radius:6px;border:1px solid #e2e8f0;margin-bottom:8px;">
          <div><strong>Nhiệt độ biển:</strong> 28.5°C • <strong>Độ ẩm:</strong> 82%</div>
          <div><strong>Gió:</strong> Đông Bắc 6.5 m/s (Cấp 4) • <strong>Sóng:</strong> 1.2 m</div>
          <div><strong>Chất lượng không khí:</strong> AQI 18 (Tốt)</div>
        </div>
        <button style="width:100%;padding:6px;background:#0284c7;color:#fff;border:none;border-radius:6px;font-weight:700;font-size:11.5px;cursor:pointer;" onclick="App.selectProvince('VN_DN'); App.switchTab('tab-overview');">
          Xem thời tiết TP. Đà Nẵng
        </button>
      </div>
    `);
    this.mapMarkers.push(hsMarker);

    // 3. Điểm quan trắc hành chính Quần đảo Trường Sa (Huyện Trường Sa, Tỉnh Khánh Hòa)
    const tsIcon = L.divIcon({
      className: 'island-flag-pin',
      html: `
        <div class="island-flag-pin" title="Quần đảo Trường Sa (Tỉnh Khánh Hòa, Việt Nam)">
          <div class="flag-icon-circle"><i class="fa-solid fa-star"></i></div>
        </div>
      `,
      iconSize: [32, 32],
      iconAnchor: [16, 16]
    });
    const tsMarker = L.marker([8.647, 111.919], { icon: tsIcon, zIndexOffset: 900 }).addTo(this.map);
    tsMarker.bindTooltip('<strong>QUẦN ĐẢO TRƯỜNG SA</strong><br><small style="color:#fef08a;">(Tỉnh Khánh Hòa, Việt Nam)</small>', {
      permanent: false,
      direction: 'top',
      className: 'island-sovereignty-badge',
      offset: [0, -10]
    });
    tsMarker.bindPopup(`
      <div style="font-family:'Plus Jakarta Sans',sans-serif;min-width:240px;line-height:1.5;">
        <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
          <i class="fa-solid fa-circle-dot" style="color:#0284c7;"></i>
          <h4 style="font-size:14px;font-weight:800;margin:0;color:#0f172a;">QUẦN ĐẢO TRƯỜNG SA</h4>
        </div>
        <p style="font-size:11.5px;color:#475569;margin-bottom:8px;">
          <strong>Đơn vị hành chính:</strong> Huyện Trường Sa, Tỉnh Khánh Hòa, Việt Nam<br>
          <strong>Cơ sở quan trắc:</strong> Trạm Khí tượng Hải văn Đảo Trường Sa Lớn
        </p>
        <div style="font-size:11.5px;background:#f8fafc;padding:8px;border-radius:6px;border:1px solid #e2e8f0;margin-bottom:8px;">
          <div><strong>Nhiệt độ biển:</strong> 29.2°C • <strong>Độ ẩm:</strong> 85%</div>
          <div><strong>Gió:</strong> Đông Nam 5.2 m/s (Cấp 3) • <strong>Sóng:</strong> 1.0 m</div>
          <div><strong>Chất lượng không khí:</strong> AQI 15 (Tốt)</div>
        </div>
        <button style="width:100%;padding:6px;background:#0284c7;color:#fff;border:none;border-radius:6px;font-weight:700;font-size:11.5px;cursor:pointer;" onclick="App.selectProvince('VN_KH'); App.switchTab('tab-overview');">
          Xem thời tiết Tỉnh Khánh Hòa
        </button>
      </div>
    `);
    this.mapMarkers.push(tsMarker);

    // 4. Các điểm quan trắc 34 tỉnh thành Việt Nam
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
      marker.bindPopup(`
        <div style="font-family:'Plus Jakarta Sans',sans-serif;min-width:190px;">
          <h4 style="font-size:14px;font-weight:800;margin-bottom:4px;color:#0f172a;">${p.name}</h4>
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

"""
    js_content = js_content[:m_start] + new_markers_code + js_content[m_end:]
    print("Updated updateMapMarkers in js_content")

# 3. Add renderGeoPandasLayer function to js/app.js
render_geo_fn = """  // Phương thức tải và hiển thị ranh giới đa giác GeoPandas lên bản đồ Leaflet
  async renderGeoPandasLayer() {
    try {
      let geoData = null;
      const resp = await fetch('/api/spatial/regions-geojson');
      if (resp.ok) {
        geoData = await resp.json();
      } else {
        const localResp = await fetch('data/districts.json');
        if (localResp.ok) geoData = await localResp.json();
      }

      if (geoData && geoData.features && this.map) {
        this.geoJsonDistrictsLayer = L.geoJSON(geoData, {
          style: (feature) => ({
            color: '#0284c7',
            weight: 2,
            opacity: 0.9,
            fillColor: feature.properties.color || '#38bdf8',
            fillOpacity: 0.25
          }),
          onEachFeature: (feature, layer) => {
            const props = feature.properties || {};
            layer.bindTooltip(`<strong>Quận ${props.district_name || ''}</strong><br>Diện tích: ${props.area_km2 || '5.3'} km²<br>PM2.5: ${props.pm25 || '15'} µg/m³`, {
              sticky: true,
              direction: 'top'
            });
            layer.bindPopup(`
              <div style="font-family:'Plus Jakarta Sans',sans-serif;min-width:200px;">
                <h4 style="margin:0 0 4px;color:#0284c7;">Quận ${props.district_name}</h4>
                <p style="font-size:12px;color:#64748b;margin:0 0 8px;">Đơn vị hành chính: ${props.city || 'Hà Nội'}, ${props.country || 'Việt Nam'}</p>
                <div style="font-size:12px;line-height:1.5;">
                  <div><strong>Diện tích GeoPandas:</strong> ${props.area_km2 || '5.3'} km² (UTM 48N)</div>
                  <div><strong>Nồng độ bụi PM2.5:</strong> ${props.pm25 || '15'} µg/m³</div>
                  <div><strong>Chỉ số AQI:</strong> ${props.aqi || Math.round((props.pm25 || 15) * 1.8)} (${props.aqi_level || 'Tốt'})</div>
                </div>
              </div>
            `);
          }
        }).addTo(this.map);
      }
    } catch (e) {
      console.warn('GeoPandas layer render note:', e);
    }
  },

"""

if "renderGeoPandasLayer()" not in js_content:
    insert_pos = js_content.find("  setMapLayer(layerType) {")
    if insert_pos != -1:
        js_content = js_content[:insert_pos] + render_geo_fn + js_content[insert_pos:]
        print("Added renderGeoPandasLayer() to js_content")

# 4. Replace remaining English chart text
js_content = js_content.replace("text: 'AQI Index'", "text: 'Chỉ số chất lượng không khí (AQI)'")
js_content = js_content.replace("'Int8 Quantized'", "'Lượng tử hóa Int8'")
js_content = js_content.replace("'FP32 Raw'", "'Mô hình gốc FP32'")
js_content = js_content.replace("'FP32 Gốc'", "'Mô hình gốc FP32'")

with open(js_file, "w", encoding="utf-8") as f:
    f.write(js_content)
print("Saved js/app.js successfully!")

# 5. Update index.html map card header & buttons
html_file = os.path.join(ROOT, "index.html")
with open(html_file, "r", encoding="utf-8") as f:
    html_content = f.read()

# Replace map card header
old_html_map_header = """              <h3 class="card-title"><i class="fa-solid fa-map-location-dot"></i> Bản Đồ Khí Tượng & GIS Việt Nam (Hoàng Sa & Trường Sa)</h3>
              <p style="font-size:12px;color:var(--text-muted);margin-top:2px;">
                <i class="fa-solid fa-flag" style="color:#ef4444;"></i> Bản đồ chuẩn Việt Nam – Khẳng định chủ quyền không thể tách rời đối với Quần đảo Hoàng Sa (TP. Đà Nẵng) và Quần đảo Trường Sa (Tỉnh Khánh Hòa)
              </p>"""

new_html_map_header = """              <h3 class="card-title"><i class="fa-solid fa-map-location-dot"></i> Bản Đồ Địa Lý & Khí Tượng Việt Nam (Hệ Thống Quan Trắc Đất Liền)</h3>
              <p style="font-size:12px;color:var(--text-muted);margin-top:2px;">
                <i class="fa-solid fa-circle-check" style="color:#10b981;"></i> Bản đồ mạng lưới quan trắc khí tượng các tỉnh thành Việt Nam – Tọa độ chuẩn WGS84 & Phân tích không gian GeoPandas (Hoàng Sa thuộc TP. Đà Nẵng, Trường Sa thuộc Tỉnh Khánh Hòa)
              </p>"""

if old_html_map_header in html_content:
    html_content = html_content.replace(old_html_map_header, new_html_map_header)
    print("Updated map header in index.html")

# Add GeoPandas layer toggle button in index.html
old_btn_group = """              <button class="map-layer-btn" onclick="App.setMapLayer('wind')">Tốc độ gió (m/s)</button>
            </div>"""

new_btn_group = """              <button class="map-layer-btn" onclick="App.setMapLayer('wind')">Tốc độ gió (m/s)</button>
              <button class="map-layer-btn" onclick="App.setMapLayer('geopandas')"><i class="fa-solid fa-draw-polygon"></i> Ranh giới GeoPandas</button>
            </div>"""

if old_btn_group in html_content:
    html_content = html_content.replace(old_btn_group, new_btn_group)
    print("Added GeoPandas button to index.html")

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)
print("Saved index.html successfully!")
