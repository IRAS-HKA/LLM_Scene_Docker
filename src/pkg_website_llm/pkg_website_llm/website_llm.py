from flask import Flask, render_template, request, jsonify

from action_msgs.msg import GoalStatus
import rclpy
from rclpy.node import Node
from .UserInput import UserInput
from .WebsiteFeedbackData import WebsiteFeedbackData
from .UserInputServiceSender import UserInputService 
from .ActionClientToPreProcessing import LLMActionClient
from .PackItemServer import PackItemsService
from .SelectedItemsToPack import SelectedItems

from .ParamGetter import ParamGetter
from .FileReadWriter import FileReadWriter

import os
import glob
import re

# Assuming this script is located in ros_ws/src/pkg_website_llm/pkg_website_llm/website_llm.py
# Get the absolute path to the directory containing this script
current_dir = os.path.abspath(os.path.dirname(__file__))
print("Vor Slash")
print(current_dir)

# Set the templates folder to the 'templates' directory relative to the current directory
template_dir = os.path.join(current_dir, 'templates')

#static_dir = os.path.join(current_dir, 'static')

static_dir = '/home/robot/ros_ws/src/pkg_website_llm/pkg_website_llm/static'

# Create the Flask app with the correct template folder

#app = Flask(__name__, template_folder='/home/robot/ros_ws/src/pkg_website_llm/pkg_website_llm/templates', static_url_path='/static')
app = Flask(__name__, template_folder='/home/robot/ros_ws/src/pkg_website_llm/pkg_website_llm/templates', static_folder=static_dir, static_url_path='')



@app.route('/')
def index():
    file_path_box = "/home/robot/ros_ws/src/pkg_website_llm/pkg_website_llm/static/Hintergrund.png"
    file_path_pack = "/home/robot/ros_ws/src/pkg_website_llm/pkg_website_llm/static/PackPlanBild.png"
        
    if os.path.exists(file_path_box):
        server.get_logger().info("Hintergrund.png wird gelöscht")
        os.remove(file_path_box)
        
    if os.path.exists(file_path_pack):
        server.get_logger().info("PackPlanBild.png wird gelöscht")
        os.remove(file_path_pack)
    # for root, dirs, files in os.walk(static_dir):
    #     for file in files:
    #         server.get_logger().info(os.path.join(root, file))
    
    FileReadWriter.writeWebsiteFeedbackInitially()
    FileReadWriter.writeUserInputInitially()

    return render_template('index.html')

@app.route('/button_click', methods=['POST'])
def button_click():
    FileReadWriter.writeWebsiteFeedbackInitially()
    FileReadWriter.writeUserInputInitially()
    
    # Receive User Input from the website
    data = request.json
    user_input = data.get('user_input', '')
    command = data.get('communication_form', '')
    sel_language = data.get('selected_language', '')
    
    server.get_logger().info(f"Command (von webseite_llm): {command} and User Input: {user_input} and language is: {sel_language}")

    # write it to the ROS2 parameter server    
    #parameter_setter = ParamGetter()
    #mod_user_input = "'" + user_input.replace("BEFEHL:", "").replace("Frage:", "")  + "'"
    #parameter_setter.set_ros2_param('user_input',mod_user_input)
    #parameter_setter.set_ros2_param('user_command', command)
    mod_user_input = "'" + user_input.replace("BEFEHL:", "").replace("Frage:", "")  + "'"
    FileReadWriter.writeUserInputFile("user_input", mod_user_input)
    FileReadWriter.writeUserInputFile("user_command", command)
    FileReadWriter.writeUserInputFile("sel_language", sel_language)

    
    # This is to call the LLM Action server directly
    future = server.send_goal(user_input)
    server.get_logger().info(f"Server status: {server.status}")
    
    # check if goal status is succeeded otherwise spin the node until it is finished!
    while server.status != GoalStatus.STATUS_SUCCEEDED:
        server.get_logger().info(f"Server status: {server.status}")
        rclpy.spin_once(server)
    server.get_logger().info(f"Server status finished: {server.status}")

    # Handle the result
    result = server.get_result()
    server.get_logger().info(f"Spin until future complete done ")
    server.get_logger().info(f"Ergebnis Typ: {type(result)}  {result}")
    
    # Give the feedback to the user in a chat bubble
    if "command" in command and sel_language == "de":
        result = "Diese Objekte werden gepackt: " + result
    elif "command" in command and sel_language == "en":
        result = "These objects are being packed: " + result
    else :
        result = ""+ result 
      
           
    return jsonify({"message": "Button was clicked!", "received": result})

@app.route('/button_approve', methods=['POST'])
def button_approve():
    
    # Set User approval to True
    #parameter_setter = ParamGetter()
    #parameter_setter.set_ros2_param('user_approval',"True")
    FileReadWriter.writeUserInputFile("user_approval", "True")
    
    return jsonify({"message": "Approved by user!", "received": "Approval"})

@app.route('/button_disapprove', methods=['POST'])
def button_disapprove():

    # Set User approval to False
    #parameter_setter = ParamGetter()
    #parameter_setter.set_ros2_param('user_approval', "False")
    FileReadWriter.writeUserInputFile("user_approval", "False")


    return jsonify({"message": "Disapproved by user", "received": "Disapproval"})

@app.route('/get_data')
def get_data():
    
    # this method is used to get the website feedback data from the ROS2 parameter server
    # parameter_getter = ParamGetter()

    # if parameter_getter.checkIfNodeAvailable("/LLM/Parameter_Setter"):
        
    #     server.get_logger().info("Node gefunden!")
    #     class_id_packages =  parameter_getter.get_ros2_param('package')
    #     class_names = re.findall(r"class_name='(.*?)'", class_id_packages)
    #     server.get_logger().info(class_id_packages)
    #     cylinder_Ids_string =  parameter_getter.get_ros2_param('cylinder_Ids')
    #     cylinder_ids = re.findall(r"cylinder_ids=\[(.*?)\]", cylinder_Ids_string)
    #     cylinder_ids_lists = [list(map(int, ids.split(','))) for ids in cylinder_ids]
        
    #     node_list = parameter_getter.get_ros2_param('node_list')


    #     data = {
    #         'package_content': class_names,
    #         'cylinder_ids': cylinder_ids_lists,
    #         'node_list': node_list.replace("String value is: ", ""),  
    #     }
    # else:
    #     #server.get_clock().sleep_for(rclpy.duration.Duration(seconds=5))
    #     server.get_logger().info("Node NICHT gefunden!")
    #     data = {
    #         'package_content': "NO DATA",
    #         'cylinder_ids': "NO DATA",
    #         'node_list': "NO DATA", 
    #     }


    try:
        class_id_packages = FileReadWriter.readWebsiteFeedbackFile("package")
        class_names = re.findall(r"class_name='(.*?)'", class_id_packages)
        
        class_id_cylinder = FileReadWriter.readWebsiteFeedbackFile("cylinder_Ids")
        cylinder_ids = re.findall(r"cylinder_ids=\[(.*?)\]", class_id_cylinder)
        cylinder_ids_lists = [list(map(int, ids.split(','))) for ids in cylinder_ids]
        
        node_list = FileReadWriter.readWebsiteFeedbackFile("node_list")    
        
        feedback_string = FileReadWriter.readWebsiteFeedbackFile("feedback_string")        
                
        data = {
            'package_content': class_names,
            'cylinder_ids': cylinder_ids_lists,
            'node_list': node_list,
            'feedback_string': feedback_string,  
        }
    except:
        data = {
            'package_content': "NO DATA",
            'cylinder_ids': "NO DATA",
            'node_list': "NO DATA", 
        }

        

    return jsonify(data)


def main():
    print('Hi from LLM_Website. It is starting up.')
    global server
    rclpy.init()
    server = LLMActionClient()
    server.get_logger().info('LLMActionClient Node wurde erstellt')

    try:
        app.run(host='127.0.0.1', port=8080)

    except KeyboardInterrupt:
        print("Server wird beendet")

            
        server.destroy_node() 
        rclpy.shutdown()

if __name__ == '__main__':
    main()
