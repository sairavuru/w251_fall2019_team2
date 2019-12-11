FROM ubuntu

# build this: e.g sudo docker build -t mqtt_broker .
# to run this container, do:
# on the host:
# sudo docker run --rm -ti -v /tmp:/tmp --name mqtt_broker mqtt_broker

RUN apt update

ENV DEBIAN_FRONTEND=noninteractive

RUN apt install -y git cmake unzip wget pkg-config build-essential python-opencv python-pip vim-tiny mosquitto-clients libopencv-dev
RUN pip install paho-mqtt ibm-cos-sdk
RUN pip install numpy
RUN apt install nano

WORKDIR /
COPY broker.py /usr/src/app/

CMD ["python","/usr/src/app/broker.py"]
