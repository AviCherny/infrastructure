import requests
from api.builders.url_builder import distances_url


def distance_payload(from_airport: str = "TLV", to_airport: str = "JFK") -> dict:
    return {"from": from_airport, "to": to_airport}


def post_distance(session: requests.Session, payload: dict) -> requests.Response:
    return session.post(distances_url(), json=payload)
