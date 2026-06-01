

def test_debug_mode_disabled():
    """Ensure the Flask app is not running with debug mode enabled."""
    import ast
    import os

    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    with open(app_path, "r") as f:
        source = f.read()

    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            # Match app.run(...)
            if isinstance(func, ast.Attribute) and func.attr == "run":
                for keyword in node.keywords:
                    if keyword.arg == "debug":
                        value = keyword.value
                        # Must not be True
                        assert not (isinstance(value, ast.Constant) and value.value is True), \
                            "app.run() must not be called with debug=True"
                        assert not (isinstance(value, ast.NameConstant) and value.value is True), \
                            "app.run() must not be called with debug=True"