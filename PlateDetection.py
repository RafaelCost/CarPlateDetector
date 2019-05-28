#!/usr/bin/env python
# coding: utf-8

# In[4]:


from skimage.io import imread
from skimage.filters import threshold_otsu
from skimage import measure
from skimage.measure import regionprops
from skimage.transform import resize
from skimage import measure
from skimage.measure import regionprops
from skimage.io import imread
from skimage.filters import threshold_otsu
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.externals import joblib

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import cv2
import imutils
import numpy as np
import matplotlib.patches as patches
import os
import pickle


# In[5]:


def plateIdentification(image):
    label_image = measure.label(image)

    plate_dimensions = (0.03*label_image.shape[0], 0.08*label_image.shape[0], 0.15*label_image.shape[1], 0.3*label_image.shape[1])
    plate_dimensions2 = (0.08*label_image.shape[0], 0.2*label_image.shape[0], 0.15*label_image.shape[1], 0.4*label_image.shape[1])
    min_height, max_height, min_width, max_width = plate_dimensions
    plate_objects_cordinates = []
    plate_like_objects = []

    flag = 0
    for region in regionprops(label_image):
        if region.area < 50:
            continue
        min_row, min_col, max_row, max_col = region.bbox
        region_height = max_row - min_row
        region_width = max_col - min_col

        if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
            print('in')
            flag = 1
            plate_like_objects.append(image[min_row:max_row,
                                      min_col:max_col])
            plate_objects_cordinates.append((min_row, min_col,
                                             max_row, max_col))
    if flag == 0:
        min_height, max_height, min_width, max_width = plate_dimensions2
        plate_objects_cordinates = []
        plate_like_objects = []

        for region in regionprops(label_image):
            if region.area < 50:
                continue
            min_row, min_col, max_row, max_col = region.bbox
            region_height = max_row - min_row
            region_width = max_col - min_col
            if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
                plate_like_objects.append(image[min_row:max_row,
                                          min_col:max_col])
                plate_objects_cordinates.append((min_row, min_col,
                                                 max_row, max_col))
    return plate_like_objects, plate_objects_cordinates


# In[23]:


def caractersSegmentation(plate_like_objects):
    license_plate = np.invert(plate_like_objects[0])
    labelled_plate = measure.label(license_plate)
    fig, ax3 = plt.subplots(1)
    ax3.imshow(license_plate, cmap="gray")

    character_dimensions = (0.35*license_plate.shape[0], 0.60*license_plate.shape[0], 0.05*license_plate.shape[1], 0.15*license_plate.shape[1])
    min_height, max_height, min_width, max_width = character_dimensions

    characters = []
    counter=0
    column_list = []
    for regions in regionprops(labelled_plate):
        y0, x0, y1, x1 = regions.bbox
        region_height = y1 - y0
        region_width = x1 - x0

        if region_height > min_height and region_height < max_height and region_width > min_width and region_width < max_width:
            roi = license_plate[y0:y1, x0:x1]
            resized_char = resize(roi, (20, 20))
            #if counter!=0:
            characters.append(resized_char)
            counter+=1
            column_list.append(x0)
    return characters


# In[7]:


def plateSegmentation(car_image):
    car_image = imutils.rotate(car_image, 270)
    print(car_image.shape)

    gray_car_image = car_image * 255

    threshold_value = threshold_otsu(gray_car_image)
    binary_car_image = gray_car_image > threshold_value

    plate_like_objects, plate_objects_cordinates = plateIdentification(binary_car_image)

    return caractersSegmentation(plate_like_objects)


# In[8]:


letters = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D',
            'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z'
        ]

def read_training_data(training_directory):
    image_data = []
    target_data = []
    for each_letter in letters:
        for each in range(10):
            image_path = os.path.join(training_directory, each_letter, each_letter + '_' + str(each) + '.jpg')
            img_details = imread(image_path, as_grey=True)
            binary_image = img_details < threshold_otsu(img_details)
            flat_bin_image = binary_image.reshape(-1)
            image_data.append(flat_bin_image)
            target_data.append(each_letter)
    return (np.array(image_data), np.array(target_data))


# In[9]:


def cross_validation(model, num_of_fold, train_data, train_label):
    accuracy_result = cross_val_score(model, train_data, train_label,
                                      cv=num_of_fold)
    print("Cross Validation Result for ", str(num_of_fold), " -fold")

    print(accuracy_result * 100)


# In[10]:


def train():
    print('reading data')
    training_dataset_dir = 'C:/Users/UFC/Documents/APODI/Detecção de placas/train20X20'
    image_data, target_data = read_training_data(training_dataset_dir)
    print('reading data completed')

    svc_model = SVC(kernel='linear', probability=True)
    cross_validation(svc_model, 4, image_data, target_data)
    print('training model')
    svc_model.fit(image_data, target_data)

    print("model trained.saving model..")
    filename = 'C:/Users/UFC/Documents/APODI/Detecção de placas/finalized_model.sav'
    pickle.dump(svc_model, open(filename, 'wb'))
    print("model saved")


# In[13]:


def predict_carac(characters):
    filename = 'finalized_model.sav'
    model = pickle.load(open(filename, 'rb'))
    classification_result = []
    for each_character in characters:
        each_character = each_character.reshape(1, -1);
        result = model.predict(each_character)
        classification_result.append(result)

    plate_string = ''
    for eachPredict in classification_result:
        plate_string += eachPredict[0]
    return plate_string


# In[26]:


def predict_car_plate(path_name):
    characters = plateSegmentation(imread(path_name, as_gray=True))
    plate = predict_carac(characters)
    return plate



# In[ ]:
