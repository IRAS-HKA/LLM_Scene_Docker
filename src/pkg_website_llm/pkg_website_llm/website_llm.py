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
    for root, dirs, files in os.walk(static_dir):
        for file in files:
            server.get_logger().info(os.path.join(root, file))

    return render_template('index.html')

@app.route('/button_click', methods=['POST'])
def button_click():
    
    data = request.json
    user_input = data.get('user_input', '')
    command = data.get('communication_form', '')
    server.get_logger().info(f"Command (von webseite_llm): {command}")

    server.get_logger().info(f"Anfrage (von webseite_llm): {user_input}")
    
    parameter_setter = ParamGetter()

    # String wird in der Website gespeichert!
    mod_user_input = "'" + user_input.replace("BEFEHL:", "").replace("Frage:", "")  + "'"
    parameter_setter.set_ros2_param('user_input',mod_user_input)
    
    parameter_setter.set_ros2_param('user_command', command)
    
    # if not rclpy.ok():
    #     rclpy.init(args=None)
    
    
    # This is to call the LLM Action server directly
    
    #future = server.send_goal(user_input)
    server.get_logger().info(f"Input: {user_input}")
    future = server.send_goal(user_input)
    #print("Datenobjekt Typ Future", type(future))
    server.get_logger().info(f"Server status: {server.status}")
    while server.status != GoalStatus.STATUS_SUCCEEDED:
        server.get_logger().info(f"Server status: {server.status}")
        rclpy.spin_once(server)
    server.get_logger().info(f"Server status finished: {server.status}")
    # result = server.get_result()
    result = server.get_result()
    server.get_logger().info(f"Spin until future complete done ")

    server.get_logger().info(f"Ergebnis: {type(result)}")
    server.get_logger().info(f"Ergebnis: {result}")
    
    if "BEFEHL" in user_input:
        result = "Diese Objekte werden gepackt: " + result
    elif "SzenenChat" in user_input:
        result = "Diese Objekte wurden gefunden: " + result
    else :
        result = ""+ result 
    
   #rclpy.init()  # Muss aufgerufen werden, bevor irgendein ROS2-Code ausgeführt wird
    
           
    return jsonify({"message": "Button was clicked!", "received": result})

@app.route('/button_approve', methods=['POST'])
def button_approve():

    UserInput.setApproval(True)
    server.get_logger().info(f"Meinung des Users: {UserInput.getApproval()}")
    
    # rclpy.init()
    #pack_server = PackItemsService()
    #server.get_logger().info("PackItemsService Node erstellt!")
    parameter_setter = ParamGetter()
    parameter_setter.set_ros2_param('user_approval',"True")


    #pack_server.spinNode()


    return jsonify({"message": "Approved by user!", "received": "Approval"})

@app.route('/button_disapprove', methods=['POST'])
def button_disapprove():

    UserInput.setApproval(False)
    server.get_logger().info(f"Meinung des Users: { UserInput.getApproval()}")
    parameter_setter = ParamGetter()
    parameter_setter.set_ros2_param('user_approval', "False")


    return jsonify({"message": "Disapproved by user", "received": "Disapproval"})

@app.route('/get_data')
def get_data():
    
    parameter_getter = ParamGetter()

    if parameter_getter.checkIfNodeAvailable("/LLM/Parameter_Setter"):
        server.get_logger().info("Node gefunden!")
        class_id_packages =  parameter_getter.get_ros2_param('package')
        class_names = re.findall(r"class_name='(.*?)'", class_id_packages)
        server.get_logger().info(class_id_packages)
        cylinder_Ids_string =  parameter_getter.get_ros2_param('cylinder_Ids')
        cylinder_ids = re.findall(r"cylinder_ids=\[(.*?)\]", cylinder_Ids_string)
        cylinder_ids_lists = [list(map(int, ids.split(','))) for ids in cylinder_ids]

        #'picture': WebsiteFeedbackData.getImagePath(),
        data = {
            'package_content': class_names,
            'cylinder_ids': cylinder_ids_lists,
            #'package_content': parameter_getter.get_ros2_param('package'),
            #'cylinder_ids': parameter_getter.get_ros2_param('cylinder_Ids'),   
        }
    else:
        server.get_logger().info("Node NICHT gefunden!")
        data = {
            'package_content': "NO DATA",
            'cylinder_ids': "NO DATA",
            #'package_content': parameter_getter.get_ros2_param('package'),
            #'cylinder_ids': parameter_getter.get_ros2_param('cylinder_Ids'),   
        }
        

    return jsonify(data)


def main():
    print('Hi from LLM_Website. It is starting up.')
    global server
    rclpy.init()
    server = LLMActionClient()
    server.get_logger().info('LLMActionClient Node wurde erstellt')
    #app.run(debug=True, host='127.0.0.1', port=8080)
    try:
        app.run(host='127.0.0.1', port=8080)
        # rclpy.spin(server)
    except KeyboardInterrupt:
        print("Server wird beendet")
        server.destroy_node() 
        rclpy.shutdown()

if __name__ == '__main__':
    main()
