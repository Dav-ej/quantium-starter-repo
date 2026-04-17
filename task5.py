from task4 import app as source_app


def test_001_header_is_present(dash_duo):
    app = source_app
    dash_duo.start_server(app)

    dash_duo.wait_for_text_to_equal("h1", "Soul Foods Pink Morsel Sales Explorer", timeout=4)
    assert dash_duo.find_element("h1").text == "Soul Foods Pink Morsel Sales Explorer"
    assert dash_duo.get_logs() == [], "browser console should contain no error"


def test_002_visualisation_is_present(dash_duo):
    app = source_app
    dash_duo.start_server(app)

    dash_duo.wait_for_element("#sales-line-chart", timeout=4)
    assert dash_duo.find_element("#sales-line-chart") is not None
    assert dash_duo.get_logs() == [], "browser console should contain no error"


def test_003_region_picker_is_present(dash_duo):
    app = source_app
    dash_duo.start_server(app)

    dash_duo.wait_for_element("#region-filter", timeout=4)
    assert dash_duo.find_element("#region-filter") is not None
    assert dash_duo.get_logs() == [], "browser console should contain no error"
