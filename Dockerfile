##############################################################################
##                                 Base Image                               ##
##############################################################################
FROM hkairas/ros-kuka-eki:humble

##############################################################################
##                                 Global Dependecies                       ##
##############################################################################
RUN apt-get update && apt-get install --no-install-recommends -y \
    bash nano htop git sudo wget curl \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/* 

RUN curl https://ollama.ai/install.sh | sh

RUN pip3 install \
    ollama \
    pydantic \
    lm-format-enforcer 

RUN pip install \
    ollama \
    flask

##############################################################################
##                                  User                                    ##
##############################################################################
ARG USER=robot
ARG PASSWORD=robot
ARG UID=1000
ARG GID=1000
ENV UID=${UID}
ENV GID=${GID}
ENV USER=${USER}
RUN groupadd -g "$GID" "$USER"  && \
    useradd -m -u "$UID" -g "$GID" --shell $(which bash) "$USER" -G sudo && \
    echo "$USER:$PASSWORD" | chpasswd && \
    echo "%sudo ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/sudogrp && \
    chmod 0440 /etc/sudoers.d/sudogrp && \
    chown ${UID}:${GID} -R /home/${USER}
RUN echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> /etc/bash.bashrc

USER $USER 
RUN mkdir -p /home/$USER/dependencies_ws/src
RUN mkdir -p /home/$USER/ros_ws/src

##############################################################################
##                                 dependecies_ws                           ##
##############################################################################
WORKDIR /home/$USER/dependencies_ws/src

ARG CACHE_BUST

# object_detector_tensorflow_interfaces
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

WORKDIR /home/$USER/dependencies_ws

RUN rosdep update --rosdistro $ROS_DISTRO
RUN rosdep install --from-paths src --ignore-src -y

RUN . /opt/ros/humble/setup.sh && colcon build --symlink-install
RUN echo "source /home/$USER/dependencies_ws/install/setup.bash" >> /home/$USER/.bashrc

##############################################################################
##                                 ros_ws                                   ##
##############################################################################
WORKDIR /home/$USER/ros_ws

COPY src ./src

RUN . /opt/ros/humble/setup.sh && . /home/$USER/dependencies_ws/install/setup.sh && colcon build --symlink-install
RUN echo "source /home/$USER/ros_ws/install/setup.bash" >> /home/$USER/.bashrc

##############################################################################
##                                 autostart                                ##
##############################################################################
COPY ./startOllama.sh /home/$USER/ros_ws/startOllama.sh

RUN sudo sed --in-place --expression \
    '$isource "/home/$USER/ros_ws/install/setup.bash"' \
    /ros_entrypoint.sh

RUN sudo sed --in-place --expression \
    '$isource "/home/$USER/dependencies_ws/install/setup.bash"' \
    /ros_entrypoint.sh

RUN sudo sed --in-place --expression \
    '$isource "/home/$USER/ros_ws/install/setup.bash"' \
    /ros_entrypoint.sh

RUN sudo sed --in-place --expression \
    '$i./startOllama.sh' \
    /ros_entrypoint.sh

#RUN ollama serve & sleep 5 && ollama run mistral-nemo

CMD ["/bin/bash"]
