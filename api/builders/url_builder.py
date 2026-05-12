from config import API_BASE_URL


def airports_url() -> str:
    return f"{API_BASE_URL}/airports"


def airport_url(airport_id: str) -> str:
    return f"{API_BASE_URL}/airports/{airport_id}"


def distances_url() -> str:
    return f"{API_BASE_URL}/airports/distance"
