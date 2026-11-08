with open("js/app.js", "r", encoding="utf-8") as f:
    code = f.read()

print("File size:", len(code), "chars")
# Test for presence of all required functions
assert "initRainEngine" in code
assert "startRainAnimation" in code
assert "stopRainAnimation" in code
assert "scrubTimeOfDay" in code
assert "noon_rain" in code
assert "weather-noon" in open("css/style.css", "r", encoding="utf-8").read()
print("All assertions passed!")
