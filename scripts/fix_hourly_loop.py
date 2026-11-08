with open('js/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if "const limitHours = this.hourlyHorizon || 24;" in line:
        start_idx = i
    if start_idx != -1 and "if (container1) container1.innerHTML = html;" in line:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    replacement = [
        "    const limitHours = this.hourlyHorizon || 24;\n",
        "    const baseHourly = p.hourly_forecast_24h || [];\n",
        "\n",
        "    for (let i = 0; i < limitHours; i++) {\n",
        "      let timeStr, tempH, popH, cond;\n",
        "      if (i < baseHourly.length) {\n",
        "        const item = baseHourly[i];\n",
        "        timeStr = item.time;\n",
        "        tempH = item.temp;\n",
        "        popH = item.rain_prob;\n",
        "        cond = item.condition;\n",
        "      } else {\n",
        "        const h = (currentHour + i) % 24;\n",
        "        const dayOffset = Math.floor((currentHour + i) / 24);\n",
        "        timeStr = dayOffset > 0 ? `+${dayOffset}d ${h.toString().padStart(2, '0')}h` : `${h.toString().padStart(2, '0')}:00`;\n",
        "        tempH = Math.round((p.temp + Math.sin((currentHour + i - 8) / 3.8) * 3.5) * 10) / 10;\n",
        "        popH = Math.min(95, Math.max(5, Math.round(p.rain_prob + Math.cos(i / 2.5) * 12)));\n",
        "        cond = (h >= 6 && h <= 17) ? p.condition : 'night';\n",
        "      }\n",
        "      const hVal = (currentHour + i) % 24;\n",
        "      const isDay = (hVal >= 6 && hVal <= 17);\n",
        "      const icon = isDay ? this.getConditionIcon(cond || p.condition) : '<i class=\"fa-solid fa-moon\" style=\"color:#fef08a;\"></i>';\n",
        "\n",
        "      html += `\n",
        "        <div class=\"hourly-card\">\n",
        "          <span class=\"hourly-time\">${timeStr}</span>\n",
        "          <div class=\"hourly-icon\">${icon}</div>\n",
        "          <span class=\"hourly-temp\">${tempH}°</span>\n",
        "          <span class=\"hourly-pop\"><i class=\"fa-solid fa-umbrella\"></i> ${popH}%</span>\n",
        "        </div>\n",
        "      `;\n",
        "    }\n",
        "\n"
    ]
    lines = lines[:start_idx] + replacement + lines[end_idx:]
    with open('js/app.js', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Replaced hourly loop successfully!")
else:
    print(f"Indices not found: start_idx={start_idx}, end_idx={end_idx}")
