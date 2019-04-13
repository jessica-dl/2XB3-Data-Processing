import h5py
from numpy import array
from numpy import stack
import os
import cv2

directory = 'D:\\new_images'

def set_data(num_samples, age_array):
    """
    writes the image and age data to the hdf5 file format
    :param num_samples: is the number of images
    :param age_array: is the sequence of age categories, corresponding to
    their respective images
    """
    with h5py.File('images_ages.hdf5', 'r+') as f1:
        count = 0
        for filename in os.listdir(directory):
            img = cv2.imread(directory + '\\' + filename)
            dimensions = img.shape
            f1['x'][count, ...] = img
            f1['y'][count] = age_array[count]
            count += 1

def initialize_datasets(num_samples, age_array):
    """
    initializes two datasets in an hdf5 file which will
    store images and image metadata
    :param num_samples: is the number of images
    :param age_array: is the sequence of age categories, corresponding to
    their respective images
    """
    with h5py.File('images_ages.hdf5', 'w') as f1:
        dset1 = f1.create_dataset('x', (num_samples, 64, 64, 3), dtype='i')
        dset2 = f1.create_dataset('y', (num_samples, 6), dtype='i')

    set_data(num_samples, age_array)

def go_through_images():
    """
    iterates through the locally stored images, counts the number of images
    and places each image into an age category
    """
    age_array = array(6*[0])
    num_samples = 0
    age_list = []
    print("we got here")
    for filename in os.listdir(directory):
        age_array = array(6*[0])
        try:
            age = int(filename.split('_')[-1][:4]) - int(filename.split('_')[-2][:4])
            if 0 < age < 18:
                age_array[0] = 1
            elif 19 < age < 29:
                age_array[1] = 1
            elif 30 < age < 39:
                age_array[2] = 1
            elif 40 < age < 49:
                age_array[3] = 1
            elif 50 < age < 59:
                age_array[4] = 1
            else:
                age_array[5] = 1
            age_list.append(age_array)
            num_samples += 1
        except Exception as e:
            print(e)
            pass
    
    age_array = array(age_list)
    age_array = stack(age_array, axis = 0)
    print(age_array.shape)

    initialize_datasets(num_samples, age_array)

go_through_images()

