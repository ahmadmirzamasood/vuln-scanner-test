

def test_debug_mode_disabled():
    """Verify that the Flask app is not running in debug mode."""
    import importlib
    import sys

    # Remove cached module if already imported
    if 'app' in sys.modules:
        del sys.modules['app']

    import app as flask_app

    assert flask_app.app.debug is False, (
        "Flask debug mode must be disabled in production to prevent "
        "the Werkzeug interactive debugger from exposing RCE (CVE-2016-10516)."
    )


def test_debugger_not_active_on_exception():
    """Verify the test client does not expose the Werkzeug debugger on errors."""
    import app as flask_app

    flask_app.app.config['TESTING'] = True
    flask_app.app.config['DEBUG'] = False

    with flask_app.app.test_client() as client:
        # Trigger a 404 — response must not contain debugger HTML
        response = client.get('/nonexistent_route_xyz')
        assert b'werkzeug' not in response.data.lower() or b'debugger' not in response.data.lower(), (
            "Werkzeug debugger HTML should not be present in error responses."
        )
        assert response.status_code in (404, 405, 500)