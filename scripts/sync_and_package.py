import os
import shutil
import zipfile
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.abspath('.')
DOWNLOAD_DIR = r"C:\Users\dlhch\Downloads\airsense-ai"
STATIC_DIR = os.path.join(ROOT, 'static')
DIST_DIR = os.path.join(ROOT, 'dist')

print(f"Syncing from ROOT: {ROOT}")

# 1. Sync index.html, css/, js/ to static/ and dist/
for target_dir in [STATIC_DIR, DIST_DIR]:
    os.makedirs(target_dir, exist_ok=True)
    shutil.copy2(os.path.join(ROOT, 'index.html'), os.path.join(target_dir, 'index.html'))
    for folder in ['css', 'js']:
        src_f = os.path.join(ROOT, folder)
        dst_f = os.path.join(target_dir, folder)
        if os.path.exists(dst_f):
            shutil.rmtree(dst_f)
        shutil.copytree(src_f, dst_f)
    
    # Copy JSON files to data/ inside target
    data_target = os.path.join(target_dir, 'data')
    os.makedirs(data_target, exist_ok=True)
    data_root = os.path.join(ROOT, 'data')
    for f in os.listdir(data_root):
        if f.endswith('.json'):
            shutil.copy2(os.path.join(data_root, f), os.path.join(data_target, f))

print("Synced web files and JSONs to static/ and dist/")

# 2. Build ZIP packages
# A. Standalone website zip (index.html, css/, js/)
zip_standalone_path = os.path.join(ROOT, 'airsense-ai-website-standalone.zip')
with zipfile.ZipFile(zip_standalone_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write(os.path.join(ROOT, 'index.html'), 'index.html')
    for folder in ['css', 'js']:
        f_dir = os.path.join(ROOT, folder)
        for root_dir, _, files in os.walk(f_dir):
            for file in files:
                full_p = os.path.join(root_dir, file)
                rel_p = os.path.relpath(full_p, ROOT)
                zf.write(full_p, rel_p)
print(f"Created {zip_standalone_path} ({os.path.getsize(zip_standalone_path)} bytes)")

# B. Full website zip (index.html, css/, js/, static/, dist/)
zip_full_path = os.path.join(ROOT, 'airsense-ai-website.zip')
with zipfile.ZipFile(zip_full_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write(os.path.join(ROOT, 'index.html'), 'index.html')
    for folder in ['css', 'js', 'static', 'dist']:
        f_dir = os.path.join(ROOT, folder)
        if os.path.exists(f_dir):
            for root_dir, _, files in os.walk(f_dir):
                for file in files:
                    full_p = os.path.join(root_dir, file)
                    rel_p = os.path.relpath(full_p, ROOT)
                    zf.write(full_p, rel_p)
print(f"Created {zip_full_path} ({os.path.getsize(zip_full_path)} bytes)")

print("ALL SYNC & PACKAGING COMPLETE!")
