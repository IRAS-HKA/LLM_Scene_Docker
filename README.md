## Website_LLM_AIP:  

# Used Technologies

- Ollama to run the LLMs
- Ollama API to connect to the LLMs with Python
- Python. Flask for Frontend (as well as CSS, HTML, JavaScript)
- ROS2 to make it work with the project setting and robot
  
# Purpose of the Docker

This container is running as a ROS2 Node and contains a Ollama installation with Mistral Nemo as a LLM.
The website looks like this:

(Bild einfügen)

UserInput: The user can chat, scenechat and send commands to the LLM.
WebsiteFeedback: It shows the packed items in the box, the used cylinders as well as the running nodes.

The website also shows the image of the detected objects from the odtf.

The running LLM can be changed (instrutions below).

It also contains the website which is used to get the user input.


## How to run this container

## Start all services (Website, LLM, FeedbackService and UserInputNode)

cd && cd ros_ws && colcon build && source install/setup.bash && cd src/pkg_website_llm && cd launch && clear && ros2 launch launch_all_services.py


## How to start only the website (with FeedbackService etc.) WITHOUT LLM

custom launch File to do

## How to only the LLM

cusotm launch File to do


## How to request the User Input

1. Connect to Docker
2. enter on the terminal
   
ros2 service call /LLM/user_interaction llm_interfaces/srv/UserInteraction {''}

ros2 service call /LLM/scene_interpretation llm_interfaces/srv/SceneInterpretation "{user_input: 'TEST'}"


Please not in the {}-brackets should be the ObjectDetections, so that the Website can display them.

3. The terminal shows the user input.



## How to start the Action Client and Server to send the user input to the LLM

Client:
1. Open New Terminal
2. Connect to LLM_Docker
3. colcon build && source install/setup.bash
4. Navigate to the folder: cd src/pkg_website_llm/pkg_website_llm/
5. python3 ActionClientToPreProcessing.py 

Server:
1. Open New Terminal
2. Connect to LLM_Docker
3. colcon build && source install/setup.bash
4. Navigate to the folder: cd /src/pkg_llm_docker/pkg_llm_docker
5. python3 LLM_Action_Server.py 

### How to send a test request to the LLM
ros2 action send_goal /llm_action_server llm_action_interfaces/action/LLM "{userinput: 'BEFEHL: Box_Wischblatt' }"


## How to start the action server of the LLM

ros2 action send_goal /llm_action_server llm_action_interfaces/action/LLM "{userinput: "Box_Wischblatt"}"
