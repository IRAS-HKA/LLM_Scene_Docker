#!/bin/sh



# RUN git clone -b devel https://github.com/eshan-savla/object_detector_tensorflow.git
# RUN mv ./object_detector_tensorflow/ros/object_detector_tensorflow_interfaces . && \
#     rm -rf ./object_detector_tensorflow

SRC_CONTAINER=/home/robot/ros_ws/src
SRC_HOST=./src

# SRC_CONTAINER_2=/home/robot/ros_ws/src/object_detector_tensorflow_interfaces
# SRC_HOST_2=./src/object_detector_tensorflow_interfaces

docker run \
    -it \
    --cpus=4 \
    --memory=8g \
    --name llm_docker \
    --privileged \
    --rm \
    -e DISPLAY=$DISPLAY \
    --env-file .env \
    --volume=/dev:/dev \
    --volume=$SRC_HOST:$SRC_CONTAINER:rw \
    --network=host \
    llm_docker

    # --volume $SRC_HOST_2:$SRC_CONTAINER_2:rw \
    #      
