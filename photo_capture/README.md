See attached Dockerfile and app.py

### build container:
docker build -t photo_capture .

### to run the container on the IoT device:

xhost + 

docker run --rm -ti --privileged -e DISPLAY -v /tmp:/tmp --network dream_catcher --name photo_capture photo_capture 
