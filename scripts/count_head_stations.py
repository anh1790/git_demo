import subprocess, re
out = subprocess.check_output(['git', 'show', 'HEAD:js/stations_data.js'], encoding='utf-8')
provs = re.findall(r'"(VN_[A-Z0-9]+)"\s*:\s*\[', out)
st_ids = re.findall(r'"id":\s*"(VN_[A-Z0-9_]+)"', out)
print('Total provinces in HEAD stations_data.js:', len(provs))
print('Total stations in HEAD stations_data.js:', len(st_ids))
