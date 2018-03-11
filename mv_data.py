import os
import shutil

def move_file(path, des1, des2):
    dirs = os.listdir(path)
    for sdir in dirs:
        files = os.listdir(path+os.path.sep+sdir)
        filenum = len(files)
        for sfile in files:
            t = sfile.rfind('.')
            index = int(sfile[:t])
            if index < filenum/5*4:
                shutil.move(path+'/'+sdir+'/'+sfile,des1+sdir+'_'+sfile)
            else:
                shutil.move(path+'/'+sdir+'/'+sfile,des2+sdir+'_'+sfile)

if __name__ == "__main__":
    move_file('/Workspace/data','/Workspace/train/','/Workspace/val/')
