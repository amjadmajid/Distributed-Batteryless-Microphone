import os
import glob

class FileSelector():
    def __init__(self, rootDir):
        self.cwd = os.getcwd()
        self.path = rootDir 

    def dirSelector(self):
        os.chdir(self.path)
        exprs = glob.glob('*') # grap all dirs
        for i, expr in enumerate(exprs):
            if "logicdata" not in expr:
                print(i,'-',expr)
        exp = input('choose experiment')
        os.chdir(self.cwd)
        return exprs[int(exp)]

    def updateDataPath(self,directory):
        self.path = os.path.join(self.path, directory)
    
    def getPath(self):
        while True:
            experiment = self.dirSelector()
            self.updateDataPath(experiment)
            if os.path.isfile(self.path):
                return self.path

def main():
    fs = FileSelector('../data/')
    print(fs.getPath())

if __name__=="__main__":
    main()
