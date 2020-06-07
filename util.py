import cv2
import json
import sys
from os import listdir
from os.path import isfile, join
import numpy as np
import rasterio
import shutil
import os


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

def crop_train(overlap=True, window_size=512):
    img = cv2.imread('./new_home/odm/odm_ortho_crop.png',1)
    size = window_size
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
    box_json_dir = './new_home/temp11.json'
    msk_json_dir = './new_home/train_dhan.json'
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
    cv2.imwrite('./new_home/odm/odm_ortho_crop.png',img)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#def combine():
def coor_to_geojson():
    coor_json_dir = './data/buildings.json'
    geojson_dir = './data/geo_final.json'

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
        #print(empt)
    

    with open(geojson_dir, 'w') as f:
        json.dump(empt, f)
    

def merge_msk():
    '''overlapping output of binary masks are merged to generate mask of the whole area'''
    thresh = 230
    pixel_coun = 128
    path = './new_home/output/'

    num_row = max([int(f.split('_')[0]) for f in listdir(path) if isfile(join(path, f))]) + 1
    num_column = max([int(f.split('_')[1].split('.')[0]) for f in listdir(path) if isfile(join(path, f))]) + 1
    
    temp_list = []
    #print(num_row, num_column)
    for i in range(num_row):
        for j in range(num_column):
            #print(i,j)
            if j%2 !=0 and j!=0:

                if j == 1 :
                    img_0 = cv2.imread(path + str(i)+'_'+str(j-1)+'.jpg', 0)
                    height = img_0.shape[0]
                    width = img_0.shape[1]
                img_1 = cv2.imread(path + str(i)+'_'+str(j)+'.jpg', 0)
                img_2 = cv2.imread(path + str(i)+'_'+str(j+1)+'.jpg', 0)

                img_0[:,-pixel_coun:] = np.where(img_1[:,int((width/2)-pixel_coun):int(width/2)]>thresh, 255, img_0[:,-pixel_coun:])
                img_2[:,0:pixel_coun] = np.where(img_1[:,int(width/2):int(width/2)+pixel_coun]>thresh, 255, img_2[:,0:pixel_coun])
                
                img_0 = np.concatenate((img_0,img_2), axis=1)
                #cv2.imwrite('./data/trial.jpg', img_0)
                #print(asd)
        if i == 0 :
            final_img = img_0
        else :
            final_img[-pixel_coun:,:] = np.where(img_0[int((height/2)-pixel_coun):int(height/2),:]>thresh, 255, final_img[-pixel_coun:,:])
            final_img = np.concatenate((final_img,img_0[int(height/2):,:]), axis=0)

    cv2.imwrite('./data/merged_msk.jpg', final_img)
    #print(asd)


from GPSPhoto import gpsphoto

def wrt_geo_viz():
    '''given a directory of jpeg images, a geojson file is written with long,lat and alt for each image'''

    path = '/media/antor/Transcend/drone/data/dhanmondi/100MEDIA/'
    json_out_path = './new_home/geojson_viz.json'

    file_lst = [f for f in listdir(path) if isfile(join(path, f))]
    empt = {"type": "FeatureCollection", "features": []}

    print('writing long, lat to geojson file ......')
    for i in range(len(file_lst)):
        file_path = join(path, file_lst[i])
        data = gpsphoto.getGPSData(file_path)
        empt["features"].append({"id": str(file_lst[i]),"type": "Feature","geometry":{"type":"Point", "coordinates":[data['Longitude'],data['Latitude']]},
                            "properties":{"image_id":str(file_lst[i]),"longitude":data['Longitude'],"latitude":data['Latitude'],"altitude":data['Altitude']}})

        if i%501 == 500 or i==len(file_lst) :
            print(str(i)+' images processed....')

    with open(json_out_path, 'w') as f:
        json.dump(empt, f)

def json_to_imgid():
    '''given a json file as input, returns a list of image filenames'''

    json_path = './new_home/drn_dep4.geojson'

    img_ids = []
    with open(json_path) as json_file:
        data = json.load(json_file)
        for i in range(len(data['features'])):
            img_ids.append(data['features'][i]['properties']['image_id'])
    
    return img_ids

def bulk_copy():
    list_img = json_to_imgid()
    
    for i in range(len(list_img)):
        print(i)
        os.system('cp '+'/media/antor/Transcend/drone/data/dhanmondi/100MEDIA/'+list_img[i]+' /media/antor/Transcend/temp/')
        
from crop_sc import read_tally_from_file, find_boundary


def mrg_dhan_msk():
    path_to_msk = './new_home/output/'
    file_lst = [int(f.split('.')[0]) for f in listdir(path_to_msk) if isfile(join(path_to_msk, f))]
    file_lst.sort()
    #print(file_lst)
    #print(asd)

    start_offset = 4096
    constant = 3072
    fixing_ovrlp_win = int(constant/2)
    bin_thresh = 230
    tif_width = 44699
    tif_height = 41861

    tallies = read_tally_from_file()
    tallylen = len(tallies)
    #print(tallylen)
    #print(asd)
    overlap = True

    if overlap == True :
        window_step = constant//2
    else :
        window_step = constant

    top_blank = 0
    bottom_blank = 0

    i = 0
    minus_flag = True
    row_flag = True
    row_count = 0
    while i < tallylen:
        if tallies[i][0] == -1 and tallies[i][1] == -1 and minus_flag == True:
            top_blank += 1

        if tallies[i][0] == -1 and tallies[i][1] == -1 and minus_flag == False:
            bottom_blank += 1

        if tallies[i][0] != -1 and tallies[i][1] != -1:
            print('row_count',row_count)
            minus_flag = False

            startcol, stopcol = find_boundary(i, i+constant, tallies)

            startcol = startcol + start_offset
            stopcol = stopcol - start_offset

            #
            row_img = np.zeros((constant,startcol))

            #print(row_img.shape)
            if (stopcol - startcol) < constant:
                i += 1
                continue
            print('starts are', startcol, stopcol)
            counter = 0
            for j in range(startcol, stopcol, window_step):
    
                if stopcol - j < constant :
                    print(stopcol-j)
                    break
                print('col_count',counter)
                if j == startcol :
                    print(file_lst[0])
                    img = cv2.imread('./new_home/output/'+str(file_lst.pop(0))+'.jpg',0)
                    row_img = np.concatenate((row_img,img),axis=1)

                else :
                    print(file_lst[0])
                    img = cv2.imread('./new_home/output/'+str(file_lst.pop(0))+'.jpg',0)
                    row_img[:,-fixing_ovrlp_win:] = np.where(img[:,0:fixing_ovrlp_win]>bin_thresh, 255, row_img[:,-fixing_ovrlp_win:])
                    row_img = np.concatenate((row_img,img[:,-fixing_ovrlp_win:]),axis=1)
                    #print(row_img.shape)
                    #print(asd
                counter += 1
            row_img = np.concatenate((row_img,np.zeros((constant,tif_width-j))),axis=1)
            #print(row_img.shape)
            #cv2.imwrite('./data/dhanmondi/temp.jpg',row_img)
            #print(asd)
            i += ((window_step) - 1)
            row_count +=1
            if row_flag == True :
                vert_img = row_img
                #i += ((window_step) - 1)
                row_flag = False
                #print('hwll')
                cv2.imwrite('./data/dhanmondi/temp.jpg',vert_img)
                continue
            #print(row_flag)
            if row_flag == False :
                vert_img[-fixing_ovrlp_win:,:] = np.where(row_img[0:fixing_ovrlp_win,:]>bin_thresh, 255, vert_img[-fixing_ovrlp_win:,:])
                vert_img = np.concatenate((vert_img,row_img[fixing_ovrlp_win:,:]),axis=0)
                cv2.imwrite('./data/dhanmondi/merged_0.jpg', vert_img)
                #print(asd)

        i += 1
    
    #vert_img = np.concatenate((np.zeros((top_blank,tif_width)),vert_img),axis=0)
    #vert_img = np.concatenate((vert_img, np.zeros((bottom_blank,tif_width))),axis=0)

    cv2.imwrite('./data/dhanmondi/merged_0.jpg', vert_img)




if __name__ == "__main__":
    #mrg_dhan_msk()
    img = cv2.imread('./data/dhanmondi/merged_0.jpg',0)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #shutil.copy('/media/antor/Transcend/drone/data/dhanmondi/100MEDIA/'+list_img[i],'/media/antor/Transcend/temp/')
    #wrt_geo_viz()
    #coor_to_geojson()
    #merge_msk()
    #img_crop_prctg()
    #crop_train()
    #labelbox_to_mskrcnn()
    pass

