import cv2
import numpy as np
import os
import sys
import tensorflow as tf


from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4

images = []
labels = []

directory = 'gtsrb'

for folder in os.listdir(directory):
	if folder == '.DS_Store':
		continue
	for file in os.listdir(os.path.join(directory, folder)):
		images.append(cv2.imread(os.path.join(directory, folder, file)))
		labels.append(int(folder))
w = [i.shape[0] for i in images]
l = [i.shape[1] for i in images]
print(sum(w)/len(w))
print(sum(l)/len(l))




'''

print(images[0])
print(type(images[0]))
print(images[0].shape)
print(labels[0])


image = cv2.imread(os.path.join(path, *paths)"/gtsrb/0/00000_00000.ppm")
print(image)
print(type(image))



    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

'''