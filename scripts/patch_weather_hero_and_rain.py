import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
js_file = os.path.join(ROOT, "js", "app.js")
css_file = os.path.join(ROOT, "css", "style.css")

with open(js_file, "r", encoding="utf-8") as f:
    js_content = f.read()

# 1. Update initRainEngine and startRainAnimation
old_rain_block = """  // =========================================================================
  // DYNAMIC WEATHER ANIMATION & RAIN ENGINE
  // ========================================================================="""

# Find initRainEngine to stopRainAnimation
start_idx = js_content.find(old_rain_block)
end_idx = js_content.find("  getEffectiveWeatherCondition(baseCondition) {")

if start_idx != -1 and end_idx != -1:
    new_rain_block = """  // =========================================================================
  // DYNAMIC WEATHER ANIMATION & RAIN ENGINE
  // =========================================================================
  initRainEngine() {
    const streamContainer = document.getElementById('hero-rain-stream');
    const canvas = document.getElementById('hero-rain-canvas');
    const dropsContainer = document.getElementById('hero-rain-drops');
    if (!streamContainer || !canvas) return;

    // 1. Populate CSS fallback raindrops & sliding water trickles if empty
    if (dropsContainer && dropsContainer.children.length === 0) {
      let dropsHtml = '';
      for (let i = 0; i < 35; i++) {
        const left = Math.round((i * 2.85 + (i % 7) * 0.5) * 10) / 10;
        const dur = (0.5 + ((i * 7) % 10) * 0.035).toFixed(2);
        const delay = (-((i * 13) % 20) * 0.05).toFixed(2);
        const height = 22 + (i % 5) * 4;
        dropsHtml += `<div class="rain-streak" style="left:${left}%; animation-duration:${dur}s; animation-delay:${delay}s; height:${height}px;"></div>`;
      }
      for (let j = 0; j < 12; j++) {
        const left = (4 + j * 8).toFixed(1);
        const dur = (2.8 + (j % 4) * 0.4).toFixed(2);
        const delay = (-j * 0.3).toFixed(2);
        dropsHtml += `<div class="rain-trickle" style="left:${left}%; animation-duration:${dur}s; animation-delay:${delay}s;"></div>`;
      }
      dropsContainer.innerHTML = dropsHtml;
    }

    // 2. Setup Canvas Particles with reliable sizing
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const heroCard = document.getElementById('dynamic-weather-hero');
    const width = (streamContainer.clientWidth > 0 ? streamContainer.clientWidth : (heroCard ? heroCard.clientWidth : 0)) || 950;
    const height = (streamContainer.clientHeight > 0 ? streamContainer.clientHeight : (heroCard ? heroCard.clientHeight : 0)) || 270;

    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    canvas.style.width = '100%';
    canvas.style.height = '100%';

    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    // Create 70 realistic flowing raindrop particles
    this.rainParticles = [];
    for (let i = 0; i < 70; i++) {
      this.rainParticles.push({
        x: Math.random() * (width + 80) - 30,
        y: Math.random() * height,
        length: 16 + Math.random() * 22,
        speed: 14 + Math.random() * 12,
        opacity: 0.4 + Math.random() * 0.45,
        thickness: 1.1 + Math.random() * 1.1,
        splash: null
      });
    }

    // Create 14 gentle flowing water beads (giọt nước đang chảy xuống bề mặt kính)
    this.waterTrickles = [];
    for (let j = 0; j < 14; j++) {
      this.waterTrickles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: 1.8 + Math.random() * 1.5,
        speed: 0.9 + Math.random() * 1.4,
        tailLength: 12 + Math.random() * 16,
        opacity: 0.45 + Math.random() * 0.45
      });
    }

    this.rainCanvasContext = ctx;
    this.rainCanvasWidth = width;
    this.rainCanvasHeight = height;
  },

  startRainAnimation() {
    if (!this.rainParticles || this.rainParticles.length === 0) {
      this.initRainEngine();
    }
    if (this.rainAnimActive) return;
    this.rainAnimActive = true;

    const animate = () => {
      if (!this.rainAnimActive) return;
      const ctx = this.rainCanvasContext;
      const w = this.rainCanvasWidth || 950;
      const h = this.rainCanvasHeight || 270;
      if (!ctx) return;

      ctx.clearRect(0, 0, w, h);
      const slantX = 4.2;

      // Draw falling raindrops
      for (let i = 0; i < this.rainParticles.length; i++) {
        const p = this.rainParticles[i];
        p.x += slantX * (p.speed / 20);
        p.y += p.speed;

        // Draw active splash ripple
        if (p.splash) {
          ctx.beginPath();
          ctx.ellipse(p.splash.x, p.splash.y, p.splash.rX, p.splash.rY, 0, 0, Math.PI * 2);
          ctx.strokeStyle = `rgba(224, 242, 254, ${p.splash.opacity})`;
          ctx.lineWidth = 1;
          ctx.stroke();

          p.splash.rX += 1.3;
          p.splash.rY += 0.55;
          p.splash.opacity -= 0.12;
          if (p.splash.opacity <= 0) {
            p.splash = null;
          }
        }

        // Drop hit ground -> create splash
        if (p.y > h - 4) {
          if (Math.random() < 0.4) {
            p.splash = { x: p.x, y: h - 3, rX: 2.5, rY: 1.2, opacity: 0.65 };
          }
          p.y = -p.length - Math.random() * 25;
          p.x = Math.random() * (w + 100) - 50;
        }

        // Gradient streak
        const grad = ctx.createLinearGradient(p.x, p.y, p.x - slantX, p.y - p.length);
        grad.addColorStop(0, `rgba(255, 255, 255, ${p.opacity})`);
        grad.addColorStop(0.75, `rgba(186, 230, 253, ${p.opacity * 0.75})`);
        grad.addColorStop(1, 'rgba(255, 255, 255, 0)');

        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(p.x - slantX, p.y - p.length);
        ctx.strokeStyle = grad;
        ctx.lineWidth = p.thickness;
        ctx.lineCap = 'round';
        ctx.stroke();

        // Droplet head
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.thickness * 0.85, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${p.opacity * 0.95})`;
        ctx.fill();
      }

      // Draw sliding water trickle beads (giọt nước đang chảy xuống bề mặt kính)
      if (this.waterTrickles) {
        for (let j = 0; j < this.waterTrickles.length; j++) {
          const t = this.waterTrickles[j];
          t.y += t.speed;
          t.x += Math.sin(t.y * 0.04) * 0.25;
          if (t.y > h + 10) {
            t.y = -20;
            t.x = Math.random() * w;
          }

          // Wet water trail
          ctx.beginPath();
          ctx.moveTo(t.x, Math.max(0, t.y - t.tailLength));
          ctx.lineTo(t.x, t.y);
          ctx.strokeStyle = `rgba(224, 242, 254, ${t.opacity * 0.45})`;
          ctx.lineWidth = t.radius * 0.9;
          ctx.lineCap = 'round';
          ctx.stroke();

          // Droplet head bead
          ctx.beginPath();
          ctx.arc(t.x, t.y, t.radius, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(255, 255, 255, ${t.opacity * 0.9})`;
          ctx.fill();

          // Glass water highlight
          ctx.beginPath();
          ctx.arc(t.x - t.radius * 0.3, t.y - t.radius * 0.3, t.radius * 0.35, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(255, 255, 255, 0.95)';
          ctx.fill();
        }
      }

      this.rainAnimId = requestAnimationFrame(animate);
    };

    this.rainAnimId = requestAnimationFrame(animate);
  },

  stopRainAnimation() {
    this.rainAnimActive = false;
    if (this.rainAnimId) {
      cancelAnimationFrame(this.rainAnimId);
      this.rainAnimId = null;
    }
    if (this.rainCanvasContext) {
      this.rainCanvasContext.clearRect(0, 0, this.rainCanvasWidth || 950, this.rainCanvasHeight || 270);
    }
  },

"""
    js_content = js_content[:start_idx] + new_rain_block + js_content[end_idx:]
    print("Updated rain engine in js_content")

# 2. Update renderHeroWeather
old_render_start = "  renderHeroWeather() {"
old_render_end = "  scrubTimeOfDay(period) {"

r_start = js_content.find(old_render_start)
r_end = js_content.find(old_render_end)

if r_start != -1 and r_end != -1:
    new_render_hero = """  renderHeroWeather() {
    const p = this.getSelectedProvince();
    if (!p || !p.id) return;
    const st = this.getSelectedStation();
    const activeTemp = (st && st.temp != null) ? Number(st.temp) : (Number(p.temp) || 25);
    const activePm25 = (st && st.pm25 != null) ? Number(st.pm25) : (Number(p.pm25) || 15);
    const activeAqi = (st && st.aqi != null) ? Number(st.aqi) : Math.round(activePm25 * 1.8);
    const activeAqiLevel = (st && st.aqi_level) ? st.aqi_level : (p.aqi_level || 'Tốt');

    const condition = this.getEffectiveWeatherCondition(p.condition);
    const heroCard = document.getElementById('dynamic-weather-hero');
    if (!heroCard) return;

    // Guaranteed class reset & application
    const cssCondClass = `weather-${condition.replace(/_/g, '-')}`;
    heroCard.className = `weather-stage ${cssCondClass}`;

    // Inline style guarantee: ensures rich gradient is ALWAYS visible even if external CSS has caching issues
    const bgMap = {
      'sunny': 'linear-gradient(135deg, #0284c7 0%, #38bdf8 60%, #fdba74 100%)',
      'noon': 'linear-gradient(135deg, #0284c7 0%, #0ea5e9 40%, #38bdf8 75%, #fde047 100%)',
      'noon_rain': 'linear-gradient(135deg, #0369a1 0%, #0284c7 40%, #2563eb 75%, #60a5fa 100%)',
      'partly_cloudy': 'linear-gradient(135deg, #0369a1 0%, #0284c7 45%, #7dd3fc 100%)',
      'cloudy': 'linear-gradient(135deg, #334155 0%, #475569 50%, #94a3b8 100%)',
      'overcast': 'linear-gradient(135deg, #1e293b 0%, #334155 70%, #64748b 100%)',
      'light_rain': 'linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #60a5fa 100%)',
      'heavy_rain': 'linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #1d4ed8 100%)',
      'thunderstorm': 'linear-gradient(135deg, #09090b 0%, #1e1b4b 50%, #312e81 100%)',
      'strong_wind': 'linear-gradient(135deg, #0e7490 0%, #0284c7 50%, #38bdf8 100%)',
      'foggy': 'linear-gradient(135deg, #475569 0%, #64748b 50%, #cbd5e1 100%)',
      'night': 'linear-gradient(135deg, #020617 0%, #0b1528 50%, #1e293b 100%)',
      'night_rain': 'linear-gradient(135deg, #020617 0%, #0c1c38 50%, #172554 100%)',
      'night_thunderstorm': 'linear-gradient(135deg, #020617 0%, #180d2b 50%, #2e1065 100%)',
      'night_foggy': 'linear-gradient(135deg, #090d16 0%, #1e293b 50%, #334155 100%)',
      'sunset': 'linear-gradient(135deg, #431407 0%, #9a3412 35%, #ea580c 70%, #fde047 100%)',
      'sunset_rain': 'linear-gradient(135deg, #2b1108 0%, #7c2d12 40%, #c2410c 70%, #0369a1 100%)'
    };
    heroCard.style.background = bgMap[condition] || 'linear-gradient(135deg, #0284c7 0%, #0369a1 40%, #075985 100%)';

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

    let isRaining = false;

    if (condition === 'sunny' || condition === 'noon') {
      if (sunEl) {
        sunEl.style.display = 'block';
        sunEl.style.background = 'radial-gradient(circle, #fef08a 25%, #f59e0b 75%, #ea580c 100%)';
        sunEl.style.boxShadow = '0 0 60px rgba(251, 191, 36, 0.9), 0 0 120px rgba(245, 158, 11, 0.6)';
      }
    } else if (condition === 'noon_rain') {
      if (sunEl) {
        sunEl.style.display = 'block';
        sunEl.style.background = 'radial-gradient(circle, #fef08a 25%, #f59e0b 75%, #ea580c 100%)';
      }
      if (cloud1) cloud1.style.display = 'block';
      if (rainStream) { rainStream.style.display = 'block'; isRaining = true; }
    } else if (condition === 'partly_cloudy') {
      if (sunEl) {
        sunEl.style.display = 'block';
        sunEl.style.background = 'radial-gradient(circle, #fef08a 20%, #f59e0b 80%)';
        sunEl.style.boxShadow = '0 0 45px rgba(251, 191, 36, 0.7)';
      }
      if (cloud1) cloud1.style.display = 'block';
    } else if (condition === 'cloudy' || condition === 'overcast') {
      if (cloud1) cloud1.style.display = 'block';
      if (cloud2) cloud2.style.display = 'block';
    } else if (condition === 'light_rain') {
      if (cloud1) cloud1.style.display = 'block';
      if (rainStream) { rainStream.style.display = 'block'; isRaining = true; }
    } else if (condition === 'heavy_rain') {
      if (cloud1) cloud1.style.display = 'block';
      if (cloud2) cloud2.style.display = 'block';
      if (rainStream) { rainStream.style.display = 'block'; isRaining = true; }
    } else if (condition === 'thunderstorm') {
      if (cloud1) cloud1.style.display = 'block';
      if (cloud2) cloud2.style.display = 'block';
      if (rainStream) { rainStream.style.display = 'block'; isRaining = true; }
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
      if (rainStream) { rainStream.style.display = 'block'; isRaining = true; }
    } else if (condition === 'night_thunderstorm') {
      if (starField) starField.style.display = 'block';
      if (cloud1) cloud1.style.display = 'block';
      if (cloud2) cloud2.style.display = 'block';
      if (rainStream) { rainStream.style.display = 'block'; isRaining = true; }
      if (lightning) lightning.style.display = 'block';
    } else if (condition === 'night_foggy') {
      if (fogLayer) fogLayer.style.display = 'block';
      if (moonEl) moonEl.style.display = 'block';
    } else if (condition === 'sunset') {
      if (sunEl) {
        sunEl.style.display = 'block';
        sunEl.style.background = 'radial-gradient(circle, #fde047 20%, #ea580c 80%)';
        sunEl.style.boxShadow = '0 0 50px rgba(234, 88, 12, 0.8), 0 0 90px rgba(253, 224, 71, 0.5)';
      }
      if (cloud1) cloud1.style.display = 'block';
    } else if (condition === 'sunset_rain') {
      if (sunEl) {
        sunEl.style.display = 'block';
        sunEl.style.background = 'radial-gradient(circle, #fde047 20%, #ea580c 80%)';
        sunEl.style.boxShadow = '0 0 50px rgba(234, 88, 12, 0.8), 0 0 90px rgba(253, 224, 71, 0.5)';
      }
      if (cloud1) cloud1.style.display = 'block';
      if (rainStream) { rainStream.style.display = 'block'; isRaining = true; }
    }

    // Toggle Rain Engine
    if (isRaining) {
      this.startRainAnimation();
    } else {
      this.stopRainAnimation();
    }

    // Content adaptation per session mode
    const mode = this.timeScrubMode || 'now';
    let timeStr = '';
    let periodLabel = '';
    let displayTemp = activeTemp;
    let displayFeels = Math.round((activeTemp + 1.2) * 10) / 10;
    let displayWeatherText = p.weather_text;
    let displayAdvice = p.outdoor_advice || '';
    let displayHum = p.humidity;
    let displayWind = `${p.wind_speed} m/s ${p.wind_dir}`;
    let displayRain = `${p.rain_prob}% (${p.rain_mm}mm)`;
    let displayUv = p.uv;

    if (mode === 'noon') {
      timeStr = '12:00';
      periodLabel = 'Trưa (Nắng)';
      displayTemp = Math.round((activeTemp + 2.5) * 10) / 10;
      displayFeels = Math.round((displayTemp + 1.8) * 10) / 10;
      displayHum = Math.max(45, p.humidity - 12);
      displayUv = Math.max(p.uv, 8.5);
      if (condition === 'noon_rain') {
        displayWeatherText = 'Trưa có mưa rào rải rác, trời se mát';
        displayAdvice = `Thời tiết trưa tại ${p.name} có mưa rào nhẹ đan xen nắng trưa, thích hợp nghỉ ngơi hoặc dùng bữa trong nhà.`;
      } else {
        displayWeatherText = 'Trưa nắng rực rỡ, trời quang mây';
        displayAdvice = `Thời tiết trưa tại ${p.name}: Nắng vàng ấm áp, gió mát. ${p.outdoor_advice || 'Nên mang kính râm và mũ nón khi di chuyển ngoài trời.'}`;
        displayRain = '5% (0.0mm)';
      }
    } else if (mode === 'sunset') {
      timeStr = '17:45';
      periodLabel = 'Hoàng hôn';
      displayTemp = Math.round((activeTemp - 0.8) * 10) / 10;
      displayFeels = Math.round((displayTemp + 0.4) * 10) / 10;
      displayHum = Math.min(90, p.humidity + 6);
      displayUv = 1.5;
      if (condition === 'sunset_rain') {
        displayWeatherText = 'Mưa chiều hoàng hôn, không khí se lạnh';
        displayAdvice = `Hoàng hôn tại ${p.name} có mưa bay lãng mạn xứ Huế, thích hợp ngắm cảnh kèm ô/áo mưa mỏng.`;
      } else {
        displayWeatherText = 'Hoàng hôn buông xuống, trời se lạnh và dịu mát';
        displayAdvice = `Khung cảnh chiều tà tại ${p.name} tuyệt đẹp, hoàng hôn nhuộm đỏ đường chân trời, rất lý tưởng đi dạo hoặc chụp ảnh.`;
        displayRain = '10% (0.0mm)';
      }
    } else if (mode === 'night') {
      timeStr = '21:30';
      periodLabel = 'Đêm (Trăng sao)';
      displayTemp = Math.round((activeTemp - 3.2) * 10) / 10;
      displayFeels = Math.round((displayTemp - 0.4) * 10) / 10;
      displayHum = Math.min(95, p.humidity + 10);
      displayUv = 0;
      if (condition === 'night_rain' || condition === 'night_thunderstorm') {
        displayWeatherText = 'Mưa đêm rả rích, trời trở lạnh về khuya';
        displayAdvice = `Đêm tại ${p.name} có mưa và gió lạnh, thích hợp quây quần trong nhà hoặc thưởng thức trà nóng.`;
      } else {
        displayWeatherText = 'Đêm trăng sao thanh bình, gió nhẹ mát lành';
        displayAdvice = `Bầu trời đêm tại ${p.name} trong xanh vằng vặc trăng sao, gió nhẹ trong lành mát mẻ, lý tưởng để nghỉ ngơi thư giãn.`;
        displayRain = '5% (0.0mm)';
      }
    } else {
      // mode === 'now'
      const now = new Date();
      const hr = now.getHours();
      timeStr = `${String(hr).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
      periodLabel = (hr >= 18 || hr < 6) ? 'Ban đêm' : (hr >= 17 ? 'Hoàng hôn' : 'Ban ngày');
    }

    const aqi = Math.round(activePm25 * 1.8);
    const condIcon = this.getConditionIcon(condition);

    const setElText = (id, text) => {
      const el = document.getElementById(id);
      if (el) el.innerText = text;
    };
    const setElHtml = (id, html) => {
      const el = document.getElementById(id);
      if (el) el.innerHTML = html;
    };

    setElHtml('hero-location-name', `<i class="fa-solid fa-location-dot"></i> ${p.name} • ${p.type}`);
    setElHtml('hero-cond-badge', `${condIcon} ${displayWeatherText} <span style="opacity:0.85;font-size:11px;margin-left:4px;">(${timeStr} • ${periodLabel})</span>`);
    setElText('hero-temp-val', `${displayTemp}°`);
    setElText('hero-feels-val', `Cảm giác như ${displayFeels}°C`);
    setElText('hero-summary-text', `Thời tiết tại ${p.name}: ${displayWeatherText}. ${displayAdvice}`);
    setElText('hero-hum-val', `${displayHum}%`);
    setElText('hero-wind-val', displayWind);
    setElText('hero-rain-val', displayRain);
    setElText('hero-uv-val', `${displayUv} (${this.getUvText(displayUv)})`);
    setElText('hero-aqi-val', `${aqi} (${activeAqiLevel})`);
  },

"""
    js_content = js_content[:r_start] + new_render_hero + js_content[r_end:]
    print("Updated renderHeroWeather in js_content")

with open(js_file, "w", encoding="utf-8") as f:
    f.write(js_content)
print("Saved js/app.js successfully!")

# 3. Update css/style.css to ensure base background-color and prevent white screen on transitions
with open(css_file, "r", encoding="utf-8") as f:
    css_content = f.read()

# Replace .weather-stage
old_ws = """.weather-stage {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
  min-height: 270px;
  box-shadow: var(--shadow-lg);
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  color: #ffffff;
  background: linear-gradient(135deg, #0284c7 0%, #0369a1 40%, #075985 100%); /* Default background guarantee: never white screen */
}"""

new_ws = """.weather-stage {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
  min-height: 270px;
  box-shadow: var(--shadow-lg);
  transition: box-shadow 0.3s ease, transform 0.3s ease;
  color: #ffffff;
  background-color: #0369a1;
  background: linear-gradient(135deg, #0284c7 0%, #0369a1 40%, #075985 100%); /* Default background guarantee: never white screen */
}

/* Background Gradients & Colors for Weather Conditions */
.weather-stage.weather-sunny {
  background-color: #0284c7;
  background: linear-gradient(135deg, #0284c7 0%, #38bdf8 60%, #fdba74 100%);
}
.weather-stage.weather-noon {
  background-color: #0284c7;
  background: linear-gradient(135deg, #0284c7 0%, #0ea5e9 40%, #38bdf8 75%, #fde047 100%);
}
.weather-stage.weather-noon-rain {
  background-color: #0369a1;
  background: linear-gradient(135deg, #0369a1 0%, #0284c7 40%, #2563eb 75%, #60a5fa 100%);
}
.weather-stage.weather-partly-cloudy {
  background-color: #0369a1;
  background: linear-gradient(135deg, #0369a1 0%, #0284c7 45%, #7dd3fc 100%);
}
.weather-stage.weather-cloudy {
  background-color: #334155;
  background: linear-gradient(135deg, #334155 0%, #475569 50%, #94a3b8 100%);
}
.weather-stage.weather-overcast {
  background-color: #1e293b;
  background: linear-gradient(135deg, #1e293b 0%, #334155 70%, #64748b 100%);
}
.weather-stage.weather-light-rain {
  background-color: #1e3a8a;
  background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #60a5fa 100%);
}
.weather-stage.weather-heavy-rain {
  background-color: #0f172a;
  background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #1d4ed8 100%);
}
.weather-stage.weather-thunderstorm {
  background-color: #09090b;
  background: linear-gradient(135deg, #09090b 0%, #1e1b4b 50%, #312e81 100%);
}
.weather-stage.weather-strong-wind {
  background-color: #0e7490;
  background: linear-gradient(135deg, #0e7490 0%, #0284c7 50%, #38bdf8 100%);
}
.weather-stage.weather-foggy {
  background-color: #475569;
  background: linear-gradient(135deg, #475569 0%, #64748b 50%, #cbd5e1 100%);
}
.weather-stage.weather-night {
  background-color: #0b1528;
  background: linear-gradient(135deg, #020617 0%, #0b1528 50%, #1e293b 100%);
}
.weather-stage.weather-sunset {
  background-color: #9a3412;
  background: linear-gradient(135deg, #431407 0%, #9a3412 35%, #ea580c 70%, #fde047 100%);
}"""

# Find from .weather-stage down to .weather-stage.weather-sunset { ... }
end_sunset_idx = css_content.find(".weather-stage.weather-sunset {")
if end_sunset_idx != -1:
    end_sunset_close = css_content.find("}", end_sunset_idx) + 1
    start_ws_idx = css_content.find(".weather-stage {")
    css_content = css_content[:start_ws_idx] + new_ws + css_content[end_sunset_close:]
    print("Updated weather-stage classes in css/style.css")

with open(css_file, "w", encoding="utf-8") as f:
    f.write(css_content)
print("Saved css/style.css successfully!")
