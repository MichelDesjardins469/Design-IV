import json


class ValuesSaver:
    def __init__(self, filePath):
        self.filePath = filePath
        self.values = None

    # Always need to call this first in order to read the file
    def getValues(self):
        with open(self.filePath, "r") as openedFile:
            currentValues = json.load(openedFile)
        return currentValues

    def updateValues(self, newValues):
        self.values = self.getValues()
        self.values.update(newValues)
        json_object_formatted = json.dumps(self.values, indent=4)
        with open(self.filePath, "w") as outputFile:
            outputFile.write(json_object_formatted)


saver = ValuesSaver("values.json")
# This part is only used as an example
# In use, the newDictValues will come directly from the interface
saver.getValues()
newDictValues = {"value1": "Hi", "value2": {"value3": "bonjour"}}
saver.updateValues(newDictValues)
