# '''
# File: _KMeans Cloud Detection.py_

# Requirements: numpy, opencv, matplotlib

# Input:
# image_folder (string): Specify path to image
# timestamp (string): Image name without extension (Reads in png by default)

# Output:
# cloud_detection (dictionary): Key is cloud number and value is a dictionary with timestamp, cloud_no, algorithm, centroidX and centroidY for that cloud.'''

# Importing Libraries
import numpy as np
import cv2
import rasterio
import matplotlib.pyplot as plt
import pandas as pd


def classify(tifPath, x, y, mask):
    sat_data = rasterio.open(tifPath)
    img = sat_data.read(1)
    print("TIFF Shape: ", img.shape)
    c, h, l, m = 0, 0, 0, 0
    print(len(x),len(y))
    
    applied = img * mask
    # plt.imshow(applied)
    # plt.colorbar()
    # plt.show()
    BR=pd.read_excel('BackgroundJobs/Step1Mask/Step2Features/TIR.xlsx')
    # BR = pd.read_excel('./TIR(1).xlsx')
    BR.set_index(['Pixel_Val'], inplace=True)
    BR = BR.to_dict()["BT"]
    
    cloud_type = {}
    cloud_type["cyclone"] = len(np.where(applied >= 896)[0])
    cloud_type["high_clouds"] = len(np.where((792 <= applied) & (applied < 896))[0])
    cloud_type["medium_clouds"] = len(np.where((676 <= applied) & (applied < 792))[0])
    cloud_type["low_clouds"] = len(np.where((100 <= applied) & (applied < 676))[0])
    
    print("Cloud Type: ", max(cloud_type, key=cloud_type.get))
    return max(cloud_type, key=cloud_type.get)

def step1Kmeans(imagePath, output_folder,tifImagePath,fileName,number):
    gx = []
    gy = []
    gcomx = []
    gcomy = []
    gtype = []
    gno = []
    
    img = cv2.imread(imagePath)
    Z = img.reshape((-1,3))

    # convert to np.float32
    Z = np.float32(Z)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 4
    ret, label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))
    res2bw = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)
    colors = np.unique(res2bw)

    # Plotting grayscale masks
    #plt.imshow(res2bw, cmap = 'gray')
    #plt.colorbar()
    #plt.show()
    print(output_folder ,  fileName)
    cv2.imwrite(output_folder + fileName, res2bw)
    #   
    # Removing background, since the darkest color is sky
    colors = colors[1:]
    #print(colors)
    com = {}
    # Processing every cloud
    cloud_detection = {}
    for i in range(0, len(colors)):
        filter_mask = (res2bw == colors[i]).astype(int)
        binary_mask = filter_mask
        filter_mask = cv2.convertScaleAbs(filter_mask, alpha=(255.0))
        co_ordinates = np.where(filter_mask == 0)
        x = co_ordinates[0]
        y = co_ordinates[1]
        cloudType = classify(tifImagePath, x , y, binary_mask)

        mean_x = np.mean(x)
        mean_y = np.mean(y)
        com[i] = [round(mean_x, 2), round(mean_y, 2)]
        
        gx.extend(x)
        gy.extend(y)
        gtype.extend([cloudType] * len(x))
        gcomx.extend([int(mean_x)] * len(x))
        gcomy.extend([int(mean_y)] * len(y))
        gno.extend([i] * len(x))



        cloud_detection[str(i)] = {'cloud_no': i, 
                                'com_x': mean_x, 
                                'com_y': mean_y,
                                'type': cloudType}


    # Print cloud detection output
    print(cloud_detection)
    df = pd.DataFrame()
    df["x"] = gx
    df["y"] = gy
    df["comx"] = gcomx
    df["comy"] = gcomy
    df["type"] = gtype
    g["cloud_no"] = gno
    df.set_index(['x', 'y'], inplace=True)
    df.to_csv('step1ExcelOutputKmeans/pixel_by_pixel_of_satellite'+ str(number) +'.csv')

    return cloud_detection

# image_folder = './images/'
# timestamp = '2'
# file_type = 'png'
# output_folder = './output/'
# kmeans_cloud_detection(image_folder, timestamp, file_type, output_folder)