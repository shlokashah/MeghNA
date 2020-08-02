import pandas as pd
import numpy as np
import cv2 as cv2
import rasterio

def classify(tifPath, x, y):
    sat_data = rasterio.open(tifPath)
    img = sat_data.read(1)
    c, h, l, m = 0, 0, 0, 0
    print(len(x),len(y))
    return
    BR=pd.read_excel('BackgroundJobs/Step1Mask/Step2Features/TIR.xlsx')
    for i in range(len(x)):
        print(i)
        for j in range(len(y)):
            # print(i,j,img[x[i]][y[j]])
            # print(BR)
            img[x[i]][y[j]] = BR["BT"][img[x[i]][y[j]] // 1]
            if(img[x[i]][y[j]] < 200):
                c += 1
            if(200 < img[x[i]][y[j]] < 243):
                h += 1
            if(243 < img[x[i]][y[j]] < 270):
                m += 1
            else:
                l += 1
    
    mx = max(c, h, l, m)
    step2Directory = "BackgroundJobs/Step1Mask/Step2Features/"
    f = open(step2Directory + "step2MaskOutputs.txt","w+")
    mx = max(c, h, l, m)
    print(mx,c,h,l,m)
    if(mx == c):
        f.write("Cyclone\n")
    elif(mx == h):
        f.write("High\n")
    elif(mx == m):
        f.write("Medium\n")
    else:
        f.write("Low\n")

    f.close()
