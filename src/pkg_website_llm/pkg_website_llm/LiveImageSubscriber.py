import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os
from datetime import datetime
import time

class ImageSaver(Node):
    def __init__(self):
        super().__init__('image_saver')
        self.subscription = self.create_subscription(
            Image,
            '/detection_node/result_image',
            self.listener_callback,
            10)
        self.subscription  
        self.bridge = CvBridge()
        self.save_path = os.path.join(os.path.expanduser('~'), 'ros_ws', 'src', 'pkg_website_llm', 'pkg_website_llm', 'static' )  
        os.makedirs(self.save_path, exist_ok=True)
        
        
    
    def listener_callback(self, msg):
        
        # Convert the ROS Image message to an OpenCV image
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
        
        # Overwrite the existing image with the timestamp as the name
        image_name = "Hintergrund.png"
        image_path = os.path.join(self.save_path, image_name)
        
        # Save the image and wait for 10 seconds
        cv2.imwrite(image_path, cv_image)
        self.get_logger().info(f'Saved image to {image_path}')
        time.sleep(10)

def main(args=None):
    rclpy.init(args=args)
    image_saver = ImageSaver()
    rclpy.spin(image_saver)
    image_saver.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
