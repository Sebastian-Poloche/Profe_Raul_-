import os
import requests


class APIClient:
    

    def __init__(self):
        base_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/api/")
        if not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url

    def get(self, endpoint: str):
        try:
            response = requests.get(self.base_url + endpoint, timeout=5)
            response.raise_for_status()
            return response.json(), None

        except requests.exceptions.RequestException as e:
            return None, str(e)

    def post(self, endpoint: str, data: dict):
        try:
            response = requests.post(self.base_url + endpoint, json=data, timeout=5)
            response.raise_for_status()
            return response.json(), None

        except requests.exceptions.RequestException as e:
            return None, str(e)

    def put(self, endpoint: str, data: dict):
        try:
            response = requests.put(self.base_url + endpoint, json=data, timeout=5)
            response.raise_for_status()
            return response.json(), None

        except requests.exceptions.RequestException as e:
            return None, str(e)

    def delete(self, endpoint: str):
        try:
            response = requests.delete(self.base_url + endpoint, timeout=5)
            response.raise_for_status()
            return True, None

        except requests.exceptions.RequestException as e:
            return None, str(e)
