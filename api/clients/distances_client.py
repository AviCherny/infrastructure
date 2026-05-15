import requests
from api.builders.url_builder import distances_url
from api.builders.body_builder import BodyBuilder


def post_distance(session: requests.Session, from_airport: str, to_airport: str) -> requests.Response:
    body = BodyBuilder().set("from", from_airport).set("to", to_airport).build()
    return session.post(distances_url(), json=body)
