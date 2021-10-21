import classBuilder

class classInfoC:
    def __init__(self, classname):
        self.className = classname
        self.variablesType = []
        self.variablesName = []
        self.jsonKeys = []


    # getter
    def get_className(self):
        return self.className

    def get_variablesType(self):
        return self.variablesType

    def get_variablesName(self):
        return self.variablesName

    def get_jsonKeys(self):
        return self.jsonKeys

    def add_info(self, variableType, variableName, jsonKey):
        classBuld = classBuilder.classBuilder()
        if variableName in self.variablesName:
            # if name is repeated add Str then try it again
            variableName = variableName[:15] + classBuld.randomString(8, classBuld.lettersAndNumbers)
            self.add_info(variableType, variableName, jsonKey)
        if jsonKey in self.jsonKeys:
            return
        self.variablesType.append(variableType)
        self.variablesName.append(variableName)
        self.jsonKeys.append(jsonKey)

