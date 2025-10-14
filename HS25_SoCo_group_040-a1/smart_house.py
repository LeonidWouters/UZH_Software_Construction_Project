import pprint
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

# Subclass <Light>

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

# test_light = make_light("Test Light", "Living Room", 19.79, "off", 90)
#
# toggle_status(test_light)
# print(test_light)
# print(get_power_consumption_light(test_light))
# print(describe_device_light(test_light))

# Subclass <Thermostat>

def make_thermostat(name: str, location: str, base_power: float, status, room_temperature: int, target_temperature: int):
    thermostat = make_device(name, location, base_power, status)
    thermostat.update(make_connectable())
    thermostat["_classname"] = "Thermostat"
    thermostat["_parent"] = ["Device", "Connectable"]
    thermostat["room_temperature"] = room_temperature
    thermostat["target_temperature"] = target_temperature
    return thermostat


def get_power_consumption_thermostat(thermostat):
    if thermostat["status"] == "on":
        return thermostat["base_power"]*abs(thermostat["target_temperature"] - thermostat["room_temperature"])
    else:
        return 0


def describe_device_thermostat(thermostat):
    pass


# test_thermo = make_thermostat("test_thermo", "bathroom", 4.9, "off", 18, 23)
# pprint.pprint(test_thermo)
# toggle_status(test_thermo)
# connect(test_thermo, "19.09.22.11.001")
# pprint.pprint(test_thermo)
# print(get_power_consumption_thermostat(test_thermo))




