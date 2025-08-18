# OpenWebUI Home Assistant Control

## Overview

`openwebui_ha_control.py` is a Python module designed to provide seamless integration between Open WebUI and a Home Assistant instance. It exposes a set of tools for interacting with Home Assistant's REST API, allowing you to list entities and services, query entity states, and call services directly from Open WebUI.

## Features
- **Configuration Management**: Uses Pydantic for robust validation of Home Assistant connection details (URL and API token).
- **Service Listing**: Fetches all available Home Assistant services.
- **Entity Listing**: Retrieves all entities (states) from Home Assistant.
- **Domain Filtering**: Filters entities by domain (e.g., `light`, `switch`).
- **Service Calls**: Allows you to call any Home Assistant service with custom data.
- **Entity State Query**: Gets the current state of any entity by its ID.

## How It Works with Open WebUI
Open WebUI can use this module to:
- Display Home Assistant entities and services in its interface.
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
   services = tools.list_services()
   print(services)
   ```

3. **List Entities**
   ```python
   entities = tools.list_entities()
   print(entities)
   ```

4. **Filter Entities by Domain**
   ```python
   lights = tools.get_entities_by_domain("light")
   print(lights)
   ```

5. **Call a Service**
   ```python
   result = tools.call_service("light", "turn_on", {"entity_id": "light.living_room"})
   print(result)
   ```

6. **Get Entity State**
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
