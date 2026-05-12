import requests
from api.builders.url_builder import distances_url
from api.builders.body_builder import distances_body


def post_distance(session: requests.Session, from_airport: str, to_airport: str) -> requests.Response:
    return session.post(distances_url(), json=distances_body(from_airport, to_airport))
