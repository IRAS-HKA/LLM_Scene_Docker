import subprocess
import time
class ParamGetter:

    def __init__(self):
        pass
    
    def checkIfNodeAvailable(self,node_name):
        command = ['ros2', 'node', 'list']
        
        try:
            # Den Befehl ausführen und das Ergebnis erfassen
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print(command)
            if node_name in result.stdout:
                return True
            else:
                return False

        except subprocess.CalledProcessError as e:
                # Fehlerbehandlung
            print(f"Error executing command: {e}")
            print(f"stderr: {e.stderr}")

    def listAllNodes(self):
        command = ['ros2', 'node', 'list']
        
        while(self.checkIfParamIsInUse()):
            time.sleep(0.500) 
        try:
            # Den Befehl ausführen und das Ergebnis erfassen
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            
            list_nodes = []
            relevant_nodes_llm = ["/LLM/LLM1", "/LLM/delete_parameter_service", "/LLM/feedbackwebsite", "/LLM/pack_item_server", "/LLM/saveImageFromODTF", "/LLM/user_input_sender", "/LLM/website"]
            
            if all(string in result for string in relevant_nodes_llm):
                list_nodes.append("LLM Nodes")
           
            for node in result.stdout.split("\n"):
                if "Coordinator" in node:
                    list_nodes.append("AIP Coordinator")
                
                elif "genicam_driver" in node:
                    list_nodes.append("ROS2 Camera Driver")
                
                elif "moveit_wrapper" in node:
                    list_nodes.append("MoveIt Wrapper")
                    
                elif "gripper_controller" in node:
                    list_nodes.append("Gripper Controller")
            
            return list_nodes
        
        
        except subprocess.CalledProcessError as e:
                # Fehlerbehandlung
            print(f"Error executing command: {e}")
            print(f"stderr: {e.stderr}")
        
    

    def checkIfParamIsInUse(self):
        try:
            # Führe das ps-Kommando aus und überprüfe die Ausgabe
            result = subprocess.run(["ps", "aux"], capture_output=True, text=True, check=True)
        
            # Prüfe, ob "ros2 param get" in der Ausgabe enthalten ist
            if "ros2 param get" in result.stdout or "ros2 param set" in result.stdout:
                return True
            else:
                return False
            
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Ausführen des Kommandos: {e}")
            return False
        
            
    def get_ros2_param(self,var_name):
        
        while(self.checkIfParamIsInUse() or not self.checkIfNodeAvailable("Parameter_Setter")):
            time.sleep(0.500) 
            
        # Der genaue Terminalaufruf
        command = ['ros2', 'param', 'get', '/LLM/Parameter_Setter', var_name]

        try:
            # Den Befehl ausführen und das Ergebnis erfassen
            result = subprocess.run(command, capture_output=True, text=True, check=True)
                    

            # Falls notwendig, können Sie auch das Ergebnis zurückgeben
            return result.stdout
        except subprocess.CalledProcessError as e:

            print(f"Error executing command: {e}")
            print(f"stderr: {e.stderr}")

    def set_ros2_param(self,var_name, value):
        
        while(self.checkIfParamIsInUse() or not self.checkIfNodeAvailable("Parameter_Setter")):
            time.sleep(0.500)
             
        # Der genaue Terminalaufruf
        command = ['ros2', 'param', 'set', '/LLM/Parameter_Setter', var_name, value]

        time.sleep(0.30)

        try:
            # Den Befehl ausführen und das Ergebnis erfassen
            result = subprocess.run(command, capture_output=True, text=True, check=True)

            # Falls notwendig, können Sie auch das Ergebnis zurückgeben
            return result.stdout
                
        except subprocess.CalledProcessError as e:
            # Fehlerbehandlung
            print(f"Error executing command: {e}")
            print(f"stderr: {e.stderr}")

