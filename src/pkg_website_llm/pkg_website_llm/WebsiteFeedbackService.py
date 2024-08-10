from llm_interfaces.srv import WebsiteFeedback

import rclpy
from rclpy.node import Node
from .WebsiteFeedbackData import WebsiteFeedbackData

from .ParamGetter import ParamGetter


class MinimalService(Node):

    def __init__(self):
        super().__init__('website_feedback_server')
        self.srv = self.create_service(WebsiteFeedback, 'get_website_feedback', self.save_data_for_website)
        self.get_logger().info('Service was initialized')

    def save_data_for_website(self, request,response):
        self.get_logger().info('Incoming request received')
                
        self.get_logger().info(f'Cylinder IDs: {request.cylinder_ids}')      
        self.get_logger().info(f'Cylinder IDs: {type(request.cylinder_ids)}')  
        
        self.get_logger().info(f'Package: {request.package}')
        
        #WebsiteFeedbackData.setCylinderIds(str(request.cylinder_ids.cylinder_ids))       
        #WebsiteFeedbackData.setPackage(str(request.package))
        param = ParamGetter()
        param.set_ros2_param('cylinder_Ids', str(request.cylinder_ids))
        param.set_ros2_param('package', str(request.package))
        
        
        #self.get_logger().info(f'getCylinderIDs: {WebsiteFeedbackData.getCylinderIds()}')
        #self.get_logger().info(f'getPackage: {WebsiteFeedbackData.getPackage()}')
        
        self.get_logger().info('Set website feedback ')
         
        return response


def main():
    rclpy.init()

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()