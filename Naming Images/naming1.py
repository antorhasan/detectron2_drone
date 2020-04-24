import shutil
import os
from os import listdir
from os.path import isfile, join


def find_largest_num(path):
    all_files = [f for f in listdir(path) if isfile(join(path, f))]
    largest_num = 0
    #print(all_files)

    for name in all_files:
        num = name.split(".")[0].split("_")[1]
        num1 = int(num)
        #print(num, " - ", num1)
        if num1 > largest_num:
            largest_num = num1 

    return largest_num




def rename_all(num):

    dest = "/media/antor/Transcend/drone/data/dhanmondi/100MEDIA"
    path2 = "/media/antor/Transcend/drone/data/dhanmondi/1"+num+"MEDIA"
    temppath = "/media/antor/Transcend/drone/data/dhanmondi/temp"

    '''
    orig_files = [f for f in listdir(path1) if isfile(join(path1, f))]
    last_num = orig_files[-1].split(".")[0].split("_")[1]
    last_num = int(last_num)
    '''

    last_num = find_largest_num(dest)
    #print(last_num)

    valid_num = last_num + 1


    #copy to temp folder
    tobecopied = [f for f in listdir(path2) if isfile(join(path2, f))]
    for name in tobecopied:
        path = path2 + "/" + name 
        x = shutil.copy(path, temppath)


    #rename in temp folder
    toberenamed = [f for f in listdir(temppath) if isfile(join(temppath, f))]
    for name in toberenamed:
        oldname = temppath + "/" + name
        newname = temppath + "/" + "DJI_" + str(valid_num) + ".JPG"
        os.rename(oldname, newname)
        valid_num += 1



    #copy to original folder
    finalcopy = [f for f in listdir(temppath) if isfile(join(temppath, f))]
    #print(finalcopy)

    for name in finalcopy:
        path = temppath + "/" + name 
        x = shutil.copy(path, dest)

for i in range(3,10):
    print(i)
    rename_all('0'+str(i))
    os.system("sudo rm -r /media/antor/Transcend/drone/data/dhanmondi/temp/*")

for i in range(10,13):
    print(i)
    rename_all(str(i))
    os.system("sudo rm -r /media/antor/Transcend/drone/data/dhanmondi/temp/*")







