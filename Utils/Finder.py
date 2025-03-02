import os
from datetime import datetime
from time import sleep

def get_time():
    sleep(1)
    return datetime.now().strftime("%y%m%d-%H%M%S")

class DicomFinder():
    def __init__(self,):
        '''Use find() method to find dicom files.'''
        pass

    def find(self, root):
        '''
        return: list of dictionaries.  
        ```python
        dictionary = {
            'path':  path of dicom,
            'folder':  path of folder of dicoms,
            'subject':  name of subject
        }
        ```
        '''
        if os.path.isdir(root):
            dcmlist = self.traverser(root, [], root)
            return dcmlist

    def traverser(self, folder, dcmlist:list, root):
        if os.path.isdir(folder):
            filelist:list = os.listdir(folder)
            filelist.sort()
            if len(filelist)==0:
                pass
            elif self.with_dcm(filelist):
                pathdict = {}
                pathdict['path'] = os.path.join(folder, filelist[0])
                pathdict['folder'] = folder
                pathdict['subject'] = self.subjectname(folder, root)
                if len(pathdict['subject'])==0: pathdict['subject'] = get_time()
                dcmlist.append(pathdict)
            else:
                for subf in filelist:
                    subpath = os.path.join(folder, subf)
                    dcmlist = self.traverser(subpath, dcmlist, root)
        return dcmlist

    def subjectname(self, folder:str, root:str):
        '''Extract the name of the first folder under the root in folder.'''
        remain = folder[len(root):]
        return remain.lstrip(os.sep).split(os.sep)[0]
    
    def with_dcm(self, filelist):
        '''Check if there is any dicom file in filelist'''
        filelist = [f for f in filelist if f.endswith('.dcm')]
        if len(filelist)==0:
            return None
        else:
            return True
