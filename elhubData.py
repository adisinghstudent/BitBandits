#Python og Pandas: For å simulere og generere data relatert til forbruk og solcelleenergi.
import json
import requests

class ElhubData:
    def __init__(self):
        self.base_url = "https://api.elhub.no/energy-data/v0"

    def get_consumption_groups(self):
        endpoint = f"{self.base_url}/consumption-groups"
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error:", response.status_code, response.text)

    def get_consumption_group_by_id(self, group_id):
        endpoint = f"{self.base_url}/consumption-groups/{group_id}"
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error:", response.status_code, response.text)

    def get_updates(self):
        endpoint = f"{self.base_url}/updates"
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error:", response.status_code, response.text)


data = ElhubData()

print(data.get_consumption_group_by_id(1))