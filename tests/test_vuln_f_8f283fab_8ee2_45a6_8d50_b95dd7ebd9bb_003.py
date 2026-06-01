

def test_debug_mode_disabled():
    import ast
    import re
    with open('app.py', 'r') as f:
        source = f.read()
    # Check that debug=True is not passed to app.run()
    debug_true_pattern = re.compile(r'app\.run\s*\([^)]*debug\s*=\s*True[^)]*\)')
    assert not debug_true_pattern.search(source), "app.run() must not be called with debug=True"

def test_debug_mode_disabled_runtime(client):
    import app as flask_app
    assert flask_app.app.debug is False, "Flask app.debug must be False at runtime"