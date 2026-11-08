import subprocess, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

out = subprocess.check_output(['git', 'show', 'HEAD:js/stations_data.js'], encoding='utf-8')
# Find the JSON-like object
start = out.find('{')
end = out.rfind('}') + 1
stations_json = out[start:end]

# Verify it can be loaded as JSON
stations_dict = json.loads(stations_json)
print(f"Successfully loaded {len(stations_dict)} provinces and {sum(len(v) for v in stations_dict.values())} stations from git HEAD!")
print("Hanoi stations count:", len(stations_dict["VN_HN"]))
print("Hanoi station IDs:", [s["id"] for s in stations_dict["VN_HN"]])

# Save this template to a file
with open("backend/services/stations_template.json", "w", encoding="utf-8") as f:
    json.dump(stations_dict, f, ensure_ascii=False, indent=2)
print("Saved template to backend/services/stations_template.json")
