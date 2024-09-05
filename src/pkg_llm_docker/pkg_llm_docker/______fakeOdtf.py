import geometry_msgs.msg
import sensor_msgs.msg
import object_detector_tensorflow_interfaces.msg
import ast
import re

def preprocess_detection_string(detection_string):
    # Replace specific class object instantiations with Python dicts
    detection_string = re.sub(
        r'object_detector_tensorflow_interfaces\.msg\.Detection\(',
        '{',
        detection_string
    )
    detection_string = re.sub(r'geometry_msgs\.msg\.Point\(', '{', detection_string)
    detection_string = re.sub(r'sensor_msgs\.msg\.RegionOfInterest\(', '{', detection_string)
    detection_string = detection_string.replace(')', '}')
    
    # Replace '=' with ':' to make it a valid Python dictionary string
    detection_string = re.sub(r'(\w+)=', r'"\1":', detection_string)
    
    # Replace booleans with lowercase counterparts
    detection_string = detection_string.replace("False", "false")
    detection_string = detection_string.replace("True", "true")
    
    # Fix strings by adding quotes
    detection_string = re.sub(r'(\w+)=([a-zA-Z_]\w*)', r'\1="\2"', detection_string)
    
    return detection_string

def parse_detection_string(detection_string):
    detection_list = []
    
    # Preprocess the detection string
    preprocessed_string = preprocess_detection_string(detection_string)
    
    # Parse the string into a list of dictionaries
    parsed_list = ast.literal_eval(preprocessed_string)
    
    for detection_dict in parsed_list:
        center = detection_dict['center']
        bounding_box = detection_dict['bounding_box']
        
        # Create the corresponding message objects
        center_point = geometry_msgs.msg.Point(
            x=center['x'],
            y=center['y'],
            z=center['z']
        )
        
        roi = sensor_msgs.msg.RegionOfInterest(
            x_offset=bounding_box['x_offset'],
            y_offset=bounding_box['y_offset'],
            height=bounding_box['height'],
            width=bounding_box['width'],
            do_rectify=bounding_box['do_rectify']
        )
        
        detection = object_detector_tensorflow_interfaces.msg.Detection(
            class_id=detection_dict['class_id'],
            class_name=detection_dict['class_name'],
            probability=detection_dict['probability'],
            center=center_point,
            bounding_box=roi
        )
        
        detection_list.append(detection)
    
    return detection_list

detection_string = "[object_detector_tensorflow_interfaces.msg.Detection(class_id=4, class_name='Box_Wischblatt', probability=0.9999112486839294, center=geometry_msgs.msg.Point(x=543.5, y=608.5, z=0.0), bounding_box=sensor_msgs.msg.RegionOfInterest(x_offset=321, y_offset=480, height=257, width=445, do_rectify=False)), object_detector_tensorflow_interfaces.msg.Detection(class_id=3, class_name='Keilriemen_gross', probability=0.9998945593833923, center=geometry_msgs.msg.Point(x=629.5, y=405.5, z=0.0), bounding_box=sensor_msgs.msg.RegionOfInterest(x_offset=336, y_offset=332, height=147, width=587, do_rectify=False)), object_detector_tensorflow_interfaces.msg.Detection(class_id=5, class_name='Box_Messwertgeber', probability=0.9998105764389038, center=geometry_msgs.msg.Point(x=800.0, y=524.0, z=0.0), bounding_box=sensor_msgs.msg.RegionOfInterest(x_offset=737, y_offset=465, height=118, width=126, do_rectify=False))]"

detections = parse_detection_string(detection_string)
