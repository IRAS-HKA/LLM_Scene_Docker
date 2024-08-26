import os
from cv_bridge import CvBridge
import cv2

class WebsiteFeedbackData:
    # Data declaration
    _cylinder_ids = ""
    _package = ""
    _grasp_pose = ""
    _place_pose = ""
    _file_path_image = "/static/images/PackPlan.png"
    
    
    # Cylinder IDs
    @classmethod
    def getCylinderIds(cls):
        return cls._cylinder_ids
    
    @classmethod
    def setCylinderIds(cls, cylinder_ids):
        cls._cylinder_ids = cylinder_ids
        
    # Package
    @classmethod
    def getPackage(cls):
        return cls._package
    
    @classmethod
    def setPackage(cls, package): 
        cls._package = package
        
    # file path image
    
    @classmethod
    def getImagePath(cls):
        if os.path.isfile(cls._file_path_image):
            return cls._file_path_image
        else:
            return "/static/images/Platzhalter.png"
        
    @classmethod
    def setImagePath(cls, image_array):
        bridge = CvBridge()
        # Konvertiere die ROS 2 Image-Nachricht zurück in ein OpenCV-Bild
        picture = bridge.imgmsg_to_cv2(image_array, "passthrough")  
        cv2.imwrite(cls._file_path_image, picture)
    
    