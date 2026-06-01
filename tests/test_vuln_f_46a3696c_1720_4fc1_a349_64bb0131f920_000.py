

def test_debug_mode_disabled():
    """Verify that the Flask app is not running in debug mode."""
    import importlib
    import app as flask_app

    # Debug mode must be False to prevent Werkzeug debugger exposure
    assert flask_app.app.debug is False, (
        "Flask debug mode is enabled — this exposes the Werkzeug interactive "
        "debugger and allows Remote Code Execution via PIN reconstruction."
    )

def test_debugger_endpoint_not_accessible():
    """Verify that the Werkzeug debugger endpoint is not accessible."""
    import app as flask_app

    client = flask_app.app.test_client()
    # With debug=False, /__debugger__ should not be a valid route
    response = client.get('/__debugger__')
    assert response.status_code == 404, (
        f"Debugger endpoint returned {response.status_code} instead of 404 — "
        "the interactive debugger may still be accessible."
    )