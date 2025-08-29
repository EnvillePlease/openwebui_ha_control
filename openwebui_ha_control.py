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

    def get_home_device_domains(self):
        v=self.valves
        client = Client(v.HA_URL, v.HA_API_TOKEN)
        
        response = client.get_domains()
        
        return response

    def get_rooms(self) -> str:
        v=self.valves
        client = Client(v.HA_URL, v.HA_API_TOKEN)
        
        payload = "{{ areas() }}"
        response = client.get_rendered_template(payload)
        
        areas = []
        area_ids = ast.literal_eval(response)

        for area_id in area_ids:
            try:
                area_name = self.get_room_name(area_id)
                if area_name != "" and area_name != "None" and area_name is not None:
                    areas.append(self.Room(room_id=area_id, room_name=area_name))
            except Exception as e:
                print(f"Error getting room name for {area_id}: {e}")

        serializable_areas = [a.dict() for a in areas]
        json_string = json.dumps(serializable_areas)

        return json_string

    def get_room_name(self,area_id) -> str:
        v=self.valves
        client = Client(v.HA_URL, v.HA_API_TOKEN)
        
        payload = "{{ area_name('" + area_id + "') }}"
        response = client.get_rendered_template(payload)

        return response
    
    def get_room_id(self,area_name) -> str:
        v=self.valves
        client = Client(v.HA_URL, v.HA_API_TOKEN)
        
        payload = "{{ area_id('" + area_name + "') }}"
        response = client.get_rendered_template(payload)

        return response