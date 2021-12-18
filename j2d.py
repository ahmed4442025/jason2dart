import json
import os
import classInfoC
import classBuilder
import interactive


class json2dart:

    def __init__(self):
        self.hashClasses = {}
        self.builder = classBuilder.classBuilder()
        self.classes = []

    def initializ(self, jsonObj, className, isArr):
        tempClass = classInfoC.classInfoC(className)
        if className in self.hashClasses:
            tempClass = self.hashClasses[className]
        else:
            self.hashClasses[className] = tempClass

        if not isArr:
            for key in jsonObj:
                childJson = jsonObj[key]
                name = self.builder.getNewName(key)
                varTypej = type(childJson)
                varType = self.builder.typeToVarType(varTypej, name)
                tempClass.add_info(varType, name, key)
                self.hashClasses[className] = tempClass

                if 'dict321:' in varType:
                    self.initializ(childJson, name + 'C', False)
                if 'arr321:' in varType:
                    self.initializ(childJson, name + 'C', True)
        else:
            for i in range(len(jsonObj)):
                json2 = jsonObj[i]
                if json2 is None:
                    continue
                for key in json2:
                    childJson = json2[key]
                    name = self.builder.getNewName(key)
                    varType = type(childJson)
                    varType = self.builder.typeToVarType(varType, name)
                    tempClass.add_info(varType, name, key)
                    self.hashClasses[className] = tempClass

                    if 'dict321:' in varType:
                        self.initializ(childJson, name + 'C', False)
                    if 'arr321:' in varType:
                        self.initializ(childJson, name + 'C', True)

    def buildAll(self, json, className):
        self.initializ(json, className, False)
        for i in self.hashClasses:
            tempClass = self.hashClasses[i]
            classNamep = tempClass.get_className()
            keys = tempClass.get_jsonKeys()
            vars = tempClass.get_variablesType()
            varNames = tempClass.get_variablesName()
            self.classes.append(self.builder.buildClassT(classNamep, vars, varNames, keys))

    def printAll(self):
        for i in self.classes:
            print(i)

    def saveAll(self, outputPath):
        m = ''
        for i in self.classes:
            m += i + '\n\n'
        o = open(outputPath, 'w', encoding="UTF-8")
        o.write(m)
        o.close()
        return len(self.classes)


def main2():
    interActiv = interactive.interactive()
    input, output, className = interActiv.getOption()
    if input == -1:
        print('\nERROR ! no input found')
        interActiv.printHelp()
    else:
        if os.path.exists(input):
            f = open(input, 'r', encoding="UTF-8")
            json1 = json.load(f)
            j2d = json2dart()
            j2d.buildAll(json1, className)
            numClass = j2d.saveAll(output)
            print('Converted successfully !')
            print(f'{numClass} classes have been generated')
        else:
            print('\nERROR ! input file path not found')


main2()
input('. .  .')
