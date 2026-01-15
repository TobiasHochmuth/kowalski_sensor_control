#!/usr/bin/env bash

# exit when any command fails
set -e

# Check if the script is running as root
[[ $EUID != 0 ]] && echo "Script must run as root."  && exit 1


BUILD_TOOLS=(
)

BUILD_LIBS=(
    python3-requests
    iproute2
    libgpiod-dev
    python3-libgpiod
    build-essential
    python3-dev
)

# Install necessary dependencies
apt update

apt -y install ${BUILD_LIBS[*]}

pip install --upgrade pip
pip install --no-cache-dir adafruit-circuitpython-dht

rm -rf /var/lib/apt/lists/*
