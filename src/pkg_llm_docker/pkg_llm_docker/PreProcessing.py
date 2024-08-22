from .MainLLM import AnswerFormat
#import roslib
#roslib.load_manifest('pkg_website_llm')
#from pkg_website_llm.UserInput import UserInput
#import fakeOdtf

# from rclpy.node import Node
# import ast
# import yaml
# import os
# import rclpy

from .shared import Node, ast, yaml, os, rclpy
from pkg_website_llm.FileReadWriter import FileReadWriter


class PreProcessing(Node):
    
    
    def __init__(self, detections):
        self.detections = detections
        
    def loadAdditionalInformationYAML(self, class_name):
        
        current_directory = os.getcwd()

        print(f"Das aktuelle Verzeichnis ist: {current_directory}")
        
        #yaml_data = open('./material_master.yaml', 'r')
        yaml_data = open('/home/robot/ros_ws/src/pkg_llm_docker/pkg_llm_docker/material_master.yaml', 'r')
        
        if os.path.isfile('/home/robot/ros_ws/src/pkg_llm_docker/pkg_llm_docker/material_master.yaml'):
            print(f"{yaml_data} ist eine Datei.")
        else:
            print(f"{yaml_data} ist keine Datei.")
        
        # YAML-Daten laden
        data = yaml.safe_load(yaml_data)
        
        # Array 
        object_mass = []
        length_mass = []
        width_mass = []
        height_mass = []
        
        
        # for each object in the scene description
        for object in class_name:
            index_object = data["Label ODTF"].index(object)

            obj_object_mass = data["Gewicht [kg]"][index_object]
            obj_length_mass = data["Länge [mm]"][index_object]
            obj_width_mass = data["Breite [mm]"][index_object]
            obj_height_mass = data["Höhe [mm]"][index_object]
            
            object_mass.append(obj_object_mass)
            length_mass.append(obj_length_mass)
            width_mass.append(obj_width_mass)
            height_mass.append(obj_height_mass)

        return object_mass,length_mass,width_mass,height_mass


    # def receiveDetections(self):
    #     # Call the DetectionSubscriber Node
    #     #rclpy.init(args=None)

    #     #my_subscriber = DetectionSubscriber()

    #     #rclpy.spin(my_subscriber)
        
    #     #my_subscriber.destroy_node()
    #     #rclpy.shutdown()
    #     #self.detections = my_subscriber.detections
    #     pass
    
    # Abfrage 
    def formatPrompt(self,sceneDescription,userInput, chatmodus, sel_language):
        
        # Receive the detections from the DetectionSubscriber
        #self.receiveDetections()
        
        #prompt = f'Es liegt die folgende Szene vor: Wir haben eine Box mit Gegenständen darin: 1. {sceneDescription[0].class_name} mit der Eigenschaft x= {sceneDescription[0].center.x} y={sceneDescription[0].center.y} z= {sceneDescription[0].center.z}  2. Keilriemen_gross mit der Eigenschaft x=629.5, y=405.5, z=0.0 3. Box_Messwertgeber mit der Eigenschaft x=800.0, y=524.0, z=0.0. Wo befindet sich der das Wischblatt?: {AnswerFormat.schema_json()} :\n'
        classname = ["Box_Wischblatt", "Keilriemen_gross", "Box_Messwertgeber", "Keilriemen_klein"]
        center_x = [543.5, 629.5, 800.0, 500.4]
        center_y = [608.5, 405.5, 524.0, 320.1]
        center_z=  [0.01, 0.001, 0.002, 0.01]
        object_mass,length_mass,width_mass,height_mass = PreProcessing.loadAdditionalInformationYAML(self,classname)
        
        
        # classname = []
        # center_x = []
        # center_y = []
        
        # # Put the detections in the arrays
        # for detection in self.detections:
        #     classname.append(detection.class_name)
        #     center_x.append(detection.center.x)
        #     center_y.append(detection.center.y)
        # object_mass,length_mass,width_mass,height_mass = PreProcessing.loadAdditionalInformationYAML(self,classname)
        
        
         
        
        print(f"sel_language: {sel_language}")
        # Change the prompt based on the language
        if (sel_language == "de"):
            
            prompt = 'Detektierte Objekte: \n'
            for i in range(len(classname)):
                prompt += f'{i+1}. {classname[i]}: Position x= {center_x[i]} y={center_y[i]} Gewicht: {object_mass[i]} kg Länge: {length_mass[i]} mm Breite: {width_mass[i]} mm Höhe: {height_mass[i]} mm \n' 
            
            chatmodus = chatmodus.replace("String value is:","")
        
            if "command" in chatmodus and userInput !="":
                prompt += f' Answer the name and position in a short json object. Wo befindet sich {userInput}?\n'
            
            elif "scenechat" in chatmodus and userInput !="" :
                prompt += f' {userInput}?\n'
        
            # Beschreibung
            elif "chat" in chatmodus and userInput !="":
                prompt = userInput
        
        # No User Input
            else:
                prompt += f'Bitte beschreibe dem User den Sachverhalt und bitte ihn dir eine Frage zu stellen.:\n'
                
        elif (sel_language == "en"):
            
            # Translate the classname list 
            classname = FileReadWriter.translateToEnglisch(classname)
            
            prompt = 'Recognized objects: \n'
            for i in range(len(classname)):
                prompt += f'{i+1}. {classname[i]}: Position x= {center_x[i]} y={center_y[i]} mass: {object_mass[i]} kg length: {length_mass[i]} mm width: {width_mass[i]} mm height: {height_mass[i]} mm \n' 
            
            if "command" in chatmodus and userInput !="":
                prompt += f' Answer the name and position in a short json object. Where is {userInput}?\n'
            
            elif "scenechat" in chatmodus and userInput !="" :
                prompt += f' {userInput}?\n'
        
            # Beschreibung
            elif "chat" in chatmodus and userInput !="":
                prompt = userInput
            
        else:
            return "Error: Language not supported."
        
        
        # classname = ["Box_Wischblatt", "Keilriemen_gross", "Box_Messwertgeber", "Keilriemen_klein"]
        # center_x = [543.5, 629.5, 800.0, 500.4]
        # center_y = [608.5, 405.5, 524.0, 320.1]
        # center_z=  [0.01, 0.001, 0.002, 0.01]

        




        #if "BEFEHL:" in user_command:
        #    userInput = userInput.replace("BEFEHL:","")
        

        

        return prompt
    




