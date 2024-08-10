import rclpy
from rclpy.node import Node

from .ParamGetter import ParamGetter
from std_srvs.srv import Empty


class MinimalService(Node):

    def __init__(self):
        super().__init__('delete_parameter_server')
        self.srv = self.create_service(Empty, 'delete_parameters', self.save_data_for_website)
        self.get_logger().info('Service was initialized')

    def save_data_for_website(self, request,response):
        self.get_logger().info('DELETE request received')
                
            

        param = ParamGetter()
        param.set_ros2_param('user_input', "")
        param.set_ros2_param('pack_list', "")
        param.set_ros2_param('user_approval', False)


        self.get_logger().info('DELETED userinput, pack_list and user_approval')
         
        return response


def main():
    rclpy.init()

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()