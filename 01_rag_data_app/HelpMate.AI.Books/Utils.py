import os
import json

class Utils:
    def getJSONAsString(_file_path):
        json_string=""
        with open(_file_path) as f:
            d = json.load(f)
            json_string=str(d)
            json_string=json_string.replace("'","\"")
            #print(json_string)
        return json_string

    def getJSONObject(_file_path):
        return json.loads(Utils.getJSONAsString(_file_path))
    
    def getJSONAsClass(TargetClass,_file_path):
        jsonObj=Utils.getJSONObject(_file_path)
        return TargetClass(**jsonObj)

    class Keys:
        Flagged='Flagged'
        NotFlagged="Not Flagged"
    
    class Messages:
        Flagged="Sorry, I cannot process this as this query seems inappropriate from Books Context (Message flagged)\n. Quitting."
        CannotProcess="Sorry I cant process this, it may be out of scope"
        AtLeastWords="Please enter at least 3 words separated by space"
        Chat_Input_PlaceHolder="Enter your query related to books here, provide at least 3 words"
        Spinner="processing..."
        RewordPrompt="Please reword your Prompt it may be missing the recommended attributes:{}"