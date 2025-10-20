# Import smart_house.py to get the classes and methods
import smart_house
import time
import sys

def parse_args(): ##### DISCLAIMER - parse_args function is generated with help from ChatGPT
    select = None
    verbose = False
    i = 1
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == "--select" and i + 1 < len(sys.argv):
            select = sys.argv[i + 1]
            i += 2
            continue
        if a == "--verbose":
            verbose = True
            i += 1
            continue
        i += 1
    return select, verbose

##### run_tests adapted from book Chapter 6 #####
def run_tests():
    select, verbose = parse_args()
    results = {"pass": 0, "fail": 0, "error": 0}
    timings = {}
    
    verbose_catch = []
    for (name, test) in globals().items():
        if not name.startswith("test_"):
            continue
        
        if not callable(test):
            verbose_catch.append(name)
            continue
        elif select and (select not in name):
            continue
        
        start = time.perf_counter_ns()
        try:
            test()
            duration = (time.perf_counter_ns() - start) / 1_000_000   
            results["pass"] += 1
            timings[name] = ("PASS", duration)
        except AssertionError:
            duration = (time.perf_counter_ns() - start) / 1_000_000  
            results["fail"] += 1
            timings[name] = ("FAIL", duration)
        except Exception:
            duration = (time.perf_counter_ns() - start) / 1_000_000
            results["error"] += 1
            timings[name] = ("ERROR", duration)

    if(verbose):
        print("These are not callable items: ")
        for names in verbose_catch:
            print(names)
    else:     
        print("### Test Results ###")
        for name, (status, duration) in timings.items():
            print(f"{name:50s} {status:6s} ({duration: 6.3f} ms)")
        print("####################")
        print(f"pass:  {results['pass']}")
        print(f"fail:  {results['fail']}")
        print(f"error: {results['error']}")


##### TESTS - for TASK 1 #####
def test_light_turn_on():
    reading_light_off = smart_house.make(smart_house.Light,
        "Reading Light 2.5", "Living Room", 300.5, "off", 90)
    smart_house.call(reading_light_off, "toggle_status")
    expected = "on"
    actual = reading_light_off["status"]
    assert expected == actual


def test_light_turn_off():
    reading_light_on = smart_house.make(smart_house.Light,
        "Reading Light 2.5", "Living Room", 300.5, "on", 90)
    smart_house.call(reading_light_on, "toggle_status")
    expected = "off"
    actual = reading_light_on["status"]
    assert expected == actual


def test_thermostat_turn_on():
    thermostat_bathroom_off_disconnected = smart_house.make(smart_house.Thermostat,
        "Bathroom Thermo 8000", "Bathroom", 985.0, "off", 18, 23)
    smart_house.call(thermostat_bathroom_off_disconnected, "toggle_status")
    expected = "on"
    actual = thermostat_bathroom_off_disconnected["status"]
    assert expected == actual


def test_thermostat_turn_off():
    thermostat_bathroom_on_disconnected = smart_house.make(smart_house.Thermostat,
        "Bathroom Thermo 8000", "Bathroom", 985.0, "on", 18, 23)
    smart_house.call(thermostat_bathroom_on_disconnected, "toggle_status")
    expected = "off"
    actual = thermostat_bathroom_on_disconnected["status"]
    assert expected == actual


def test_thermostat_connect():
    thermostat_bathroom_on_disconnected = smart_house.make(smart_house.Thermostat,
        "Bathroom Thermo 8000", "Bathroom", 985.0, "on", 18, 23)
    smart_house.call(thermostat_bathroom_on_disconnected, "connect", "192.168.1.5")
    expected_status = True
    expected_ip = "192.168.1.5"
    actual_status = thermostat_bathroom_on_disconnected["connected"]
    actual_ip = thermostat_bathroom_on_disconnected["ip"]
    assert expected_status == actual_status
    assert expected_ip == actual_ip


def test_thermostat_disconnect():
    # Create a disconnected thermostat
    thermostat_bathroom_on_disconnected = smart_house.make(smart_house.Thermostat,
        "Bathroom Thermo 8000", "Bathroom", 985.0, "on", 18, 23)
    # Connect the thermostat
    smart_house.call(thermostat_bathroom_on_disconnected, "connect", "192.168.1.5")
    # Disconnect the thermostat
    smart_house.call(thermostat_bathroom_on_disconnected, "disconnect")
    expected_status = False
    expected_ip = None
    actual_status = thermostat_bathroom_on_disconnected["connected"]
    actual_ip = thermostat_bathroom_on_disconnected["ip"]
    assert expected_status == actual_status
    assert expected_ip == actual_ip


def test_camera_turn_on():
    camera_balcony_off_disconnected = smart_house.make(smart_house.Camera,
        "Security Camera 3000", "Balcony", 245.8, "off", 2)
    smart_house.call(camera_balcony_off_disconnected, "toggle_status")
    expected = "on"
    actual = camera_balcony_off_disconnected["status"]
    assert expected == actual


def test_camera_turn_off():
    camera_balcony_on_disconnected = smart_house.make(smart_house.Camera,
        "Security Camera 3000", "Balcony", 245.8, "on", 2)
    smart_house.call(camera_balcony_on_disconnected, "toggle_status")
    expected = "off"
    actual = camera_balcony_on_disconnected["status"]
    assert expected == actual


def test_camera_connect():
    camera_balcony_on_disconnected = smart_house.make(smart_house.Camera,
        "Security Camera 3000", "Balcony", 245.8, "on", 2)
    smart_house.call(camera_balcony_on_disconnected, "connect", "192.168.1.5")
    expected_status = True
    expected_id = "192.168.1.5"
    actual_status = camera_balcony_on_disconnected["connected"]
    actual_ip = camera_balcony_on_disconnected["ip"]
    assert expected_status == actual_status
    assert expected_id == actual_ip


def test_camera_disconnect():
    camera_balcony_on_connected = smart_house.make(smart_house.Camera,
        "Security Camera 3000", "Balcony", 245.8, "on", 2)
    smart_house.call(camera_balcony_on_connected, "connect", "192.168.1.5")
    smart_house.call(camera_balcony_on_connected, "disconnect")
    expected_status = False
    expected_id = None
    actual_status = camera_balcony_on_connected["connected"]
    actual_ip = camera_balcony_on_connected["ip"]
    assert expected_status == actual_status
    assert expected_id == actual_ip


def test_light_off_get_power_consumption():
    reading_light_off = smart_house.make(smart_house.Light,
        "Reading Light 2.5", "Living Room", 300.5, "off", 90)
    expected = 0
    actual = smart_house.call(reading_light_off, "get_power_consumption")
    assert expected == actual


def test_light_on_get_power_consumption():
    reading_light_on = smart_house.make(smart_house.Light,
        "Reading Light 2.5", "Living Room", 300.5, "on", 90)
    expected = 270
    actual = smart_house.call(reading_light_on, "get_power_consumption")
    assert expected == actual


def test_thermostat_off_get_power_consumption():
    thermostat_bathroom_off_disconnected = smart_house.make(smart_house.Thermostat,
        "Bathroom Thermo 8000", "Bathroom", 985.0, "off", 18, 23)
    expected = 0
    actual = smart_house.call(thermostat_bathroom_off_disconnected, "get_power_consumption")
    assert expected == actual


def test_thermostat_on_get_power_consumption():
    thermostat_bathroom_on_disconnected = smart_house.make(smart_house.Thermostat,
        "Bathroom Thermo 8000", "Bathroom", 985.0, "on", 18, 23)
    expected = 4925
    actual = smart_house.call(thermostat_bathroom_on_disconnected, "get_power_consumption")
    assert expected == actual


def test_camera_off_get_power_consumption():
    camera_balcony_off_disconnected = smart_house.make(smart_house.Camera,
        "Security Camera 3000", "Balcony", 245.8, "off", 2)
    expected = 0
    actual = smart_house.call(camera_balcony_off_disconnected, "get_power_consumption")
    assert expected == actual


def test_camera_on_get_power_consumption():
    camera_balcony_on_disconnected = smart_house.make(smart_house.Camera,
        "Security Camera 3000", "Balcony", 245.8, "on", 2)
    expected = 491.6
    actual = smart_house.call(camera_balcony_on_disconnected, "get_power_consumption")
    assert expected == actual


def test_light_describe_device():
    reading_light_on = smart_house.make(smart_house.Light,
        "Reading Light 2.5", "Living Room", 300.5, "on", 90)
    expected = "The Reading Light 2.5 is located in the Living Room, is currently on, and is set to 90% brightness."
    actual = smart_house.call(reading_light_on, "describe_device")
    assert expected == actual


def test_thermostat_connected_describe_device():
    camera_balcony_on_disconnected = smart_house.make(smart_house.Camera,
        "Security Camera 3000", "Balcony", 245.8, "on", 8)
    smart_house.call(camera_balcony_on_disconnected, "connect", "192.168.1.5")
    expected = "The Security Camera 3000 is located in the Balcony, is currently on, and is a medium resolution sensor. It is currently connected to 192.168.1.5."
    actual = smart_house.call(camera_balcony_on_disconnected, "describe_device")
    assert expected == actual


def test_thermostat_disconnected_describe_device():
    camera_balcony_on_disconnected = smart_house.make(smart_house.Camera,
        "Security Camera 3000", "Balcony", 245.8, "on", 3)
    smart_house.call(camera_balcony_on_disconnected, "connect", "192.168.1.5")
    smart_house.call(camera_balcony_on_disconnected, "disconnect")
    expected = "The Security Camera 3000 is located in the Balcony, is currently on, and is a low resolution sensor. It is currently disconnected."
    actual = smart_house.call(camera_balcony_on_disconnected, "describe_device")
    assert expected == actual


def test_camera_connected_describe_device():
    camera_balcony_on_disconnected = smart_house.make(smart_house.Camera,
        "Security Camera 3000", "Balcony", 245.8, "on", 8)
    smart_house.call(camera_balcony_on_disconnected, "connect", "192.168.1.5")
    expected = "The Security Camera 3000 is located in the Balcony, is currently on, and is a medium resolution sensor. It is currently connected to 192.168.1.5."
    actual = smart_house.call(camera_balcony_on_disconnected, "describe_device")
    assert expected == actual


def test_camera_disconnected_describe_device():
    camera_balcony_on_disconnected = smart_house.make(smart_house.Camera,
        "Security Camera 3000", "Balcony", 245.8, "on", 8)
    smart_house.call(camera_balcony_on_disconnected, "connect", "192.168.1.5")
    smart_house.call(camera_balcony_on_disconnected, "disconnect")
    expected = "The Security Camera 3000 is located in the Balcony, is currently on, and is a medium resolution sensor. It is currently disconnected."
    actual = smart_house.call(camera_balcony_on_disconnected, "describe_device")
    assert expected == actual
      

##### TESTS - for TASK 2 #####
def test_manager_total_power():
    smart_house.global_devices.clear()
    camera = smart_house.make(smart_house.Camera, "Camera_LR", "Living Room", 500, "on", 8)           
    thermostat = smart_house.make(smart_house.Thermostat, "Thermostat_Bath", "Bathroom", 1200, "on", 18, 24)           
    smart_house.call(camera, "connect", "192.168.1.5")
    smart_house.call(thermostat, "connect", "192.168.1.5")

    manager = smart_house.make(smart_house.SmartHouseManagement, "Manager")
    expected = 4000 + 7200 + 0
    actual = smart_house.call(manager, "calculate_total_power_consumption")
    assert expected == actual


def test_manager_total_power_type_camera():
    smart_house.global_devices.clear()
    camera = smart_house.make(smart_house.Camera, "Camera_LR", "Living Room", 500, "on", 8)                        
    smart_house.call(camera, "connect", "192.168.1.5")

    manager = smart_house.make(smart_house.SmartHouseManagement, "Manager")
    expected = 4000
    actual = smart_house.call(manager, "calculate_total_power_consumption", search_type="Camera")
    assert expected == actual


def test_manager_connected_devices_any_ip():
    smart_house.global_devices.clear()
    camera = smart_house.make(smart_house.Camera, "Camera_LR", "Living Room", 500, "on", 8)           
    thermostat = smart_house.make(smart_house.Thermostat, "Thermostat_Bath", "Bathroom", 1200, "on", 18, 24)                 
    smart_house.call(camera, "connect", "192.168.1.5")
    smart_house.call(thermostat, "connect", "192.168.1.5")

    manager = smart_house.make(smart_house.SmartHouseManagement, "Manager")
    connected = smart_house.call(manager, "get_all_connected_devices")
    powers = sorted(p for (p, _) in connected)
    assert len(connected) == 2
    assert powers == [4000, 7200]
    for _, desc in connected:
        assert "Light_BR" not in desc


def test_manager_connected_devices_specific_ip():
    smart_house.global_devices.clear()
    camera = smart_house.make(smart_house.Camera, "Camera_LR", "Living Room", 500, "on", 8)           
    thermostat = smart_house.make(smart_house.Thermostat, "Thermostat_Bath", "Bathroom", 1200, "on", 18, 24)  
    smart_house.call(camera, "connect", "10.0.0.1")
    smart_house.call(thermostat, "connect", "10.0.0.2")

    manager = smart_house.make(smart_house.SmartHouseManagement, "Manager")
    connected = smart_house.call(manager, "get_all_connected_devices", ip="10.0.0.1")
    assert len(connected) == 1
    assert connected[0][0] == 4000
    assert "Camera_LR" in connected[0][1]


def test_manager_connected_devices_excludes_off_and_disconnected():
    smart_house.global_devices.clear()
    camera = smart_house.make(smart_house.Camera, "Camera_LR", "Living Room", 500, "on", 8)
    thermostat = smart_house.make(smart_house.Thermostat, "Thermostat_Bath", "Bathroom", 1200, "on", 18, 24)
    smart_house.call(camera, "connect", "192.168.1.5")
    smart_house.call(thermostat, "connect", "192.168.1.5")
    smart_house.call(camera, "disconnect")
    smart_house.call(thermostat, "toggle_status")

    manager = smart_house.make(smart_house.SmartHouseManagement, "Manager")
    connected = smart_house.call(manager, "get_all_connected_devices")
    assert connected == []


def test_manager_state_changes_total_consumption_change():
    smart_house.global_devices.clear()
    camera = smart_house.make(smart_house.Camera, "Camera_LR", "Living Room", 500, "on", 8)           
    thermostat = smart_house.make(smart_house.Thermostat, "Thermostat_Bath", "Bathroom", 1200, "on", 18, 24)  
    light = smart_house.make(smart_house.Light, "Light_BR", "Bedroom", 300, "off", 70)               
    smart_house.call(camera, "connect", "192.168.1.5")
    smart_house.call(thermostat, "connect", "192.168.1.5")

    manager = smart_house.make(smart_house.SmartHouseManagement, "Manager")
    baseline = smart_house.call(manager, "calculate_total_power_consumption")                        

    smart_house.call(light, "toggle_status")                                                          
    after_light_on = smart_house.call(manager, "calculate_total_power_consumption")
    assert after_light_on == baseline + 210

    smart_house.call(thermostat, "set_target_temperature", 26)                                        
    after_thermostat_up = smart_house.call(manager, "calculate_total_power_consumption")
    assert after_thermostat_up == after_light_on + 2400


test_variable = 5  

if __name__ == "__main__":
    run_tests()
