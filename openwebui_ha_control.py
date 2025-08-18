import requests  # For HTTP requests to Home Assistant
import os
import sys
import json
from pydantic import BaseModel, Field  # For config validation


# Tools class provides methods to interact with Home Assistant API for entity and service management.
class Tools:


    # Valves class holds configuration for Home Assistant connection, validated by Pydantic.
    class Valves(BaseModel):


        HA_URL: str = Field(
            default="https://my-home-assistant.local:8123",
            description="URL of the home assistant instance.",  # Home Assistant base URL
        )
        HA_API_TOKEN: str = Field(
            default="",
            description="Long lived API token to give Open WebUI access to home assistant.",  # Home Assistant API token
        )

    def __init__(self):
        """Initialize Tools with default Valves configuration."""
        self.valves = self.Valves()
    

    def get_config(self):
        """
        Retrieve Home Assistant URL and headers for authentication.
        Raises ValueError if configuration is incomplete.
        """
        v = self.valves
        ha_url = v.HA_URL
        ha_token = v.HA_API_TOKEN
        if not ha_url or not ha_token:
            raise ValueError("HA_URL and HA_TOKEN environment variables must be set.")
        headers = {
            "Authorization": f"Bearer {ha_token}",
            "Content-Type": "application/json",
        }
        return ha_url, headers


    def list_services(self):
        """
        List all available services from Home Assistant.
        Returns JSON response or error message.
        """
        ha_url, headers = self.get_config()
        url = f"{ha_url}/api/services"
        response = requests.get(url, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}


    def list_entities(self):
        """
        List all entities (states) from Home Assistant.
        Returns JSON response or error message.
        """
        ha_url, headers = self.get_config()
        url = f"{ha_url}/api/states"
        response = requests.get(url, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}


    def get_entities_by_domain(self, domain):
        """
        Filter entities by domain (e.g., 'light', 'switch').
        Returns a list of matching entities or empty list on error.
        """
        entities = self.list_entities()
        if isinstance(entities, dict) and "error" in entities:
            return []
        return [e for e in entities if e["entity_id"].startswith(f"{domain}.")]


    def call_service(self, domain, service, data):
        """
        Call a Home Assistant service with provided domain, service, and data.
        Returns JSON response or error message.
        """
        ha_url, headers = self.get_config()
        url = f"{ha_url}/api/services/{domain}/{service}"
        response = requests.post(url, headers=headers, json=data)
        return response.json() if response.status_code in (200, 201) else {"error": response.text}


    def get_entity_state(self, entity_id):
        """
        Get the state of a specific entity by entity_id.
        Returns JSON response or error message.
        """
        ha_url, headers = self.get_config()
        url = f"{ha_url}/api/states/{entity_id}"
        response = requests.get(url, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}