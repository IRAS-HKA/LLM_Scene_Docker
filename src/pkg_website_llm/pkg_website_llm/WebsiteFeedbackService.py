from llm_interfaces.srv import WebsiteFeedback

import rclpy
from rclpy.node import Node
from .WebsiteFeedbackData import WebsiteFeedbackData
from cv_bridge import CvBridge
import cv2
import os
from .FileReadWriter import FileReadWriter
from .ParamGetter import ParamGetter


class MinimalService(Node):

    def __init__(self):
        super().__init__('website_feedback_server')
        self.srv = self.create_service(WebsiteFeedback, 'get_website_feedback', self.save_data_for_website)
        self.get_logger().info('Service was initialized')
        self.bridge = CvBridge()
        self.save_path = os.path.join(os.path.expanduser('~'), 'ros_ws', 'src', 'pkg_website_llm', 'pkg_website_llm', 'static' ) 

    def save_data_for_website(self, request,response):
        
        # Print the incoming request for debugging
        self.get_logger().info('Incoming request received')        
        self.get_logger().info(f'Cylinder IDs: {request.cylinder_ids}')      
        self.get_logger().info(f'Cylinder IDs: {type(request.cylinder_ids)}')  
        self.get_logger().info(f'Package: {request.package}')
        

        # Overwrite the existing PackPlan image with the timestamp as the name
        cv_image = self.bridge.imgmsg_to_cv2(request.feedback.image, "8UC3")
        image_name = "PackPlanBild.png"
        image_path = os.path.join(self.save_path, image_name)
        cv2.imwrite(image_path, cv_image)
        self.get_logger().info(f'Saved image to {image_path}')
        
        
        # Write the data to the website_feedback.json file
        FileReadWriter.writeWebsiteFeedbackInitially()
        FileReadWriter.writeWebsiteFeedbackFile("cylinder_Ids", str(request.cylinder_ids))
        FileReadWriter.writeWebsiteFeedbackFile("package", str(request.package))
        FileReadWriter.writeWebsiteFeedbackFile("feedback_string", str(request.feedback.message))
        
        param = ParamGetter()
        FileReadWriter.writeWebsiteFeedbackFile("node_list", str(param.listAllNodes()))
        
        self.get_logger().info('Set website feedback data')
         
        return response


def main():
    rclpy.init()

    minimal_service = MinimalService()

    try:
        rclpy.spin(minimal_service)       

    except KeyboardInterrupt:
        print("Node stopped successfully")

    try:
        rclpy.shutdown()
    except:
        print("shutdown already called")


if __name__ == '__main__':
    main()