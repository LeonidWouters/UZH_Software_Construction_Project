# Definition of Parent Classes

# Parent Class <Devices>

def make_device(name: str, location: str, base_power: float, status: str):
    return{"name": name,
           "location": location,
           "base_power": base_power,
           "status": status,
           "_classname": "Device",
           "_parent": None
           }


def toggle_status(device):
    if device["status"] == "on":
        device["status"] = "off"
    else:
        device["status"] = "on"


def get_power_consumption():
    raise NotImplementedError("This method must be implemented in the subclasses!")


def describe_device():
    raise NotImplementedError("This method must be implemented in the subclasses!")

# Parent Class <Connectable>

def make_connectable():
    return {"connected": False,
            "ip": None,
            "_classname": "Connectable",
            "_parent": None
            }


def connect(connectable, ip):
    connectable["connected"] = True,
    connectable["ip"] = ip


def disconnect(connectable):
    connectable["connected"] = False,
    connectable["ip"] = None


def is_connected(connectable):
    return connectable["connected"]

# Definition of Subclasses

# Subclass Light

def make_light(name: str, location: str, base_power: float, status, brightness):
    light = make_device(name, location, base_power, status)
    light["brightness"] = brightness
    light["_classname"] = "Light"
    light["_parent"] = "Device"
    return light


def get_power_consumption_light(light):
    if light["status"] == "on":
        return round(light["base_power"] * light["brightness"] / 100)
    else:
        return 0


def describe_device_light(light):
    return (f"The {light['name']} is located in the {light['location']}, "
            f"is currently {light['status']}, and is set to {light['brightness']}% brightness.")

test_light = make_light("Test Light", "Living Room", 19.79, "off", 90)

toggle_status(test_light)
print(test_light)
print(get_power_consumption_light(test_light))
print(describe_device_light(test_light))



