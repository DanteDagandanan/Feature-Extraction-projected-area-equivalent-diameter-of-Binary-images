#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 09:39:00 2023

@author: engrimmanuel

"""
import cv2 as cv
import numpy as np
from skimage import measure
import glob
import pandas as pd
from natsort import natsorted
import os


imageList=natsorted(glob.glob("/addfilelocationhere/mask images/*.*"))
#"crop image_1/*.*

list_images=[]
list_fillholl=[]
value_extracted=[]
samp_file=[]
large_area=[]


path = "/home/engrimmanuel/Desktop/jackfruit task image regression task /machine learning, extract the binary images and remove background and extract the features such as area minimum and maximum axis/mask images/*.png"
output_file=open("all features extraction from image 1 to 83.csv","a")







propList=['ImageFileName','area','feret_diameter_max','eccentricity','equivalent_diameter',
          'major_axis_length','minor_axis_length','perimeter','perimeter_crofton',
          'bbox_area','convex_area', 
          'euler_number','solidity','extent', 'filled_area', 'local_centroid',
          'orientation',
          'centroid']

          #'major_axis_length','minor_axis_length','moments','moments_normalized','perimeter','perimeter_crofton']
              
                         
              
output_file.write(("\n"+"," + ",".join(propList)+"\n"))
element_imageList=0



for file in imageList :   #Iterate through each file in the list using for

    #print(file)
    #read each image files
    thresholed= cv.imread(file)
    #save the list of image in a list
    #list_images.append(thresholed)  #Create a list of images (not just file names but full images)
    #convert the images in a gray scale
    img1=cv.cvtColor(thresholed, cv.COLOR_BGR2GRAY)
    #auto threshold the image using the otsu
    ret,mask=cv.threshold(img1,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
    ret,mask=cv.threshold(mask,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
    #copy the threshoded images
    to_fill=mask.copy()
    #extract the value of shape
    hight, width = mask.shape[:2]
    #make a image that contain zero value
    mask2=np.zeros((hight+2, width+2), np.uint8)
    
    cv.floodFill(to_fill, mask2, (0,0), 255);
    im_floodfill_inv = cv.bitwise_not(to_fill)
    im_out = mask | im_floodfill_inv
    #cv.imshow("fill",im_floodfill_inv)
    #cv.imwrite(str(file)+"_fill-in.png",to_fill)
    #cv.imwrite(str(file)+"_im_out.png",im_out)
    #cv.imwrite(str(file)+"_im_floodfill_inv.png",im_floodfill_inv)
    #cv.imshow("mask2",mask2)
    #cv.imshow("im_floodfill_inv",im_floodfill_inv)
    #cv.imshow("im_out",im_out)
    #save the image in the list
    list_fillholl.append(im_out)
    ###########################################
   #extract the properties
    clusters= measure.regionprops(im_out)
    
    samp_file=file
    
    output_file=open("all features extraction from image 1 to 83.csv","a")

    
    for cluster_props in clusters:
        #output cluster properties to the excel file
        #output_file.write(str(cluster_props['Label']))
        
        for i,prop in enumerate(propList):
            
            if(prop == 'ImageFileName'): 
                while element_imageList<len(imageList):
                #for img_file in imageList:
                    to_print=str(os.path.basename(imageList[element_imageList]))
                    element_imageList=element_imageList+1
                    break
            else:
                to_print = cluster_props[prop]
            output_file.write(',' + str(to_print))
        output_file.write('\n')
    output_file.close()
                    


'''
'ImageFileName','Area','MinorAxisLength','MajorAxisLength',
          'equivalent_diameter','orientation','ConvexArea','ConvexImage','Eccentricity',
          'EulerNumber','FeretDiameter','FeretDiameterMax','HuMoments','InertiaTensor',
          'InertiaTensorEigvals','LocalCentroid','Moments','NormalizedMoments','Orientation',
          'Perimeter','CroftonPerimeter','Slice','WeightedCentralMoments','weighted_moments_central',
          'WeightedCentroid','weighted_centroid','WeightedHuMoments','weighted_moments_hu',
          'WeightedLocalCentroid','weighted_local_centroid','WeightedMoments','weighted_moments',
          'WeightedNormalizedMoments','weighted_moments_normalized'


df=pd.read_csv("coin area.csv")
#df=df.rename(columns={'Unnamed: 0':"image file name"})
df=df.drop('label',axis=1)
#df1=pd.DataFrame(df,columns=['file imgae','Area','orientation','MinorAxisLength','MajorAxisLength','equivalent_diameter'])
print(df)


img=cv.imread("images/sample nanka_sample 1_picture 3.png")
img1=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#img=cv.resize(img,(600,800))
ret,mask=cv.threshold(img1,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)

#cv.imshow("img",img)
#cv.imshow("img_d",mask)

#copy the thresholded image
to_fill=mask.copy()

h, w = mask.shape[:2]
mask2=np.zeros((h+2, w+2), np.uint8)
cv.floodFill(to_fill, mask2, (0,0), 255);
im_floodfill_inv = cv.bitwise_not(to_fill)

im_out = mask | im_floodfill_inv

cv.imshow("im_out-d",im_out)
#cv.imshow("mask2",mask2)
#cv.imshow("im_floodfill_inv",im_floodfill_inv)

##############################################

clusters= measure.regionprops(im_out)
propList=['label','Area','MinorAxisLength','MajorAxisLength','equivalent_diameter','orientation']

output_file=open("coin area.csv","w")
output_file.write(("," + ",".join(propList)+"\n"))

for cluster_props in clusters:
    #output cluster properties to the excel file
    output_file.write(str(cluster_props['Label']))
    for i,prop in enumerate(propList):
        if(prop == 'Area'): 
            to_print = cluster_props[prop]   #Convert pixel square to um square
        elif(prop == 'orientation'): 
            to_print = cluster_props[prop]*57.2958  #Convert to degrees from radians
        
        elif(prop == 'MinorAxisLength'): 
            to_print = cluster_props[prop]
        elif(prop == 'MajorAxisLength'): 
            to_print = cluster_props[prop]
        elif(prop == 'equivalent_diameter'): 
            to_print = cluster_props[prop]
        
        else: 
            to_print = cluster_props[prop]     #Reamining props, basically the ones with Intensity in its name
        output_file.write(',' + str(to_print))
    output_file.write('\n')
output_file.close()   #Closes the file, otherwise it would be read only. 


################################################


cv.waitKey(0)
cv.destroyAllWindows()'''

