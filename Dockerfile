##############################################################################
##                                 Base Image                               ##
##############################################################################
FROM hkairas/ros-kuka-eki:humble

##############################################################################
##                                  User                                    ##
##############################################################################
ARG USER=robot
ARG PASSWORD=robot
ARG UID=1000
ARG GID=1000
ARG DOMAIN_ID=66
ENV UID=${UID}
ENV GID=${GID}
ENV USER=${USER}
RUN groupadd -g "$GID" "$USER"  && \
    useradd -m -u "$UID" -g "$GID" --shell $(which bash) "$USER" -G sudo && \
    echo "$USER:$PASSWORD" | chpasswd && \
    echo "%sudo ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/sudogrp

RUN echo "export ROS_DOMAIN_ID=66" >> /etc/bash.bashrc

RUN sudo apt-get update && \
    sudo apt-get install -y python3-pip nano 


RUN curl https://ollama.ai/install.sh | sh

RUN pip3 install ollama
RUN pip3 install pydantic lm-format-enforcer 
RUN pip install ollama flask





USER $USER 
RUN rosdep update



ARG CACHE_BUST

RUN mkdir -p /home/$USER/dependencies_ws/src
WORKDIR /home/$USER/dependencies_ws/src

RUN git clone -b humble https://github.com/eshan-savla/object_detector_tensorflow.git
RUN mv ./object_detector_tensorflow/ros/object_detector_tensorflow_interfaces . && \
rm -rf ./object_detector_tensorflow

# Packing Planning Interfaces
RUN git clone --branch visualization https://github.com/SchmittAndreas/aip_packing_algorithm.git
RUN mv ./aip_packing_algorithm/aip_packing_planning_interfaces . && \
rm -rf ./aip_packing_algorithm

# Grasp Planning Interfaces
RUN git clone https://github.com/LeoSc4/aip_grasp_planning.git
RUN mv ./aip_grasp_planning/aip_grasp_planning_interfaces . && \
rm -rf ./aip_grasp_planning


RUN colcon build --symlink-install

WORKDIR /home/$USER/ros_ws

RUN colcon build --symlink-install
    
COPY --chown=$USER:$USER --chmod=0755 ./startOllama.sh /home/$USER/ros_ws/startOllama.sh
#RUN srv="ollama serve" && $srv& sleep 5 && ollama run mistral-nemo

CMD ["/bin/bash"]

#ENTRYPOINT [ "cd src ls" ]
ENTRYPOINT [ "./startOllama.sh" ]


