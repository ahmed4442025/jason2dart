import sys
import os.path
from datetime import datetime as datetime2
import datetime


class interactive:
    def printHelp(self):
        m = '\n- used  : for dart data classes generating from a json for a flutter project.\n\n'
        m += '- Usage : j2d.py [InputJsonFile] [outputDartFile] [MainClassName]\n'
        print(m)

    def getExtAndNameAndFolderPathFromPath(self, filePath):
        filePath = filePath.replace('\\', '/')
        split = os.path.splitext(filePath)
        extension = split[1]
        splitPath = split[0].split('/')
        fileName = splitPath[-1]
        dirPath = '/'.join(splitPath[0:-1])
        return extension, fileName, dirPath

    def get1arg(self, line1inputPath):
        ext, inputFileName, dirPath = self.getExtAndNameAndFolderPathFromPath(line1inputPath)
        outputPath = dirPath + "/" + inputFileName + '.dart'
        return line1inputPath, outputPath, inputFileName

    def get2arg(self, line1inputPath, line2OutputPath):
        ext, outputFileName, dirPath = self.getExtAndNameAndFolderPathFromPath(line2OutputPath)
        return line1inputPath, line2OutputPath, outputFileName
    def get3arg(self, line1inputPath, line2OutputPath, line3ClassName):
        return line1inputPath, line2OutputPath, line3ClassName

    def getOption(self):
        n = len(sys.argv)
        n1 = sys.argv[0]

        if n == 1:
            return -1, -1, -1
        if n == 2:
            return self.get1arg(sys.argv[1])
        if n == 3:
            return self.get2arg(sys.argv[1], sys.argv[2])
        if n == 4:
            return self.get3arg(sys.argv[1], sys.argv[2], sys.argv[3])