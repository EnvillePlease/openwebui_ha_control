
# For HTTP requests to Home Assistant
import requests
# For config validation
from pydantic import BaseModel, Field
import json



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
        """
        Initialize Tools with default Valves configuration.
        This sets up the connection details for Home Assistant.
        """
        self.valves = self.Valves() 

    def get_config(self):
        """
        Retrieve Home Assistant URL and headers for authentication.
        Raises ValueError if configuration is incomplete.
        Returns:
            ha_url (str): Home Assistant base URL
            headers (dict): HTTP headers for authentication
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

    def get_services(self):
        """
        List all available services from Home Assistant.
        Returns:
            dict or list: JSON response or error message.
        """
        ha_url, headers = self.get_config()
        url = f"{ha_url}/api/services"
        response = requests.get(url, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}

    def get_entities(self):
        """
        List all entities (states) from Home Assistant.
        Returns:
            dict or list: JSON response or error message.
        """
        ha_url, headers = self.get_config()
        url = f"{ha_url}/api/states"
        response = requests.get(url, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}

    def get_entities_by_domain(self, domain):
        """
        Filter entities by domain (e.g., 'light', 'switch').
        Args:
            domain (str): The domain to filter by (e.g., 'light').
        Returns:
            list: Matching entities or empty list on error.
        """
        entities = self.get_entities()
        if isinstance(entities, dict) and "error" in entities:
            return []
        return [e for e in entities if e["entity_id"].startswith(f"{domain}.")]

    def call_service(self, domain, service, data):
        """
        Call a Home Assistant service with provided domain, service, and data.
        Args:
            domain (str): The domain of the service (e.g., 'light').
            service (str): The service to call (e.g., 'turn_on').
            data (dict): Data to send with the service call.
        Returns:
            dict: JSON response or error message.
        """
        ha_url, headers = self.get_config()
        url = f"{ha_url}/api/services/{domain}/{service}"
        response = requests.post(url, headers=headers, json=data)
        return response.json() if response.status_code in (200, 201) else {"error": response.text}

    def get_entity_state(self, entity_id):
        """
        Get the state of a specific entity by entity_id.
        Args:
            entity_id (str): The entity ID to query.
        Returns:
            dict: JSON response or error message.
        """
        ha_url, headers = self.get_config()
        url = f"{ha_url}/api/states/{entity_id}"
        response = requests.get(url, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}

    def get_domains(self):
        """
        List all unique domains available in Home Assistant entities.
        Returns:
            list: Sorted list of domain names.
        """
        entities = self.get_entities()
        if isinstance(entities, dict) and "error" in entities:
            return []
        domains = {e["entity_id"].split(".")[0] for e in entities if "entity_id" in e}
        return sorted(domains)    

    def get_areas(self):
        """
        List all known Areas in Home Assistant, including their names.
        Returns:
            str: JSON-formatted string of area dicts with area_id and area_name, or error message.
        """
        ha_url, headers = self.get_config()
        url = f"{ha_url}/api/template"
        payload = {"template": "{{ areas()|tojson() }}"}
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code not in (200, 201):
            return json.dumps({"error": response.text})
        area_ids = response.json()
        if not isinstance(area_ids, list):
            return json.dumps({"error": "Unexpected response format for areas."})
        areas_with_names = []
        for area_id in area_ids:
            name_resp = self.get_area_name(area_id)
            area_name = name_resp if isinstance(name_resp, str) else name_resp.get("result", None)
            areas_with_names.append({"area_id": area_id, "area_name": area_name})
        return json.dumps(areas_with_names)

    def get_area_name(self, area_id):
        """
        Get the name of an area by its area_id using the template API.
        Args:
            area_id (str): The area ID to query.
        Returns:
            dict or str: Area name or error message.
        """
        ha_url, headers = self.get_config()
        url = f"{ha_url}/api/template"
        payload = {
            "template": "{{ area_name(area_id)|tojson() }}",
            "variables": {
                "area_id": area_id
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json() if response.status_code in (200, 201) else {"error": response.text}