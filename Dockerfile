FROM python:3.9-slim-bullseye

COPY install.sh /install.sh

RUN /install.sh

COPY app /app
RUN python /app/setup.py install

EXPOSE 80/tcp

LABEL version="0.0.1"
# TODO: Add a Volume for persistence across boots
LABEL permissions='\
{\
  "ExposedPorts": {\
    "80/tcp": {}\
  },\
  "HostConfig": {\
    "Privileged": true,\
    "Binds":[\
      "/root/.config:/root/.config",\
      "/dev:/dev",\
      "/sys:/sys"\
    ],\
    "ExtraHosts": ["host.docker.internal:host-gateway"],\
    "PortBindings": {\
      "80/tcp": [\
        {\
          "HostPort": ""\
        }\
      ]\
    },\
    "CpuPeriod":100000,\
    "CpuQuota":20000,\
    "Memory":209715200,\
  }\
}'
LABEL authors='[\
    {\
        "name": "Tobias Hochmuth",\
        "email": "contact@mud-skipper.nl"\
    }\
]'
LABEL company='{\
        "about": "",\
        "name": "Mudskipper",\
        "email": "contact@mud-skipper.nl"\
    }'
LABEL type="gpiocontrol"
LABEL tags='[\
        "sensor-reading"\
    ]'
LABEL readme='https://github.com/TobiasHochmuth/kowalski_sensor_control/blob/main/Readme.md'
LABEL links='{\
        "website": "https://github.com/TobiasHochmuth/kowalski_sensor_control",\
        "support": "https://github.com/TobiasHochmuth/kowalski_sensor_control"\
    }'
LABEL requirements="core >= 1.4"

ENTRYPOINT cd /app && python main.py
