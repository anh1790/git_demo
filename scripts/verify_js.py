import re

with open('js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Check matching braces
stack = []
for i, char in enumerate(text):
    if char in '{[(':
        stack.append((char, i))
    elif char in '}])':
        if not stack:
            print(f"Error: unmatched closing {char} at index {i}")
            break
        last, last_i = stack.pop()
        matching = {'}': '{', ']': '[', ')': '('}
        if matching[char] != last:
            print(f"Mismatch: {last} at {last_i} closed by {char} at {i}")
            break
else:
    if stack:
        print(f"Unclosed: {stack[-5:]}")
    else:
        print("Brackets & braces are perfectly balanced!")

# Check for undefined variables or broken template strings
backticks = text.count('`')
print(f"Backticks count: {backticks} (even: {backticks % 2 == 0})")
assert backticks % 2 == 0, "Unclosed template literal!"

# Check key methods exist
for m in [
    'filterOutdoorRegion',
    'selectProvinceFromSearch',
    'renderSingleProvincePill',
    'clearProvinceSearch',
    'getEffectiveWeatherCondition',
    'updateMapMarkers',
    'initMap'
]:
    assert m in text, f"Missing method {m}!"
    print(f"Verified method {m}")
