from os import listdir
from os.path import isfile, join
from PIL import Image 
import cv2 
import numpy as np 
#import tifffile as tiff
#import matplotlib.pyplot as plt
from rasterio.windows import Window
from collections import Counter
import rasterio
from rasterio.enums import Resampling
from rasterio.windows import from_bounds
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pyproj
import json



def choosepixel(path):
    img = cv2.imread(path, 0)
    plt.imshow(img, cmap='gray')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    #plt = plt.figure(figsize=(10,10))
    plt.show()

def cropandscale(path_png):
    im = cv2.imread(path_png, cv2.IMREAD_GRAYSCALE)
    #print('shape', im.shape)
    im2 = im[1674:2554, 1796:5280] #crop desired part of image
    resized = cv2.resize(im2, (9216, 1536), interpolation=cv2.INTER_CUBIC) #(width,height) resize to desired size



def pix_to_latlon(path_to_tif, px_row, px_col):
    '''change the px_row and px_col to the pixel index for lat long transformation'''
    #px_row = 100
    #px_col = 100

    with rasterio.open(path_to_tif) as map_layer:
        pixels2coords = map_layer.xy(px_row, px_col)  #input px, py
        crs = map_layer.crs

    x, y = pixels2coords

    in_proj = pyproj.Proj(init="epsg:{}".format(crs.to_epsg()))
    out_proj = pyproj.Proj(init="epsg:4326")

    lons, lats = pyproj.transform(in_proj, out_proj, x, y)

    print(lats, lons) 


def pix_to_latlon_2(path_to_tif, cnvrt_prj,pxrow, pxcol):
    '''change the px_row and px_col to the pixel index for lat long transformation'''
    #px_row = 100
    #px_col = 100

    alllons = []
    alllats = []
    with rasterio.open(path_to_tif) as map_layer:
        crs = map_layer.crs
        for i in range(len(pxrow)):
            pixels2coords = map_layer.xy(pxrow[i], pxcol[i])  #input px, py
            x, y = pixels2coords

            if cnvrt_prj == True :
                in_proj = pyproj.Proj(init="epsg:{}".format(crs.to_epsg()))
                out_proj = pyproj.Proj(init="epsg:4326")

                #print('in_prj : ', crs.to_epsg(),' out_prj : ', '4326')

                lons, lats = pyproj.transform(in_proj, out_proj, x, y)
                lons = round(lons,6)
                lats = round(lats,6)
                alllons.append(lons)
                alllats.append(lats)
            else :
                alllons.append(x)
                alllats.append(y)
        
    return alllats, alllons



def contour_find(imagepath, dsmpath, orthophotopath, offsethor, offsetver):
    buildingdict = {}

    #imagename="dsm_color.png"
    imagename = imagepath

    # Reading image 
    font = cv2.FONT_HERSHEY_COMPLEX 
    #img2 = cv2.imread(imagename, cv2.IMREAD_COLOR)  
    #(height, width) = img2.shape 
    
    # Reading same image in another  
    # variable and converting to gray scale. 
    img = cv2.imread(imagename, cv2.IMREAD_GRAYSCALE)  #cv2.IMREAD_GRAYSCALE

    imgcolor = cv2.imread(imagename)
    #imgcolor = cv2.resize(imgcolor, (500,500))
    (height, width) = img.shape 
    #print(height, width)

    _, threshold = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY) 

    # Detecting contours in image. 
    contours, _= cv2.findContours(threshold, cv2.RETR_TREE, 
                                cv2.CHAIN_APPROX_SIMPLE)       

    
    # Going through every contours found in the image. 
    round = 0
    for cnt in contours: 
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True) 

        # draws boundary of contours. 
        #cv2.drawContours(img, [approx], -1, (0, 255, 0), 3)  
        #cv2.drawContours(img, [approx], -1, (0, 255, 0))  
        cv2.drawContours(imgcolor,[approx],-1, (0, 255, 0),5)

        round += 1
        #if round < 8:
        #    continue
    
        # Used to flatted the array containing 
        # the co-ordinates of the vertices. 
        n = approx.ravel()  
        i = 0

        coordsx = []
        coordsy = []
        for i in range(0,len(n),2):
            x = n[i] + offsethor  #column
            y = n[i+1] + offsetver  #row
            coordsx.append(x)
            coordsy.append(y)
        
        
        #img2 = cv2.resize(imgcolor, (int(width/3), int(height/3))) #(width, height)
        #cv2.imshow('contour_exp', img2)  
        #cv2.imwrite('contour_exp.png',imgcolor)
        
        # Exiting the window if 'q' is pressed on the keyboard. 
        #if cv2.waitKey(0) & 0xFF == ord('q'):  
            #cv2.destroyAllWindows() 

        imagedsm = cv2.imread(dsmpath, cv2.IMREAD_GRAYSCALE)
        minx = min(coordsx)
        miny = min(coordsy)
        maxx = max(coordsx)
        maxy = max(coordsy)

        midx = (minx+maxx)//2
        midy = (miny+maxy)//2

        listofx = []
        listofy = []
        heights = []

        #finds height of building after averaging some specific points
        for tx in range(midx-SPAN, midx+SPAN, INTERVAL):
            for ty in range(midy-SPAN, midy+SPAN, INTERVAL):
                heights.append((int(imagedsm[ty, tx]))-112)

        #print('pixel intensity:', midy, midx, imagedsm[midy+offsetver, midx+offsethor])
        #height = int(imagedsm[midy+offsetver, midx+offsethor])
        #height = int(imagedsm[midy, midx])
        #height = height - 112

        height = sum(heights)/len(heights)

        if height <= 2:
            round -= 1
            continue

        #find lat lon values

        #imageortho = cv2.imread(orthophotopath, cv2.IMREAD_GRAYSCALE)
        lats, lons = pix_to_latlon_2(orthophotopath, coordsy, coordsx)
        positions = []
        height *= 2
        for i in range(len(lats)):
            temp = [lats[i], lons[i]]
            positions.append(temp)
        buildingdict[round] = [positions, height]
        #print(buildingdict)
        break

    return buildingdict

if __name__ == "__main__":
    mergedimagepath = "D:\\3D Mapping\\Code\\Corona Datalab\\Code\\Antor bhai Segmentation\\PART 3\\mergedvertical4.png"
    dsmpath = "D:\\3D Mapping\\Code\\Corona Datalab\\Code\\Antor bhai Segmentation\\PART 3\\croppedandscaledBIG3.png"
    orthophotopath = "D:\\3D Mapping\\Code\\Corona Datalab\\Code\\Antor bhai Segmentation\\PART 3\\odm_orthophoto.original.tif"
    roadpixelintensity = 112
    offsetver = 2480
    offsethor = 2350

    SPAN = 40
    INTERVAL = 10

    buildingdict = contour_find(mergedimagepath, dsmpath, orthophotopath, offsethor, offsetver)
    #print(buildingdict)

    with open('buildings_6.json', 'w') as fp:
        json.dump(buildingdict, fp)

    #choosepixel(dsmpath)
    pass












