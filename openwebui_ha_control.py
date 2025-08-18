import requests  # For HTTP requests to Home Assistant
import os
import sys
import json
from pydantic import BaseModel, Field  # For config validation

class Tools:

    class Valves(BaseModel):

        HA_URL: str = Field(
            default="https://my-home-assistant.local:8123",

        # Home Assistant base URL
            description="URL of the home assistant instance.",
        )
        HA_API_TOKEN: str = Field(
            default="",
        # Home Assistant API token
            description="Long lived API token to give Open WebUI access to home assistant.",
        )

    def __init__(self):
        self.valves = self.Valves()
        pass
    
    def get_config():
        v = valves
        ha_url = v.HA_URL
        ha_token = v.HA_API_TOKEN
        if not ha_url or not ha_token:
            raise ValueError("HA_URL and HA_TOKEN environment variables must be set.")
        headers = {
            "Authorization": f"Bearer {ha_token}",
            "Content-Type": "application/json",
        }
        return ha_url, headers


    def list_services():
        """
        Lists all available Home Assistant services.
        """
        ha_url, headers = get_config()
        url = f"{ha_url}/api/services"
        response = requests.get(url, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}


    def list_entities():
        """
        Lists all entities and their states in Home Assistant.
        """
        ha_url, headers = get_config()
        url = f"{ha_url}/api/states"
        response = requests.get(url, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}


    def get_entities_by_domain(domain):
        """
        Returns entities filtered by domain (e.g., 'light', 'sensor').
        """
        entities = list_entities()
        if isinstance(entities, dict) and "error" in entities:
            return []
        return [e for e in entities if e["entity_id"].startswith(f"{domain}.")]


    def call_service(domain, service, data):
        """
        Calls a Home Assistant service (e.g., turn_on a light).
        """
        ha_url, headers = get_config()
        url = f"{ha_url}/api/services/{domain}/{service}"
        response = requests.post(url, headers=headers, json=data)
        return response.json() if response.status_code in (200, 201) else {"error": response.text}

    def get_entity_state(entity_id):
        """
        Gets the state and attributes of a specific entity.
        """
        ha_url, headers = get_config()
        url = f"{ha_url}/api/states/{entity_id}"
        response = requests.get(url, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}