# Import smart_house.py to get the classes and methods
import smart_house
import time
import sys


##### From Book Chapter 6 #####
def run_tests():
    results = {"pass": 0, "fail": 0, "error": 0}
    timings = {}
    #Find each func that starts with "test_" in globals()
    for (name, test) in globals().items():
        if not name.startswith("test_"):
            continue

        start = time.perf_counter_ns()    #Start of time counter
        try:
            test()
            duration = (time.perf_counter_ns() - start) / 1_000_000    #End of time counter if pass
            results["pass"] += 1
            timings[name] = ("PASS", duration)
        except AssertionError:
            duration = (time.perf_counter_ns() - start) / 1_000_000    #End of time counter if fail
            results["fail"] += 1
            timings[name] = ("FAIL", duration)
        except Exception:
            duration = (time.perf_counter_ns() - start) / 1_000_000    #End of time counter if error
            results["error"] += 1
            timings[name] = ("ERROR", duration)
    #Result of each individual test incl. duration
    print("\n### Test Results ###")
    for name, (status, duration) in timings.items():
        print(f"{name:50s} {status:6s} ({duration: 6.3f} ms)")
    #Summary of all tests
    print("####################")
    print(f"pass:  {results['pass']}")
    print(f"fail:  {results['fail']}")
    print(f"error: {results['error']}")

#### End of Book Chapter 6 ####


# Defining all tests

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

#TODO Create tests for the management
#TODO Implement selective test execution with --select <pattern>
#TODO Ensure that only functions are called as tests and not variables

if __name__ == "__main__":
    run_tests()