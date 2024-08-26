# relevant für die String to Dict Konvertierung
import ast
import json

class PostProcessing:

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
                # Ergebnisliste der gefundenen Strings
                found_objects = []

                # Über die Liste von Such-Strings iterieren und prüfen, ob sie im langen Satz vorkommen
                for s in combined_search_objects:
                    if s in content:
                        found_objects.append(s)

                # Ergebnisse anzeigen
                print("Gefundene Objekte:", found_objects)
                return found_objects    
            
            # elif (type(content) == json):
            #     content_json = json.loads(content["message"]["content"])
            #     name = json.loads(content_json["name"])
            #     print("Name", name)
            #     pass
            
            # else: 
            #     list_all_items = ['Box_Gluehlampe', 'Box_Wischblatt','Keilriemen_gross', 'Box_Bremsbacke', 'Keilriemen_klein','Box_Messwertgeber']
            #     found_items_llm = [wort for wort in list_all_items if wort in content]
            #     print("found_items_llm",found_items_llm)
            #     return found_items_llm
            
        except Exception as e:
            print("*******")
            print("Conversion to dictionary failed")
            print("Fehler:",e)
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

