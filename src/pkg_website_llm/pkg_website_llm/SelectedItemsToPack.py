global _selected_items_list
class SelectedItems:
    _selected_items_list = []
    
    @classmethod
    def getPackList(cls):
        return cls._selected_items_list
    
    @classmethod
    def appendPackList(cls,input_str):
        cls._selected_items_list.append(input_str)
    
    @classmethod
    def setPackList(cls, input_list):
        cls._selected_items_list = input_list
    
    @classmethod        
    def clearPackList(cls):
        cls._selected_items_list.clear()

    # @classmethod
    @staticmethod
    def getStandardConfig():
        return ['Box_Gluehlampe', 'Box_Wischblatt','Keilriemen_gross', 'Box_Bremsbacke', 'Keilriemen_klein','Box_Messwertgeber']