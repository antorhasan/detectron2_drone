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






path1 = "D:/3D Mapping/fold1image/1"
path2 = "D:/3D Mapping/fold2image/2"
temppath = "D:/3D Mapping/fold1image/temp"

'''
orig_files = [f for f in listdir(path1) if isfile(join(path1, f))]
last_num = orig_files[-1].split(".")[0].split("_")[1]
last_num = int(last_num)
'''

last_num = find_largest_num(path1)
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
    x = shutil.copy(path, path1)









