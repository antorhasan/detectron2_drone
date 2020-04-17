
import os
from os import listdir
from os.path import isfile, join



path2 = "D:/3D Mapping/fold2image/2"
tobecopied = [f for f in listdir(path2) if isfile(join(path2, f))]

print(tobecopied)














