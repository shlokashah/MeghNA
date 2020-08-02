import cv2
from skimage import measure
import numpy as np
import imageio
from keras.models import load_model
from IsroBackend.models import ImagePredictedCNN


font = cv2.FONT_HERSHEY_SIMPLEX 
org = (50, 50) 
fontScale = 1
color = (255, 0, 0) 
thickness = 1

def get_error(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	s = measure.compare_ssim(imageA, imageB)
	return {"mse": err, "ssim": s}

def make_gif(image_paths, t):
	"""
	Returns a gif of the 4 input images and the next predicted image
	"""
	gif_path = 'BackgroundJobs/Step3/CNN_LSTM/GifOutputs/'+'motion_'+str(t)+'.gif'
	fps = 12
	images = []
	for path in image_paths:
		images.append(imageio.imread(path))

	imageio.mimsave(gif_path, images, duration=1)
	return gif_path

def predict_motion(t,currentImage):
	"""
	This function returns the path where the GIF for current motion
	is saved by the ConvLSTM model.
	:param t: number representing the latest image
	"""
	image_directory = "BackgroundJobs/Step3/CNN_LSTM/step1ImageInput/"
	print("----------------------",t)
	model = load_model('BackgroundJobs/Step3/CNN_LSTM/[3CNN_2LSTM_Sequence_4_Size_150_TIR].h5')
	images = []
	paths = []
	for i in range(t-3,t+2):
	  img = cv2.imread(image_directory +"satellite"+ str(i) + '.jpg',0)
	  img = cv2.resize(img,(150,150),interpolation=cv2.INTER_AREA)
	  images.append(img)
	  if i != t+1:
	    path = 'BackgroundJobs/Step3/CNN_LSTM/ImageOutputs/'+str(i)+'.png'
	    paths.append(path)
	    img = cv2.putText(img, str(i)+'.png', org, font,fontScale, color, thickness, cv2.LINE_AA) 
	    cv2.imwrite(path,img)
	output = model.predict(np.array(images[:-1]).reshape(1,4,150,150,1))
	output = output.reshape(150,150)
	errors = get_error(np.asarray(images[-1]), output)
	path = 'BackgroundJobs/Step3/CNN_LSTM/ImageOutputs/Predicted' + str(t+1) + '.png'
	paths.append(path)
	output = cv2.putText(output, str(t+1)+'.png', org, font,fontScale, color, thickness, cv2.LINE_AA) 
	cv2.imwrite(path,output)
	gif_path = make_gif(paths, t)

	# gif path, mse ,ssim,  in ImagePredictedCNN
	predictionModel = ImagePredictedCNN.objects.get_or_create(name=currentImage,pathToGif=gif_path,predictionOf=t,mse=errors["mse"],ssim=errors["ssim"])

	return gif_path,predictionModel