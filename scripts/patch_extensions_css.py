import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
css_path = os.path.join(ROOT, "css", "style.css")

with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

new_styles = """
/* ==========================================================================
   AIRSENSE AI - 8 FUNCTIONAL GROUPS EXTENSIONS
   ========================================================================== */

/* 1. Weather Alert Banner & Cards */
.weather-alert-banner {
  margin-bottom: 16px;
  border-radius: var(--radius-md);
  padding: 12px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  animation: slideDown 0.3s ease-out;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
}
.weather-alert-banner.alert-emergency {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  border: 1.5px solid #ef4444;
  color: #991b1b;
}
.weather-alert-banner.alert-warning {
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  border: 1.5px solid #f59e0b;
  color: #92400e;
}
.weather-alert-banner.alert-info {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border: 1.5px solid #10b981;
  color: #166534;
}
.alert-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
}
.alert-item-card {
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 10px;
  border-left: 4px solid #ef4444;
  background: var(--body-bg);
}

/* 2. Favorites & Location Actions */
.btn-favorite-star {
  background: transparent;
  border: none;
  font-size: 18px;
  color: #94a3b8;
  cursor: pointer;
  padding: 4px 8px;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.btn-favorite-star:hover, .btn-favorite-star.active {
  color: #f59e0b;
  transform: scale(1.15);
}
.btn-icon-action {
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 14px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}
.btn-icon-action:hover {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
}
.favorites-chips-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
  margin-top: 8px;
}
.fav-chip {
  background: var(--body-bg);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  font-size: 11.5px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s;
}
.fav-chip:hover, .fav-chip.active {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
}
.fav-chip .remove-fav {
  font-size: 10px;
  margin-left: 4px;
  opacity: 0.6;
}
.fav-chip .remove-fav:hover {
  opacity: 1;
}

/* 3. Hourly & Daily Horizon Toggles */
.horizon-toggle-group {
  display: inline-flex;
  align-items: center;
  background: var(--body-bg);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 2px;
  gap: 2px;
}
.horizon-btn {
  background: transparent;
  border: none;
  font-size: 11.5px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 4px;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s;
}
.horizon-btn.active {
  background: var(--card-bg);
  color: var(--primary);
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}

/* 4. AI Assistant Floating Widget & Window */
.ai-assistant-fab-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 1000;
}
.ai-assistant-fab {
  background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
  color: #ffffff;
  border: 2px solid rgba(255, 255, 255, 0.4);
  padding: 12px 20px;
  border-radius: 30px;
  font-size: 14px;
  font-weight: 800;
  box-shadow: 0 6px 20px rgba(2, 132, 199, 0.45);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.ai-assistant-fab:hover {
  transform: translateY(-3px) scale(1.04);
  box-shadow: 0 8px 24px rgba(2, 132, 199, 0.55);
}
.ai-online-dot {
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  box-shadow: 0 0 6px #10b981;
}

.ai-chat-window {
  position: fixed;
  bottom: 85px;
  right: 24px;
  width: 380px;
  max-width: calc(100vw - 32px);
  height: 520px;
  max-height: calc(100vh - 110px);
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.18);
  display: flex;
  flex-direction: column;
  z-index: 1001;
  overflow: hidden;
  animation: popIn 0.25s ease-out;
}
@keyframes popIn {
  from { opacity: 0; transform: scale(0.92) translateY(20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
.ai-chat-header {
  background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
  color: #fff;
  padding: 14px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.ai-chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: var(--body-bg);
}
.ai-chat-msg {
  max-width: 85%;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 13px;
  line-height: 1.5;
}
.ai-chat-msg.bot {
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  align-self: flex-start;
  border-bottom-left-radius: 2px;
}
.ai-chat-msg.user {
  background: var(--primary);
  color: #fff;
  align-self: flex-end;
  border-bottom-right-radius: 2px;
}
.ai-chat-suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 6px;
}
.ai-suggestion-chip {
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  color: var(--primary);
  padding: 4px 10px;
  border-radius: 14px;
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}
.ai-suggestion-chip:hover {
  background: var(--primary);
  color: #fff;
}
.ai-chat-footer {
  padding: 12px;
  background: var(--card-bg);
  border-top: 1px solid var(--border-color);
  display: flex;
  gap: 8px;
}
.ai-chat-input {
  flex: 1;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  padding: 8px 14px;
  font-size: 13px;
  background: var(--body-bg);
  color: var(--text-main);
  outline: none;
}
.ai-chat-send {
  background: var(--primary);
  color: #fff;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}
.ai-chat-send:hover {
  background: var(--primary-dark);
}
"""

if ".weather-alert-banner" not in css_content:
    css_content += new_styles
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_content)
    print("Added new extension styles to css/style.css")
else:
    print("Styles already present in css/style.css")
