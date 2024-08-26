# Purpose of the Docker

This container is running as a ROS2 Node and contains a Ollama installation with Mistral as a LLM.

It also contains the website which is used to get the user input.


## How to run this container

## Start Website, LLM, ParamSetter, FeedbackService and UserInputNode

cd && cd ros_ws && colcon build && source install/setup.bash && cd src/pkg_website_llm && cd launch && clear && ros2 launch launch_all_services.py

## Start Website and LLM via Launchfile

cd && cd ros_ws && colcon build && source install/setup.bash && cd src/pkg_website_llm && cd launch && clear && ros2 launch launch_WebsiteAndLLM.py


## Start only Website

cd && cd ros_ws && colcon build && source install/setup.bash && cd src/pkg_website_llm && cd launch && clear && ros2 launch launch_only_Website.py

## Start only LLM

cd && cd ros_ws && colcon build && source install/setup.bash && cd src/pkg_website_llm && cd launch && clear && ros2 launch launch_only_LLM.py


## Start only UserInputService
cd && cd ros_ws && colcon build && source install/setup.bash && cd src/pkg_website_llm && cd launch && clear && ros2 launch launch_only_FeedbackWebsite.py

Once the container is started, the entry point is directly on the cli of ollama.

## Call Ollama Python API test

navigate to llm_scene_docker/llm_files/

execute: 

```python3  ```
python3 MainLLM.py

## Start the website

ros2 run pkg_website_llm website_llm 

![grafik](https://github.com/user-attachments/assets/0509f24f-0c3e-44e5-864e-d25c2d7ab37e)



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



## How to mock (bypass the LLM) 

1. Connect to Docker
2. enter on the terminal:

ros2 run pkg_pack_item_server pack_item_server  

3. Result is hard coded:

['Box_Gluehlampe', 'Box_Wischblatt','Keilriemen_gross', 'Box_Bremsbacke', 'Keilriemen_klein', 'Tuete']


## How to start the action server of the LLM

ros2 action send_goal /llm_action_server llm_action_interfaces/action/LLM "{userinput: "Box_Wischblatt"}"
