

def test_debug_mode_disabled():
    import ast
    import os

    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    with open(app_path, "r") as f:
        source = f.read()

    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr == "run":
                for keyword in node.keywords:
                    if keyword.arg == "debug":
                        value = keyword.value
                        assert not (isinstance(value, ast.Constant) and value.value is True), \
                            "app.run() must not have debug=True"
                        assert not (isinstance(value, ast.NameConstant) and value.value is True), \
                            "app.run() must not have debug=True"

    # Also verify the app object itself reports debug=False at runtime
    from app import app
    assert app.debug is False, "Flask app.debug must be False"