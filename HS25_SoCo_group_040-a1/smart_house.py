#### from class notes and book ####
def call(obj, method_name, *args):
    method = find(obj["_class"], method_name)
    return method(obj, *args)

def find(cls, method_name): ## TODO: update to find both parents... atm, checks only one!
    while cls is not None:
        if method_name in cls:
            return cls[method_name]
        cls = cls["_parent"]
    raise NotImplementedError(f"Method {method_name} is not implemented")

def make(cls, *args):
    return cls["_new"](*args)
#### end - from class notes and book ####

##########################################--STEP1--##########################################
############## Parent Classes ##############
###################
### Device ###
def device_toggle_status(obj):
    if obj["status"] == "on":
        obj["status"] = "off"
    else:
        obj["status"] = "on"
        
def device_get_power_consumption(obj):
    raise NotImplementedError("This method must be implemented in the subclasses!")

def describe_device(obj):
    raise NotImplementedError("This method must be implemented in the subclasses!")        
        
def device_new(name: str, location: str, base_power: float, status: str):
    return {
        "name": name,
        "location": location,
        "base_power": float(base_power),
        "status": status,
        "_class": Device,
    }
            
Device = {
    "toggle_status": device_toggle_status,
    "get_power_consumption": device_get_power_consumption,   
    "describe_device": describe_device,
    "_classname": "Device",
    "_parent": None,
    "_new": device_new,
}
    
###################   
### Connectable ###
def connectable_connect(obj, ip):
    obj["connected"] = True
    obj["ip"] = ip

def connectable_disconnect(obj):
    obj["connected"] = False
    # obj["ip"] = None

def connectable_is_connected(obj):
    return obj["connected"]

def connectable_new():
    return {
        "connected": False,
        "ip": None,
        "_class": Connectable,
    }

Connectable = {
    "connect": connectable_connect,
    "disconnect": connectable_disconnect,
    "is_connected": connectable_is_connected,
    "_classname": "Connectable",
    "_parent": None,   
    "_new": connectable_new 
}

############## Subclasses ##############

###################
### Light ###
def light_get_power_consumption(obj):
    if obj["status"] != "on":
        return 0
    return round(obj["base_power"] * obj["brightness"] / 100)

def light_describe(obj):
    return (f"The {obj['name']} is located in the {obj['location']}, "
            f"is currently {obj['status']}, and is set to {obj['brightness']}% brightness.")
    
def light_new(name: str, location: str, base_power: float, status: str, brightness: int):
    return make(Device, name, location, base_power, status) | {
        "brightness": int(brightness),
        "_class": Light,
    }
    
Light = {
    "get_power_consumption": light_get_power_consumption,
    "describe_device": light_describe,
    "_classname": "Light",
    "_parent": Device,
    "_new": light_new,
}

# test_light = make_light("Test Light", "Living Room", 19.79, "off", 90)
#
# toggle_status(test_light)
# print(test_light)
# print(get_power_consumption_light(test_light))
# print(describe_device_light(test_light))

###################
### Thermostat ###
def thermostat_get_power_consumption(thermostat):
    if thermostat["status"] == "on":
        return thermostat["base_power"]*abs(thermostat["target_temperature"] - thermostat["room_temperature"])
    else:
        return 0

def thermostat_describe(obj):
    print("todo ... thermostat")
    ## TODO
    pass

def set_target(obj, temperature: int):
    obj["target_temperature"] = temperature

def get_target(obj):
    return obj["target_temperature"]

def thermostat_new(name: str, location: str, base_power: float, status: str, room_temperature: int, target_temperature: int):
    device = make(Device, name, location, base_power, status)
    connectable  = make(Connectable)
    return device | connectable | {
        "room_temperature": int(room_temperature),
        "target_temperature": int(target_temperature),
        "_class": Thermostat,
    }

Thermostat = {
    "get_power_consumption": thermostat_get_power_consumption,
    "describe_device": thermostat_describe,
    "set_target_temperature": set_target,
    "get_target_temperature": get_target,
    "_classname": "Thermostat",
    "_parent": [Device, Connectable], 
    "_new": thermostat_new
}

# test_thermo = make_thermostat("test_thermo", "bathroom", 4.9, "off", 18, 23)
# pprint.pprint(test_thermo)
# toggle_status(test_thermo)
# connect(test_thermo, "19.09.22.11.001")
# pprint.pprint(test_thermo)
# print(get_power_consumption_thermostat(test_thermo))


###################
### Camera ###
def camera_get_power_consumption(obj):
    if obj["status"] != "on":
        return 0
    return obj["base_power"] * obj["resolution_factor"]

def camera_describe(obj):
    ##TODO
    pass

def camera_new(name: str, location: str, base_power: float, status: str, resolution_factor: int):
    device = make(Device, name, location, base_power, status)
    connectable  = make(Connectable)
    return device | connectable | {
        "resolution_factor": int(resolution_factor),
        "_class": Camera,
    }

Camera = {
    "get_power_consumption": camera_get_power_consumption,
    "describe_device": camera_describe,
    "_classname": "Camera",
    "_parent": [Device, Connectable], 
    "_new": camera_new,
}


###################
### Task 4 - Instances ###
living_room_camera   = make(Camera,     "Camera_Test",   "Living Room", 500, "on",  8)
bathroom_thermostat  = make(Thermostat, "Thermostat_Test", "Bathroom",    1200, "on", 18, 24)
bedroom_light        = make(Light,      "Light_Test",   "Bedroom",     300, "off", 70)

devices = [living_room_camera, bathroom_thermostat, bedroom_light]

for d in devices:
    print(call(d, "describe_device"))
    print("power:", call(d, "get_power_consumption"))
    print("---")
    
### TODO: Implement more here!!! 
## task: Use the method describe device() to verify that all of the functionality is correct.
## not all functionality is listed atm...   


##########################################--STEP2--##########################################
###################
### SmartHouseManagement ###

def calculate_total_power_consumption(search_type = None, search_room = None):
    ## TODO
    pass

def get_all_device_description():
    ## TODO
    pass

def get_all_connected_devices(ip = None):
    ## TODO
    pass

def smart_house_manager_new(name: str, search_type=None, search_room=None):
    return {
        "name": name, 
        "search_type": search_type,
        "search_room": search_room,
        "_class": SmartHouseManagement
    }

SmartHouseManagement = {
    "calculate_total_power_consumption": calculate_total_power_consumption,
    "get_all_device_description": get_all_device_description,
    "get_all_connected_devices": get_all_connected_devices,
    "_classname": "SmartHouseManagement",
    "_parent": None,
    "_new": smart_house_manager_new,
}

print("manager instance dummy..")
manager_test = make(SmartHouseManagement, "Manager", "Light", "Bedroom")
print(manager_test)