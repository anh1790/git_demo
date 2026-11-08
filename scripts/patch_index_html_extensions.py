import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
html_path = os.path.join(ROOT, "index.html")

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add GPS button and Favorites container to search bar row
old_search_row = """            <input type="text" id="input-location-search" placeholder="Tìm kiếm nhanh trong 34 tỉnh thành hoặc 101 trạm đo (Hà Nội, Tây Ninh, TP.HCM, Đà Nẵng, Sa Pa, Núi Bà Đen...)..." autocomplete="off">
            <div class="search-results-dropdown" id="search-results-dropdown"></div>
          </div>
          <!-- Menu thả xuống chọn nhanh 34 Tỉnh Thành (Không bị tràn màn hình) -->"""

new_search_row = """            <input type="text" id="input-location-search" placeholder="Tìm kiếm nhanh trong 34 tỉnh thành hoặc 101 trạm đo (Hà Nội, Tây Ninh, TP.HCM, Đà Nẵng, Sa Pa, Núi Bà Đen...)..." autocomplete="off">
            <div class="search-results-dropdown" id="search-results-dropdown"></div>
          </div>
          <!-- Nút Định Vị GPS Vị Trí Hiện Tại -->
          <button class="btn-icon-action" id="btn-gps-locate" onclick="App.locateUserGPS()" title="Định vị GPS vị trí hiện tại của bạn">
            <i class="fa-solid fa-location-crosshairs"></i> <span>Định vị</span>
          </button>
          <!-- Menu thả xuống chọn nhanh 34 Tỉnh Thành (Không bị tràn màn hình) -->"""

if old_search_row in content:
    content = content.replace(old_search_row, new_search_row)
    print("Added GPS button to search row")

# Add favorites bar below search-bar-row
old_search_bar_end = """          <div class="quick-city-badge">
            <i class="fa-solid fa-tower-broadcast" style="color:var(--accent-teal);"></i>
            <span>Mạng lưới: <strong>34 Tỉnh / 101 Trạm Đo</strong></span>
          </div>
        </div>"""

new_search_bar_end = """          <div class="quick-city-badge">
            <i class="fa-solid fa-tower-broadcast" style="color:var(--accent-teal);"></i>
            <span>Mạng lưới: <strong>34 Tỉnh / 101 Trạm Đo</strong></span>
          </div>
        </div>
        <!-- Thanh Địa Điểm Yêu Thích (Lưu LocalStorage) -->
        <div class="favorites-chips-bar" id="favorites-chips-container">
          <!-- Injected by JS: Yêu thích chips -->
        </div>"""

if old_search_bar_end in content:
    content = content.replace(old_search_bar_end, new_search_bar_end)
    print("Added favorites bar below search row")

# Add alert banner right before Tab 1
old_tab_overview = """      <!-- TAB 1: TỔNG QUAN (OVERVIEW) -->
      <div class="tab-pane active" id="tab-overview">"""

new_tab_overview = """      <!-- CẢNH BÁO THỜI TIẾT & Ô NHIỄM KHẨN CẤP (BANNER ĐA CẤP ĐỘ) -->
      <div id="weather-alert-banner" class="weather-alert-banner" style="display:none;"></div>

      <!-- TAB 1: TỔNG QUAN (OVERVIEW) -->
      <div class="tab-pane active" id="tab-overview">"""

if old_tab_overview in content:
    content = content.replace(old_tab_overview, new_tab_overview)
    print("Added alert banner before Tab 1")

# Add favorite star button next to hero-location-name
old_hero_badge = """                <span class="weather-location-pill" id="hero-location-name">
                  <i class="fa-solid fa-location-dot"></i> Hà Nội • Thủ đô
                </span>"""

new_hero_badge = """                <span class="weather-location-pill" id="hero-location-name">
                  <i class="fa-solid fa-location-dot"></i> Hà Nội • Thủ đô
                </span>
                <button class="btn-favorite-star" id="btn-toggle-favorite" onclick="App.toggleFavoriteCurrentProvince()" title="Lưu/Bỏ lưu địa điểm yêu thích">
                  <i class="fa-regular fa-star"></i>
                </button>"""

if old_hero_badge in content:
    content = content.replace(old_hero_badge, new_hero_badge)
    print("Added favorite star button to hero header")

# Add hourly 24/48h toggle and daily 7/10d toggle in Tab 2
old_hourly_title = """          <h4 style="font-size:14px;color:var(--text-muted);margin-bottom:12px;">DỰ BÁO TỪNG GIỜ (24H SLIDER):</h4>"""
new_hourly_title = """          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
            <h4 style="font-size:14px;color:var(--text-muted);margin:0;">DỰ BÁO TỪNG GIỜ (SLIDER LIÊN TỤC):</h4>
            <div class="horizon-toggle-group">
              <button class="horizon-btn active" id="btn-hourly-24" onclick="App.setHourlyHorizon(24)">24 Giờ</button>
              <button class="horizon-btn" id="btn-hourly-48" onclick="App.setHourlyHorizon(48)">48 Giờ (AI)</button>
            </div>
          </div>"""

if old_hourly_title in content:
    content = content.replace(old_hourly_title, new_hourly_title)
    print("Added hourly horizon toggle to Tab 2")

old_daily_title = """          <h4 style="font-size:14px;color:var(--text-muted);margin:24px 0 12px 0;">DỰ BÁO 7 NGÀY TIẾP THEO:</h4>"""
new_daily_title = """          <div style="display:flex;align-items:center;justify-content:space-between;margin:24px 0 12px 0;">
            <h4 style="font-size:14px;color:var(--text-muted);margin:0;">DỰ BÁO NHIỀU NGÀY TỚI:</h4>
            <div class="horizon-toggle-group">
              <button class="horizon-btn active" id="btn-daily-7" onclick="App.setDailyHorizon(7)">7 Ngày</button>
              <button class="horizon-btn" id="btn-daily-10" onclick="App.setDailyHorizon(10)">10 Ngày (Mở rộng)</button>
            </div>
          </div>"""

if old_daily_title in content:
    content = content.replace(old_daily_title, new_daily_title)
    print("Added daily horizon toggle to Tab 2")

# Add weather alerts center card in Tab 2 after telemetry card
old_tab_weather_end = """            <div class="telemetry-box">
              <span class="telemetry-label">Tầm nhìn xa</span>
              <span class="telemetry-val" id="tel-vis">10.0 km</span>
            </div>
          </div>
        </div>
      </div>"""

new_tab_weather_end = """            <div class="telemetry-box">
              <span class="telemetry-label">Tầm nhìn xa</span>
              <span class="telemetry-val" id="tel-vis">10.0 km</span>
            </div>
          </div>
        </div>

        <!-- TRUNG TÂM CẢNH BÁO THỜI TIẾT & Ô NHIỄM (8 NHÓM THIÊN TAI) -->
        <div class="card" id="card-weather-alerts-center" style="margin-top:16px;">
          <div class="card-header" style="display:flex;align-items:center;justify-content:space-between;">
            <h3 class="card-title">
              <i class="fa-solid fa-triangle-exclamation" style="color:#ef4444;"></i>
              Hệ Thống Cảnh Báo Thiên Tai & Ô Nhiễm – <span id="alerts-city-title">Hà Nội</span>
            </h3>
            <span class="stat-badge" id="alerts-status-badge" style="background:#fee2e2;color:#991b1b;font-weight:700;">8 Nhóm Cảnh Báo</span>
          </div>
          <div id="weather-alerts-list-container" style="display:flex;flex-direction:column;gap:10px;">
            <!-- Injected by JS: Mưa lớn, giông sét, bão, nắng nóng, rét đậm, ngập lụt, ô nhiễm -->
          </div>
        </div>
      </div>"""

if old_tab_weather_end in content:
    content = content.replace(old_tab_weather_end, new_tab_weather_end)
    print("Added alerts center card to Tab 2")

# Add Cloud layer and Locate button in Tab 6 (Map)
old_map_btns = """              <button class="map-layer-btn" onclick="App.setMapLayer('wind')">Tốc độ gió (m/s)</button>
              <button class="map-layer-btn" onclick="App.setMapLayer('geopandas')"><i class="fa-solid fa-draw-polygon"></i> Ranh giới GeoPandas</button>"""

new_map_btns = """              <button class="map-layer-btn" onclick="App.setMapLayer('wind')">Tốc độ gió (m/s)</button>
              <button class="map-layer-btn" onclick="App.setMapLayer('clouds')"><i class="fa-solid fa-cloud"></i> Mây trời (%)</button>
              <button class="map-layer-btn" onclick="App.locateUserOnMap()"><i class="fa-solid fa-crosshairs"></i> Vị trí của tôi</button>
              <button class="map-layer-btn" onclick="App.setMapLayer('geopandas')"><i class="fa-solid fa-draw-polygon"></i> Ranh giới GeoPandas</button>"""

if old_map_btns in content:
    content = content.replace(old_map_btns, new_map_btns)
    print("Added Cloud layer and Locate button to map buttons")

# Add AI Assistant Chatbot widget before </body>
ai_chat_html = """
  <!-- =========================================================================
       TRỢ LÝ AI HỎI ĐÁP THỜI TIẾT & CHẤT LƯỢNG KHÔNG KHÍ (INTERACTIVE AI ASSISTANT)
       ========================================================================= -->
  <div class="ai-assistant-fab-container">
    <button class="ai-assistant-fab" onclick="App.toggleAiChat()" id="btn-ai-fab">
      <i class="fa-solid fa-robot"></i> <span>Trợ lý AI</span> <span class="ai-online-dot"></span>
    </button>
  </div>

  <div class="ai-chat-window" id="ai-chat-window" style="display:none;">
    <div class="ai-chat-header">
      <div style="display:flex;align-items:center;gap:10px;">
        <i class="fa-solid fa-robot" style="font-size:20px;"></i>
        <div>
          <div style="font-weight:800;font-size:14px;">Trợ Lý AI AirSense</div>
          <div style="font-size:11px;opacity:0.9;">Hỏi đáp thời tiết, AQI & khuyến nghị</div>
        </div>
      </div>
      <button style="background:transparent;border:none;color:#fff;font-size:18px;cursor:pointer;" onclick="App.toggleAiChat()"><i class="fa-solid fa-xmark"></i></button>
    </div>
    <div class="ai-chat-body" id="ai-chat-body">
      <div class="ai-chat-msg bot">
        Xin chào! Tôi là <strong>Trợ lý AI AirSense</strong>. Tôi phân tích dữ liệu quan trắc thời gian thực và mô hình học máy để giải thích thời tiết, đánh giá ô nhiễm, dự báo 24h - 48h và khuyến nghị hoạt động ngoài trời. Bạn hãy chọn câu hỏi gợi ý hoặc nhập câu hỏi:
      </div>
      <div class="ai-chat-suggestions" id="ai-chat-suggestions">
        <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText)">Hôm nay ở đây có nên chạy bộ không?</span>
        <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText)">Dự báo 24h - 48h tới có mưa không?</span>
        <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText)">Chỉ số PM2.5 và AQI hiện tại thế nào?</span>
        <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText)">Có cảnh báo giông bão, ngập lụt hay nắng nóng không?</span>
        <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText)">Bụi mịn cao do những yếu tố nào gây ra?</span>
      </div>
    </div>
    <form class="ai-chat-footer" onsubmit="event.preventDefault(); App.submitAiUserChat();">
      <input type="text" class="ai-chat-input" id="ai-chat-input" placeholder="Hỏi về thời tiết, ô nhiễm, hoạt động ngoài trời..." autocomplete="off">
      <button type="submit" class="ai-chat-send" title="Gửi câu hỏi"><i class="fa-solid fa-paper-plane"></i></button>
    </form>
  </div>
"""

if "ai-assistant-fab-container" not in content:
    content = content.replace("</body>", ai_chat_html + "\n</body>")
    print("Added AI Assistant Chatbot widget before </body>")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated index.html successfully!")
