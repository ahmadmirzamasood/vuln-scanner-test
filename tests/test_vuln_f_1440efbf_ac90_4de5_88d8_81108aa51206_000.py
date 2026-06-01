

def test_debug_mode_disabled():
    import ast
    import os

    app_path = os.path.join(os.path.dirname(__file__), 'app.py')
    with open(app_path, 'r') as f:
        source = f.read()

    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            # Check for app.run(...)
            if isinstance(func, ast.Attribute) and func.attr == 'run':
                for keyword in node.keywords:
                    if keyword.arg == 'debug':
                        value = keyword.value
                        if isinstance(value, ast.Constant):
                            assert value.value is not True, \
                                "app.run() must not be called with debug=True in production"
                        elif isinstance(value, ast.NameConstant):  # Python 3.7 compat
                            assert value.value is not True, \
                                "app.run() must not be called with debug=True in production"