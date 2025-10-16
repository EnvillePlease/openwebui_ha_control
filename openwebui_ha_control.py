import asyncio
import requests
import ast
import json
from homeassistant_api import Client
from pydantic import BaseModel, Field

class Tools:
    
    class Valves(BaseModel):

        HA_URL: str = Field(
            default="https://my-home-assistant.local:8123",
            description="URL of the home assistant instance.",  # Home Assistant base URL
        )
        HA_API_TOKEN: str = Field(
            default="",
            description="Long lived API token to give Open WebUI access to home assistant.",  # Home Assistant API token
        )

    class Room(BaseModel):

        room_id: str = Field(
            default="",
            description="ID of the area.",
        )
        room_name: str = Field(
            default="",
            description="Name of the area.",
        )

    def __init__(self):
        self.valves = self.Valves()

    def get_client(self):
        return Client(self.valves.HA_URL, self.valves.HA_API_TOKEN)

    def get_device_domains(self):
        try:
            client = self.get_client()
            return client.get_domains()
        except Exception as e:
            # Log or handle error
            return {"error": str(e)}

    def get_rooms(self) -> str:
        try:
            client = self.get_client()
            payload = "{{ areas() }}"
            response = client.get_rendered_template(payload)
            area_ids = ast.literal_eval(response)
        except Exception as e:
            return json.dumps({"error": f"Failed to get area ids: {e}"})

        areas = []
        for area_id in area_ids:
            try:
                area_name = self.get_room_name(area_id)
                if area_name:
                    areas.append(self.Room(room_id=area_id, room_name=area_name))
            except Exception as e:
                # Optionally log error
                continue

        serializable_areas = [a.dict() for a in areas]
        return json.dumps(serializable_areas)

    def get_room_name(self, area_id: str) -> str:
        try:
            client = self.get_client()
            payload = "{{ area_name('" + area_id + "') }}"
            return client.get_rendered_template(payload)
        except Exception as e:
            return ""

    def get_room_id(self, area_name: str) -> str:
        try:
            client = self.get_client()
            payload = "{{ area_id('" + area_name + "') }}"
            return client.get_rendered_template(payload)
        except Exception as e:
            return ""

    def get_all_devices(self) -> str:
        try:
            client = self.get_client()
            return client.get_entities()
        except Exception as e:
            return json.dumps({"error": f"Failed to get devices: {e}"})
        
    def get_device_by_id(self, entity_id: str) -> str:
        try:
            client = self.get_client()
            return client.get_entity(entity_id=entity_id).state
        except Exception as e:
            return json.dumps({"error": f"Failed to get device {entity_id}: {e}"})

    def get_device_by_name(self, entity_name: str) -> str:
        try:
            client = self.get_client()
            groups = client.get_entities()
            
            for group in groups.values():
                for entity in group.entities.values():
                    friendly_name = entity.state.attributes.get("friendly_name", "")
                    if friendly_name == entity_name:
                        entity_id = entity.state.entity_id
                        if not isinstance(entity_id, str):
                            entity_id = str(entity_id)
                        return self.get_device_by_id(entity_id)
        except Exception as e:
            return json.dumps({"error": f"Failed to get device {entity_name}: {e}"})