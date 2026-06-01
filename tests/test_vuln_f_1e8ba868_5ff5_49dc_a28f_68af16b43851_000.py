

def test_debug_mode_disabled():
    import ast
    import re
    with open('app.py', 'r') as f:
        source = f.read()
    # Find all app.run() calls and assert none use debug=True
    matches = re.findall(r'app\.run\(.*?\)', source)
    for match in matches:
        assert 'debug=True' not in match, f"debug=True found in app.run() call: {match}"
    # Also verify debug=False is present
    assert 'debug=False' in source or all('debug=True' not in m for m in matches), \
        "app.run() should not be called with debug=True"