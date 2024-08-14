import time

import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

from rclpy.action import ActionServer
from rclpy.node import Node

from .PreProcessing import PreProcessing
from .DetectionSubscriber import DetectionSubscriber
from object_detector_tensorflow_interfaces.msg import Detections
from .Detection import Detection
from .MainLLM import MainLLM

import threading
from pkg_website_llm.SelectedItemsToPack import SelectedItems
from pkg_website_llm.PackItemServer import PackItemsService


from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor


from llm_action_interfaces.action import LLM

from pkg_website_llm.ParamGetter import ParamGetter

from pkg_website_llm.FileReadWriter import FileReadWriter


class LLMActionServer(Node):

    def __init__(self):
        super().__init__('llm_action_server_node')
        self._action_server_callback_group = MutuallyExclusiveCallbackGroup()
        self._action_server = ActionServer(
            self,
            LLM,    
            'llm_action_server',
            self.execute_callback, callback_group=self._action_server_callback_group)
        self.get_logger().info('Action Server is ready')
        self.subscription_callback_group = MutuallyExclusiveCallbackGroup()
        self.detections_lock = threading.Lock()
        self.subscription = self.create_subscription(
            Detections,
            '/detection_node/detections',
            self.listener_callback,
            10, callback_group=self.subscription_callback_group)
        self.subscription
        self.detections = []# prevent unused variable warning
        self.get_logger().info('Subscriber wurde initalisiert')
    
    def listener_callback(self, msg):
        #self.get_logger().info('I heard: "%s"' % msg.detections)
        #self.get_logger().info('Die Nachricht wurde empfangen')
 
        with self.detections_lock:
            self.detections = msg.detections
        #prompt = PreProcessing.formatPrompt(detections, "")
        #MainLLM.startLLM(prompt)
        
    def execute_callback(self, goal_handle):
        # Define instance of PreProcessing
        with self.detections_lock:
            preprocessing_unit = PreProcessing(self.detections)
        
        # Receive user input from the website
        user_input = goal_handle.request.userinput
        self.get_logger().info('Received goal order: {0}'.format(user_input))
        self.get_logger().info('Executing goal...')
        
        # Send Feedback after 0% of the process: PreProcessing started
        feedback_msg = LLM.Feedback()
        feedback_msg.progress = 0
        goal_handle.publish_feedback(feedback_msg)
        
        
        #parameter_getter = ParamGetter()
        #user_command = parameter_getter.get_ros2_param('user_command')
        user_command = FileReadWriter.readUserInputFile('user_command')
        
        prompt = preprocessing_unit.formatPrompt("",user_input, str(user_command))
        
        # Create Prompt for the LLM (PreProcessing done) and send feedback after 50 %
        # if "BEFEHL" in user_input:
        #     prompt = preprocessing_unit.formatPrompt("",user_input, "Generate")
        # else:
        #     prompt = preprocessing_unit.formatPrompt("",user_input, "Chat")
        
        self.get_logger().info('Prompt: {0}'.format(prompt))
        self.get_logger().info('Prompt mit Anweisung: {0}'.format(user_command))
        
        feedback_msg.progress = 50
        self.get_logger().info('Feedback: {0}'.format(feedback_msg.progress))
        self.get_logger().info('LLM was started')
        goal_handle.publish_feedback(feedback_msg)
        
        # Start the LLM
        result_dict = MainLLM.startLLM(prompt, user_input,str(user_command))
        goal_handle.publish_feedback(feedback_msg)
        goal_handle.succeed()

        result = LLM.Result()
        result.llmoutput = str(result_dict)
        
        
        try:
            param = ParamGetter()
            mod_user_input = "'" + str(result_dict)  + "'"
            #param.set_ros2_param('pack_list', mod_user_input)
            FileReadWriter.writeUserInputFile('pack_list', mod_user_input)
        except Exception as e:
            self.get_logger().error(f'Saving parameter pack_list failed {e}')
        
        self.get_logger().info('LLM was executed successfully!')
        self.get_logger().info('Result: {0}'.format(result.llmoutput))
     
        return result


def main(args=None):
    print("[LLM Action Server] MAIN")
    rclpy.init(args=args)

    action_server = LLMActionServer()
    action_server.get_logger().info('Action Server erstellt')
    rclpy.spin(action_server)
    
    #executor = MultiThreadedExecutor()
    action_server.get_logger().info('executor erstellt')

    #rclpy.spin(action_server, executor=executor)
    action_server.get_logger().info('Spin beginnt')

    action_server.destroy()
    action_server.get_logger().info('Action Server beendet')


    action_server.get_logger().info('ACTION beendet')
    
    action_server.get_logger().info('Nachm Shutdown von ACTION')
    action_server.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()