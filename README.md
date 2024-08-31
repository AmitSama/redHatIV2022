# What is this code doing

## It is git repository parser to display each repo's base image provided in the Docker file

# Pre-requisites

- Python3
- pip3
- Docker
- Kubenetes

# How to build docker image

>
docker build --build-arg REPOSITORY_LIST_URL=https://gist.githubusercontent.com/jmelis/c60e61a893248244dc4fa12b946585c4/raw/25d39f67f2405330a6314cad64fac423a171162c/sources.txt . -t docker/fedora-python:v1.0

### Run container in Docker

>
docker run -t -d --name mycontainer docker/fedora-python:v1.0

### Run application in Kubernetes cluster

> kubectl apply -f manifest.yaml

### Delete Kubernetes cluster

> kubectl delete -f manifest.yaml