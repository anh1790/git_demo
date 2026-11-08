import subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
out = subprocess.check_output(['git', 'show', 'HEAD:js/stations_data.js'], encoding='utf-8')
hn_idx = out.find('"VN_HN":')
end_idx = out.find('"VN_HP":')
print(out[hn_idx:end_idx])
