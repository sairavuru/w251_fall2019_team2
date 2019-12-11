FROM ubuntu

# build this: e.g docker build -t photo_capture .
# to run this container, do:
# on the host:
# make sure you're in the X environment
# xhost +
# docker run --rm -ti --privileged -e DISPLAY -v /tmp:/tmp --network dream_catcher --name photo_capture photo_capture

RUN apt update

ENV DEBIAN_FRONTEND=noninteractive

RUN apt install -y git cmake unzip wget pkg-config build-essential python-opencv python-pip vim-tiny mosquitto-clients libopencv-dev libspatialindex-dev libfreetype6-dev libgdal-dev
RUN pip install paho-mqtt
RUN pip install numpy pandas 
RUN pip install folium geopy
RUN pip install --upgrade Cython 
RUN pip install git+git://github.com/larsyencken/proj
RUN pip install pyproj==1.9.6 osmnx==0.9
RUN apt install nano

RUN mkdir /photos
WORKDIR /photos

COPY app.py /usr/src/app/
COPY gps_logs.csv /usr/src/app/
COPY gps_simulator.py /usr/src/app/

CMD ["python","/usr/src/app/app.py"]
