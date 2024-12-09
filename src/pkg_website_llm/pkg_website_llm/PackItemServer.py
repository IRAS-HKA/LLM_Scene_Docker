import rclpy
import time
import rclpy.duration
from rclpy.node import Node
from llm_interfaces.srv import SceneInterpretation
from .SelectedItemsToPack import SelectedItems
from .FileReadWriter import FileReadWriter

class PackItemsService(Node):

    def __init__(self):
        super().__init__('pack_items_service')
        self.srv = self.create_service(SceneInterpretation, 'scene_interpretation', self.pack_items_callback)
        self.get_logger().info('Service server is ready.')
    
    def formatOutput(self):
        # Read the pack_list from the UserInput.json file
        temp = FileReadWriter.readUserInputFile('pack_list')
        cleaned_string = temp.replace("String value is: ", "").replace("'", "").replace(" ", "").replace("[", "").replace("]","").replace("\n", "")

        # Split the string into a list
        result_list = cleaned_string.split(',')

        # Replace the single quotes in the list
        result_list = [item.strip("'") for item in result_list]
        

        return result_list

    def pack_items_callback(self, request, response):
        
        while (True):

            if FileReadWriter.readUserInputFile('user_approval') == "True":
                self.get_logger().info('Data available yet.')
                
                if "No Input" not in FileReadWriter.readUserInputFile('user_approval'):
                    self.get_logger().info('Data available yet.')

                    response.objects_to_pick = self.formatOutput()
                    self.get_logger().info("TYPE objects_to_pick: {}".format(type(response.objects_to_pick)))
                    self.get_logger().info("RESPONSE objects_to_pick: {}".format(response.objects_to_pick))

                    FileReadWriter.writeUserInputInitially()
                    return response
            else:
                self.get_clock().sleep_for(rclpy.duration.Duration(seconds=5))
                self.get_logger().info('Data not available yet. Waiting for data...')

               

                
    def stop_spin(self):
        rclpy.shutdown()
        self.get_logger().info('Node has been stopped.')
    
    def spinNode(self):

        self.get_logger().info('Running the Spinning Node-Method!')

        rclpy.spin(self)
    




def main(args=None):
    rclpy.init(args=args)
    node = PackItemsService()
    try:
        rclpy.spin(node)       

    except KeyboardInterrupt:
        print("Node stopped successfully")
    try:
        rclpy.shutdown()
    except:
        print("shutdown already called")

if __name__ == '__main__':
    main()