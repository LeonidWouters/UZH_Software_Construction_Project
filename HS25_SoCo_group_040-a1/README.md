# Classes and Objects
### Creation of a new instance 
#### `make(cls, *args)`
Creates a new instance of a specified class.
- Internally calls the `_new` method of the respective class structure (e.g., `Light`, `Camera`, `Thermostat`).
- Adds the `_class` attribute so that the object knows which class it belongs to.
- Is automatically used in subclasses to create and register devices.

**Example:**
```python
living_room_light = make(Light, "Living Room Light", "Living Room", 300, "on", 80)
```
---
### Call of methods on instances 
#### `call(obj, method_name, *args, **kwargs)`
Calls a method on an object by its method name.

- Uses the find() function for method resolution along the class hierarchy
(including multiple inheritance, e.g., with Thermostat or Camera).
- Searches for the method first in the class itself, then in the parent classes.

**Example:**
```python
call(living_room_light, "get_power_consumption")
```
---
### Keeping track of created instances
#### `global_devices = []`
- Global list that stores all created device instances.
- Automatically expands in the _new functions of Light, Camera, and Thermostat.
- Enables centralized management by the SmartHouseManagement Manager
(e.g., calculating total consumption, retrieving filtered device descriptions, ...).
---
# Tests
### Task 1 — Device Tests  
- **test_light_turn_on:** light turns on when toggled 
- **test_light_turn_off:** light turns off when it’s on  
- **test_thermostat_turn_on:** thermostat turn on correctly
- **test_thermostat_turn_off:** thermostat turn off correctly
- **test_thermostat_connect:** thermostat connects correctly 
- **test_thermostat_disconnect:** thermostat disconnects correctly 
- **test_camera_turn_on:** camera on correctly
- **test_camera_turn_off:** camera off correctly
- **test_camera_connect:** camera connects correctly
- **test_camera_disconnect:** camera disconnects correctly
- **test_light_off_get_power_consumption:** light off consumption  
- **test_light_on_get_power_consumption:** light on consumption 
- **test_thermostat_off_get_power_consumption:** thermostat off consumption  
- **test_thermostat_on_get_power_consumption:** thermostat off consumption  
- **test_camera_off_get_power_consumption:** camera off consumption  
- **test_camera_on_get_power_consumption:** camera onn consumption
- **test_light_describe_device:** light description  
- **test_thermostat_connected_describe_device:** thermostat connected - description  
- **test_thermostat_disconnected_describe_device:** thermostat disconnected - description
- **test_camera_connected_describe_device:** camera connected - description 
- **test_camera_disconnected_describe_device:** camera disconnected - description

---

### Task 2 — Smart House Management Tests  
- **test_manager_total_power:** total consumption
- **test_manager_total_power_type_camera:** camera only - filtered consumption  
- **test_manager_get_all_device_description_room_filter_non_existing:** filter for non-existing room return empty device list
- **test_manager_connected_devices_any_ip:** gets all connected devices
- **test_manager_connected_devices_specific_ip:** gets all connected devices for the specific ip
- **test_manager_state_changes_total_consumption_change:** total power changes correctly with light and thermostat value change

---

# Disclaimer
- For the functions directly adapted from the lecture notes and/or book, related notes are added as comments to the functions themselves

**AI use:** 
- Create the check list of all the steps as to do items from the assignment description (to share tasks easier within the team)
- Writing of "parse_args" function for test runner
- Readme file styling
- Clarification of the callable, for implementing verbose command option

**Prompts made in ChatGPT**

1. def find(cls, method_name): ## TODO: update to find both parents... atm, checks only one! while cls is not None: if method_name in cls: return cls[method_name] cls = cls["_parent"] raise NotImplementedError(f"Method {method_name} is not implemented")
Only one parent is found here. But what if there is a list of parents?
2. How does the time.perf_counter() in python works?
3. *Add the prompts made for the parse_args and clarification of callable...
