from llm_interfaces.srv import UserInteraction
import rclpy
from rclpy.node import Node
from .UserInput import UserInput
from threading import Timer
import time

from .ParamGetter import ParamGetter


class UserInputService(Node):

    def __init__(self):
        #rclpy.init(args=None)
        super().__init__('UserInputServiceSender')
        self.srv = self.create_service(UserInteraction, 'user_interaction', self.userinput_callback)

        print("Node wurde initialisiert")

    def userinput_callback(self, request, response):
        
        param = ParamGetter()
        while True:

            user_input = param.get_ros2_param("user_input")
            user_input = user_input.replace("String value is:", "")
            user_input = user_input.strip()
            
            if user_input != "" and user_input != 'No Input':
                response.user_input = user_input
                self.get_logger().info('Outgoing User Input %s' % user_input)
                break
            else:
                time.sleep(5)
                self.get_logger().info('NO User Input available yet. Waiting for data...')

        return response
    
    def shutdown_node(self):
        rclpy.shutdown()
        self.get_logger().info('Service destroyed: %s' % UserInput.getUserInput())
        UserInput.UserInput_str = 'No Input'


def main(args=None):
    rclpy.init(args=args)

    service = UserInputService()
    service.get_logger().info('Service was started and spins now')
    rclpy.spin(service)
    #print("Service erzeugt")

    #rclpy.spin('user_input')
    #rclpy.spin(self.srv)

    

if __name__ == '__main__':
    main()