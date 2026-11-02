# -*- coding: utf-8 -*-
with open("js/app.js", "r", encoding="utf-8") as f:
    code = f.read()

target_block = """  // 5. Thanh tìm kiếm 34 tỉnh thành với Auto-complete
  setupLocationSearch() {
    const input = document.getElementById('input-location-search');
    const dropdown = document.getElementById('search-results-dropdown');
    if (!input || !dropdown) return;

    input.addEventListener('input', (e) => {
      const q = e.target.value.trim().toLowerCase();
      if (!q) {
        dropdown.style.display = 'none';
        return;
      }

      const matches = this.provinces.filter(p => 
        p.name.toLowerCase().includes(q) ||
        p.province.toLowerCase().includes(q) ||
        p.region.toLowerCase().includes(q)
      );

      if (matches.length === 0) {
        dropdown.innerHTML = '<div style="padding:12px;color:var(--text-muted);font-size:13px;text-align:center;">Không tìm thấy địa phương phù hợp</div>';
        dropdown.style.display = 'block';
        return;
      }

      dropdown.innerHTML = matches.map(p => `
        <div class="search-result-item" onclick="App.selectProvince('${p.id}'); document.getElementById('search-results-dropdown').style.display='none'; document.getElementById('input-location-search').value='${p.name}';">
          <div>
            <div class="item-title">${p.name}</div>
            <div class="item-sub">${p.type} • ${p.region} • ${p.weather_text}</div>
          </div>
          <span class="stat-badge" style="background:${p.color}20; color:${p.color};">${p.temp}°C • AQI ${Math.round(p.pm25 * 1.8)}</span>
        </div>
      `).join('');
      dropdown.style.display = 'block';
    });

    document.addEventListener('click', (e) => {
      if (!input.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.style.display = 'none';
      }
    });
  },

  // 6. Pills Lựa chọn nhanh 34 Tỉnh & Khu vực
  setupProvincePills() {
    this.filterByRegion('all');
  },

  filterByRegion(region) {
    const regionButtons = document.querySelectorAll('#region-pills-container .district-pill');
    regionButtons.forEach(btn => {
      if (btn.innerText.includes(region === 'all' ? 'Tất cả' : region)) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    const container = document.getElementById('province-pills-container');
    if (!container) return;

    const filtered = region === 'all' ? this.provinces : this.provinces.filter(p => p.region.includes(region));

    let html = '<span class="pills-label"><i class="fa-solid fa-location-dot"></i> Địa phương:</span>';
    filtered.forEach(p => {
      const activeClass = p.id === this.selectedProvinceId ? 'active' : '';
      html += `<button class="district-pill ${activeClass}" onclick="App.selectProvince('${p.id}')">${p.name}</button>`;
    });
    container.innerHTML = html;
  },

  selectProvince(provId) {
    this.selectedProvinceId = provId;
    
    document.querySelectorAll('#province-pills-container .district-pill').forEach(btn => {
      const p = this.getProvinceById(provId);
      if (p && btn.innerText === p.name) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    this.renderAll();
    this.showToast(`Đã chuyển sang theo dõi: ${this.getSelectedProvince().name}`);
  },"""

replacement_block = """  // 5. Thanh tìm kiếm 34 tỉnh thành và 101 trạm đo với Auto-complete
  setupLocationSearch() {
    const input = document.getElementById('input-location-search');
    const dropdown = document.getElementById('search-results-dropdown');
    if (!input || !dropdown) return;

    input.addEventListener('input', (e) => {
      const q = e.target.value.trim().toLowerCase();
      if (!q) {
        dropdown.style.display = 'none';
        return;
      }

      const provMatches = this.provinces.filter(p => 
        p.name.toLowerCase().includes(q) ||
        p.province.toLowerCase().includes(q) ||
        p.region.toLowerCase().includes(q)
      );

      // Tìm kiếm cả trạm quan trắc con
      const stationMatches = [];
      this.provinces.forEach(p => {
        const sts = this.getStationsForProvince(p.id);
        sts.forEach(s => {
          if (s.name.toLowerCase().includes(q) || s.type.toLowerCase().includes(q) || (s.address && s.address.toLowerCase().includes(q))) {
            stationMatches.push({ ...s, parent_prov_id: p.id, parent_prov_name: p.name });
          }
        });
      });

      if (provMatches.length === 0 && stationMatches.length === 0) {
        dropdown.innerHTML = '<div style="padding:12px;color:var(--text-muted);font-size:13px;text-align:center;">Không tìm thấy địa phương hoặc trạm quan trắc phù hợp</div>';
        dropdown.style.display = 'block';
        return;
      }

      let html = '';
      if (provMatches.length > 0) {
        html += '<div style="padding:6px 12px;font-size:11px;font-weight:800;color:var(--primary);background:var(--body-bg);">TỈNH / THÀNH PHỐ</div>';
        html += provMatches.slice(0, 5).map(p => `
          <div class="search-result-item" onclick="App.selectProvince('${p.id}'); document.getElementById('search-results-dropdown').style.display='none'; document.getElementById('input-location-search').value='${p.name}';">
            <div>
              <div class="item-title"><i class=\"fa-solid fa-location-dot\" style=\"color:var(--primary);font-size:12px;\"></i> ${p.name}</div>
              <div class="item-sub">${p.type} • ${p.region} • ${p.weather_text}</div>
            </div>
            <span class="stat-badge" style="background:${p.color}20; color:${p.color};">${p.temp}°C • AQI ${Math.round(p.pm25 * 1.8)}</span>
          </div>
        `).join('');
      }

      if (stationMatches.length > 0) {
        html += '<div style="padding:6px 12px;font-size:11px;font-weight:800;color:var(--accent-teal);background:var(--body-bg);border-top:1px solid var(--border-color);">TRẠM QUAN TRẮC CHI TIẾT</div>';
        html += stationMatches.slice(0, 5).map(s => `
          <div class="search-result-item" onclick="App.selectProvince('${s.parent_prov_id}'); App.selectStation('${s.id}'); document.getElementById('search-results-dropdown').style.display='none'; document.getElementById('input-location-search').value='${s.name}';">
            <div>
              <div class="item-title"><i class=\"fa-solid fa-tower-broadcast\" style=\"color:var(--accent-teal);font-size:12px;\"></i> ${s.name}</div>
              <div class="item-sub">${s.parent_prov_name} • ${s.type}</div>
            </div>
            <span class="stat-badge" style="background:${s.color}20; color:${s.color};">PM2.5: ${s.pm25} • AQI ${s.aqi}</span>
          </div>
        `).join('');
      }

      dropdown.innerHTML = html;
      dropdown.style.display = 'block';
    });

    document.addEventListener('click', (e) => {
      if (!input.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.style.display = 'none';
      }
    });
  },

  // 6. Quản lý phân vùng, Dropdown và Trạm Quan Trắc
  setupProvincePills() {
    this.populateProvinceDropdown();
    this.filterByRegion('all');
  },

  populateProvinceDropdown() {
    const select = document.getElementById('select-province-dropdown');
    if (!select) return;

    const regions = [
      { name: 'Miền Bắc', label: 'Miền Bắc (15 tỉnh/thành)' },
      { name: 'Miền Trung', label: 'Miền Trung (8 tỉnh/thành)' },
      { name: 'Tây Nguyên', label: 'Tây Nguyên (3 tỉnh)' },
      { name: 'Miền Nam', label: 'Miền Nam (8 tỉnh/thành)' }
    ];

    let html = '';
    regions.forEach(r => {
      const provs = this.provinces.filter(p => p.region.includes(r.name));
      html += `<optgroup label="${r.label}">`;
      provs.forEach(p => {
        html += `<option value="${p.id}" ${p.id === this.selectedProvinceId ? 'selected' : ''}>${p.name}</option>`;
      });
      html += `</optgroup>`;
    });

    select.innerHTML = html;
  },

  filterByRegion(region) {
    this.selectedRegion = region;
    const regionButtons = document.querySelectorAll('#region-pills-container .district-pill');
    regionButtons.forEach(btn => {
      const txt = btn.innerText.toLowerCase();
      const match = (region === 'all')
        ? txt.includes('tất cả')
        : (region === 'Miền Trung' ? (txt.includes('miền trung') && !txt.includes('tây nguyên')) : txt.includes(region.toLowerCase()));
      if (match) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    const container = document.getElementById('province-pills-container');
    if (!container) return;

    let filtered = this.provinces;
    if (region !== 'all') {
      if (region === 'Tây Nguyên') {
        filtered = this.provinces.filter(p => p.region.includes('Tây Nguyên'));
      } else if (region === 'Miền Trung') {
        filtered = this.provinces.filter(p => p.region.includes('Miền Trung'));
      } else {
        filtered = this.provinces.filter(p => p.region.includes(region));
      }
    }

    let html = '<span class="pills-label"><i class="fa-solid fa-location-dot"></i> Địa phương:</span>';
    filtered.forEach(p => {
      const activeClass = (p.id === this.selectedProvinceId) ? 'active' : '';
      html += `<button class="district-pill ${activeClass}" onclick="App.selectProvince('${p.id}')">${p.name}</button>`;
    });
    container.innerHTML = html;

    // Nếu tỉnh hiện tại không nằm trong vùng đã lọc, chuyển sang tỉnh đầu tiên của vùng
    if (region !== 'all' && filtered.length > 0 && !filtered.some(p => p.id === this.selectedProvinceId)) {
      this.selectProvince(filtered[0].id);
    } else {
      this.renderStationPills();
    }
  },

  renderStationPills() {
    const container = document.getElementById('station-pills-container');
    const provNameEl = document.getElementById('station-prov-name');
    const p = this.getSelectedProvince();
    if (provNameEl) provNameEl.innerText = p.name;
    if (!container) return;

    const stations = this.getStationsForProvince(p.id);
    if (!stations || stations.length === 0) {
      container.style.display = 'none';
      return;
    }
    container.style.display = 'flex';

    if (!this.selectedStationId || !stations.some(s => s.id === this.selectedStationId)) {
      this.selectedStationId = stations[0].id;
    }

    let html = `<span class="pills-label"><i class="fa-solid fa-tower-broadcast" style="color:var(--accent-teal);"></i> Đo từng trạm (<strong style="color:var(--primary);">${p.name}</strong> - ${stations.length} trạm):</span>`;
    stations.forEach(s => {
      const isActive = (s.id === this.selectedStationId) ? 'active' : '';
      const aqi = s.aqi || Math.round(s.pm25 * 1.8);
      html += `
        <button class="station-pill ${isActive}" data-station-id="${s.id}" onclick="App.selectStation('${s.id}')">
          <span>${s.name}</span>
          <span class="station-type-tag">${s.type}</span>
          <span style="font-size:10px;font-weight:800;color:${isActive ? '#fff' : s.color};">AQI ${aqi}</span>
        </button>
      `;
    });
    container.innerHTML = html;
  },

  selectProvince(provId) {
    this.selectedProvinceId = provId;
    this.selectedStationId = null;

    const select = document.getElementById('select-province-dropdown');
    if (select) select.value = provId;

    document.querySelectorAll('#province-pills-container .district-pill').forEach(btn => {
      const p = this.getProvinceById(provId);
      if (p && btn.innerText.trim() === p.name.trim()) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    this.renderStationPills();
    this.renderAll();
    this.showToast(`Đã chuyển sang theo dõi: ${this.getSelectedProvince().name}`);
  },"""

code = code.replace("\r\n", "\n")
target_block = target_block.replace("\r\n", "\n")
replacement_block = replacement_block.replace("\r\n", "\n")

if target_block in code:
    code = code.replace(target_block, replacement_block, 1)
    with open("js/app.js", "w", encoding="utf-8") as f:
        f.write(code)
    print("Step 2 of patch applied successfully!")
else:
    print("Target block for step 2 not found!")
