import requests
from api.builders.url_builder import distances_url
from api.builders.body_builder import BodyBuilder


def distance_payload(from_airport: str, to_airport: str) -> dict:
    return BodyBuilder().set("from", from_airport).set("to", to_airport).build()


def post_distance(session: requests.Session, payload: dict) -> requests.Response:
    return session.post(distances_url(), json=payload)
