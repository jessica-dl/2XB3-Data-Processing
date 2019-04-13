##  @file faceDetector.py
#   @author Jeff Gibson
#   @brief module which handles the processing and uploading of images to the cloud bucket
#   @date 2019/03/12
import cv2
import sys
import numpy as np
import os
import csv
import requests
from google.cloud import storage
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep


def send_post(age, img_url):
    """
    sends a post request to the cloud based SQL database.
    :param age: is the age of the current subject being uploaded
    :param img_url: is the url which will be stored in the cloud bucket
        so that the image can be retreived during training.

    """
    
    cloud_url = 'https://us-central1-cs-2xb3.cloudfunctions.net/function-2'
    file = {'age': age, 'url': img_url}
    r = requests.post(url=cloud_url, data=file)

    paste_url = r.text
    print(paste_url)


def upload_to_bucket(file_name):
    """
    uploads the image to the google cloud bucket
    :param file_name: is the name of the file to be uploaded

    """

    bucket_url = 'https://console.cloud.google.com/storage/browser/cs2xb3_images'
    """credentials_dict = {
    'type': 'service_account',
    'client_id': os.environ['BACKUP_CLIENT_ID'],
    'client_email': os.environ['BACKUP_CLIENT_EMAIL'],
    'private_key_id': os.environ['BACKUP_PRIVATE_KEY_ID'],
    'private_key': os.environ['BACKUP_PRIVATE_KEY'],
    }
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        credentials_dict
    )"""
    credential_path = 'D:\\imdb_crop\\CS 2XB3-432908677e3a.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
    client = storage.Client()
    bucket = client.get_bucket('cs2xb3_images')
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)

def process_images():
    """
    processes the locally stored images, ensuring that a single face is detected,
    that the image is of size 64x64, and that the face occupies 50% or more of the total
    image size.

    """
    image_list = []
    for i in range (0,10):
        directory = 'D:\\imdb_crop\\imdb_crop\\0' + str(i)
        for filename in os.listdir(directory):

            imagePath = directory + '\\' + filename
            cascPath = sys.argv[1]

            faceCascade = cv2.CascadeClassifier(cascPath)
            faceCascade.load('D:\\haarcascade_frontalface_default.xml')

            image = cv2.imread(imagePath)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize=(30, 30),
                flags = cv2.CASCADE_SCALE_IMAGE
            )

            padding = 20

            print("Found {0} faces!".format(len(faces)))
            if (len(faces) == 1):
                for (x, y, w, h) in faces:
                    cv2.rectangle(image, (x-padding, y-padding), (x + w + padding, y + h + padding), (0, 255, 0), 2)
                    sub_face = image[y:y+h, x:x+w]
                    resize_image = cv2.resize(sub_face, (64,64))
                if ((((y + h) - y) > 64) and ((x + w) - x) > 64):
                #Check if sub_face size is greater than 150x150, if this is true place the filename in the list
                    try:
                        age = int(filename.split('_')[-1][:4]) - int(filename.split('_')[-2][:4])
                    except:
                        pass
                    finally:
                        cv2.imwrite('D:\\new_images\\' + filename, resize_image)
                        image_list.append('D:\\new_images\\' + filename)
                        cv2.waitKey(0)

    for i in range (10,100):
        directory = 'D:\\imdb_crop\\imdb_crop\\' + str(i)

        for filename in os.listdir(directory):

            imagePath = directory + '\\' + filename
            cascPath = sys.argv[1]

            faceCascade = cv2.CascadeClassifier(cascPath)
            faceCascade.load('D:\\haarcascade_frontalface_default.xml')

            image = cv2.imread(imagePath)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize=(30, 30),
                flags = cv2.CASCADE_SCALE_IMAGE
            )

            padding = 20

            print("Found {0} faces!".format(len(faces)))
            if (len(faces) == 1):
                for (x, y, w, h) in faces:
                    cv2.rectangle(image, (x-padding, y-padding), (x + w + padding, y + h + padding), (0, 255, 0), 2)
                    sub_face = image[y:y+h, x:x+w]
                    resize_image = cv2.resize(sub_face, (64,64))
                #Check if sub_face size is greater than 150x150 if true place filename in list
                if ((((y + h) - y) > 64) and ((x + w) - x) > 64):
                    try:
                        age = int(filename.split('_')[-1][:4]) - int(filename.split('_')[-2][:4])
                    except:
                        pass
                    finally:
                        cv2.imwrite('D:\\new_images\\' + filename, resize_image)
                        image_list.append('D:\\new_images\\' + filename)
                        cv2.waitKey(0)


def upload_stuff():
    """
    iterates through the locally stored files and calls send_post
    and upload_to_bucket to perform their respective functions.
    """
    directory = 'D:\\new_images'
    for filename in os.listdir(directory):
        try:
            upload_to_bucket(directory + filename)
            age = int(filename.split('_')[-1][:4]) - int(filename.split('_')[-2][:4])
            send_post(age, directory)
        except:
            pass

#process_images()
upload_stuff()