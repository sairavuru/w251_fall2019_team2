# IoT Broker on TX2

### Create an alpine container on network hw3-network-tx2

```docker run -ti --name iot-broker --network dream_catcher alpine ash```


### Add packages to the container

```
apk add nano
apk add mosquitto
apk add mosquitto-clients
```

### Modify mosquitto configuration file:
```nano /etc/mosquitto/mosquitto.conf```

#### to:
```
connection ibmcloud
address IP_ADDRESS:PORT

topic topic/dream_catcher both 0
```
### Run mosquitto broker
```mosquitto -c /etc/mosquitto/mosquitto.conf```

mosquitto[23]: mosquitto version 1.6.3 starting
mosquitto[23]: Config loaded from /etc/mosquitto/mosquitto.conf.
mosquitto[23]: Opening ipv4 listen socket on port 1883.
mosquitto[23]: Opening ipv6 listen socket on port 1883.
