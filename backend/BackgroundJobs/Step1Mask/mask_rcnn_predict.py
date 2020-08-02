import os
from mrcnn.config import Config
from mrcnn import model as modellib
from mrcnn import visualize
import numpy as np
import colorsys
import argparse
import imutils
import random
import cv2
import matplotlib.pyplot as plt
from collections import defaultdict
from Step2Features.step2 import classify

ap = argparse.ArgumentParser()
ap.add_argument("-w", "--weights", required=True,
	help="path to Mask R-CNN model weights")
ap.add_argument("-l", "--labels", required=True,
	help="path to class labels file")
ap.add_argument("-i", "--image", required=True,
	help="path to input image to apply Mask R-CNN to")
ap.add_argument("-ti", "--tifName", required=True,
	help="path to input image to apply Mask R-CNN to")
args = vars(ap.parse_args())

CLASS_NAMES = open(args["labels"]).read().strip().split("\n")

hsv = [(i / len(CLASS_NAMES), 1, 1.0) for i in range(len(CLASS_NAMES))]
COLORS = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
random.seed(42)
random.shuffle(COLORS)

class SimpleConfig(Config):
	NAME = "coco_inference"
	GPU_COUNT = 1
	IMAGES_PER_GPU = 1
	NUM_CLASSES = len(CLASS_NAMES)

config = SimpleConfig()

print("[INFO] loading Mask R-CNN model...")
model = modellib.MaskRCNN(mode="inference", config=config,
	model_dir=os.getcwd())
model.load_weights(args["weights"], by_name=True)


image = cv2.imread(args["image"])
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = imutils.resize(image, width=512)


print("[INFO] making predictions with Mask R-CNN...")
r = model.detect([image], verbose=1)[0]

cloud_coordinates = {}
for i in range(0, r["rois"].shape[0]):
	classID = r["class_ids"][i]
	mask = r["masks"][:, :, i]
	color = COLORS[classID][::-1]
	coordinates = np.where(mask == True)
	x = coordinates[1]
	y = coordinates[0]
	cloud_coordinates[str(i)] = {'x':x,'y':y}
	image = visualize.apply_mask(image, mask, color, alpha=0.5)
	# print(image)

image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
# print(r['scores'])
count = 0
for i in range(0, len(r["scores"])):
	(startY, startX, endY, endX) = r["rois"][i]
	classID = r["class_ids"][i]
	label = CLASS_NAMES[classID]
	score = r["scores"][i]
	color = [int(c) for c in np.array(COLORS[classID]) * 255]
	cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
	text = "{}:{:}: {:.3f}".format(label,count, score)
	y = startY - 10 if startY - 10 > 10 else startY + 10
	cv2.putText(image, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX,0.6, color,2)
	count = count + 1
	# print("hey")

com = defaultdict(list)
step1Directory = "BackgroundJobs/Step1Mask/"
f = open(step1Directory + "step1MaskOutputs.txt","w")
for i in range(r['rois'].shape[0]):
	l = (r['rois'][i].tolist())
	x = (l[1]+l[3])/2
	y = (l[0]+l[2])/2
	f.write(str(i+1)+" " +str(x)+" "+str(y) +"\n")
	com[i].append(x)
	com[i].append(y)
f.close()
print(r['rois'])
print(r['masks'])
print("--------------------------------------------------",com)


f = open("BackgroundJobs/Step1Mask/currentImage.txt","r")
i = f.read()
i = int(i) 	
print(i)
f.close()
plt.imshow(image, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.savefig("BackgroundJobs/Step1Mask/step1ImageOutput/satellite"+str(i)+".jpg", bbox_inches='tight')
print("Mask Image saved to :- BackgroundJobs/Step1Mask/step1ImageOutput/satellite"+str(i)+".jpg")