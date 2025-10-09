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