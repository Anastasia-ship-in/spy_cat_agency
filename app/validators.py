import requests


def validate_breed(breed: str) -> bool:
    response = requests.get("https://api.thecatapi.com/v1/breeds")
    breeds = [item["name"] for item in response.json()]
    return breed in breeds
