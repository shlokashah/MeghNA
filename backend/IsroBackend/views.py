from django.conf import settings
import os
from decimal import Decimal
import csv
import datetime
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,JSONParser
from django.core.serializers.json import DjangoJSONEncoder
import json
import traceback
from . import cloudDetection , tifToImageConvert
from .models import ImageFileName, ImageMaskDetails, ImageMaskPreds, ImagePredictedCNN, ImagePredictedMPA
from django.forms.models import model_to_dict
import pandas as pd
class CloudDetails(APIView):
    parser_classes = (JSONParser,)
    '''
    Point (int,int)
    TIR1 count double
    Cloudy bool 
    type string
    top temp string(int + K)
    height string
    '''
    def get(self,request):
        return HttpResponse(status=403)

    def post(self,request):
        # try:
        print(eval(request.body.decode('ASCII')))
        l = eval(request.body.decode('ASCII'))
        print(type(l))
        # body = request.body.split(',')
        # print(body)
        # body_unicode = request.body.decode('utf-8')
        # body_data = json.loads(body_unicode)
        # print(body_data)
        posx = l['posx']
        posy = l['posy']

        if int(posy) < 150 :
            pred = ImageMaskPreds.objects.all().filter(pix_y=150)[0]
        else:
            pred = ImageMaskPreds.objects.all().filter(pix_y=250)[0]
        pred = model_to_dict(pred)
        print(pred)
        print(type(pred))
        for i in pred:
            if i == 'cloud_type':
                cloud_type = pred['cloud_type']
            if i == 'top_temp':
                top_temp = pred['top_temp']
            if i == 'top_height':
                top_height = pred['top_height']
            if i == 'lat':
                lat = pred['lat']
            if i == 'lon':
                lon = pred['lon']


        jsonresp = {
                "posx":  posx,
                "posy":  posy,
                "tir1Count": "581.00",
                "cloudy": True,
                "type":  str(cloud_type),
                "topTemp": str(top_temp) + ' K',
                "height":  str(top_height) + " meters",
                "lat" : str(lat),
                "lon" : str(lon),
            }
        return Response(jsonresp, content_type='application/json',status=200)
        # except Exception as e:
        #     traceback.print_exc()
        #     print(e)
        #     return HttpResponse(status=403)

class CloudPredictionDetails(APIView):
    parser_classes = (MultiPartParser,)
    '''
    Time Slot String
    Direction string
    speed String
    '''
    def get(self,request):
        try:
            # print(os.path.dirname(__file__))
                # directory = 'C:/Users/parth jardosh/Desktop/Desktop/sih2020/DjangoServer/IsroDjangoBackend/IsroBackend/media/'
                # directory_TIf = directory + 'Tif_Images/'
            
                # for index,file in enumerate(os.listdir(directory_TIf)):
                    # filename = os.fsdecode(file)
                    # print(filename)
                # inputFileTifName = '3DIMG_07NOV2019_0000_L1C_SGP.tif'
            # inputFileName = 'ConvertedImage_' + str(index) + '.jpeg'
                # input_image_path_tif =  directory + 'Tif_Images/' + inputFileTifName
                # input_image_path_converted_color =  directory + 'images/Color/' + inputFileName
                # input_image_path_converted_bw =  directory + 'images/BW/' + inputFileName
                # outputMaskColored = 'colored_mask.png'
                # output_image_path_colored = directory + 'images/ColoredMask/' + outputMaskColored
                # output_image_path =     directory + 'images/BWMask/' + outputMaskBW

                # tifToImageConvert.conversion(input_image_path_tif ,input_image_path_converted_color ,input_image_path_converted_bw)
                # cloudDetection.detection(input_image_path_tif,output_image_path,output_image_path_colored)
            # directory = 'C:/Users/parth jardosh/Desktop/Desktop/sih2020/DjangoServer/IsroDjangoBackend/IsroBackend/media/csvs/'
            # for idx,fileName in enumerate(os.listdir(directory)):
            #     print(fileName)
            #     fileName = 'ConvertedImage_' + idx
            #     path = directory + fileName +'.csv'
            #     with open(path) as f:
            #             reader = csv.reader(f)
            #             print('entering for loop')
            #             # newImageName = ImageFileName()
            #             # newImageName.name = fileName + '.jpeg'
            #             # newImageName.save()
                        
            #             currentImage,created = ImageFileName.objects.get_or_create(
            #                 name=fileName+'.jpeg'
            #                 )   
            #             print('image name record saved',created)
            #             for index,row in enumerate(reader):
            #                 if index !=0 :
            #                     # print(row[0],row[1],row[2])
            #                     # print(currentImage)
            #                     # a = row[1]
            #                     # print(a)
            #                     # print(type(a))
            #                     # a = float(a)
            #                     # print(type(a))
            #                     # print(a)
            #                     _, created = ImageMaskDetails.objects.get_or_create(
            #                         name = currentImage,
            #                         label = int(row[0]),
            #                         avg_x = float(row[1]),
            #                         avg_y = float(row[2]),
            #                         mass = int(row[6]),
            #                         major_minor = float(row[5]),
            #                         com_x = float(row[4]),
            #                         com_y = float(row[3]),
            #                         lat = float(row[3]),
            #                         lon = float(row[3]),
            #                         top_temp = float(row[3]),
            #                         top_height = float(row[3]),
            #                         cloud_type = row[]
            #                         )
            #                     print(created,end=' ')
            #                 else:
            #                     # print(row[0],row[1],row[2])
            #                     print(idx, "header row ignored",end="\n")

            # outputMaskBW = 'Clouds_Labelled.png'
            # now = datetime.datetime.now()
            # print (now.minute, now.second)
            # nowmin = now.minute
            # nowhr = now.hour

            # inputFileName = 'ConvertedImage_2.jpeg'# + str(nowmin) + '.jpeg'
            # rangeTime = str(nowhr) + ":" + str(nowmin) + ' - ' + str(nowhr) + ":" + str(nowmin + 1)
            step1Directory = "BackgroundJobs/Step1Mask/"
            # ------------------------------------------------------------------
            # loading the next file
            f = open(step1Directory + "currentImage.txt","r")
            i = f.read()
            f.close()
            i = str(6)
            fileName = "satellite" + i + ".jpg"
            tifImageNames = ["3DIMG_07NOV2019_0000_L1C_SGP.tif",  "3DIMG_07NOV2019_1000_L1C_SGP.tif","3DIMG_07NOV2019_0030_L1C_SGP.tif",  "3DIMG_07NOV2019_1030_L1C_SGP.tif","3DIMG_07NOV2019_0100_L1C_SGP.tif",  "3DIMG_07NOV2019_1100_L1C_SGP.tif","3DIMG_07NOV2019_0130_L1C_SGP.tif",  "3DIMG_07NOV2019_1130_L1C_SGP.tif","3DIMG_07NOV2019_0200_L1C_SGP.tif",  "3DIMG_07NOV2019_1200_L1C_SGP.tif","3DIMG_07NOV2019_0230_L1C_SGP.tif",  "3DIMG_07NOV2019_1230_L1C_SGP.tif","3DIMG_07NOV2019_0300_L1C_SGP.tif",  "3DIMG_07NOV2019_1300_L1C_SGP.tif","3DIMG_07NOV2019_0330_L1C_SGP.tif",  "3DIMG_07NOV2019_1330_L1C_SGP.tif","3DIMG_07NOV2019_0400_L1C_SGP.tif",  "3DIMG_07NOV2019_1400_L1C_SGP.tif","3DIMG_07NOV2019_0430_L1C_SGP.tif",  "3DIMG_07NOV2019_1430_L1C_SGP.tif","3DIMG_07NOV2019_0500_L1C_SGP.tif",  "3DIMG_07NOV2019_1500_L1C_SGP.tif","3DIMG_07NOV2019_0530_L1C_SGP.tif",  "3DIMG_07NOV2019_1530_L1C_SGP.tif","3DIMG_07NOV2019_0600_L1C_SGP.tif",  "3DIMG_07NOV2019_1600_L1C_SGP.tif","3DIMG_07NOV2019_0630_L1C_SGP.tif",  "3DIMG_07NOV2019_1630_L1C_SGP.tif","3DIMG_07NOV2019_0700_L1C_SGP.tif",  "3DIMG_07NOV2019_2000_L1C_SGP.tif","3DIMG_07NOV2019_0730_L1C_SGP.tif",  "3DIMG_07NOV2019_2030_L1C_SGP.tif","3DIMG_07NOV2019_0800_L1C_SGP.tif",  "3DIMG_07NOV2019_2100_L1C_SGP.tif","3DIMG_07NOV2019_0830_L1C_SGP.tif",  "3DIMG_07NOV2019_2130_L1C_SGP.tif","3DIMG_07NOV2019_0859_L1C_SGP.tif",  "3DIMG_07NOV2019_2200_L1C_SGP.tif","3DIMG_07NOV2019_0900_L1C_SGP.tif",  "3DIMG_07NOV2019_2230_L1C_SGP.tif","3DIMG_07NOV2019_0929_L1C_SGP.tif",  "3DIMG_07NOV2019_2300_L1C_SGP.tif","3DIMG_07NOV2019_0930_L1C_SGP.tif",  "3DIMG_07NOV2019_2330_L1C_SGP.tif","3DIMG_07NOV2019_0959_L1C_SGP.tif"]
            print(i)
            kmeansPath = "BackgroundJobs/Step1KMeans/step1ImageOutputKmeans/" + i + ".png"
            mpaPath = ""
            maskPath = "BackgroundJobs/Step1Mask/step1ImageOutput/" + fileName
            cnnPath = "BackgroundJobs/Step3/CNN_LSTM/ImageOutputs/" + fileName
            filePaths = [tifImageNames[int(i)-1],kmeansPath, maskPath, cnnPath, fileName]
            currentImage = ImageFileName.objects.get(name=fileName)
            
            kmeans = []
            qs = ImageMaskDetails.objects.filter(name=currentImage, algorithm="K-Means")
            # print(qs)
            for j in qs:
                temp = []
                temp.append(j.maskNumber)
                temp.append(j.com_x)
                temp.append(j.com_y)
                temp.append(j.timeTakenCPU)
                temp.append(j.timeTakenHuman)
                temp.append(j.cloudType)
                kmeans.append(temp)
            mask = []
            qs = ImageMaskDetails.objects.filter(name=currentImage, algorithm="Mask RCNN")
            # print(qs)
            for j in qs:
                temp = []
                temp.append(j.maskNumber)
                temp.append(j.com_x)
                temp.append(j.com_y)
                temp.append(j.timeTakenCPU)
                temp.append(j.timeTakenHuman)
                temp.append(j.cloudType)
                mask.append(temp)
            
            mpa = []
            qs = ImagePredictedMPA.objects.filter(name=currentImage)
            print(qs)
            for j in qs:
                temp = []
                temp.append(j.predictionOf)
                temp.append(j.pred_com_x)
                temp.append(j.pred_com_y)
                temp.append(j.error)
                mpa.append(temp)

            cnn = []
            qs = ImagePredictedCNN.objects.get(name=currentImage)
            print(qs)
            cnn.append(qs.predictionOf)
            cnn.append(qs.pathToGif)
            cnn.append(qs.mse)
            cnn.append(qs.ssim)
            


            

            jsonresp = {
                'image': filePaths,
                'kmeans' : kmeans,
                'mask' : mask,
                'mpa' : mpa,
                'cnn' : cnn,
            }
            return Response(jsonresp, content_type='application/json')
        except Exception as e:
                traceback.print_exc()
                print(e)
                return HttpResponse(status=403)


    def post(self,request):

        # try:
        print(eval(request.body.decode('ASCII')))
        l = eval(request.body.decode('ASCII'))
        print(type(l))
        # body = request.body.split(',')
        # body_unicode = request.body.decode('utf-8')
        # body_data = json.loads(body_unicode)
        # print(body_data)
        input_x = int(l['posx'])
        input_y = int(l['posy'])
        imageName = l['imageName']
        print(input_x,input_y,imageName)
        # file_path = settings.STATIC_ROOT
        # print(file_path)
        df = pd.read_csv('step1ExcelOutputKmeans/pixel_by_pixel_of_'+ imageName+'.csv')
        df.set_index(['x', 'y'], inplace=True)
        result = df.to_dict()
        # print(result)
        cloudy = True
        jsonresp = {}
        try:
            # comx = result['comx'][(input_x, input_y)]
            print("hgjvkbjn")
            # print(comx)
            # comy = result['comy'][(input_x, input_y)]
            # print(result['type'])
            typeC = result['type'][(input_x, input_y)]
            print(typeC)
            mask = result['cloud_no'][(input_x,input_y)]

            jsonresp = {
                "mask" : mask,
                "type" : typeC,
                "cloudy": cloudy,
                }
        except Exception as e:
            cloudy = False
            jsonresp = {
                "cloudy" : cloudy
            }

        return Response(jsonresp, content_type='application/json',status=200)

        # if int(posy) < 150 :
        #     pred = ImageMaskPreds.objects.all().filter(pix_y=150)[0]
        # else:
        #     pred = ImageMaskPreds.objects.all().filter(pix_y=250)[0]
        # pred = model_to_dict(pred)
        # print(pred)
        # print(type(pred))
        # for i in pred:
        #     if i == 'cloud_type':
        #         cloud_type = pred['cloud_type']
        #     if i == 'top_temp':
        #         top_temp = pred['top_temp']
        #     if i == 'top_height':
        #         top_height = pred['top_height']
        #     if i == 'lat':
        #         lat = pred['lat']
        #     if i == 'lon':
        #         lon = pred['lon']





# pred.pix_y = 250
#         pred.lat = 35.681719
#         pred.lon = 65.352400
#         pred.height = 2000.0
#         pred.temp = 240.580
#         pred.cloud = "Cirrus"
#         pred.save()
#         print("preds saved")