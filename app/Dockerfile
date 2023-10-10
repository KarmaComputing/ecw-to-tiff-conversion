# Use Ubuntu 20.04 as the base image
FROM ubuntu:20.04

# Update the package index and install necessary dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.9 python3.9-dev python3.9-distutils python3-pip

# Make sure pip is up to date
RUN python3.9 -m pip install --upgrade pip

USER root

WORKDIR /ecw-to-tiff
COPY ./requirements.txt /ecw-to-tiff
RUN pip3 install -r requirements.txt
COPY ./tif-to-COG.sh /ecw-to-tiff
COPY ./ecw-to-COG.sh /ecw-to-tiff
COPY ./ /ecw-to-tiff
ENTRYPOINT ["/ecw-to-tiff/entrypoint.sh"]

