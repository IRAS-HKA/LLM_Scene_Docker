# relevant für die String to Dict Konvertierung
import ast
import json

class PostProcessing:

    # This method is used when the respone is nit easy to parse due the special array forms or dictionaries in arrays
    # Then it checks for the objects of the material list in German or English and returns a list of the found objects
    def formatToDict(content):
        print("---------------------------------------")
        print("Type of content:",type(content))

        print(".....Verarbeitung des JSON-Strings beginnt....")
        try:
                   
            if (type(content) == dict):
                print("Name", content['name'])
                return content['name']
            
            elif (type(content) == str) :
                # Language DE
                search_objects = ['Box_Gluehlampe', 'Box_Wischblatt','Keilriemen_gross', 'Box_Bremsbacke', 'Keilriemen_klein','Box_Messwertgeber','Box\_Gluehlampe', 'Box\_Wischblatt','Keilriemen\_gross', 'Box\_Bremsbacke', 'Keilriemen\_klein','Box\_Messwertgeber']
                # Language EN
                search_objects_eng = ['Box_Glowlamp', 'V-belt_large','Box_Wipingblade', 'V-belt_small', 'Bag','Box_Measurementtransmitter']
                
                combined_search_objects = search_objects + search_objects_eng
                
                # Result list of found objects
                found_objects = []

                # Check if String is available
                for s in combined_search_objects:
                    if s in content:
                        found_objects.append(s)

                print("Gefundene Objekte:", found_objects)
                return found_objects    
            

            
        except Exception as e:
            print("*******")
            print("Conversion to dictionary failed")
            print("Error:",e)
            print("*******")
            return "No content found"
    
    
    def formatToString(content):
        return content['message']['content']
        
    def getWantedObject(dict_response):
        return dict_response['answer']['object']
    
    def getWantedPositon(dict_response):
        return dict_response['answer']['Position']
    
    # makes sense for handeling timeouts
    def getUsedTime(start, end):
        return end-start

