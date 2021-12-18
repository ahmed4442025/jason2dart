import json
import random


class classBuilder:

    def __init__(self):

        self.newLine = '\n'
        self.dictTempFlag = 'dict321'
        self.arrTempFlag = 'arr321'

        self.abc = 'abcdefghijklmnopqrstuvwxyz'
        self.ABC = self.abc.upper()
        self.numbers = '0123456789'
        self.lettersAndNumbers = self.abc + self.ABC + self.numbers
        self.maxNameSize = 20

    # random String
    def randomString(self, size=8, chars='#'):
        if chars != '#':
            chars = self.abc + self.ABC
        return ''.join(random.choice(chars) for _ in range(size))

    # fix variable name if null or too long or repeated
    def getNewName(self, name):
        newName = self.filterName(name)
        # var = null
        if len(newName) == 0:
            newName = self.randomString()
        # var too long
        if len(newName) > self.maxNameSize:
            newName = newName[0:self.maxNameSize]
        # first char is not number
        if newName[0] in self.numbers:
            newName = 'a' + newName

        return newName

    # remove all bad chars
    def filterName(self, name):
        newName = ''
        for i in name:
            if i in self.abc or i in self.ABC or i in (self.numbers + '_'):
                newName += i
        return newName

    # return 1 var field in class
    def buildVar(self, var, name):
        # if obj remove the flag and use the name
        if self.dictTempFlag in var:
            var = var.split(':')[1]
        # if arr return => List<classNameC> className = [];
        if self.arrTempFlag in var:
            var = var.split(':')[1]
            return '  List<' + var + '>? ' + name + ';' + self.newLine
        return '  ' + var + '? ' + name + ';' + self.newLine

    # return all vars in class
    def buildVars(self, vars, names):
        m = '  // vars' + self.newLine
        for i in range(len(vars)):
            m += self.buildVar(vars[i], names[i])
        m += self.newLine
        return m

    # return class Constructor
    def buildClassConst(self, className, names):
        m = '  //The Constructor' + self.newLine
        m += '  ' + className
        m += '(' + self.newLine + '{'
        l = len(names)
        for i in range(len(names)):
            m += 'this.' + names[i]
            if i != l - 1:
                m += ', ' + self.newLine + '      '
        m += '});' + self.newLine + self.newLine
        return m

    # the field of variable in factory method
    # check if normal var or dic or arr
    def factoryField(self, name, newClassName, var, namej):
        m = ''
        # if dic call (fromJson) method
        # className_R.var = otherClassC.fromJson(json['data']);
        if self.dictTempFlag in var:
            var = var.split(':')[1]
            tempVarName = name + self.randomString(3, self.abc)

            # add (if) json is null
            m += "    var " + tempVarName + " = json['" + namej + "'];" + self.newLine
            m += "if (" + tempVarName + " != null){" + self.newLine
            m += '    ' + newClassName + '.' + name + ' = ' + var + ".fromJson(" + tempVarName + ");"
            m += self.newLine + '    }'
        # if array use for loop
        elif self.arrTempFlag in var:
            var = var.split(':')[1]
            # loop
            m += '      {0}.{1} = [];'.format(newClassName, name) + self.newLine
            m += '''    for (var item in json['{0}'])'''.format(namej) + '{' + self.newLine
            m += "      if (item == null) continue;" + self.newLine
            m += '''      {0} temp = {0}.fromJson(item);'''.format(var) + self.newLine
            m += '      {0}.{1}!.add(temp);'.format(newClassName, name) + self.newLine
            m += '}'
        else:
            # normal var (int, string, bool)
            m = '''{0}{2}.{1} = json['{3}'];'''.format('    ', name, newClassName, namej)
        m += self.newLine
        return m

    # build method take json obj and return class obj as factory
    def buildFactory(self, className, names, vars, namesj):
        spaces4 = '    '
        # temp name '_R' to make sure the names are not repeated
        newClassName = className + '_R'
        # start of the method
        m = '  factory '
        m += className
        m += '.fromJson(Map<String, dynamic> json) {'
        m += self.newLine
        m += '{0}{1} {2} = {1}();'.format(spaces4, className, newClassName)
        m += self.newLine

        # set variable and get json data by key
        # className_R.var = json['data'];
        for i in range(len(names)):
            name = names[i]
            var = vars[i]
            namej = namesj[i]
            m += self.factoryField(name, newClassName, var, namej)

        # end of the method
        m += '{0}return {1};'.format(spaces4, newClassName)
        m += self.newLine + '}' + self.newLine
        return m

    def buildOneFieldToJsonArr(self, jsonKey, varName):
        m = "    if (" + varName + " != null) {" + self.newLine
        m += "      data['{0}'] = {1}!.map((v) => v.toJson()).toList();".format(jsonKey, varName) + self.newLine
        m += "    }" + self.newLine
        return m

    def buildOneFieldToJsonObj(self, jsonKey, varName):
        m = "    if (" + varName + " != null) {" + self.newLine
        m += "      data['" + jsonKey + "'] = " + varName + "!.toJson();" + self.newLine
        m += "    }" + self.newLine
        return m

    def buildOneFieldToJson(self, jsonKey, varName, varType):
        if self.arrTempFlag in varType:
            return self.buildOneFieldToJsonArr(jsonKey, varName)
        if self.dictTempFlag in varType:
            return self.buildOneFieldToJsonObj(jsonKey, varName)
        m = '    if (' + varName + ' != null)'
        m += " data['" + jsonKey + "'] = " + varName + ";" + self.newLine
        return m

    # .toJson()
    def buildToJson(self, jsonKeys, varNames, varTypes):
        m = '  Map<String, dynamic> toJson() {' + self.newLine
        m += '     final Map<String, dynamic> data = Map<String, dynamic>();' + self.newLine
        for i in range(len(jsonKeys)):
            m += self.buildOneFieldToJson(jsonKeys[i], varNames[i], varTypes[i])
        m += '    return data;' + self.newLine
        m += ' }' + self.newLine
        return m

    # build 1 class with this info
    def buildClassT(self, className, varTypes, varnames, jsonKeys):
        classStart = 'class '
        classStart2 = ' {' + self.newLine + self.newLine
        m = classStart + className
        m += classStart2
        m += self.buildVars(varTypes, varnames)
        m += self.buildClassConst(className, varnames)
        m += self.buildFactory(className, varnames, varTypes, jsonKeys)
        m += self.buildToJson(jsonKeys, varnames, varTypes)
        m += '}'
        return m

    def flagTheVarType(self, varType, objName):
        # if obj or arr return FLAG:NAME + 'C' (C = first char in class)
        # flag use to recognize the type (if need Special process)
        # the flag will remove when build the class
        if varType == 'dict':
            return self.dictTempFlag + ':' + objName + 'C'
        if varType == 'arr':
            return self.arrTempFlag + ':' + objName + 'C'

    # check if type is arr or obj or . .
    def typeToVarType(self, typeStr, name):
        hashVars = {"<class 'str'>": 'String', "<class 'int'>": 'int', "<class 'bool'>": 'bool',
                    "<class 'dict'>": 'dict', "<class 'list'>": 'arr'}

        if str(typeStr) in hashVars:
            result = hashVars[str(typeStr)]
        else:
            return 'String'
        if result in 'dict:arr':
            result = self.flagTheVarType(result, name)
        return result
