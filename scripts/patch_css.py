css_addon = """
/* ==========================================================================
   HOÀNG SA & TRƯỜNG SA SOVEREIGNTY & VIETNAMESE MAP ENHANCEMENTS
   ========================================================================== */
.island-sovereignty-badge {
  background: #dc2626 !important;
  color: #fff !important;
  font-weight: 800 !important;
  font-size: 11px !important;
  border: 1.5px solid #fef08a !important;
  border-radius: 6px !important;
  padding: 4px 10px !important;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.5) !important;
  white-space: nowrap !important;
  display: flex !important;
  align-items: center !important;
  gap: 5px !important;
}
.island-sovereignty-badge::before {
  border-top-color: #dc2626 !important;
}

.island-flag-pin {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}
.island-flag-pin .flag-icon-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #dc2626;
  border: 2px solid #fef08a;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fef08a;
  font-size: 14px;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.5);
  animation: pulseSovereignty 2s infinite ease-in-out;
}
@keyframes pulseSovereignty {
  0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }
  50% { transform: scale(1.1); box-shadow: 0 0 0 8px rgba(220, 38, 38, 0); }
}

.map-sovereignty-box {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  padding: 9px 14px;
  border-radius: 8px;
  border-left: 4px solid #dc2626;
  font-size: 11.5px;
  line-height: 1.45;
  color: #1e293b;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.15);
  max-width: 400px;
  margin: 10px !important;
  border-top: 1px solid rgba(220, 38, 38, 0.2);
}
[data-theme="dark"] .map-sovereignty-box {
  background: rgba(15, 23, 42, 0.92);
  color: #f1f5f9;
  border-left-color: #ef4444;
}

.sea-label-badge {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  color: #0284c7 !important;
  font-weight: 900 !important;
  font-size: 13px !important;
  letter-spacing: 2px !important;
  text-shadow: 1px 1px 3px #fff, -1px -1px 3px #fff, 1px -1px 3px #fff, -1px 1px 3px #fff;
}
[data-theme="dark"] .sea-label-badge {
  color: #38bdf8 !important;
  text-shadow: 1px 1px 3px #020617, -1px -1px 3px #020617;
}

/* Dynamic Weather Backgrounds for Night & Dusk Rain */
.weather-stage.weather-night-rain {
  background: linear-gradient(135deg, #020617 0%, #0c1c38 50%, #172554 100%);
}
.weather-stage.weather-night-thunderstorm {
  background: linear-gradient(135deg, #020617 0%, #180d2b 50%, #2e1065 100%);
}
.weather-stage.weather-sunset-rain {
  background: linear-gradient(135deg, #2b1108 0%, #7c2d12 40%, #c2410c 70%, #0369a1 100%);
}
.weather-stage.weather-night-foggy {
  background: linear-gradient(135deg, #090d16 0%, #1e293b 50%, #334155 100%);
}

/* Outdoor recommendation card selection & Clear Search Button */
.outdoor-card.selected-outdoor-card {
  border: 2px solid var(--primary) !important;
  box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.25), 0 8px 20px rgba(0, 0, 0, 0.1) !important;
  transform: translateY(-2px);
}
.btn-clear-search {
  background: #fee2e2 !important;
  color: #dc2626 !important;
  border-color: #fca5a5 !important;
  font-weight: 700 !important;
}
[data-theme="dark"] .btn-clear-search {
  background: rgba(220, 38, 38, 0.25) !important;
  color: #fca5a5 !important;
  border-color: rgba(220, 38, 38, 0.4) !important;
}
"""

with open('css/style.css', 'r', encoding='utf-8') as f:
    current_css = f.read()

if 'HOÀNG SA & TRƯỜNG SA SOVEREIGNTY' not in current_css:
    with open('css/style.css', 'a', encoding='utf-8') as f:
        f.write(css_addon)
    print("Added sovereignty and weather styles to css/style.css")
else:
    print("Styles already present in css/style.css")
