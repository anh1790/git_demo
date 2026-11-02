"""
Frontend DOM & Structure Unit Tests.
Kiểm thử cấu trúc giao diện HTML, các thành phần tương tác, responsive meta,
navigation tabs, form controls, và các container dữ liệu.
"""

from bs4 import BeautifulSoup
import pytest

def test_html_doctype_and_metadata(index_html_content):
    soup = BeautifulSoup(index_html_content, "html.parser")
    # 1. Kiểm tra tiêu đề và bộ ký tự UTF-8
    assert soup.title is not None
    assert "AI WEATHER & AIR QUALITY" in soup.title.string or "Smart Weather" in soup.title.string
    
    # 2. Viewport responsive cho Desktop, Tablet và Mobile
    viewport = soup.find("meta", attrs={"name": "viewport"})
    assert viewport is not None
    assert "width=device-width" in viewport.get("content", "")

def test_navigation_sidebar_all_7_tabs(index_html_content):
    soup = BeautifulSoup(index_html_content, "html.parser")
    expected_tabs = [
        "tab-overview",
        "tab-weather",
        "tab-compare",
        "tab-airquality",
        "tab-aiforecast",
        "tab-map",
        "tab-outdoor"
    ]
    nav_buttons = soup.find_all("button", attrs={"data-tab": True})
    rendered_tabs = [btn["data-tab"] for btn in nav_buttons]
    for tab in expected_tabs:
        assert tab in rendered_tabs, f"Thieu nut dieu huong cho tab: {tab}"

def test_all_7_tab_panes_present(index_html_content):
    soup = BeautifulSoup(index_html_content, "html.parser")
    expected_panes = [
        "tab-overview",
        "tab-weather",
        "tab-compare",
        "tab-airquality",
        "tab-aiforecast",
        "tab-map",
        "tab-outdoor"
    ]
    for pane_id in expected_panes:
        pane = soup.find("div", id=pane_id)
        assert pane is not None, f"Thieu tab pane container id='{pane_id}'"
        assert "tab-pane" in pane.get("class", [])

def test_header_and_search_controls(index_html_content):
    soup = BeautifulSoup(index_html_content, "html.parser")
    # Nút làm mới dữ liệu
    btn_refresh = soup.find("button", id="btn-refresh")
    assert btn_refresh is not None
    assert "App.refreshAllDataWithAnimation()" in btn_refresh.get("onclick", "")

    # Ô tìm kiếm địa phương
    input_search = soup.find("input", id="input-location-search")
    assert input_search is not None
    assert "34 tỉnh" in input_search.get("placeholder", "")

    # Dropdown kết quả tìm kiếm
    dropdown = soup.find("div", id="search-results-dropdown")
    assert dropdown is not None

def test_region_pills_filter(index_html_content):
    soup = BeautifulSoup(index_html_content, "html.parser")
    container = soup.find("div", id="region-pills-container")
    assert container is not None
    pills = container.find_all("button", class_="district-pill")
    pill_texts = [p.get_text(strip=True) for p in pills]
    assert any("Tất cả" in t for t in pill_texts)
    assert any("Miền Bắc" in t for t in pill_texts)
    assert any("Miền Trung" in t for t in pill_texts)
    assert any("Tây Nguyên" in t for t in pill_texts)
    assert any("Miền Nam" in t for t in pill_texts)

def test_ai_forecast_tab_components(index_html_content):
    soup = BeautifulSoup(index_html_content, "html.parser")
    pane = soup.find("div", id="tab-aiforecast")
    assert pane is not None

    # Nút chọn 3 mô hình ML
    btn_rf = pane.find("button", id="btn-model-rf")
    btn_nn = pane.find("button", id="btn-model-nn")
    btn_base = pane.find("button", id="btn-model-base")
    assert btn_rf is not None and "Random_Forest" in btn_rf.get("onclick", "")
    assert btn_nn is not None and "Neural_Network" in btn_nn.get("onclick", "")
    assert btn_base is not None and "Baseline_Persistence" in btn_base.get("onclick", "")

    # Nút chọn chế độ Int8 Quantized và FP32
    btn_opt = pane.find("button", id="btn-precision-opt")
    btn_fp32 = pane.find("button", id="btn-precision-fp32")
    assert btn_opt is not None
    assert btn_fp32 is not None

    # Canvas vẽ biểu đồ dự báo
    canvas = pane.find("canvas", id="forecastChart")
    assert canvas is not None

def test_concurrency_load_test_ui(index_html_content):
    soup = BeautifulSoup(index_html_content, "html.parser")
    # Nút kiểm thử 12 CCU
    btn_12 = soup.find("button", id="btn-concurrency-test")
    assert btn_12 is not None
    assert "App.runLiveConcurrencyTest(12)" in btn_12.get("onclick", "")

    # Nút kiểm thử 20 CCU
    btn_20 = soup.find("button", id="btn-concurrency-test-20")
    assert btn_20 is not None
    assert "App.runLiveConcurrencyTest(20)" in btn_20.get("onclick", "")

    # Hộp log console kiểm thử tải
    console_box = soup.find("div", id="concurrency-console-box")
    assert console_box is not None

def test_weather_map_and_sovereignty_assertion(index_html_content):
    soup = BeautifulSoup(index_html_content, "html.parser")
    map_pane = soup.find("div", id="tab-map")
    assert map_pane is not None

    # Container bản đồ Leaflet
    map_div = map_pane.find("div", id="weather-leaflet-map")
    assert map_div is not None

    # Tuyên bố khẳng định chủ quyền Hoàng Sa & Trường Sa
    text = map_pane.get_text()
    assert "Hoàng Sa" in text, "Thiếu ghi nhận Hoàng Sa trên bản đồ"
    assert "Trường Sa" in text, "Thiếu ghi nhận Trường Sa trên bản đồ"
    assert "Đà Nẵng" in text or "Khánh Hòa" in text

def test_outdoor_tab_region_filters(index_html_content):
    soup = BeautifulSoup(index_html_content, "html.parser")
    outdoor_pane = soup.find("div", id="tab-outdoor")
    assert outdoor_pane is not None

    # Các nút lọc vùng miền của Tab 7
    reg_container = outdoor_pane.find("div", id="outdoor-region-filters-container")
    assert reg_container is not None
    assert outdoor_pane.find("button", id="btn-outdoor-reg-all") is not None
    assert outdoor_pane.find("button", id="btn-outdoor-reg-bac") is not None
    assert outdoor_pane.find("button", id="btn-outdoor-reg-trung") is not None
    assert outdoor_pane.find("button", id="btn-outdoor-reg-taynguyen") is not None
    assert outdoor_pane.find("button", id="btn-outdoor-reg-nam") is not None

def test_mobile_bottom_navigation_bar(index_html_content):
    soup = BeautifulSoup(index_html_content, "html.parser")
    mobile_nav = soup.find("nav", class_="mobile-bottom-nav")
    assert mobile_nav is not None
    mobile_btns = mobile_nav.find_all("button", class_="mobile-nav-btn")
    assert len(mobile_btns) >= 5, "Mobile bottom navigation phải có ít nhất 5 tab chính"
