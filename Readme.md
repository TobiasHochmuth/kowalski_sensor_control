# Kowalski Sensor Control

Controls a ds18b20 temperature sensor and a dht22 humidity/temperature sensor.

Enable qemu static support with a docker

```
docker buildx create --name multiarch --driver docker-container --use
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
```

Then build it:

```
docker buildx build --platform linux/amd64,linux/arm/v7 . -t tobiashochmuth/sensors:general --output type=registry
```

Then pull it in blueos (or load it as an extension on blueos using their UI inside installed extensions):

```
red-pill
sudo docker run -d --net=host --name=gpiocontrol --restart=unless-stopped tobiashochmuth/sensors:general
```