from llm_interfaces.srv import UserInteraction
import rclpy
from rclpy.node import Node
from .UserInput import UserInput
from threading import Timer
import time

from .FileReadWriter import FileReadWriter

class UserInputService(Node):

    def __init__(self):
        super().__init__('UserInputServiceSender')
        self.srv = self.create_service(UserInteraction, 'user_interaction', self.userinput_callback)
        
        print("Node wurde initialisiert")

    def userinput_callback(self, request, response):
        
        while True:

            if (FileReadWriter.readUserInputFile("user_input")== None):
                time.sleep(2)
                self.get_logger().info('NO User Input available yet. Waiting for data...')
                continue

            user_input = FileReadWriter.readUserInputFile("user_input")
            user_input = user_input.replace("String value is:", "")
            user_input = user_input.strip()
            
            if user_input != "" and user_input != 'No Input':
                response.user_input = user_input
                self.get_logger().info('Outgoing User Input %s' % user_input)
                return response
            else:
                time.sleep(2)
                self.get_logger().info('NO User Input available yet. Waiting for data...')

        
    
    def shutdown_node(self):
        rclpy.shutdown()
        self.get_logger().info('Service destroyed: %s' % UserInput.getUserInput())


def main(args=None):
    rclpy.init(args=args)

    service = UserInputService()
    service.get_logger().info('Service was started and spins now')
    rclpy.spin(service)


    

if __name__ == '__main__':
    main()