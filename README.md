###
Build Image
##
docker build . -t docker/fedora-python:v1.0

###
Run container

##
docker run -t -d --name mycontainer docker/fedora-python:v1.0 