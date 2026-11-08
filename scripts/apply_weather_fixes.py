import os
import shutil

BASE_DIR = r"C:\Users\dlhch\.gemini\antigravity\scratch\air-quality-ai"

# 1. Update css/style.css
css_path = os.path.join(BASE_DIR, "css", "style.css")
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Fix 1a: Replace .weather-stage with default fallback background + add .weather-stage.weather-noon and .weather-noon-rain
old_stage_block = """.weather-stage {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
  min-height: 270px;
  box-shadow: var(--shadow-lg);
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  color: #ffffff;
}

/* Background Gradients for Weather Conditions */
.weather-stage.weather-sunny {
  background: linear-gradient(135deg, #0284c7 0%, #38bdf8 60%, #fdba74 100%);
}"""

new_stage_block = """.weather-stage {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
  min-height: 270px;
  box-shadow: var(--shadow-lg);
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  color: #ffffff;
  background: linear-gradient(135deg, #0284c7 0%, #0369a1 40%, #075985 100%); /* Default background guarantee: never white screen */
}

/* Background Gradients for Weather Conditions */
.weather-stage.weather-sunny {
  background: linear-gradient(135deg, #0284c7 0%, #38bdf8 60%, #fdba74 100%);
}
.weather-stage.weather-noon {
  background: linear-gradient(135deg, #0284c7 0%, #0ea5e9 40%, #38bdf8 75%, #fde047 100%);
}
.weather-stage.weather-noon-rain {
  background: linear-gradient(135deg, #0369a1 0%, #0284c7 40%, #2563eb 75%, #60a5fa 100%);
}"""

# Support both \r\n and \n
if old_stage_block in css:
    css = css.replace(old_stage_block, new_stage_block)
elif old_stage_block.replace("\r\n", "\n") in css.replace("\r\n", "\n"):
    # Normalize and replace
    css = css.replace("\r\n", "\n").replace(old_stage_block.replace("\r\n", "\n"), new_stage_block.replace("\r\n", "\n"))
else:
    print("WARNING: Could not find old_stage_block in css/style.css")

# Fix 1b: Replace .rain-stream with fluid rain canvas and individual falling streaks
old_rain_block = """/* 3. Rain Stream */
.rain-stream {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: linear-gradient(to bottom, rgba(255,255,255,0) 0%, rgba(186, 230, 253, 0.75) 70%, rgba(255,255,255,0) 100%);
  background-size: 2px 28px;
  background-repeat: repeat;
  animation: rainFall 0.35s linear infinite;
  opacity: 0.7;
}

@keyframes rainFall {
  0% { background-position: 0 0; }
  100% { background-position: -30px 110px; }
}"""

new_rain_block = """/* 3. Rain Stream & Realistic Fluid Water Flowing Drops */
.rain-stream {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
  z-index: 3;
}

.rain-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.rain-drops-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
}

/* Fallback individual flowing raindrops */
.rain-streak {
  position: absolute;
  top: -50px;
  width: 1.5px;
  background: linear-gradient(to bottom, rgba(255,255,255,0) 0%, rgba(186, 230, 253, 0.75) 60%, #ffffff 100%);
  border-radius: 0 0 2px 2px;
  transform: rotate(12deg);
  animation: rainDropFlow linear infinite;
  opacity: 0.8;
  pointer-events: none;
}

/* Flowing glass water trickle bead */
.rain-trickle {
  position: absolute;
  top: -20px;
  width: 3.5px;
  height: 8px;
  background: radial-gradient(circle at 40% 40%, rgba(255,255,255,0.95) 0%, rgba(186, 230, 253, 0.65) 60%, rgba(2, 132, 199, 0.3) 100%);
  border-radius: 50% 50% 60% 60%;
  animation: rainTrickleFlow linear infinite;
  opacity: 0.75;
  filter: drop-shadow(0 2px 3px rgba(0,0,0,0.15));
  pointer-events: none;
}

@keyframes rainDropFlow {
  0% {
    transform: translateY(0) rotate(12deg);
    opacity: 0;
  }
  15% {
    opacity: 0.85;
  }
  85% {
    opacity: 0.85;
  }
  100% {
    transform: translateY(350px) rotate(12deg);
    opacity: 0;
  }
}

@keyframes rainTrickleFlow {
  0% {
    transform: translateY(0);
    opacity: 0;
  }
  10% {
    opacity: 0.85;
  }
  90% {
    opacity: 0.85;
  }
  100% {
    transform: translateY(300px);
    opacity: 0;
  }
}"""

if old_rain_block in css:
    css = css.replace(old_rain_block, new_rain_block)
elif old_rain_block.replace("\r\n", "\n") in css.replace("\r\n", "\n"):
    css = css.replace("\r\n", "\n").replace(old_rain_block.replace("\r\n", "\n"), new_rain_block.replace("\r\n", "\n"))
else:
    print("WARNING: Could not find old_rain_block in css/style.css")

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)
print("css/style.css updated successfully.")

# 2. Update index.html
html_path = os.path.join(BASE_DIR, "index.html")
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

old_rain_div = '<div class="rain-stream" id="hero-rain-stream" style="display:none;"></div>'
new_rain_div = """<div class="rain-stream" id="hero-rain-stream" style="display:none;">
              <canvas class="rain-canvas" id="hero-rain-canvas"></canvas>
              <div class="rain-drops-container" id="hero-rain-drops"></div>
            </div>"""

if old_rain_div in html:
    html = html.replace(old_rain_div, new_rain_div)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html updated successfully.")
else:
    print("WARNING: Could not find old_rain_div in index.html (already updated or formatting mismatch)")

# 3. Update js/app.js
js_path = os.path.join(BASE_DIR, "js", "app.js")
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

# Add rain engine call to init()
old_init_resize = """    // Auto-resize leaflet map on tab switch
    window.addEventListener('resize', () => {
      if (this.map && this.currentTab === 'tab-map') {
        this.map.invalidateSize();
      }
    });"""

new_init_resize = """    // Auto-resize leaflet map and rain canvas on resize
    window.addEventListener('resize', () => {
      if (this.map && this.currentTab === 'tab-map') {
        this.map.invalidateSize();
      }
      if (this.rainAnimActive) {
        this.initRainEngine();
      }
    });"""

if old_init_resize in js:
    js = js.replace(old_init_resize, new_init_resize)
elif old_init_resize.replace("\r\n", "\n") in js.replace("\r\n", "\n"):
    js = js.replace("\r\n", "\n").replace(old_init_resize.replace("\r\n", "\n"), new_init_resize.replace("\r\n", "\n"))

# Replace getEffectiveWeatherCondition, renderHeroWeather, scrubTimeOfDay, getConditionIcon, and add rain engine
old_weather_section = """  // =========================================================================
  // DYNAMIC WEATHER ANIMATION ENGINE
  // =========================================================================
  getEffectiveWeatherCondition(baseCondition) {
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
  },

  getConditionIcon(cond) {
    switch (cond) {
      case 'sunny': return '<i class="fa-solid fa-sun" style="color:#f59e0b;"></i>';
      case 'partly_cloudy': return '<i class="fa-solid fa-cloud-sun" style="color:#38bdf8;"></i>';
      case 'cloudy': return '<i class="fa-solid fa-cloud" style="color:#cbd5e1;"></i>';
      case 'overcast': return '<i class="fa-solid fa-cloud" style="color:#94a3b8;"></i>';
      case 'light_rain': return '<i class="fa-solid fa-cloud-rain" style="color:#60a5fa;"></i>';
      case 'heavy_rain': return '<i class="fa-solid fa-cloud-showers-heavy" style="color:#3b82f6;"></i>';
      case 'thunderstorm': return '<i class="fa-solid fa-cloud-bolt" style="color:#a855f7;"></i>';
      case 'foggy': return '<i class="fa-solid fa-smog" style="color:#e2e8f0;"></i>';
      case 'night': return '<i class="fa-solid fa-moon" style="color:#fef08a;"></i>';
      case 'sunset': return '<i class="fa-solid fa-sun" style="color:#ea580c;"></i>';
      default: return '<i class="fa-solid fa-cloud-sun"></i>';
    }
  },"""

new_weather_section = """  // =========================================================================
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
      for (let j = 0; j < 10; j++) {
        const left = (6 + j * 9.5).toFixed(1);
        const dur = (3.0 + (j % 4) * 0.5).toFixed(2);
        const delay = (-j * 0.35).toFixed(2);
        dropsHtml += `<div class="rain-trickle" style="left:${left}%; animation-duration:${dur}s; animation-delay:${delay}s;"></div>`;
      }
      dropsContainer.innerHTML = dropsHtml;
    }

    // 2. Setup Canvas Particles
    const dpr = window.devicePixelRatio || 1;
    const width = streamContainer.clientWidth || 900;
    const height = streamContainer.clientHeight || 270;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.scale(dpr, dpr);

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

    // Create 12 gentle flowing water beads (giọt nước đang chảy)
    this.waterTrickles = [];
    for (let j = 0; j < 12; j++) {
      this.waterTrickles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: 1.6 + Math.random() * 1.4,
        speed: 0.8 + Math.random() * 1.3,
        tailLength: 10 + Math.random() * 14,
        opacity: 0.4 + Math.random() * 0.4
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
      const w = this.rainCanvasWidth || 900;
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

      // Draw sliding water trickle beads (giọt nước đang chảy xuống bề mặt)
      if (this.waterTrickles) {
        for (let j = 0; j < this.waterTrickles.length; j++) {
          const t = this.waterTrickles[j];
          t.y += t.speed;
          if (t.y > h) {
            t.y = -15;
            t.x = Math.random() * w;
          }

          // Wet water trail
          ctx.beginPath();
          ctx.moveTo(t.x, t.y - t.tailLength);
          ctx.lineTo(t.x, t.y);
          ctx.strokeStyle = `rgba(224, 242, 254, ${t.opacity * 0.4})`;
          ctx.lineWidth = t.radius * 0.95;
          ctx.stroke();

          // Droplet head bead
          ctx.beginPath();
          ctx.arc(t.x, t.y, t.radius, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(255, 255, 255, ${t.opacity * 0.85})`;
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
      this.rainCanvasContext.clearRect(0, 0, this.rainCanvasWidth || 900, this.rainCanvasHeight || 270);
    }
  },

  getEffectiveWeatherCondition(baseCondition) {
    const cond = baseCondition || 'sunny';
    const isRainy = cond.includes('rain') || cond === 'thunderstorm';

    if (this.timeScrubMode && this.timeScrubMode !== 'now') {
      const mode = this.timeScrubMode;
      if (mode === 'noon') {
        return isRainy ? 'noon_rain' : 'noon';
      } else if (mode === 'sunset') {
        return isRainy ? 'sunset_rain' : 'sunset';
      } else if (mode === 'night') {
        return (cond === 'thunderstorm') ? 'night_thunderstorm' : (isRainy ? 'night_rain' : 'night');
      }
      return mode;
    }

    // Tự động nhận diện chu kỳ Ngày / Hoàng hôn / Đêm theo ngày giờ thực tế của hệ thống
    const now = new Date();
    const hr = now.getHours();
    const min = now.getMinutes();

    const isNight = (hr >= 18 && min >= 30) || (hr > 18) || (hr < 6);
    const isSunset = (hr === 17) || (hr === 18 && min < 30);

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

    // Guaranteed class reset & application
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

    document.getElementById('hero-location-name').innerHTML = `<i class="fa-solid fa-location-dot"></i> ${p.name} • ${p.type}`;
    document.getElementById('hero-cond-badge').innerHTML = `${condIcon} ${displayWeatherText} <span style="opacity:0.85;font-size:11px;margin-left:4px;">(${timeStr} • ${periodLabel})</span>`;
    document.getElementById('hero-temp-val').innerText = `${displayTemp}°`;
    document.getElementById('hero-feels-val').innerText = `Cảm giác như ${displayFeels}°C`;
    document.getElementById('hero-summary-text').innerText = `Thời tiết tại ${p.name}: ${displayWeatherText}. ${displayAdvice}`;
    document.getElementById('hero-hum-val').innerText = `${displayHum}%`;
    document.getElementById('hero-wind-val').innerText = displayWind;
    document.getElementById('hero-rain-val').innerText = displayRain;
    document.getElementById('hero-uv-val').innerText = `${displayUv} (${this.getUvText(displayUv)})`;
    document.getElementById('hero-aqi-val').innerText = `${aqi} (${activeAqiLevel})`;
  },

  scrubTimeOfDay(period) {
    this.timeScrubMode = period;
    document.querySelectorAll('.time-scrub-btn').forEach(btn => btn.classList.remove('active'));
    const targetBtn = document.getElementById(`btn-scrub-${period}`);
    if (targetBtn) {
      targetBtn.classList.add('active');
    } else if (typeof event !== 'undefined' && event && event.currentTarget) {
      event.currentTarget.classList.add('active');
    }

    this.renderHeroWeather();
  },

  getConditionIcon(cond) {
    switch (cond) {
      case 'sunny':
      case 'noon': return '<i class="fa-solid fa-sun" style="color:#f59e0b;"></i>';
      case 'noon_rain': return '<i class="fa-solid fa-cloud-sun-rain" style="color:#38bdf8;"></i>';
      case 'partly_cloudy': return '<i class="fa-solid fa-cloud-sun" style="color:#38bdf8;"></i>';
      case 'cloudy': return '<i class="fa-solid fa-cloud" style="color:#cbd5e1;"></i>';
      case 'overcast': return '<i class="fa-solid fa-cloud" style="color:#94a3b8;"></i>';
      case 'light_rain': return '<i class="fa-solid fa-cloud-rain" style="color:#60a5fa;"></i>';
      case 'heavy_rain': return '<i class="fa-solid fa-cloud-showers-heavy" style="color:#3b82f6;"></i>';
      case 'thunderstorm': return '<i class="fa-solid fa-cloud-bolt" style="color:#a855f7;"></i>';
      case 'foggy':
      case 'night_foggy': return '<i class="fa-solid fa-smog" style="color:#e2e8f0;"></i>';
      case 'night': return '<i class="fa-solid fa-moon" style="color:#fef08a;"></i>';
      case 'night_rain': return '<i class="fa-solid fa-cloud-moon-rain" style="color:#93c5fd;"></i>';
      case 'night_thunderstorm': return '<i class="fa-solid fa-bolt" style="color:#c084fc;"></i>';
      case 'sunset': return '<i class="fa-solid fa-sun" style="color:#ea580c;"></i>';
      case 'sunset_rain': return '<i class="fa-solid fa-cloud-rain" style="color:#fb923c;"></i>';
      default: return '<i class="fa-solid fa-cloud-sun"></i>';
    }
  },"""

if old_weather_section in js:
    js = js.replace(old_weather_section, new_weather_section)
elif old_weather_section.replace("\r\n", "\n") in js.replace("\r\n", "\n"):
    js = js.replace("\r\n", "\n").replace(old_weather_section.replace("\r\n", "\n"), new_weather_section.replace("\r\n", "\n"))
else:
    print("WARNING: Could not find old_weather_section in js/app.js")

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)
print("js/app.js updated successfully.")

# 4. Synchronize all modified files to static/
static_css = os.path.join(BASE_DIR, "static", "css", "style.css")
static_js = os.path.join(BASE_DIR, "static", "js", "app.js")
static_html = os.path.join(BASE_DIR, "static", "index.html")

shutil.copy2(css_path, static_css)
shutil.copy2(js_path, static_js)
shutil.copy2(html_path, static_html)
print("Synchronized updated files to static/css, static/js, static/index.html.")
