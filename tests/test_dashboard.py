import json


def test_dashboard_data(desktop_app_auth):
    payload = json.dumps({"total": 16, "passed": 7, "failed": 2, "norun": 7})
    desktop_app_auth.intercept_request('**/getstat*', payload)
    desktop_app_auth.refresh_dashboard()
    assert desktop_app_auth.get_total_tests_stats() == '16'
    desktop_app_auth.stop_intercept('**/getstat*')