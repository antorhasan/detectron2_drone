<<<<<<< HEAD
import cv2
import json
import sys
from os import listdir
from os.path import isfile, join
import numpy as np


def make_train_single():
    '''crop the appropriate train segment from original image'''
    img = cv2.imread('./home/home.jpg', 1)

    img = img[36:8090,87:9410,:]

    print(img.shape)
    #img = img[-4608:,:,:]
    img = img[0:1536,:,:]

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite('./home/val2.jpg', img)

def crop_train(overlap=True):
    img = cv2.imread('./new_home/odm/odm_ortho_crop.png',1)
    size = 512
    num_ver = int(img.shape[0] / size)
    num_hor = int(img.shape[1] / size)
    
    #print(num_hor,num_ver)
    if overlap==True:
        size = int(size/2)
        for i in range((num_ver*2)-1):
            for j in range((num_hor*2)-1):
                img_temp = img[size*i:(size*i)+(size*2),size*j:size*j+(size*2),:]
                cv2.imwrite('./new_home/odm/crop/'+str(i)+'_'+str(j)+'.jpg', img_temp)
    #print(asd)
    else:
        for i in range(num_ver):
            for j in range(num_hor):
                img_temp = img[size*i:size*(i+1),size*j:size*(j+1),:]
                cv2.imwrite('./new_home/odm/crop/'+str(i)+'_'+str(j)+'.jpg', img_temp)

def labelbox_to_mskrcnn():
    '''reads the json output from labelbox json export and converts it into a suitable
    json format to be consumed by detectron 2 maskrcnn'''
    box_json_dir = './new_home/export-2020-04-10T19_54_39.610Z.json'
    msk_json_dir = './new_home/train_crop.json'
    empt = {}
    with open(box_json_dir) as json_file:
        data = json.load(json_file)
        for i in range(len(data)):
            regions = {}
            for j in range(len(data[i]["Label"]["building"])):
                all_x = []
                all_y = []
                for k in range(len(data[i]["Label"]["building"][j]["geometry"])):
                    all_x.append(data[i]["Label"]["building"][j]["geometry"][k]["x"])
                    all_y.append(data[i]["Label"]["building"][j]["geometry"][k]["y"])
                regions.update({str(j):{"shape_attributes":{"all_points_x":all_x,"all_points_y":all_y},"region_attributes":{}}})
                            
            empt.update({data[i]["ID"]:{"filename":data[i]["External ID"],"regions":regions}})

    with open(msk_json_dir, 'w') as f:
        json.dump(empt, f)

def img_crop_prctg():
    img = cv2.imread('./new_home/odm/odm_orthophoto.png')
    img = img[2480:5552,2350:5934,:]
    cv2.imwrite('./new_home/odm/odm_ortho_cropn.png',img)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#def combine():
def coor_to_geojson():
    coor_json_dir = '../buildings.json'
    geojson_dir = '../geo_final.json'

    empt = {"type": "FeatureCollection", "features": []}
    with open(coor_json_dir) as json_file:
        data = json.load(json_file)

        for i in range(1,len(data)+1):
            temp_list = []
            for j in range(len(data[str(i)][0])):
                temp_list.append([data[str(i)][0][j][1],data[str(i)][0][j][0]])
            temp_list.append([data[str(i)][0][0][1],data[str(i)][0][0][0]])
            empt["features"].append({"id": str(i),"type": "Feature","properties":{"height":data[str(i)][1]},"geometry":{"type":"Polygon", "coordinates":[temp_list]}})
            #print(i)
        print(empt)
    

    with open(geojson_dir, 'w') as f:
        json.dump(empt, f)
    

def merge_msk():
    pixel_coun = 256
    path = './new_home/output/'

    num_row = max([int(f.split('_')[0]) for f in listdir(path) if isfile(join(path, f))])
    num_column = max([int(f.split('_')[1].split('.')[0]) for f in listdir(path) if isfile(join(path, f))])
    
    for i in range(num_row):
        for j in range(num_column):
            print(j)
            if j%2 !=0 and j!=0:
                img_0 = cv2.imread(path + str(i)+'_'+str(j-1)+'.jpg', 0)
                img_1 = cv2.imread(path + str(i)+'_'+str(j)+'.jpg', 0)
                img_2 = cv2.imread(path + str(i)+'_'+str(j+1)+'.jpg', 0)

                print(img_2.shape,img_1.shape,img_0.shape)
                #img_0[:,pixel_coun:] = img_1[:,:pixel_coun] 
                #img_2[:,:pixel_coun] = img_1[:,pixel_coun:]

                img_0[:,pixel_coun:] = np.where(img_1[:,0:pixel_coun]==255, 255, img_0[:,pixel_coun:])
                img_2[:,:pixel_coun] = np.where(img_1[:,pixel_coun:]==255, 255, img_2[:,:pixel_coun])
                
                img = np.concatenate((img_0,img_2), axis=1)

                cv2.imwrite('./temp.jpg', img)
                print(asd)
            


    

#make_train_single()
#crop_train()
if __name__ == "__main__":
    merge_msk()
    #img_crop_prctg()
    #crop_train()
    #labelbox_to_mskrcnn()
    pass

=======
import cv2
import json
import sys
from os import listdir
from os.path import isfile, join
import numpy as np


def make_train_single():
    '''crop the appropriate train segment from original image'''
    img = cv2.imread('./home/home.jpg', 1)

    img = img[36:8090,87:9410,:]

    print(img.shape)
    #img = img[-4608:,:,:]
    img = img[0:1536,:,:]

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite('./home/val2.jpg', img)

def crop_train(overlap=True):
    img = cv2.imread('./new_home/odm/odm_ortho_crop.png',1)
    size = 512
    num_ver = int(img.shape[0] / size)
    num_hor = int(img.shape[1] / size)
    
    #print(num_hor,num_ver)
    if overlap==True:
        size = int(size/2)
        for i in range((num_ver*2)-1):
            for j in range((num_hor*2)-1):
                img_temp = img[size*i:(size*i)+(size*2),size*j:size*j+(size*2),:]
                cv2.imwrite('./new_home/odm/crop/'+str(i)+'_'+str(j)+'.jpg', img_temp)
    #print(asd)
    else:
        for i in range(num_ver):
            for j in range(num_hor):
                img_temp = img[size*i:size*(i+1),size*j:size*(j+1),:]
                cv2.imwrite('./new_home/odm/crop/'+str(i)+'_'+str(j)+'.jpg', img_temp)

def labelbox_to_mskrcnn():
    '''reads the json output from labelbox json export and converts it into a suitable
    json format to be consumed by detectron 2 maskrcnn'''
    box_json_dir = './new_home/export-2020-04-10T19_54_39.610Z.json'
    msk_json_dir = './new_home/train_crop.json'
    empt = {}
    with open(box_json_dir) as json_file:
        data = json.load(json_file)
        for i in range(len(data)):
            regions = {}
            for j in range(len(data[i]["Label"]["building"])):
                all_x = []
                all_y = []
                for k in range(len(data[i]["Label"]["building"][j]["geometry"])):
                    all_x.append(data[i]["Label"]["building"][j]["geometry"][k]["x"])
                    all_y.append(data[i]["Label"]["building"][j]["geometry"][k]["y"])
                regions.update({str(j):{"shape_attributes":{"all_points_x":all_x,"all_points_y":all_y},"region_attributes":{}}})
                            
            empt.update({data[i]["ID"]:{"filename":data[i]["External ID"],"regions":regions}})

    with open(msk_json_dir, 'w') as f:
        json.dump(empt, f)

def img_crop_prctg():
    img = cv2.imread('./new_home/odm/odm_orthophoto.png')
    img = img[2480:5552,2350:5934,:]
    cv2.imwrite('./new_home/odm/odm_ortho_cropn.png',img)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#def combine():
def coor_to_geojson():
    coor_json_dir = '../buildings.json'
    geojson_dir = '../geo_final.json'

    empt = {"type": "FeatureCollection", "features": []}
    with open(coor_json_dir) as json_file:
        data = json.load(json_file)

        for i in range(1,len(data)+1):
            temp_list = []
            for j in range(len(data[str(i)][0])):
                temp_list.append([data[str(i)][0][j][1],data[str(i)][0][j][0]])
            temp_list.append([data[str(i)][0][0][1],data[str(i)][0][0][0]])
            empt["features"].append({"id": str(i),"type": "Feature","properties":{"height":data[str(i)][1]},"geometry":{"type":"Polygon", "coordinates":[temp_list]}})
            #print(i)
        print(empt)
    

    with open(geojson_dir, 'w') as f:
        json.dump(empt, f)
    

def merge_msk():
    pixel_coun = 256
    path = './new_home/output/'

    num_row = max([int(f.split('_')[0]) for f in listdir(path) if isfile(join(path, f))])
    num_column = max([int(f.split('_')[1].split('.')[0]) for f in listdir(path) if isfile(join(path, f))])
    
    for i in range(num_row):
        for j in range(num_column):
            print(j)
            if j%2 !=0 and j!=0:
                img_0 = cv2.imread(path + str(i)+'_'+str(j-1)+'.jpg', 0)
                img_1 = cv2.imread(path + str(i)+'_'+str(j)+'.jpg', 0)
                img_2 = cv2.imread(path + str(i)+'_'+str(j+1)+'.jpg', 0)

                print(img_2.shape,img_1.shape,img_0.shape)
                #img_0[:,pixel_coun:] = img_1[:,:pixel_coun] 
                #img_2[:,:pixel_coun] = img_1[:,pixel_coun:]

                img_0[:,pixel_coun:] = np.where(img_1[:,0:pixel_coun]==255, 255, img_0[:,pixel_coun:])
                img_2[:,:pixel_coun] = np.where(img_1[:,pixel_coun:]==255, 255, img_2[:,:pixel_coun])
                
                img = np.concatenate((img_0,img_2), axis=1)

                cv2.imwrite('./temp.jpg', img)
                print(asd)
            


    

#make_train_single()
#crop_train()
if __name__ == "__main__":
    merge_msk()
    #img_crop_prctg()
    #crop_train()
    #labelbox_to_mskrcnn()
    pass

>>>>>>> f0615e03475350f291b5d0d75a8d95e5c3256f78
