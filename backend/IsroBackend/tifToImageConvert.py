import cv2

import math
import rasterio
import matplotlib.pyplot as plt
import os
def conversion(tifFilePath,ColortoSaveAs, JPEGtoSaveAs):
    sat_data = rasterio.open(tifFilePath)
    b = sat_data.read(1)
    fig = plt.imshow(b)
    #plt.colorbar()
    # plt.show()
    plt.savefig(ColortoSaveAs)

    image = cv2.imread(ColortoSaveAs , cv2.IMREAD_GRAYSCALE)
    cv2.imwrite(JPEGtoSaveAs,image)
    # j=1
    # for i in os.listdir("C:\\Users\\aumkar\\Downloads\\infrared"):
    #     image = cv2.imread('C:\\Users\\aumkar\\Downloads\\infrared\\'+i,cv2.IMREAD_GRAYSCALE)
    #     print(image.shape)
    #     cv2.imwrite("sat"+str(j)+".jpg",image)
    #     j+=1