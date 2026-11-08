import os

app_file = os.path.abspath("backend/app.py")
with open(app_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.strip().startswith('@app.get("/apidoc")'):
        skip = True
        new_lines.append('@app.get("/apidoc")\n')
        new_lines.append('@app.get("/apidocs")\n')
        new_lines.append('@app.get("/api-docs")\n')
        new_lines.append('@app.get("/apidoc.html")\n')
        new_lines.append('async def apidoc_page():\n')
        new_lines.append('    """Phục vụ trực tiếp giao diện tài liệu Swagger UI OpenAPI tương tác."""\n')
        new_lines.append('    doc_file = STATIC_DIR / "apidoc.html"\n')
        new_lines.append('    if not doc_file.exists():\n')
        new_lines.append('        doc_file = BASE_DIR / "apidoc.html"\n')
        new_lines.append('    if doc_file.exists():\n')
        new_lines.append('        return FileResponse(doc_file, media_type="text/html")\n')
        new_lines.append('    return RedirectResponse(url="/docs")\n\n')
        new_lines.append('@app.get("/")\n')
        new_lines.append('@app.get("/index.html")\n')
        new_lines.append('async def root():\n')
        new_lines.append('    """Trang chủ chuyển hướng thẳng tới giao diện người dùng."""\n')
        new_lines.append('    index_file = STATIC_DIR / "index.html"\n')
        new_lines.append('    if not index_file.exists():\n')
        new_lines.append('        index_file = BASE_DIR / "index.html"\n')
        new_lines.append('    if index_file.exists():\n')
        new_lines.append('        return FileResponse(index_file, media_type="text/html")\n')
        new_lines.append('    return {"message": "Air Quality Forecasting API is running. Visit /docs for Swagger UI."}\n\n')
        continue
    
    if skip:
        if line.strip().startswith('@app.get("/manifest.json")'):
            skip = False
            new_lines.append(line)
        continue
    new_lines.append(line)

with open(app_file, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Updated backend/app.py routes successfully!")
