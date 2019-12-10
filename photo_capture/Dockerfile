FROM ubuntu

# build this: e.g docker build -t photo_capture .
# to run this container, do:
# on the host:
# make sure you're in the X environment
# xhost +
# docker run --rm -ti --privileged -e DISPLAY -v /tmp:/tmp --network dream_catcher --name photo_capture photo_capture

RUN apt update

ENV DEBIAN_FRONTEND=noninteractive

RUN apt install -y python-opencv python-pip vim-tiny mosquitto-clients libopencv-dev
RUN pip install paho-mqtt
RUN pip install numpy
RUN apt install nano

RUN mkdir /photos
WORKDIR /photos

COPY app.py /usr/src/app/
COPY gps_logs.csv /usr/src/app/

CMD ["python","/usr/src/app/app.py"]
