# Website_LLM_AIP: 

This repository was created to extend the Automated Item Picking project of the Karlsruhe University of Applied Sciences with user interaction via a website and large language model for the scene understanding of the objects to be picked.

### Typical Use Case:

There are objects on a surface, which are to be packed by a KUKA robot, e.g. for despatch.
The user should not only be able to name the exact objects to be gripped for the packing process, e.g. box_wiper blade, but should also be able to ask questions about them. 

Example: Which object can I use to clean my car windscreen? Which objects can I only use to repair the engine? 

Once the docker container is started, the user can choose if only the llm or the combination of website and LLM shall be started.

To interact with the robot, ROS2 is used. The userinput as well as the llmoutput are accessible via ROS2 Service calls shown below.

![WebsiteImage](https://github.com/user-attachments/assets/ecaf8e81-4b81-49e9-b7fc-9b127d4f71dd)


## Used Technologies

- Ollama to run the LLMs 
- Ollama API to connect to the LLMs with Python (https://github.com/ollama/ollama-python)
- Python. Flask for Frontend (as well as CSS, HTML, JavaScript)
- ROS2 to make it work with the project setting and robot

## Structure of the Docker container

In total there are 4 packages created on its own in this docker container, the rest are imported from the other docker containers:

UserFrontend/ Website : *pkg_website_llm*

LLM-Call/Pre-/PostProcessing: *pkg_llm_docker*

ROS2 Interfaces to the other dockers: *llm_interfaces*

ROS2 Action Interface used interally: *llm_action_interfaces*

## Purpose of the Docker

This container is running as a ROS2 Node and contains a Ollama installation with Mistral Nemo as a LLM.


UserInput: The user can chat, scenechat and send commands to the LLM.
WebsiteFeedback: It shows the packed items in the box, the used cylinders as well as the running nodes.

The website also shows the image of the detected objects from the odtf.

The running LLM can be changed (instrutions below).

It also contains the website which is used to get the user input.

## Usage of this docker container in the context of the entire project

This repo explains the context and the interplay of the different docker container
[Link](https://github.com/IRAS-HKA/aip_wiki/blob/main/docs%2Foverview_repository.md).

## How to run this container

## Start all services (Website, LLM, FeedbackService and UserInputNode)

1. Start the container (if not already built, it will do it automatically)
   
```bash
   source start_docker.sh
```
1. Build and source in the dependencies && ros2_ws folder (in this order)
```bash   
    cd dependencies_ws
    source install/setup.bash
    colcon build && source install/setup.bash

    and 

    cd ros_ws
    source install/setup.bash
    colcon build && source install/setup.bash
```
1. Run the corresponding launchFile
```bash
    cd && cd ros_ws && colcon build && source install/setup.bash && cd src/pkg_website_llm && cd launch && clear && ros2 launch launch_all_services.py
```

## How to start only the website (with FeedbackService etc.) WITHOUT LLM
``` bash
    cd && cd ros_ws && colcon build && source install/setup.bash && cd src/pkg_website_llm && cd launch && clear && ros2 launch launch_UserInterface_without_llm.py
```
## How to only run the LLM

```bash
    cd && cd ros_ws && colcon build && source install/setup.bash && cd src/pkg_website_llm && cd launch && clear && ros2 launch launch_only_LLM.py
```


## How to request the User Input

1. Connect to Docker
2. enter on the terminal && source first

```bash  
ros2 service call /LLM/user_interaction llm_interfaces/srv/UserInteraction {''}

ros2 service call /LLM/scene_interpretation llm_interfaces/srv/SceneInterpretation "{user_input: 'TEST'}"

```
Please not in the {}-brackets should be the ObjectDetections, so that the Website can display them.



1. The terminal shows the user input.

#### User Input: Service Call: UserInteraction  

The behaviour tree can access the UserInput as a string via a service. This is available as soon as the user has pressed the ‘Send’ button. 


### How to send a test request to the LLM
ros2 action send_goal /LLM/llm_action_server llm_action_interfaces/action/LLM "{userinput: 'Box_Wischblatt'}"

#### LLM Output (SceneInterpretation) Action: 

The LLM can either be addressed internally by an action call (combination of website and LLM) or by an explicit terminal action call. 

In the first case, the response from the ActionServer is only available if the user has agreed to the result by clicking the ‘Confirm’ button.  

A regular check of the UserApprovals prevents, for example, a declaration text of a wipe sheet from being processed into an unusable packing plan. 

As only one prompt can be executed at a time with Ollama, it was decided to implement it with a ROS2 action. 

This means that the processing progress can be queried at any time and duplicate requests, which can cause crashes, can be avoided.  

Due to the long calculation time of the LLM, the user could be tempted to send another prompt. The resulting possible crash should be avoided. 



## How to change the used LLM

1. Search for compatible model on https://ollama.com/library 
2. Change it in start_ollama.sh -> line 9
3. Change it in pkg_llm_docker OllamaInteraction.py 
   Chat and Generate-Function!
```python 
    # Chat functionality with Ollama API
    def getObjectFromScene(role, prompt):
        return ollama.chat(model='mistral-nemo', messages=[
                {
                    'role': role,
                    'content': prompt,
                    'options': {"seed": 123},
                    "context": [],
                },
        ])
```
