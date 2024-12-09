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
        self.detections = []
        self.get_logger().info('Subscriber was initalised')
    
    def listener_callback(self, msg):
        # check with the lock if the detections are already being processed
        with self.detections_lock:
            self.detections = msg.detections

        
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
        
        
        # Check which user command and with language is selected
        user_command = FileReadWriter.readUserInputFile('user_command')
        sel_language = FileReadWriter.readUserInputFile('sel_language')
        
        self.get_logger().info('sel_language: {0}'.format(sel_language))
        
        # Format the prompt to be used in the LLM
        prompt = preprocessing_unit.formatPrompt("",user_input, str(user_command), str(sel_language))
                
        self.get_logger().info('Prompt: {0}'.format(prompt))
        self.get_logger().info('User Command: {0}'.format(user_command))
        
        # If the preprocessing was successful, send feedback of 50 % progress
        feedback_msg.progress = 50
        self.get_logger().info('Feedback: {0}'.format(feedback_msg.progress))
        self.get_logger().info('LLM was started')
        goal_handle.publish_feedback(feedback_msg)
        
        # Start the LLM with the formatted prompt
        result_dict = MainLLM.startLLM(prompt, user_input,str(user_command))
        
        # send the feedback
        goal_handle.publish_feedback(feedback_msg)
        goal_handle.succeed()

        result = LLM.Result()
        result.llmoutput = str(result_dict)
        
        
        # In order to print the results on the website in the correct language, the result is translated back to German or Englisch
        try:
            # Translate back to German
            if sel_language == "en":
                self.get_logger().info('Result (Englisch): {0}'.format(result_dict))
                result_dict = FileReadWriter.translateToGerman(result_dict)
            
            mod_user_input = "'" + str(result_dict)  + "'"

            FileReadWriter.writeUserInputFile('pack_list', mod_user_input)
            
        except Exception as e:
            self.get_logger().error(f'Translation of result failed, check  if UserInput.json is correct {e}')
        
        self.get_logger().info('LLM was executed successfully!')
        self.get_logger().info('Result: {0}'.format(result.llmoutput))
     
        return result


def main(args=None):
    rclpy.init(args=args)

    action_server = LLMActionServer()
    action_server.get_logger().info('Action Server started')
    rclpy.spin(action_server)
    
    action_server.get_logger().info('Created executor ')

    action_server.get_logger().info('Spin has started')

    action_server.destroy()
    action_server.get_logger().info('Action Server and ACTION destroyed')

    action_server.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()