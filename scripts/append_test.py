import os

test_file = os.path.abspath("tests/backend/test_api_endpoints.py")
with open(test_file, "r", encoding="utf-8") as f:
    content = f.read()

new_test = """

def test_endpoint_apidoc_and_root_html_pages():
    from backend.app import apidoc_page, root
    res_doc = run_coro(apidoc_page())
    assert "apidoc.html" in str(res_doc.path)
    assert res_doc.media_type == "text/html"
    
    res_root = run_coro(root())
    assert "index.html" in str(res_root.path)
    assert res_root.media_type == "text/html"
"""

if "test_endpoint_apidoc_and_root_html_pages" not in content:
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(content + new_test)
    print("Added test_endpoint_apidoc_and_root_html_pages successfully!")
else:
    print("Test already present.")
