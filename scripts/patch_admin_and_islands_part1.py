import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 1. Update css/style.css
css_path = os.path.join(ROOT, "css", "style.css")
with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

island_css = """
/* Nhãn đơn vị hành chính tiếng Việt có dấu chuẩn */
.admin-province-label {
  background: rgba(255, 255, 255, 0.94) !important;
  color: #0f172a !important;
  font-weight: 700 !important;
  font-size: 11px !important;
  border: 1px solid #cbd5e1 !important;
  border-radius: 4px !important;
  padding: 2px 7px !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15) !important;
  white-space: nowrap !important;
  pointer-events: none !important;
}
.admin-capital-label {
  background: #0284c7 !important;
  color: #ffffff !important;
  font-weight: 800 !important;
  border: 1.5px solid #38bdf8 !important;
  box-shadow: 0 3px 8px rgba(2, 132, 199, 0.4) !important;
}

/* Huy hiệu và biểu tượng hải đảo tiếng Việt */
.island-item-badge {
  background: #0369a1 !important;
  color: #ffffff !important;
  font-weight: 700 !important;
  font-size: 10px !important;
  border: 1px solid #7dd3fc !important;
  border-radius: 4px !important;
  padding: 2px 7px !important;
  box-shadow: 0 2px 6px rgba(3, 105, 161, 0.35) !important;
  white-space: nowrap !important;
}
.island-item-pin {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #0284c7;
  border: 2px solid #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-size: 10.5px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
  cursor: pointer;
  transition: transform 0.2s ease;
}
.island-item-pin:hover {
  transform: scale(1.15);
  background: #0369a1;
}
.island-icon-inner {
  display: flex;
  align-items: center;
  justify-content: center;
}
"""

if ".admin-province-label" not in css_content:
    css_content += island_css
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_content)
    print("Updated css/style.css with island and admin label styles")
else:
    print("css/style.css already contains island styles")

print("Step 1 done")
