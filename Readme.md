# 2XB3-Data-Processing

## faceDetector.py Usage

This module will iterate through a directory of images, detecting faces. If a single face is detected,
the size of the image is at least 64x64, and the detected face occupies at least 50% of the total image
size, then that image will be added to a new directory called new_images.

`python faceDetector.py <directory_name>`

## create_database.py Usage

This module will package all images in a directory into hdf5 file format so that it can be easily accessed
for training. It will then output a file called images_ages.hdf5 in the current directory, which contains the
one-hot encoded age information as well as the images.

`python create_database.py <directory_name>`
