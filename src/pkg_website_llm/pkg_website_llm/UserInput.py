class UserInput:
    userInput_str = 'No Input'
    approval_bool = False
    
    def getUserInput():
        return UserInput.userInput_str
    
    def setUserInput(input):
        UserInput.userInput_str = input
        
    def getApproval():
        return UserInput.approval_bool
    
    def setApproval(approval):
        UserInput.approval_bool = approval
