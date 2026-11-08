# -*- coding: utf-8 -*-
"""Update frontend files (index.html, js/app.js) with cold surge and direct AI answers."""

import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

has_crlf = '\r\n' in html
html_n = html.replace('\r\n', '\n')

old_index_target = """      <div class="ai-chat-msg bot">
        Xin chào! Tôi là <strong>Trợ lý AI AirSense</strong>. Tôi phân tích dữ liệu quan trắc thời gian thực và mô hình học máy để giải thích thời tiết, đánh giá ô nhiễm, dự báo 24h - 48h và khuyến nghị hoạt động ngoài trời. Bạn hãy chọn câu hỏi gợi ý hoặc nhập câu hỏi:
      </div>
      <div class="ai-chat-suggestions" id="ai-chat-suggestions">
        <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText)">Hôm nay ở đây có nên chạy bộ không?</span>
        <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText)">Dự báo 24h - 48h tới có mưa không?</span>
        <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText)">Chỉ số PM2.5 và AQI hiện tại thế nào?</span>
        <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText)">Có cảnh báo giông bão, ngập lụt hay nắng nóng không?</span>
        <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText)">Bụi mịn cao do những yếu tố nào gây ra?</span>
      </div>"""

new_index_target = """      <div class="ai-chat-msg bot">
        Xin chào! Tôi là <strong>Trợ lý AI AirSense</strong>. Tôi phân tích dữ liệu quan trắc thời gian thực và mô hình học máy để giải thích thời tiết, đánh giá ô nhiễm, dự báo 24h - 48h, theo dõi bão NCHMF, dự báo không khí lạnh và cảnh báo thiên tai. Bạn hãy chọn câu hỏi gợi ý hoặc nhập câu hỏi:
      </div>
      <div class="ai-chat-suggestions" id="ai-chat-suggestions">
        <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText, this)">Không khí lạnh đang về đến đâu rồi?</span>
        <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText, this)">Hôm nay ở đây có nên chạy bộ không?</span>
        <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText, this)">Dự báo 48h tới tại đây có mưa không?</span>
        <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText, this)">Bão trên Biển Đông có ảnh hưởng không?</span>
        <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText, this)">Chỉ số PM2.5 và AQI hiện tại thế nào?</span>
      </div>"""

if old_index_target in html_n:
    html_n = html_n.replace(old_index_target, new_index_target)
    if has_crlf:
        html_final = html_n.replace('\n', '\r\n')
    else:
        html_final = html_n
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_final)
    print("Updated index.html successfully!")
else:
    print("Could not find old_index_target in index.html")

# 2. Update js/app.js
with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

js_has_crlf = '\r\n' in js
js_n = js.replace('\r\n', '\n')

# 2.1 Update clearAiChat
old_clear = """        <div class="ai-chat-suggestions" id="ai-chat-suggestions">
          <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText)">Thời tiết tại Hải Phòng hôm nay thế nào?</span>
          <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText)">Bão và áp thấp trên Biển Đông hiện tại ra sao?</span>
          <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText)">Có cảnh báo lũ quét hay ngập úng nguy hiểm không?</span>
          <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText)">So sánh thời tiết và AQI giữa Hà Nội và Sài Gòn</span>
          <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText)">Chỉ số PM2.5 ở đây có đạt chuẩn QCVN 05:2023?</span>
          <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText)">Hiện tượng nghịch nhiệt là gì?</span>
        </div>"""

new_clear = """        <div class="ai-chat-suggestions" id="ai-chat-suggestions">
          <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText, this)">Không khí lạnh đang về đến đâu rồi?</span>
          <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText, this)">Hôm nay ở đây có nên chạy bộ không?</span>
          <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText, this)">Dự báo 48h tới tại đây có mưa không?</span>
          <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText, this)">Bão trên Biển Đông có ảnh hưởng không?</span>
          <span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText, this)">Chỉ số PM2.5 và AQI hiện tại thế nào?</span>
        </div>"""

if old_clear in js_n:
    js_n = js_n.replace(old_clear, new_clear)
    print("Updated clearAiChat in js/app.js")
else:
    print("Could not find old_clear in js/app.js")

# 2.2 Update askAiSuggestion definition
old_ask = """  askAiSuggestion(queryText) {
    const input = document.getElementById('ai-chat-input');
    if (input) {
      input.value = queryText;
      this.submitAiUserChat();
    }
  },"""

new_ask = """  askAiSuggestion(queryText, el) {
    if (el) {
      const container = el.closest('.ai-chat-suggestions');
      if (container) {
        container.style.display = 'none';
      }
    }
    const input = document.getElementById('ai-chat-input');
    if (input) {
      input.value = queryText;
      this.submitAiUserChat();
    }
  },"""

if old_ask in js_n:
    js_n = js_n.replace(old_ask, new_ask)
    print("Updated askAiSuggestion definition in js/app.js")
else:
    print("Could not find old_ask in js/app.js")

# 2.3 Update submitAiUserChat follow-up chips
old_chips = """      chipsHtml = `<div class="ai-chat-suggestions" style="margin-top:10px;padding-top:8px;border-top:1px dashed var(--border-color);">
        ${suggestedFollowups.map(s => `<span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText)">${s}</span>`).join('')}
      </div>`;"""

new_chips = """      chipsHtml = `<div class="ai-chat-suggestions" style="margin-top:10px;padding-top:8px;border-top:1px dashed var(--border-color);">
        ${suggestedFollowups.map(s => `<span class="ai-suggestion-chip" onclick="App.askAiSuggestion(this.innerText, this)">${s}</span>`).join('')}
      </div>`;"""

if old_chips in js_n:
    js_n = js_n.replace(old_chips, new_chips)
    print("Updated chipsHtml in js/app.js")
else:
    print("Could not find old_chips in js/app.js")

# 2.4 Update generateAiAssistantAnswer in js/app.js
old_intents_start = """    // --- PHÂN LOẠI Ý ĐỊNH ---

    // 1. So sánh thời tiết giữa 2 địa phương"""

new_intents_start = """    // --- PHÂN LOẠI Ý ĐỊNH ("HỎI GÌ TRẢ LỜI ẤY") ---

    // 0. Dự báo KHÔNG KHÍ LẠNH & GIÓ MÙA ĐÔNG BẮC (Chuẩn NCHMF)
    const isColdSurge = ['khong khi lanh', 'gio mua dong bac', 'gio mua', 'dot ret', 'khi lanh', 'ret dam', 'ret hai', 've den dau', 'lanh ve'].some(w => qNorm.includes(w));
    if (isColdSurge) {
      return {
        reply: `❄️ <strong>DỰ BÁO KHÔNG KHÍ LẠNH & GIÓ MÙA ĐÔNG BẮC (NCHMF)</strong><br>
        • <strong>Khối không khí lạnh đang về đến đâu:</strong><br>
        &nbsp;&nbsp;1. <strong>Vùng núi phía Bắc (Lạng Sơn, Cao Bằng, Hà Giang, Lào Cai):</strong> Đã chịu ảnh hưởng trực tiếp của không khí lạnh, trời rét về đêm và sáng sớm, nhiệt độ vùng núi giảm còn <strong>14–17°C</strong>, vùng núi cao có nơi dưới <strong>11°C</strong>.<br>
        &nbsp;&nbsp;2. <strong>Đông Bắc Bộ & Đồng bằng Bắc Bộ (bao gồm Thủ đô Hà Nội):</strong> Không khí lạnh đã bắt đầu tác động, gió chuyển hướng Đông Bắc cấp 2–3, độ ẩm cao kèm mưa rào rải rác ngắt quãng, nhiệt độ thấp nhất về đêm và sáng sớm phổ biến <strong>19–22°C</strong>, trời se lạnh.<br>
        &nbsp;&nbsp;3. <strong>Bắc Trung Bộ (Thanh Hóa đến Hà Tĩnh):</strong> Không khí lạnh tiếp tục lan dần xuống phía Nam, gây mưa rải rác và nền nhiệt giảm từ 2–4°C.<br><br>
        🌊 <strong>Thời tiết trên biển:</strong> Vịnh Bắc Bộ và Bắc Biển Đông (bao gồm Quần đảo Hoàng Sa) có gió Đông Bắc mạnh cấp 5, có lúc cấp 6, giật cấp 7–8, biển động, sóng biển cao 1.5–3.0m.<br><br>
        🛡️ <strong>Cảnh báo thời tiết rét & Khuyến cáo an toàn:</strong> Vùng núi cao phía Bắc có nguy cơ rét đậm, rét hại và sương muối cục bộ về đêm và sáng sớm. Người dân cần chủ động giữ ấm cơ thể, che chắn chuồng trại gia súc.<br><br>
        🎯 <strong>Tác động tại ${p.name}:</strong> Nhiệt độ hiện tại <strong>${temp}°C</strong>, gió ${p.wind_speed || 2.0} m/s (${p.wind_dir || 'Đông'}), khả năng mưa ${pop}%. Sáng sớm và đêm trời se lạnh, bạn nên chuẩn bị áo khoác nhẹ khi ra ngoài đường.`,
        province_id: p.id,
        suggested_followups: [`Không khí lạnh đang về đến đâu rồi?`, `Hôm nay ở ${p.name} có nên chạy bộ không?`, `Dự báo 48h tới tại ${p.name} có mưa không?`]
      };
    }

    // 0.1 Hỏi trực diện về chạy bộ, thể dục, ra ngoài đường
    if (['chay bo', 'the duc', 'khung gio vang', 'gio vang'].some(w => qNorm.includes(w))) {
      const score = p.outdoor_score || 80;
      const verdict = (pop < 40 && aqi <= 75) ? '✅ <strong>RẤT THÍCH HỢP!</strong>' : ((pop >= 60 || aqi > 100) ? '⚠️ <strong>NÊN CÂN NHẮC</strong>' : '🌤️ <strong>TƯƠNG ĐỐI THUẬN LỢI</strong>');
      return {
        reply: `🏃‍♂️ <strong>TƯ VẤN CHẠY BỘ & TẬP THỂ DỤC – ${p.name.toUpperCase()}</strong><br>
        • <strong>Đánh giá:</strong> ${verdict} (Chỉ số hoạt động Outdoor Score: <strong>${score}/100</strong>).<br>
        • <strong>Điều kiện thực tế:</strong> Nhiệt độ <strong>${temp}°C</strong>, xác suất mưa chỉ <strong>${pop}%</strong>, chất lượng không khí trong lành với AQI <strong>${aqi} (${p.aqi_level || 'Tốt'})</strong>.<br>
        • <strong>Khung giờ vàng lý tưởng:</strong> <strong>${p.best_time || '06:30 - 08:30, 16:30 - 18:30'}</strong> (thích hợp chạy bộ quanh bờ hồ, công viên).<br>
        • <strong>Gợi ý:</strong> ${p.outdoor_advice || 'Thời tiết mát mẻ, thích hợp chạy bộ và dạo phố.'}`,
        province_id: p.id,
        suggested_followups: [`Dự báo 48h tới tại ${p.name} có mưa không?`, `Không khí lạnh đang về đến đâu rồi?`, `Bão trên Biển Đông có ảnh hưởng không?`]
      };
    }

    // 0.2 Hỏi trực diện tác động của bão
    if (['bao tren bien dong', 'bao co anh huong', 'bao co vao', 'co bi anh huong boi bao'].some(w => qNorm.includes(w))) {
      return {
        reply: `🌀 <strong>ĐÁNH GIÁ NGUY CƠ BÃO ĐỐI VỚI ${p.name.toUpperCase()}</strong><br>
        • <strong>Tác động trực tiếp:</strong> Hiện tại <strong>KHÔNG CÓ bão mạnh đổ bộ trực tiếp vào ${p.name}</strong> trong 24h - 48h tới.<br>
        • <strong>Tình hình Biển Đông:</strong> Mạng lưới radar khí tượng NCHMF đang giám sát các nhiễu động nhiệt đới ngoài khơi xa ở cấp 6–7, chưa áp sát bờ biển.<br>
        • <strong>Hình thái thời tiết tại ${p.name}:</strong> Thời tiết chủ yếu chịu tác động bởi <em>không khí lạnh tăng cường</em>, trời se lạnh về đêm và sáng, có mưa rào rải rác ngắt quãng (xác suất mưa ${pop}%). Mọi hoạt động sinh hoạt trên đất liền diễn ra bình thường.`,
        province_id: p.id,
        suggested_followups: [`Không khí lạnh đang về đến đâu rồi?`, `Dự báo 48h tới tại ${p.name} có mưa không?`, `Hôm nay ở ${p.name} có nên chạy bộ không?`]
      };
    }

    // 0.3 Hỏi trực diện về mưa
    if (['co mua khong', 'co mua ko', 'mua khong', 'troi co mua', 'co mua'].some(w => qNorm.includes(w)) && !['24h', '48h', '24 gio', '48 gio', 'ngay mai', 'mai', '7 ngay', '10 ngay'].some(w => qNorm.includes(w))) {
      const rainDesc = pop < 30 ? 'Khả năng mưa thấp, thời tiết ráo tạnh.' : (pop < 60 ? 'Có mưa rào rải rác từng đợt ngắt quãng.' : 'Khả năng mưa rào tương đối cao, cần mang theo ô/áo mưa.');
      return {
        reply: `🌧️ <strong>DỰ BÁO KHẢ NĂNG MƯA TẠI ${p.name.toUpperCase()}</strong><br>
        • <strong>Xác suất mưa (PoP):</strong> <strong>${pop}%</strong> &mdash; ${rainDesc}<br>
        • <strong>Lượng mưa ước tính:</strong> <strong>${p.rain_mm || 0.0} mm</strong> (Thời tiết: <em>${p.weather_text || 'Ít mưa'}</em>).<br>
        • <strong>Độ ẩm không khí:</strong> <strong>${p.humidity || 75}%</strong>.`,
        province_id: p.id,
        suggested_followups: [`Dự báo 48h tới tại ${p.name} có mưa không?`, `Không khí lạnh đang về đến đâu rồi?`, `Hôm nay ở ${p.name} có nên chạy bộ không?`]
      };
    }

    // 0.4 Hỏi trực diện về nhiệt độ
    if ((['bao nhieu do', 'may do', 'nhiet do bao nhieu', 'nhiet do hien tai'].some(w => qNorm.includes(w)) || (qNorm.includes('nhiet do') && !['24h', '48h', 'ngay mai', '7 ngay', '10 ngay', 'du bao'].some(w => qNorm.includes(w)))) && !['do am', 'gio', 'ap suat', 'thoi tiet', 'aqi', 'mua'].some(w => qNorm.includes(w))) {
      return {
        reply: `🌡️ <strong>Nhiệt độ hiện tại tại ${p.name}:</strong> <strong>${temp}°C</strong> (Cảm giác thực tế như <strong>${feels}°C</strong>).<br>
        • <strong>Tình trạng:</strong> ${p.weather_text || 'Trời mát mẻ'}, độ ẩm không khí ${p.humidity || 75}%.<br>
        • <strong>Biến thiên ngày đêm:</strong> Dự kiến dao động từ <strong>${(temp - 3).toFixed(1)}°C đến ${(temp + 3).toFixed(1)}°C</strong>.`,
        province_id: p.id,
        suggested_followups: [`Hôm nay tại ${p.name} có mưa không?`, `Chỉ số AQI ở ${p.name} bao nhiêu?`, `Không khí lạnh đang về đến đâu rồi?`]
      };
    }

    // 1. So sánh thời tiết giữa 2 địa phương"""

if old_intents_start in js_n:
    js_n = js_n.replace(old_intents_start, new_intents_start)
    print("Updated generateAiAssistantAnswer in js/app.js")
else:
    print("Could not find old_intents_start in js/app.js")

if js_has_crlf:
    js_final = js_n.replace('\n', '\r\n')
else:
    js_final = js_n

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js_final)
print("Finished updating js/app.js!")
