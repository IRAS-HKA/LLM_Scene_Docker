import rclpy
import time
from rclpy.node import Node
from llm_interfaces.srv import SceneInterpretation
from .SelectedItemsToPack import SelectedItems
from .UserInput import UserInput
from .ParamGetter import ParamGetter

class PackItemsService(Node):

    def __init__(self):
        super().__init__('pack_items_service')
        self.srv = self.create_service(SceneInterpretation, 'scene_interpretation', self.pack_items_callback)
        self.get_logger().info('Service server is ready.')
    
    def formatOutput(self):
        param = ParamGetter()
        temp = param.get_ros2_param('pack_list')

        cleaned_string = temp.replace("String value is: ", "").replace("'", "").replace(" ", "").replace("[", "").replace("]","").replace("\n", "")

        # Den String in eine Liste aufteilen
        result_list = cleaned_string.split(',')

        # Entfernen der zusätzlichen einfachen Anführungszeichen um die Listenelemente
        result_list = [item.strip("'") for item in result_list]

        return result_list

    def pack_items_callback(self, request, response):
        #self.get_logger().info('Packlist:'.format(SelectedItems.getPackList()))
        param = ParamGetter()
        while (True):
            #if (SelectedItems.getPackList() != [] and UserInput.getApproval() == True):
            if (param.get_ros2_param('pack_list') != ""):
                self.get_logger().info('Data available yet.')
                # response.objects_to_pick = SelectedItems.getPackList()
                # response.objects_to_pick = ['Box_Gluehlampe', 'Box_Wischblatt','Keilriemen_gross', 'Box_Bremsbacke', 'Keilriemen_klein','Box_Messwertgeber']
                #response.objects_to_pick = ['Box_Wischblatt']
                
                
                response.objects_to_pick = self.formatOutput()
                self.get_logger().info("TYPE objects_to_pick: {}".format(type(response.objects_to_pick)))
                self.get_logger().info("RESPONSE objects_to_pick: {}".format(response.objects_to_pick))
                
                # response.objects_to_pick = SelectedItems.getStandardConfig()                
                
                #self.get_logger().info('Packlist:'.format(SelectedItems.getPackList()))
                #response.objects_to_pick = ['Box_Gluehlampe', 'Box_Wischblatt','Keilriemen_gross', 'Box_Bremsbacke', 'Keilriemen_klein', 'Tuete']
                return response
            else:
                time.sleep(5)
                self.get_logger().info('Data not available yet. Waiting for data...')
                #self.get_logger().info('Packlist:'.format(SelectedItems.getPackList()))
                #self.get_logger().info('Approval USer'.format(UserInput.getApproval()))


                
    def stop_spin(self):
        rclpy.shutdown()
        self.get_logger().info('Node has been stopped.')
    
    def spinNode(self):

        self.get_logger().info('Bin in der Hilfsmethode!')
        #rclpy.spin_once(self, timeout_sec=15.0)
        rclpy.spin(self)
        self.get_logger().info('FERTIG mit Hilfsmethode!')
    




def main(args=None):
    rclpy.init(args=args)
    node = PackItemsService()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()