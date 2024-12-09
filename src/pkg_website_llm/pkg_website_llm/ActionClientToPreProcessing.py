import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
#from .UserInput import UserInput

from action_msgs.msg import GoalStatus

from llm_action_interfaces.action import LLM

import time

class LLMActionClient(Node):

    # Initialize the ActionClient of the LLM and the GoalStatus
    def __init__(self):
        super().__init__('llm_action_client')
        self._action_client = ActionClient(self, LLM, 'llm_action_server')
        self.status = GoalStatus.STATUS_UNKNOWN
        self.get_logger().info('Action Client initialized')

    def send_goal(self, user_input):
        self.get_logger().info('Beginning of sending the goal')
        self.status = GoalStatus.STATUS_EXECUTING
        self.get_logger().info('User Input in send_goal: {0}'.format(user_input))
        request_msg = LLM.Goal()
        request_msg.userinput = str(user_input)

        self._action_client.wait_for_server(timeout_sec=10.0)
        
        self.get_logger().info("Server was found")
        self._send_goal_future = self._action_client.send_goal_async(request_msg)
        self.get_logger().info("Goal was sent")
        
        temp = self._send_goal_future.add_done_callback(self.goal_response_callback) 
        self.get_logger().info("Callback added to future")
        return temp

    def goal_response_callback(self, future):
        goal_handle = future.result()
        
        if not goal_handle.accepted:
            self.get_logger().info('LLM request rejected :(')
            return

        self.get_logger().info('LLM request accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)
        

    def get_result_callback(self, future):

        try:
            result = future.result().result
            self.get_logger().info('TYPE: {0}'.format(type(result)))
            self.status = GoalStatus.STATUS_SUCCEEDED
            self._result = result.llmoutput 
            self.get_logger().info('Result: {0}'.format(self._result))

        except Exception as e:
            self.get_logger().error('Exception in get_result_callback: {0}'.format(e))
        

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.progress))
        
    def get_result(self):
        return self._result
    
        

def main(args=None):
    rclpy.init(args=args)  
    action_client = LLMActionClient()
    

if __name__ == '__main__':
    main()
