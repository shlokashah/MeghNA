from django.db import models

class ImageFileName(models.Model):
    name = models.CharField(max_length=100,default=None)

class ImageMaskDetails(models.Model):
	name = models.ForeignKey(ImageFileName,default=None,on_delete=models.PROTECT)
	maskNumber = models.FloatField(null=True)
	algorithm = models.CharField(null=True,max_length=100,default=None,)
	com_x = models.FloatField(null = True)
	com_y =   models.FloatField(null = True)
	timeTakenCPU = models.FloatField(null=True)
	timeTakenHuman = models.FloatField(null=True)
	cloudType = models.CharField(null=True,max_length=100,default=None,)

	def __str__(self):
			return str(self.maskNumber) +"\t" + str(self.algorithm) +"\t" + str(self.name.name)
class ImagePredictedCNN(models.Model):
	name = models.ForeignKey(ImageFileName,default=None,on_delete=models.PROTECT)
	predictionOf = models.FloatField(null = True)
	pathToGif = models.CharField(null=True,max_length=100,default=None,)
	mse = models.FloatField(null = True)
	ssim = models.FloatField(null = True)

	def __str__(self):
			return str(self.name) +"\t" + str(self.pathToGif)

class ImagePredictedMPA(models.Model):
	name = models.ForeignKey(ImageFileName,default=None,on_delete=models.PROTECT)
	predictionOf = models.FloatField(null = True)
	pred_com_x = models.FloatField(null = True)
	pred_com_y = models.FloatField(null = True)
	error = models.FloatField(null = True)

	def __str__(self):
			return str(self.name.name) +"\t" + str(self.predictionOf)

class ImageMaskPreds(models.Model):
	maskKey = models.ForeignKey(ImageMaskDetails,default=None,on_delete=models.PROTECT)
	maskNumber = models.FloatField(null=True)
	lat = models.FloatField(null = True)
	lon = models.FloatField(null = True)
	top_temp = models.FloatField(null = True)
	top_height = models.FloatField(null = True)
	cloud_type = models.TextField(max_length = 100, default = None , null = True)
