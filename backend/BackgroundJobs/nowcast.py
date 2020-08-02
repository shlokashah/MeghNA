import rasterio
import time
from BackgroundJobs.Step1Mask.step1 import step1
from IsroBackend.models import ImageFileName, ImageMaskDetails, ImageMaskPreds, ImagePredictedCNN, ImagePredictedMPA
from BackgroundJobs.Step1KMeans.step1Kmeans import step1Kmeans
from BackgroundJobs.Step3.CNN_LSTM.step3 import predict_motion as cnnLSTM
from BackgroundJobs.Step3.MPA.step3 import predict_motion as mpaAlgo
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
import cv2 as cv
def saveStep2Output(currentMask,k):
	step2Directory = "BackgroundJobs/Step1Mask/Step2Features/"
	f = open(step2Directory + "step2MaskOutputs.txt","r")
	lines = f.readlines()
	for line in lines:
		print(line[:-1])
		maskFeatures, created = ImageMaskPreds.objects.get_or_create(maskKey=currentMask,maskNumber=k,cloud_type=line)
		if created:
			print("features stored")

def callStep1(step1MaskImageName,currentAlgorithm,step1Directory,currentImage,tifFileName,number):
	t0= time.clock()
	ht0 = time.time()
	print("Hello:", step1MaskImageName)
	if currentAlgorithm == "Mask RCNN":
		step1(step1MaskImageName,step1Directory,tifFileName)
		t1 = time.clock() - t0
		ht1 = time.time() - ht0
		print(ht1)
		f = open(step1Directory + "step1MaskOutputs.txt","r")
		lines = f.readlines()
		for line in lines:
			k,com_x,com_y = line.split(" ")
			print(k,com_x,com_y,"-------------")
			currentMask, maskCreated = ImageMaskDetails.objects.get_or_create(name=currentImage,maskNumber=k,algorithm=currentAlgorithm,com_x=com_x,com_y=com_y,timeTakenCPU=t1,timeTakenHuman=ht1)
			if maskCreated:
				saveStep2Output(currentMask,k)

			print("created",k) if maskCreated else print("already done")
	else:
		output = "BackgroundJobs/Step1KMeans/step1ImageOutputKmeans/"
		step1MaskImageName = "BackgroundJobs/Step1KMeans/step1ImageInputKmeans/" + str(number) + ".png"
		fileName = str(number) + ".png"
		res = step1Kmeans(step1MaskImageName, output, tifFileName,fileName, number)
		t1 = time.clock() - t0
		ht1 = time.time() - ht0
		print(ht1)
		for i in range(len(res)):
			k = res[str(i)]["cloud_no"]
			com_x = res[str(i)]["com_x"]
			com_y = res[str(i)]["com_y"]
			typeCloud = res[str(i)]["type"]
			currentMask, maskCreated = ImageMaskDetails.objects.get_or_create(name=currentImage,maskNumber=k,algorithm=currentAlgorithm,com_x=com_x,com_y=com_y,timeTakenCPU=t1,timeTakenHuman=ht1,cloudType=typeCloud)
			print("created",k) if maskCreated else print("already done")
	# --------------------------------------------------------------
	# print(resultStep1)

def loadImage():
	tifImageNames = ["3DIMG_07NOV2019_0000_L1C_SGP.tif",  "3DIMG_07NOV2019_1000_L1C_SGP.tif","3DIMG_07NOV2019_0030_L1C_SGP.tif",  "3DIMG_07NOV2019_1030_L1C_SGP.tif","3DIMG_07NOV2019_0100_L1C_SGP.tif",  "3DIMG_07NOV2019_1100_L1C_SGP.tif","3DIMG_07NOV2019_0130_L1C_SGP.tif",  "3DIMG_07NOV2019_1130_L1C_SGP.tif","3DIMG_07NOV2019_0200_L1C_SGP.tif",  "3DIMG_07NOV2019_1200_L1C_SGP.tif","3DIMG_07NOV2019_0230_L1C_SGP.tif",  "3DIMG_07NOV2019_1230_L1C_SGP.tif","3DIMG_07NOV2019_0300_L1C_SGP.tif",  "3DIMG_07NOV2019_1300_L1C_SGP.tif","3DIMG_07NOV2019_0330_L1C_SGP.tif",  "3DIMG_07NOV2019_1330_L1C_SGP.tif","3DIMG_07NOV2019_0400_L1C_SGP.tif",  "3DIMG_07NOV2019_1400_L1C_SGP.tif","3DIMG_07NOV2019_0430_L1C_SGP.tif",  "3DIMG_07NOV2019_1430_L1C_SGP.tif","3DIMG_07NOV2019_0500_L1C_SGP.tif",  "3DIMG_07NOV2019_1500_L1C_SGP.tif","3DIMG_07NOV2019_0530_L1C_SGP.tif",  "3DIMG_07NOV2019_1530_L1C_SGP.tif","3DIMG_07NOV2019_0600_L1C_SGP.tif",  "3DIMG_07NOV2019_1600_L1C_SGP.tif","3DIMG_07NOV2019_0630_L1C_SGP.tif",  "3DIMG_07NOV2019_1630_L1C_SGP.tif","3DIMG_07NOV2019_0700_L1C_SGP.tif",  "3DIMG_07NOV2019_2000_L1C_SGP.tif","3DIMG_07NOV2019_0730_L1C_SGP.tif",  "3DIMG_07NOV2019_2030_L1C_SGP.tif","3DIMG_07NOV2019_0800_L1C_SGP.tif",  "3DIMG_07NOV2019_2100_L1C_SGP.tif","3DIMG_07NOV2019_0830_L1C_SGP.tif",  "3DIMG_07NOV2019_2130_L1C_SGP.tif","3DIMG_07NOV2019_0859_L1C_SGP.tif",  "3DIMG_07NOV2019_2200_L1C_SGP.tif","3DIMG_07NOV2019_0900_L1C_SGP.tif",  "3DIMG_07NOV2019_2230_L1C_SGP.tif","3DIMG_07NOV2019_0929_L1C_SGP.tif",  "3DIMG_07NOV2019_2300_L1C_SGP.tif","3DIMG_07NOV2019_0930_L1C_SGP.tif",  "3DIMG_07NOV2019_2330_L1C_SGP.tif","3DIMG_07NOV2019_0959_L1C_SGP.tif"]
	step1Directory = "BackgroundJobs/Step1Mask/"
	# ------------------------------------------------------------------
	# loading the next file
	f = open(step1Directory + "currentImage.txt","r")
	i = f.read()
	fileName = "satellite" + i + ".jpg"
	step1MaskImageName =step1Directory + "step1ImageInput/"+ fileName
	print(i)
	i = int(i)
	i = (int(i) +1)%45
	if i == 0:
		i = 45

	tifFileName = step1Directory +"INSAT3D_TIR1_India/"+ tifImageNames[i-1]
	f.close()
	# increasing the filename by 1 to get the next file in the next iteration
	f = open(step1Directory + "currentImage.txt","w")
	f.write(str(i))
	f.close()
	# ------------------------------------------------------------------
	# create an entry of the file if it does not exist

	# which algorithm is used?
	detectionAlgorithm = ["K-Means", "Mask RCNN"]
	currentDetectionAlgorithm = detectionAlgorithm[0]

	motionAlgorithm = ["CNN_LSTM", "MPA"]
	currentMotionAlgorithm = motionAlgorithm[1]
	
	currentImage, _ = ImageFileName.objects.get_or_create(name=fileName)
	# ------------------------------------------------------------------
	callStep1(step1MaskImageName,currentDetectionAlgorithm,step1Directory,currentImage,tifFileName,i-1)
	# if currentMotionAlgorithm == "CNN_LSTM":
	# 	print("Mask of ",(i-1)," has been generated")
	# 	gif_path, predictionModel = cnnLSTM(i-1,currentImage)
	# 	print(gif_path)
	# elif currentMotionAlgorithm == "MPA":
	# 	mpaAlgo(i-1,currentImage)
	# 	print("MPA done")

def tif_to_png(image_folder, timestamp):
	sat_data = rasterio.open(image_folder + timestamp + '.tif')
	image = sat_data.read(1)

	# Save tif file as png
	#cv2.imwrite(output_folder + timestamp + '.png', image)
	return image

def updateDetails():
	loadImage()

	print("End of the batch")