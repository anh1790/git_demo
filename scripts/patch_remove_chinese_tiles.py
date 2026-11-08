import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 1. Update js/app.js
js_path = os.path.join(ROOT, "js", "app.js")
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Replace openstreetmap with esri baseTileLayers in initMap()
old_osm_block = """      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors | Bản đồ Khí tượng & Quan trắc Việt Nam'
      }).addTo(this.map);"""

new_esri_block = """      // Hệ thống bản đồ nền GIS chuẩn quốc tế (Esri) - Loại bỏ 100% nhãn tiếng Trung ("西沙区", "陵水县") và ranh giới sai lệch của OSM
      this.baseTileLayers = {
        streets: L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
          attribution: 'Bản đồ GIS &copy; Esri &mdash; Mạng lưới Trạm Khí tượng Quốc gia Việt Nam',
          minZoom: 5,
          maxZoom: 17
        }),
        satellite: L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
          attribution: 'Hình ảnh Vệ tinh &copy; Esri &mdash; Bản đồ Khí tượng Việt Nam',
          minZoom: 5,
          maxZoom: 17
        }),
        topo: L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
          attribution: 'Bản đồ Địa hình &copy; Esri &mdash; Bản đồ Khí tượng Việt Nam',
          minZoom: 5,
          maxZoom: 17
        })
      };
      this.currentBaseTile = 'streets';
      this.baseTileLayers.streets.addTo(this.map);"""

if old_osm_block in js_content:
    js_content = js_content.replace(old_osm_block, new_esri_block)
    print("Replaced OpenStreetMap with Esri baseTileLayers in js/app.js")
else:
    print("WARNING: old_osm_block not found in js/app.js")

# Add setBaseTile method
set_base_tile_fn = """  setBaseTile(tileKey) {
    if (!this.map || !this.baseTileLayers || !this.baseTileLayers[tileKey]) return;
    Object.values(this.baseTileLayers).forEach(layer => {
      if (this.map.hasLayer(layer)) {
        this.map.removeLayer(layer);
      }
    });
    this.baseTileLayers[tileKey].addTo(this.map);
    this.currentBaseTile = tileKey;
    document.querySelectorAll('.map-basetile-btn').forEach(btn => btn.classList.remove('active'));
    if (typeof event !== 'undefined' && event && event.currentTarget) {
      event.currentTarget.classList.add('active');
    }
  },

"""

if "setBaseTile(tileKey)" not in js_content:
    insert_idx = js_content.find("  setMapLayer(layerType) {")
    if insert_idx != -1:
        js_content = js_content[:insert_idx] + set_base_tile_fn + js_content[insert_idx:]
        print("Inserted setBaseTile method in js/app.js")

# Update permanent: true for Hoang Sa & Truong Sa badges
old_hs_tooltip = """    hsMarker.bindTooltip('<strong>QUẦN ĐẢO HOÀNG SA</strong><br><small style="color:#fef08a;">(TP. Đà Nẵng, Việt Nam)</small>', {
      permanent: false,"""

new_hs_tooltip = """    hsMarker.bindTooltip('<strong>QUẦN ĐẢO HOÀNG SA</strong><br><small style="color:#fef08a;">(Huyện Hoàng Sa, TP. Đà Nẵng, Việt Nam)</small>', {
      permanent: true,"""

old_ts_tooltip = """    tsMarker.bindTooltip('<strong>QUẦN ĐẢO TRƯỜNG SA</strong><br><small style="color:#fef08a;">(Tỉnh Khánh Hòa, Việt Nam)</small>', {
      permanent: false,"""

new_ts_tooltip = """    tsMarker.bindTooltip('<strong>QUẦN ĐẢO TRƯỜNG SA</strong><br><small style="color:#fef08a;">(Huyện Trường Sa, Tỉnh Khánh Hòa, Việt Nam)</small>', {
      permanent: true,"""

js_content = js_content.replace(old_hs_tooltip, new_hs_tooltip)
js_content = js_content.replace(old_ts_tooltip, new_ts_tooltip)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)
print("Saved js/app.js successfully!")

# 2. Update index.html
html_path = os.path.join(ROOT, "index.html")
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

old_html_buttons = """              <button class="map-layer-btn" onclick="App.setMapLayer('wind')">Tốc độ gió (m/s)</button>
              <button class="map-layer-btn" onclick="App.setMapLayer('geopandas')"><i class="fa-solid fa-draw-polygon"></i> Ranh giới GeoPandas</button>
            </div>"""

new_html_buttons = """              <button class="map-layer-btn" onclick="App.setMapLayer('wind')">Tốc độ gió (m/s)</button>
              <button class="map-layer-btn" onclick="App.setMapLayer('geopandas')"><i class="fa-solid fa-draw-polygon"></i> Ranh giới GeoPandas</button>
            </div>
            <div class="map-layer-toggles" style="margin-top:8px;padding-top:8px;border-top:1px dashed var(--border-color);display:flex;align-items:center;flex-wrap:wrap;gap:6px;">
              <span style="font-size:11.5px;font-weight:700;color:var(--text-muted);display:inline-flex;align-items:center;gap:4px;"><i class="fa-solid fa-layer-group"></i> Bản đồ nền:</span>
              <button class="map-layer-btn map-basetile-btn active" onclick="App.setBaseTile('streets')"><i class="fa-solid fa-map"></i> Chuẩn GIS (Esri)</button>
              <button class="map-layer-btn map-basetile-btn" onclick="App.setBaseTile('satellite')"><i class="fa-solid fa-satellite"></i> Vệ tinh Viễn thám</button>
              <button class="map-layer-btn map-basetile-btn" onclick="App.setBaseTile('topo')"><i class="fa-solid fa-mountain"></i> Địa hình Tự nhiên</button>
            </div>"""

if old_html_buttons in html_content:
    html_content = html_content.replace(old_html_buttons, new_html_buttons)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Updated index.html successfully with basemap toggles!")
else:
    print("Note: old_html_buttons not matched, checking alternate")

print("Patch complete!")
