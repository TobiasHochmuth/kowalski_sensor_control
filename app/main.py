#! /usr/bin/env python3
import os
import time
import glob
from loguru import logger
import socket

import sys
sys.path.append('/usr/lib/python3/dist-packages') # necessary as requests is installed using apt
import requests

import time

# Internal Url for MAVLink2REST API
url = "http://172.18.0.1:6040/mavlink"
# url = "http://blueos.local/mavlink2rest"

SERVICE_NAME = "GPIO Control"

logger.info(f"Starting {SERVICE_NAME}!")

# routing_table = os.popen("ip route show | grep default | awk '{print $3}'").read().strip()
# logger.info(f"routing table {routing_table}") # should be 172.18.0.1, left here for debugging

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80)) # Doesn't actually send data
# local_ip = s.getsockname()[0] # should be 172.18.0.X, left here for debugging
# s.close()

# logger.info(f"default socket {local_ip}")

# This function finds the correct iio device path automatically for dht22
# def find_dht_path():
#     base_path = "/sys/bus/iio/devices/"
#     for device in os.listdir(base_path):
#         with open(os.path.join(base_path, device, "name"), "r") as f:
#             if "dht11" in f.read():
#                 return os.path.join(base_path, device)
#     return None

# dht22_path = find_dht_path()

# if not dht22_path:
#     logger.info("DHT22 sensor not found in /sys/bus/iio/devices/")

# def get_humid():
#     try:
#         with open(os.path.join(dht22_path, "in_humidityrelative_input"), "r") as f:
#             hum = float(f.read()) / 1000
#             return hum
#     except Exception as e:
#         logger.info(f"Error reading sensor: {e}")
    
# # Find the device folder for ds18b20 (starts with 28-)
# base_dir = '/sys/bus/w1/devices/'
# device_folders = glob.glob(base_dir + '28*')
# if not device_folders:
#     logger.info("No temp sensor found")

# device_file = device_folders[0] + '/w1_slave'
# def get_temp():
#     try:
#         logger.info("Reading temperature")
        
#         with open(device_file, 'r') as f:
#             lines = f.readlines()
            
#         if lines[0].strip()[-3:] != 'YES':
#             return "CRC Check Failed"

#         # Find 't=' and parse the temperature
#         equals_pos = lines[1].find('t=')
#         if equals_pos != -1:
#             temp_string = lines[1][equals_pos+2:]
#             return float(temp_string) / 1000.0
#     except Exception as e:
#         logger.info(f"Reading temperature failed {e}")
#         return f"Error: {e}"
    
#     return "ok"

def find_leak_path1():
    base_path = "/sys/class/leds/"
    if not os.path.exists(base_path):
        return None
        
    for device in os.listdir(base_path):
        if "water_leak1" in device:
            return os.path.join(base_path, device, "brightness")
    return None

leak_sensor_path1 = find_leak_path1()

def find_leak_path2():
    base_path = "/sys/class/leds/"
    if not os.path.exists(base_path):
        return None
        
    for device in os.listdir(base_path):
        if "water_leak2" in device:
            return os.path.join(base_path, device, "brightness")
    return None

leak_sensor_path2 = find_leak_path2()

def monitor_leak(leak_sensor_path):
    path = leak_sensor_path
    
    if not path:
        logger.info("Sensor path not found. Check your dtoverlay config.")
        return

    logger.info(f"Monitoring sensor via: {path}")

    with open(path, "r") as f:
        # Read the 'brightness' (0 for dry, 1 for wet)
        state = f.read().strip()


def format_mavlink_str(name):
    # Ensure name is exactly 10 characters, padded with null terminators
    char_list = list(name[:10])
    while len(char_list) < 10:
        char_list.append("\u0000")
    return char_list


# Check sensor values and post them every 2 seconds
if __name__ == "__main__":
    # temp_name = format_mavlink_str("temp")
    # humid_name = format_mavlink_str("humid")
    leak_name1 = format_mavlink_str("leak1")
    leak_name2 = format_mavlink_str("leak2")

    while True:
        # current_temp = get_temp()

        # current_humid = get_humid()

        current_leak1 = monitor_leak(leak_sensor_path1)
        current_leak2 = monitor_leak(leak_sensor_path2)

        try:
            current_leak1 = float(current_leak1)
        except Exception:
            current_leak1 = 0.0

        try:
            current_leak2 = float(current_leak2)
        except Exception:
            current_leak2 = 0.0

        # payload_temp = {
        #     "header": {
        #         "system_id": 255,
        #         "component_id": 1,
        #         "sequence": 0
        #     },
        #     "message": {
        #         "type": "NAMED_VALUE_FLOAT",
        #         "time_boot_ms": 0,
        #         "name": temp_name,
        #         "value": current_temp
        #     }
        # }
        try:
            current_leak1 = float(current_leak1)
        except Exception:
            current_leak = 0.0
        # payload_humid = {
        #     "header": {
        #         "system_id": 255,
        #         "component_id": 2,
        #         "sequence": 0
        #     },
        #     "message": {
        #         "type": "NAMED_VALUE_FLOAT",
        #         "time_boot_ms": 0,
        #         "name": humid_name,
        #         "value": current_humid
        #     }
        # }

        payload_leak1 = {
            "header": {
                "system_id": 255,
                "component_id": 3,
                "sequence": 0
            },
            "message": {
                "type": "NAMED_VALUE_FLOAT",
                "time_boot_ms": 0,
                "name": leak_name1,
                "value": current_leak1
            }
        }

        payload_leak2 = {
            "header": {
                "system_id": 255,
                "component_id": 4,
                "sequence": 0
            },
            "message": {
                "type": "NAMED_VALUE_FLOAT",
                "time_boot_ms": 0,
                "name": leak_name2,
                "value": current_leak2
            }
        }

        # logger.info(f"Temp: {current_temp}")
        
        # logger.info(f"Humidity: {current_humid}")

        if(current_leak1 == 1):
            logger.info(f"The submarine is leaking in the front!! {current_leak1}")
        else:
            logger.info(f"No leak detected in the front, value: {current_leak1}")

        if(current_leak2 == 1):
            logger.info(f"The submarine is leaking in the back!! {current_leak2}")
        else:
            logger.info(f"No leak detected in the back, value: {current_leak2}")
        
            
        # response_temp = requests.post(url, json=payload_temp)
        # logger.info(f"Response temp: {response_temp.status_code}, {response_temp.text}")

        # response_humid = requests.post(url, json=payload_humid)
        # logger.info(f"Response humid: {response_humid}")

        response_leak1 = requests.post(url, json=payload_leak1)
        logger.info(f"Response leak: {response_leak1}")

        response_leak2 = requests.post(url, json=payload_leak2)
        logger.info(f"Response leak: {response_leak2}")

        time.sleep(2)
