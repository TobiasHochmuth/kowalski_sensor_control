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
def find_dht_path():
    base_path = "/sys/bus/iio/devices/"
    for device in os.listdir(base_path):
        with open(os.path.join(base_path, device, "name"), "r") as f:
            if "dht11" in f.read():
                return os.path.join(base_path, device)
    return None

dht22_path = find_dht_path()

if not dht22_path:
    logger.info("DHT22 sensor not found in /sys/bus/iio/devices/")

def get_humid():
    try:
        with open(os.path.join(dht22_path, "in_humidityrelative_input"), "r") as f:
            hum = float(f.read()) / 1000
            return hum
    except Exception as e:
        logger.info(f"Error reading sensor: {e}")
    
# Find the device folder for ds18b20 (starts with 28-)
base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')
if not device_folders:
    logger.info("No temp sensor found")

device_file = device_folders[0] + '/w1_slave'
def get_temp():
    try:
        logger.info("Reading temperature")
        
        with open(device_file, 'r') as f:
            lines = f.readlines()
            
        if lines[0].strip()[-3:] != 'YES':
            return "CRC Check Failed"

        # Find 't=' and parse the temperature
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            return float(temp_string) / 1000.0
    except Exception as e:
        logger.info(f"Reading temperature failed {e}")
        return f"Error: {e}"
    
    return "ok"

# Check sensor values and post them every 2 seconds
if __name__ == "__main__":
    while True:
        current_temp = get_temp()

        current_humid = get_humid()

        payload_temp = {
            "header": {
                "system_id": 1,
                "component_id": 100,
                "sequence": 0
            },
            "message": {
                "type": "NAMED_VALUE_FLOAT",
                "time_boot_ms": 0,
                "value": current_temp,
                "name": "temp1"
            }
        }

        payload_humid = {
            "header": {
                "system_id": 1,
                "component_id": 101,
                "sequence": 0
            },
            "message": {
                "type": "NAMED_VALUE_FLOAT",
                "time_boot_ms": 0,
                "value": current_humid,
                "name": "humid"
            }
        }
        logger.info(f"Temp: {current_temp}")
        
        logger.info(f"Humidity: {current_humid}")
        
            
        response_temp = requests.post(url, json=payload_temp)
        logger.info(f"Response temp: {response_temp}")

        response_humid = requests.post(url, json=payload_humid)
        logger.info(f"Response humid: {response_humid}")
        time.sleep(2)
