import rclpy
from rclpy.node import Node
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter, ParameterType

class ParameterServer(Node):
    def __init__(self):
        super().__init__('parameter_server')
        self.declare_parameter('user_input', 'No Input')
        self.declare_parameter('user_approval', False)
        self.declare_parameter('pack_list', '')
        self.declare_parameter('cylinder_Ids', '')
        self.declare_parameter('package', '')
        self.declare_parameter('image_path', '')
        
        
        self.get_logger().info('Parameter Server started.')

def main(args=None):
    rclpy.init(args=args)
    node = ParameterServer()
    rclpy.spin(node)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
