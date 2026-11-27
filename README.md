
> [!WARNING]
> **Deprecated and archived:** This repository has been archived and development has stopped. It is retained for reference only and will not receive updates or fixes.

# OpenWebUI Home Assistant Control

## Overview

`openwebui_ha_control.py` is a Python module that provides a set of tools for interacting with a Home Assistant instance via its REST API. It is designed to be used with Open WebUI, enabling you to list entities, services, domains, and areas, query entity states, and call services directly from Python code.

## Features
- **Configuration Management**: Uses Pydantic for robust validation of Home Assistant connection details (URL and API token).
- **Service Listing**: Fetches all available Home Assistant services.
- **Entity Listing**: Retrieves all entities (states) from Home Assistant.
- **Domain Listing**: Lists all unique domains present in your Home Assistant entities.
- **Area Listing**: Lists all known areas, including both `area_id` and `area_name` (using the template API).
- **Entity State Query**: Gets the current state of any entity by its ID.
- **Service Calls**: Allows you to call any Home Assistant service with custom data.

## How It Works with Open WebUI
Open WebUI can use this module to:
- Display Home Assistant entities, services, domains, and areas in its interface.
- Allow users to control devices, automations, and other Home Assistant features directly from the WebUI.
- Provide feedback and error messages from Home Assistant to the user.

## Usage
1. **Configuration**
   - Set your Home Assistant URL and API token in the `Valves` class, either by editing the defaults or programmatically.
   - Example:
     ```python
     tools = Tools()
     tools.valves.HA_URL = "https://your-ha-instance.local:8123"
     tools.valves.HA_API_TOKEN = "your_long_lived_token"
     ```

2. **List Services**
   ```python
   services = tools.get_services()
   print(services)
   ```

3. **List Entities**
   ```python
   entities = tools.get_entities()
   print(entities)
   ```

4. **List Domains**
   ```python
   domains = tools.get_domains()
   print(domains)
   ```

5. **List Areas (with names)**
   ```python
   areas_json = tools.get_areas()
   print(areas_json)  # JSON string with area_id and area_name
   ```

6. **Get Area Name**
   ```python
   area_name = tools.get_area_name("your_area_id")
   print(area_name)
   ```

7. **Call a Service**
   ```python
   result = tools.call_service("light", "turn_on", {"entity_id": "light.living_room"})
   print(result)
   ```

8. **Get Entity State**
   ```python
   state = tools.get_entity_state("light.living_room")
   print(state)
   ```

## Requirements
- Python 3.8+
- `requests` library
- `pydantic` library

Install dependencies:
```bash
pip install requests pydantic
```

## Security Note
Always keep your Home Assistant API token secure. Do not expose it in public repositories or logs.

## License
MIT

## Author
EnvillePlease
