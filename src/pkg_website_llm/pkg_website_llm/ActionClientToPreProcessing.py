import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from .UserInput import UserInput

from llm_action_interfaces.action import LLM

class LLMActionClient(Node):

    def __init__(self):
        super().__init__('llm_action_client')
        self._action_client = ActionClient(self, LLM, 'llm_action_server')

        self.get_logger().info('Action Client initialized')

    def send_goal(self, user_input):
        self.get_logger().info('ANFANG send goal')
        
        self.get_logger().info('User Input in send_goal: {0}'.format(user_input))
        request_msg = LLM.Goal()
        request_msg.userinput = str(user_input)

        self._action_client.wait_for_server(timeout_sec=10.0)
        print("Server gefunden")
        self._send_goal_future = self._action_client.send_goal_async(request_msg)
        print("Ziel gesendet")
        self.get_logger().info('ENDE send goal')
        
        temp = self._send_goal_future.add_done_callback(self.goal_response_callback)

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
            self._result = result.llmoutput 
            self.get_logger().info('Result: {0}'.format(self._result))

        except Exception as e:
            self.get_logger().error('Exception in get_result_callback: {0}'.format(e))
        
        
        rclpy.shutdown()
        
        

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.progress))
        
    def get_result(self):
        return self._result

def main(args=None):
    rclpy.init(args=args)  
    action_client = LLMActionClient()

    userInput = UserInput.getUserInput()
    print(userInput)
    action_client.get_logger().info('UserInput: {0}'.format(userInput)) 

    action_client.send_goal(userInput)

    print("Goal sent")
    rclpy.spin(action_client)


if __name__ == '__main__':
    main()
