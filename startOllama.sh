#!/bin/bash
echo "Running OLLAMA server"
source /opt/ros/humble/setup.bash
source /home/robot/ros_ws/install/setup.bash
# Start the OLLAMA server
srv="ollama serve"
$srv &
sleep 5
ollama run mistral-nemo



