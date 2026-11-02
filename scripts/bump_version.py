with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('href="css/style.css?v=7"', 'href="css/style.css?v=8"')
text = text.replace('js/stations_data.js?v=7', 'js/stations_data.js?v=8')
text = text.replace('js/embedded_data.js?v=7', 'js/embedded_data.js?v=8')
text = text.replace('js/app.js?v=7', 'js/app.js?v=8')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Bumped version to v=8 in index.html")
