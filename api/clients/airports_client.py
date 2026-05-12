import requests
from api.builders.url_builder import airports_url, airport_url


def get_airports(session: requests.Session) -> requests.Response:
    return session.get(airports_url())


def get_airport(session: requests.Session, airport_id: str) -> requests.Response:
    return session.get(airport_url(airport_id))
