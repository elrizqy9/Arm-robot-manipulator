import cv2 as cv 
import numpy as np
import math
# inisialisasi variabel distance
KNOWN_DISTANCE = 11.6 #INCHES
MATANG_WIDTH = 1.5 #INCHES
MENTAH_WIDTH = 1.525 #INCHES
BUSUK_WIDTH  = 1.65 #INCHES

# Object detector konstan 
CONFIDENCE_THRESHOLD = 0.4
NMS_THRESHOLD = 0.3 # non maximum supression
# memilih suatu ensita yang tumpang tindih, misal BB (probabilitas)

# colors for object detected
COLORS = [(255,0,0),(255,0,255),(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
GREEN =(0,255,0)
BLACK =(0,0,0)
RED = (22,25,204)
BLUE = (84,42,31)
# defining fonts 
FONTS = cv.FONT_HERSHEY_COMPLEX

# getting class names from classes.txt f===ile 
classfile = (r'E:\tutu\coco.names')
class_names = []
with open(classfile, "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

#  setttng up opencv net
modelConfiguration = r"E:\tutu\yolov4-tiny-custom.cfg"
modelWeights = r"E:\tutu\yolov4-tiny-custom_last.weights"

yoloNet = cv.dnn.readNet(modelConfiguration, modelWeights)

yoloNet.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
yoloNet.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)

model = cv.dnn_DetectionModel(yoloNet)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)



class detect():
    def __init__(self) -> None:
        pass
    # object detector funciton /method
    def object_detector(self,image):
        classes, scores, boxes = model.detect(image, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        # membuat empty list untuk menambah object ata
        # .shap = tupple/ array ( isinya lebih darisatu)
        height, width, channels = image.shape
        data_list =[]
        for (classid, score, box) in zip(classes, scores, boxes):
            # zip = misal item pertama pada setiap operato ipasangkan satu sama lain dst
            # define color of each, object based on its class id 
            color= COLORS[int(classid) % len(COLORS)]
        
            label = "%s : %f" % (class_names[classid[0]], score)

            # draw rectangle on and label on object
            # harus integer
            center_x=int( box[0] + box[2]/2)
            center_y= int(box[1] + box[3]/2) 
            cv.rectangle(image, box, color, 2)
            cv.putText(image, label, (box[0], box[1]-14), FONTS, 0.5, color, 2)
                
            # getting the data 
            # 1: class name  2: object width in pixels, 3: position where have to draw text(distance)
            # nambah variabel list 3 -5
            if classid ==0: # MATANG class id 
                data_list.append([class_names[classid[0]], box[2], (box[0], box[1]-2),str(center_x),str(center_y),str(width),str(height)])
            elif classid ==1:# MENTAH
                data_list.append([class_names[classid[0]], box[2], (box[0], box[1]-2),str(center_x),str(center_y),str(width),str(height)])
            elif classid ==2: #BUSUK
                data_list.append([class_names[classid[0]], box[2], (box[0], box[1]-2),str(center_x),str(center_y),str(width),str(height)])
            else:
                data_list.append([class_names[classid[0]], box[2], (box[0], box[1]-2),str(center_x),str(center_y),str(width),str(height)])
            #print(data_list)
            # if you want inclulde more classes then you have to simply add more [elif] statements here
            # returning list containing the object data. 
            
     
        return data_list
    

    def focal_length_finder (self,measured_distance, real_width, width_in_rf):
        focal_length = (width_in_rf * measured_distance) / real_width
        return focal_length

    # distance finder function 
    def distance_finder(self,focal_length, real_object_width, width_in_frmae):
        distance = (real_object_width * focal_length) / width_in_frmae
        return distance



