# -*- coding: utf-8 -*-
with open("js/app.js", "r", encoding="utf-8") as f:
    code = f.read()

target_end = """      this.mapMarkers.push(marker);
    });
  },"""

replacement_end = """      this.mapMarkers.push(marker);
    });

    // Hiển thị các trạm quan trắc chi tiết của tỉnh đang chọn
    const currProv = this.getSelectedProvince();
    const stations = this.getStationsForProvince(currProv.id);
    stations.forEach(s => {
      const sAqi = s.aqi || Math.round(s.pm25 * 1.8);
      const isSelected = (s.id === this.selectedStationId);
      const sIcon = L.divIcon({
        className: 'custom-station-pin',
        html: `<div style="background:${s.color || '#0d9488'};width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:10px;border:${isSelected ? '3px solid #f59e0b' : '2px solid #fff'};box-shadow:0 2px 6px rgba(0,0,0,0.4);">${sAqi}</div>`,
        iconSize: [26, 26],
        iconAnchor: [13, 13]
      });

      const sMarker = L.marker([s.lat, s.lon], { icon: sIcon }).addTo(this.map);
      sMarker.bindPopup(`
        <div style="font-family:'Plus Jakarta Sans',sans-serif;min-width:180px;">
          <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
            <i class="fa-solid fa-tower-broadcast" style="color:#0d9488;"></i>
            <h4 style="font-size:13px;font-weight:800;margin:0;color:#0f172a;">${s.name}</h4>
          </div>
          <span style="display:inline-block;padding:2px 6px;border-radius:4px;font-size:10px;font-weight:700;background:${s.color}20;color:${s.color};margin-bottom:6px;">${s.type}</span>
          <p style="font-size:11px;color:#64748b;margin-bottom:6px;">${s.address || currProv.name}</p>
          <div style="font-size:11px;display:flex;flex-direction:column;gap:2px;margin-bottom:8px;">
            <span><strong>AQI:</strong> ${sAqi} (${s.aqi_level || 'Trung bình'})</span>
            <span><strong>PM2.5:</strong> ${s.pm25} µg/m³ • <strong>Nhiệt độ:</strong> ${s.temp || currProv.temp}°C</span>
          </div>
          <button style="width:100%;padding:5px;background:#0d9488;color:#fff;border:none;border-radius:6px;font-weight:700;font-size:11px;cursor:pointer;" onclick="App.selectStation('${s.id}'); App.switchTab('tab-aiforecast');">
            Chọn trạm này & Dự báo AI
          </button>
        </div>
      `);
      this.mapMarkers.push(sMarker);
    });
  },"""

code = code.replace("\r\n", "\n")
target_end = target_end.replace("\r\n", "\n")
replacement_end = replacement_end.replace("\r\n", "\n")

if target_end in code:
    code = code.replace(target_end, replacement_end, 1)
    with open("js/app.js", "w", encoding="utf-8") as f:
        f.write(code)
    print("Map markers patched successfully!")
else:
    print("Target end for map markers not found!")
