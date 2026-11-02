with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Hero Scrubber
old_scrub = """            <div class="weather-hero-right">
              <!-- Nút chuyển đổi khung giờ xem trước hiệu ứng động -->
              <div class="time-scrub-controls">
                <button class="time-scrub-btn active" onclick="App.scrubTimeOfDay('now')">Hiện tại</button>
                <button class="time-scrub-btn" onclick="App.scrubTimeOfDay('noon')">Trưa (Nắng)</button>
                <button class="time-scrub-btn" onclick="App.scrubTimeOfDay('sunset')">Hoàng hôn</button>
                <button class="time-scrub-btn" onclick="App.scrubTimeOfDay('night')">Đêm (Trăng)</button>
              </div>
            </div>"""

new_scrub = """            <div class="weather-hero-right">
              <!-- Nút chuyển đổi khung giờ xem trước hiệu ứng động -->
              <div class="time-scrub-controls">
                <button class="time-scrub-btn active" id="btn-scrub-now" onclick="App.scrubTimeOfDay('now')" title="Tự động bám sát giờ thực tế trên máy tính"><i class="fa-solid fa-clock"></i> Tự động (Giờ thực tế)</button>
                <button class="time-scrub-btn" id="btn-scrub-noon" onclick="App.scrubTimeOfDay('noon')"><i class="fa-solid fa-sun"></i> Trưa (Nắng)</button>
                <button class="time-scrub-btn" id="btn-scrub-sunset" onclick="App.scrubTimeOfDay('sunset')"><i class="fa-solid fa-cloud-sun"></i> Hoàng hôn</button>
                <button class="time-scrub-btn" id="btn-scrub-night" onclick="App.scrubTimeOfDay('night')"><i class="fa-solid fa-moon"></i> Đêm (Trăng sao)</button>
              </div>
            </div>"""

if old_scrub in content:
    content = content.replace(old_scrub, new_scrub)
    print("Updated Hero Scrubber")
else:
    print("Old scrubber not found directly, checking normalized...")
    # normalize CRLF
    content_norm = content.replace('\r\n', '\n')
    old_scrub_norm = old_scrub.replace('\r\n', '\n')
    if old_scrub_norm in content_norm:
        content = content_norm.replace(old_scrub_norm, new_scrub.replace('\r\n', '\n'))
        print("Updated Hero Scrubber via normalized")

# 2. Update Tab 6 Map Header
old_map_header = """          <div class="card-header">
            <h3 class="card-title"><i class="fa-solid fa-map-location-dot"></i> Bản Đồ Khí Tượng & Chất Lượng Không Khí Toàn Quốc</h3>
            <div class="map-layer-toggles">"""

new_map_header = """          <div class="card-header">
            <div>
              <h3 class="card-title"><i class="fa-solid fa-map-location-dot"></i> Bản Đồ Khí Tượng & GIS Việt Nam (Hoàng Sa & Trường Sa)</h3>
              <p style="font-size:12px;color:var(--text-muted);margin-top:2px;">
                <i class="fa-solid fa-flag" style="color:#ef4444;"></i> Bản đồ chuẩn Việt Nam • Khẳng định chủ quyền không thể tách rời đối với Quần đảo Hoàng Sa (TP. Đà Nẵng) và Quần đảo Trường Sa (Tỉnh Khánh Hòa)
              </p>
            </div>
            <div class="map-layer-toggles">"""

if old_map_header in content:
    content = content.replace(old_map_header, new_map_header)
    print("Updated Map Header")
else:
    content_norm = content.replace('\r\n', '\n')
    old_map_header_norm = old_map_header.replace('\r\n', '\n')
    if old_map_header_norm in content_norm:
        content = content_norm.replace(old_map_header_norm, new_map_header.replace('\r\n', '\n'))
        print("Updated Map Header via normalized")

# 3. Update Tab 7 Outdoor Region Filter
old_outdoor_header = """          <!-- Activity Filter Buttons -->
          <div class="activity-filters-row" id="activity-filters-container">"""

new_outdoor_header = """          <!-- Outdoor Region Filter Row (Lọc theo Miền chuẩn xác) -->
          <div class="outdoor-region-filter-row" id="outdoor-region-filters-container" style="display:flex;align-items:center;gap:8px;margin-bottom:14px;flex-wrap:wrap;padding:6px 0;border-bottom:1px solid var(--border-color);">
            <span style="font-size:12px;font-weight:700;color:var(--text-muted);"><i class="fa-solid fa-layer-group" style="color:var(--primary);"></i> Lọc theo Vùng miền:</span>
            <button class="district-pill active" id="btn-outdoor-reg-all" onclick="App.filterOutdoorRegion('all')">Tất cả (34 tỉnh)</button>
            <button class="district-pill" id="btn-outdoor-reg-bac" onclick="App.filterOutdoorRegion('Miền Bắc')">Miền Bắc (15)</button>
            <button class="district-pill" id="btn-outdoor-reg-trung" onclick="App.filterOutdoorRegion('Miền Trung')">Miền Trung (8)</button>
            <button class="district-pill" id="btn-outdoor-reg-taynguyen" onclick="App.filterOutdoorRegion('Tây Nguyên')">Tây Nguyên (3)</button>
            <button class="district-pill" id="btn-outdoor-reg-nam" onclick="App.filterOutdoorRegion('Miền Nam')">Miền Nam (8)</button>
          </div>

          <!-- Activity Filter Buttons -->
          <div class="activity-filters-row" id="activity-filters-container">"""

if old_outdoor_header in content:
    content = content.replace(old_outdoor_header, new_outdoor_header)
    print("Updated Outdoor Tab Filters")
else:
    content_norm = content.replace('\r\n', '\n')
    old_outdoor_header_norm = old_outdoor_header.replace('\r\n', '\n')
    if old_outdoor_header_norm in content_norm:
        content = content_norm.replace(old_outdoor_header_norm, new_outdoor_header.replace('\r\n', '\n'))
        print("Updated Outdoor Tab Filters via normalized")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("index.html patched successfully!")
