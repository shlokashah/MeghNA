from django.contrib import admin
from .models import ImageFileName , ImageMaskDetails,ImageMaskPreds, ImagePredictedCNN, ImagePredictedMPA
admin.site.register(ImageMaskPreds)
admin.site.register(ImageFileName)
admin.site.register(ImageMaskDetails)
admin.site.register(ImagePredictedCNN)
admin.site.register(ImagePredictedMPA)