import requests
from api.clients.airports_client import get_airports, get_airport
from api.clients.distances_client import post_distance

session = requests.Session()

# Get all airports
response = get_airports(session)
print("Status:", response.status_code)
print("Body:", response.json())

response = get_airport(session, "JFK")
print("Status:", response.status_code)
print("Body:", response.json())

response = post_distance(session, "JFK", "LAX")
print("Status:", response.status_code)
print("Body:", response.json())

