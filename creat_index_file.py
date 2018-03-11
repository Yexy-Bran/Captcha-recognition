import os

def creat_index_txt(path,trainname,valname):
    dirs = os.listdir(path)
    train = []
    val = []
    for sdir in dirs:
        if ord(sdir)>=65:
            files = os.listdir(path+os.path.sep+sdir)
            filenum = len(files)
            label = ord(sdir)-65+10
            for sfile in files:
                t = sfile.rfind('.')
                index = int(sfile[:t])
                if index < filenum/5*4:
                    train.append(sdir+'_'+sfile+' '+str(label))
                else:
                    val.append(sdir+'_'+sfile+' '+str(label))
        else:
            files = os.listdir(path+os.path.sep+sdir)
            filenum = len(files)
            label = ord(sdir)-48
            for sfile in files:
                t = sfile.rfind('.')
                index = int(sfile[:t])
                if index < filenum/5*4:
                    train.append(sdir+'_'+sfile+' '+str(label))
                else:
                    val.append(sdir+'_'+sfile+' '+str(label))
    traintxt = open(trainname, 'wb')
    valtxt = open(valname, 'wb')
    for i in train:
        traintxt.write(i+'\n')
    for i in val:
        valtxt.write(i+'\n')
    traintxt.close()
    valtxt.close()

if __name__ == "__main__":
    creat_index_txt('/home/yxy/Workspace/data','train.txt','val.txt')
