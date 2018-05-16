import os
class FileReader():

    def __init__(self):
        self.lineList = []   

    def replace_lineList(self, currLineList):
        newLineList = []
        for line in currLineList:
            lineArr = line.split()
            newLineList.append(lineArr[1] + "," + lineArr[0])
        self.lineList = newLineList
        

    def process_email(self):
        ext_list = []
        for line in self.lineList:
            line = line.replace("\n","")
            ext_list.append(line)

        self.replace_lineList(ext_list)
        return self.lineList
        


    def open_file(self,filepath):
        file = None
        if os.path.exists(filepath):
            file = open(filepath,'r')
            with file as line:
                self.lineList = line.readlines()
                line.close()
            return self.lineList
        else:
            print("FILE " + filepath + " DOES NOT EXIST!")
            return self.lineList

    def read_file(self,filepath):
        file = None
        if os.path.exists(filepath):
            file = open(filepath,'r')
            with file as line:
                self.lineList = line.readlines()
                line.close()
            return self.lineList
        else:
            print("FILE " + filepath + " DOES NOT EXIST!")
            return self.lineList
