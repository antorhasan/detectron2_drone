import torch, torchvision
import json
from os import listdir
from os.path import isfile, join

# You may need to restart your runtime prior to this, to let your installation take effect
# Some basic setup
# Setup detectron2 logger

import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import cv2
import random
#from google.colab.patches import cv2_imshow

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

import os
import numpy as np
import json
from detectron2.structures import BoxMode

def get_building_dicts(img_dir):
    json_file = os.path.join(img_dir, "via_region_data.json")

    #if img_dir!="new_home/val" :
    with open(json_file) as f:
        imgs_anns = json.load(f)

    dataset_dicts = []
    #if img_dir!="new_home/val" :
    for idx, v in enumerate(imgs_anns.values()):
        record = {}
        
        filename = os.path.join(img_dir, v["filename"])
        height, width = cv2.imread(filename).shape[:2]
        
        record["file_name"] = filename
        record["image_id"] = idx
        record["height"] = height
        record["width"] = width
    
        annos = v["regions"]
        objs = []
        for _, anno in annos.items():
            assert not anno["region_attributes"]
            anno = anno["shape_attributes"]
            px = anno["all_points_x"]
            py = anno["all_points_y"]
            poly = [(x + 0.5, y + 0.5) for x, y in zip(px, py)]
            poly = [p for x in poly for p in x]

            obj = {
                "bbox": [np.min(px), np.min(py), np.max(px), np.max(py)],
                "bbox_mode": BoxMode.XYXY_ABS,
                "segmentation": [poly],
                "category_id": 0,
                "iscrowd": 0
            }
            objs.append(obj)
        record["annotations"] = objs
        dataset_dicts.append(record)
    #elif img_dir=="new_home/val" :


    return dataset_dicts


from detectron2.data import DatasetCatalog, MetadataCatalog
for d in ["train", "val"]:
    DatasetCatalog.register("building_" + d, lambda d=d: get_building_dicts("new_home/" + d))
    MetadataCatalog.get("building_" + d).set(thing_classes=["building"])
building_metadata = MetadataCatalog.get("building_train")

dataset_dicts = get_building_dicts("new_home/train")
for d in random.sample(dataset_dicts, 5):
    img = cv2.imread(d["file_name"])
    visualizer = Visualizer(img[:, :, ::-1], metadata=building_metadata, scale=0.5)
    vis = visualizer.draw_dataset_dict(d)
    #cv2_imshow(vis.get_image()[:, :, ::-1])
    """ cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',vis.get_image()[:, :, ::-1])
    cv2.waitKey(0)
    cv2.destroyAllWindows() """
    #print(d["file_name"])
    #cv2.imwrite('./new_home/viz_train/'+d["file_name"].split('/')[2],vis.get_image()[:, :, ::-1])
    #print(asd)
#print(asd)
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg

cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.DATASETS.TRAIN = ("building_train",)
cfg.DATASETS.TEST = ()
cfg.DATALOADER.NUM_WORKERS = 2
cfg.MODEL.WEIGHTS = "detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl"  # Let training initialize from model zoo
cfg.SOLVER.IMS_PER_BATCH = 2
cfg.SOLVER.BASE_LR = 0.00025  # pick a good LR
cfg.SOLVER.MAX_ITER = 500   # 300 iterations seems good enough for this toy dataset; you may need to train longer for a practical dataset
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128   # faster, and good enough for this toy dataset (default: 512)
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  # only has one class (ballon)

os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
trainer = DefaultTrainer(cfg) 
trainer.resume_or_load(resume=False)
trainer.train()

# Look at training curves in tensorboard:
#%load_ext tensorboard
#%tensorboard --logdir output

cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.95   # set the testing threshold for this model
cfg.DATASETS.TEST = ("building_val", )
predictor = DefaultPredictor(cfg)

from detectron2.utils.visualizer import ColorMode
#dataset_dicts = get_building_dicts("new_home/val")

#with open('app.json', 'w') as fp:
#    json.dump(outputs, fp)
file1 = open("myfile.txt","w") 
dataset_dicts = [f for f in listdir("new_home/val") if isfile(join("new_home/val",f))]
print(dataset_dicts)
count = 0
for d in dataset_dicts:
    temp_list = []
    #im = cv2.imread(d["file_name"])
    im = cv2.imread("./new_home/val/"+d)
    outputs = predictor(im)
    val_dic = np.asarray(outputs["instances"].pred_masks.cpu(), dtype=np.uint8)
    val_dic = np.where(val_dic!=0,255,0)
    #print(val_dic,val_dic.shape)
    for i in range(val_dic.shape[0]):
        #cv2.imwrite('./new_home/output/'+d["file_name"].split('/')[2].split('.')[0]+'_'+str(i)+'.png', val_dic[i,:,:])
        #cv2.imwrite('./new_home/output/'+str(count)+'.png', val_dic[i,:,:])
        temp_list.append(val_dic[i,:,:])
        count+=1

    temp_list = np.asarray(temp_list)
    print(temp_list.shape)
    bin_mask = temp_list[0,:,:]
    print(bin_mask.shape)
    if temp_list.shape[0] > 1:
        for i in range(temp_list.shape[0]-1):
            bin_mask = np.where(temp_list[i+1,:,:]==255, 255, bin_mask)

    bin_mask = np.asarray(bin_mask, dtype=np.uint8)
    print(d["file_name"].split('/')[2])
    cv2.imwrite('./new_home/output/'+d["file_name"].split('/')[2], bin_mask)

    v = Visualizer(im[:, :, ::-1],
                metadata=building_metadata, 
                scale=0.8, 
                instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels
    )
    v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    #cv2_imshow(v.get_image()[:, :, ::-1])
    """ cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',v.get_image()[:, :, ::-1])
    cv2.waitKey(0)
    cv2.destroyAllWindows() """
    #cv2.imwrite('./new_home/viz_val/'+d["file_name"].split('/')[2],v.get_image()[:, :, ::-1])
    cv2.imwrite('./new_home/viz_val/'+d,v.get_image()[:, :, ::-1])
    file1.write(str(outputs)) 
    #count += 1

file1.close()
    


