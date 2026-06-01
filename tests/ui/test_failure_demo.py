import pytest
import allure


@pytest.mark.ui
@pytest.mark.xfail(
    strict=True,
    reason="Intentional failure: verifies screenshot, video, and trace are captured on failure",
)
@allure.feature("Flights")
@allure.story("Diagnostics")
def test_flight_results_contain_searched_cities_xfail(home_page):
    results = home_page.search_flights("Boston", "Rome")
    # Wrong assertion: heading shows the searched cities, not "Paris"
    # This test always fails — confirming failure diagnostics run on every CI push.
    # If it unexpectedly passes, strict=True causes the suite to fail, which is correct.
    assert "Paris" in results.get_heading()
