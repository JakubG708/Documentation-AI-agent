import os

class RepositoryAssigner:
    def __init__(self, repository):
        self.repository = repository
        self.assignation = {}

    def assign(self,fileName:str ,language: str):
        self.assignation[fileName] = language

    def getAssignations(self):
        return self.assignation
    
    def getAssignation(self, fileName:str):
        return self.assignation[fileName]
    
    def removeAssignation(self, fileName: str):
        self.assignation.pop(fileName, None)

    
    def readRepoFiles(self):
        for root, dirs, files in os.walk(self.repository):
            if '.git' in dirs:
                dirs.remove('.git')
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, self.repository)
                self.assignation[relative_path] = ""



