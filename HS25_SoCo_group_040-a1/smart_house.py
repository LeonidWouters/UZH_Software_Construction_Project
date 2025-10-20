# Global Dictionary of created Devices
global_devices = []

#### this part is adopted from class notes and book ####
def call(obj, method_name, *args, **kwargs):
    method = find(obj["_class"], method_name)
    return method(obj, *args, **kwargs)

def find(cls, method_name):
    # 1. Search in the class itself
    if method_name in cls:
        return cls[method_name]
    # 2. If nothing is found in class, search in parents
    parents = cls.get("_parent")
    # If there is no parent defined, raise an Error
    if not parents:
        raise NotImplementedError(f"Method {method_name} is not implemented")
    # If there is only one parent, create a list of the single parent
    if not isinstance(parents, list):
        parents = [parents]
    # Iterate over the list of parents, even if there is only one parent (then only one iteration)
    for p in parents:
        try:
            return find(p, method_name)
        except NotImplementedError:
            pass
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
    obj["ip"] = None            #This way, the key 'ip' stays in the dictionary!

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
    obj = make(Device, name, location, base_power, status) | {
        "brightness": int(brightness),
        "_class": Light,
    }
    global_devices.append(obj)
    return obj
    
Light = {
    "get_power_consumption": light_get_power_consumption,
    "describe_device": light_describe,
    "_classname": "Light",
    "_parent": Device,
    "_new": light_new,
}


###################
### Thermostat ###
def thermostat_get_power_consumption(thermostat):
    if thermostat["status"] == "on":
        return thermostat["base_power"]*abs(thermostat["target_temperature"] - thermostat["room_temperature"])
    else:
        return 0

def thermostat_describe(obj):
    if obj['connected']:
        return (f"The {obj['name']} is located in the {obj['location']}, "
                f"is currently {obj['status']}, and is currently set to {obj['target_temperature']} degree in a {obj['room_temperature']}"
                f" degree room. It is currently connected to {obj['ip']}.")
    else:
        return (f"The {obj['name']} is located in the {obj['location']}, "
                f"is currently {obj['status']}, is set to {obj['target_temperature']} degree in a {obj['room_temperature']}"
                f" degree room. It is currently disconnected.")

def set_target(obj, temperature: int):
    obj["target_temperature"] = temperature

def get_target(obj):
    return obj["target_temperature"]

def thermostat_new(name: str, location: str, base_power: float, status: str, room_temperature: int, target_temperature: int):
    device = make(Device, name, location, base_power, status)
    connectable  = make(Connectable)
    obj = device | connectable | {
        "room_temperature": int(room_temperature),
        "target_temperature": int(target_temperature),
        "_class": Thermostat,
    }
    global_devices.append(obj)
    return obj

Thermostat = {
    "get_power_consumption": thermostat_get_power_consumption,
    "describe_device": thermostat_describe,
    "set_target_temperature": set_target,
    "get_target_temperature": get_target,
    "_classname": "Thermostat",
    "_parent": [Device, Connectable], 
    "_new": thermostat_new
}


###################
### Camera ###
def camera_get_power_consumption(obj):
    if obj["status"] != "on":
        return 0
    return obj["base_power"] * obj["resolution_factor"]

def camera_describe(obj):
    resolution_factor = ""
    if obj["resolution_factor"] < 5:
        resolution_factor = "low"
    if 5 <= obj["resolution_factor"] <10:
        resolution_factor = "medium"
    if obj["resolution_factor"] >= 10:
        resolution_factor = "high"

    if obj["connected"]:
        return (f"The {obj['name']} is located in the {obj['location']}, "
                f"is currently {obj['status']}, and is a {resolution_factor} resolution sensor."
                f" It is currently connected to {obj['ip']}.")
    else:
        return (f"The {obj['name']} is located in the {obj['location']}, "
                f"is currently {obj['status']}, and is a {resolution_factor} resolution sensor."
                f" It is currently disconnected.")

def camera_new(name: str, location: str, base_power: float, status: str, resolution_factor: int):
    device = make(Device, name, location, base_power, status)
    connectable  = make(Connectable)
    obj = device | connectable | {
        "resolution_factor": int(resolution_factor),
        "_class": Camera,
    }
    global_devices.append(obj)
    return obj

Camera = {
    "get_power_consumption": camera_get_power_consumption,
    "describe_device": camera_describe,
    "_classname": "Camera",
    "_parent": [Device, Connectable], 
    "_new": camera_new,
}

if __name__ == "__main__":
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

    print("=== Testing Thermostat ===")
    call(bathroom_thermostat, "connect", "192.168.1.5")
    print("Connected?", call(bathroom_thermostat, "is_connected"))
    print(call(bathroom_thermostat, "describe_device"))
    print("Power:", call(bathroom_thermostat, "get_power_consumption"))
    #call(bathroom_thermostat, "toggle_status")
    call(bathroom_thermostat, "disconnect")
    print("Connected?", call(bathroom_thermostat, "is_connected"))
    print(call(bathroom_thermostat, "describe_device"))
    print("Power:", call(bathroom_thermostat, "get_power_consumption"))
    print("---")

    print("=== Testing Camera ===")
    call(living_room_camera, "connect", "192.168.1.5")
    print("Connected?", call(living_room_camera, "is_connected"))
    print(call(living_room_camera, "describe_device"))
    print("Power:", call(living_room_camera, "get_power_consumption"))
    #call(living_room_camera, "toggle_status")
    #call(living_room_camera, "disconnect")
    print("Connected?", call(living_room_camera, "is_connected"))
    print(call(living_room_camera, "describe_device"))
    print("Power:", call(living_room_camera, "get_power_consumption"))
    print("---")


##########################################--STEP2--##########################################
###################
### SmartHouseManagement - Part I ###
def calculate_total_power_consumption(obj, *, search_type = None, search_room = None):
    if search_type is None:
        search_type = obj.get("search_type")
    if search_room is None:
        search_room = obj.get("search_room")
        
    # print("search type: ", search_type)
    # print("search room: ", search_room)    
    total_power_consumption = 0
    for device in global_devices:
        if search_type and device["_class"]["_classname"] != search_type:
            continue
        if search_room and device["location"] != search_room:
            continue
        total_power_consumption += call(device, "get_power_consumption")
    return total_power_consumption

def get_all_device_description(obj, *, search_type= None, search_room = None):
    if search_type is None:
        search_type = obj.get("search_type")
    if search_room is None:
        search_room = obj.get("search_room")
    list_of_descriptions = []
    for device in global_devices:
        if search_type and device["_class"]["_classname"] != search_type:
            continue
        if search_room and device["location"] != search_room:
            continue
        list_of_descriptions.append(call(device, "describe_device"))
    return list_of_descriptions

def get_all_connected_devices(obj, ip=None):
    results = []
    for device in global_devices:
        if device["_class"]["_classname"] not in ("Thermostat", "Camera"):
            continue
        if not call(device, "is_connected"):
            continue
        if device["status"] != "on":
            continue
        if ip is not None and device["ip"] != ip:
            continue
        results.append((
            call(device, "get_power_consumption"),
            call(device, "describe_device"),
        ))
    return results

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


### SmartHouseManagement - Part II ###
if __name__ == "__main__":
    print("######## Manager Instances - Smart House Management Part II ########")

    call(living_room_camera, "connect", "192.168.1.5")
    call(bathroom_thermostat, "connect", "192.168.1.5")
    manager = make(SmartHouseManagement, "Manager")

    print("**** All devices:")
    for d in call(manager, "get_all_device_description"):
        print("\t-", d)
    print("**** Total power consumption:", call(manager, "calculate_total_power_consumption"))
    print("**** Total power consumption for the camera:", call(manager, "calculate_total_power_consumption", search_type="Camera"))
    print("**** Devices in Bedroom:")
    for device in call(manager, "get_all_device_description", search_room="Bedroom"):
        print("\t-", device)
    print("**** Devices in non-existing room:")
    for device in call(manager, "get_all_device_description", search_room="Some room unknown"):
        print("\t-", device)   
    print("**** All connected devices:")
    for power, device in call(manager, "get_all_connected_devices"):
        print("\t-", power, device)
    print("**** All Connected devices to 192.168.1.5:")
    for power, device in call(manager, "get_all_connected_devices", ip="192.168.1.5"):
        print("\t-", power, device)
    print("**** Connected devices non-existing ip: ", call(manager, "get_all_connected_devices", ip="192.168.1.9"))

### SmartHouseManagement - Part III ###
    print("######## Manager Instances - Smart House Management Part III ########")
    print("**** initial power consumption:", call(manager, "calculate_total_power_consumption"))
    call(bedroom_light, "toggle_status")
    call(bathroom_thermostat, "set_target_temperature", 26)
    print("**** Total consumption after light on and thermostat temp increase:", call(manager, "calculate_total_power_consumption"))

    call(bedroom_light, "toggle_status")
    call(bathroom_thermostat, "set_target_temperature", 22)
    print("**** Total consumption after light off, temp down:", call(manager, "calculate_total_power_consumption"))
    

