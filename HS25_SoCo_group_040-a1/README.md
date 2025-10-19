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
