class SelectedItems:
    selected_items_list = []
    
    def getPackList():
        return SelectedItems.selected_items_list
    
    def appendPackList(input_str):
        SelectedItems.selected_items_list.append(input_str)
        
    def setPackList(input_list):
        SelectedItems.selected_items_list = input_list
        
    def clearPackList():
        SelectedItems.selected_items_list.clear()
        
    def getStandardConfig():
        return ['Box_Gluehlampe', 'Box_Wischblatt','Keilriemen_gross', 'Box_Bremsbacke', 'Keilriemen_klein','Box_Messwertgeber']