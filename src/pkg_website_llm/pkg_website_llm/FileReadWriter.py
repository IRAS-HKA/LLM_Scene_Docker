import json
import os

class FileReadWriter:
    
    @staticmethod
    def writeWebsiteFeedbackInitially():
        # Ausgabe des aktuellen Verzeichnisses

        file_name = "/home/robot/ros_ws/src/pkg_website_llm/pkg_website_llm/WebsiteFeedback.json"
        with open(file_name, 'w') as file:
            data = {
                "cylinder_Ids": "",
                "package": "",
                "node_list": "",
                "feedback_string": "No String"
            }
            json.dump(data, file)
    
   
    @staticmethod
    def readWebsiteFeedbackFile(parameter):
        file_name = "/home/robot/ros_ws/src/pkg_website_llm/pkg_website_llm/WebsiteFeedback.json"
        with open(file_name, 'r') as file:
            data = json.load(file)
            
        if parameter in data:
            return data[parameter]
            
        return None
        
    @staticmethod
    def writeWebsiteFeedbackFile(parameter, value):
        file_name = "/home/robot/ros_ws/src/pkg_website_llm/pkg_website_llm/WebsiteFeedback.json"

        # Open the file in read mode to load the data
        with open(file_name, 'r') as file:
            data = json.load(file)
        
        # Modify the data
        if parameter in data:
            data[parameter] = value
        
        # Open the file in write mode to save the modified data
        with open(file_name, 'w') as file:
            json.dump(data, file)

    @staticmethod
    def writeUserInputInitially():
        # Ausgabe des aktuellen Verzeichnisses

        file_name = "/home/robot/ros_ws/src/pkg_website_llm/pkg_website_llm/UserInput.json"
        with open(file_name, 'w') as file:
            data = {
                "user_input": "No Input",
                "user_command": "",
                "user_approval": "False",
                "pack_list": "",
                "sel_language": ""
            }
            json.dump(data, file)
            
    @staticmethod
    def readUserInputFile(parameter):
        file_name = "/home/robot/ros_ws/src/pkg_website_llm/pkg_website_llm/UserInput.json"
        with open(file_name, 'r') as file:
            data = json.load(file)
            
        if parameter in data:
            return data[parameter]
            
        return None
        
    @staticmethod
    def writeUserInputFile(parameter, value):
        file_name = "/home/robot/ros_ws/src/pkg_website_llm/pkg_website_llm/UserInput.json"

        # Open the file in read mode to load the data
        with open(file_name, 'r') as file:
            data = json.load(file)
        
        # Modify the data
        if parameter in data:
            data[parameter] = value
        
        # Open the file in write mode to save the modified data
        with open(file_name, 'w') as file:
            json.dump(data, file)


    @staticmethod
    def translateToEnglisch(list_of_german_words):
        file_name = "/home/robot/ros_ws/src/pkg_website_llm/pkg_website_llm/translation.json"
        with open(file_name, 'r') as file:
            data = json.load(file)
        
        list_of_english_words = []
        
        for german_word in list_of_german_words:
            if german_word in data:
                list_of_english_words.append(data[german_word]["English"])
                
        if list_of_english_words == []:
            print("Liste ist leer.")
            return []
                            
        return list_of_english_words
    
    @staticmethod
    def translateToGerman(list_of_english_words):
        file_name = "/home/robot/ros_ws/src/pkg_website_llm/pkg_website_llm/translation.json"
        
        with open(file_name, 'r') as file:
            data = json.load(file)
        
        list_of_german_words = []
        
        for english_word in list_of_english_words:
            for key, value in data.items():
                if value["English"] == english_word:
                    german_word = key
                    list_of_german_words.append(german_word)

                
        if list_of_german_words == []:
            print("Liste ist leer.")
            return []
                            
        return list_of_german_words