from IsroBackend.models import ImagePredictedMPA, ImageMaskDetails
import math

def predict_motion(t,currentImage):
	# t-2
	t = int(t)
	print(t)
	com1 = {}
	for i in range(0,3):
		curr = "satellite" + str(t-2) + ".jpg"
		print("a",i,curr)
		currMask = ImageMaskDetails.objects.get(name__name=curr,maskNumber=float(i))
		# print(currMask.maskNumber)
		com1[i] = [currMask.com_x, currMask.com_y]
	# t-1
	com2 = {}
	for i in range(0,3):
		print("b",i)
		curr = "satellite" + str(t-1) + ".jpg"
		currMask = ImageMaskDetails.objects.get(name__name=curr,maskNumber=float(i))
		# print(currMask.maskNumber)
		com2[i] = [currMask.com_x, currMask.com_y]
	# t
	com3 = {}
	for i in range(0,3):
		curr = "satellite" + str(t) + ".jpg"
		currMask = ImageMaskDetails.objects.get(name__name=curr,maskNumber=float(i))
		# print(currMask.maskNumber)
		com3[i] = [currMask.com_x, currMask.com_y]
	# t+1
	com4 = {}
	for i in range(0,3):
		curr = "satellite" + str(t+1) + ".jpg"
		currMask = ImageMaskDetails.objects.get(name__name=curr,maskNumber=float(i))
		# print(currMask.maskNumber)
		com4[i] = [currMask.com_x, currMask.com_y]
	print(com1,com2,com3,com4)
	predicted = {}
	error = {}
	for cloud_index in range(0, 3):
		x1 = com1[cloud_index][0]
		y1 = com1[cloud_index][1]

		x2 = com2[cloud_index][0]
		y2 = com2[cloud_index][1]

		x3 = com3[cloud_index][0]
		y3 = com3[cloud_index][1]

		x4 = com4[cloud_index][0]
		y4 = com4[cloud_index][1]

		x = (x1 + x2) / 2
		y = (y1 + y2) / 2

		predicted_x4 = ((x + x3) / 2) + (x3 - x)
		predicted_y4 = ((y + y3) / 2) + (y3 - y)

		predicted[cloud_index] = [predicted_x4, predicted_y4]

		error[cloud_index] = round(math.sqrt(pow(abs(predicted_x4 - x4), 2) + pow(abs(predicted_y4 - y4), 2)), 2)
		predictionModel = ImagePredictedMPA.objects.get_or_create(name=currentImage, predictionOf=cloud_index+1, pred_com_x=predicted_x4, pred_com_y=predicted_y4,error=error[cloud_index])


	print("Actual COM at t + 1: ", com4)
	print("Predicted COM at t + 1: ", predicted)
	print("Error: ", error)
	# return predictionModel