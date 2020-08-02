# %%
'''
# Cloud Detection using Clustering
'''

# %%
'''
### Importing the image
'''

# %%
import os
import math
import rasterio
import numpy as np
import pandas as pd
from scipy import ndimage
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy import ndimage

def feature_mean(values):
    return np.nanmean(values)

def feature_std(values):
    return np.nanstd(values)

def feature_entropy(values):
    total = np.nansum(values)
    entropy = 0.0
    for x in values:
        u=x/total
        entropy+=(u*(1-u))
    return entropy

def feature_busyness(values):
    return (abs(values[0]-values[1])+abs(values[1]-values[2])+abs(values[2]-values[5])+abs(values[5]-values[8])+
    abs(values[8]-values[7])+abs(values[7]-values[6])+abs(values[6]-values[3])+abs(values[3]-values[0])+
    abs(values[1]-values[4])+abs(values[3]-values[4])+abs(values[5]-values[4])+abs(values
        [7]-values[4]))/12.0

def fill(data, start_coords, fill_value):
    global cloud_pixel_list, label_number
    xsize, ysize = data.shape
    orig_value = data[start_coords[0], start_coords[1]]
    stack = set(((start_coords[0], start_coords[1]),))
    if fill_value == orig_value:
        raise ValueError("Filling region with same value "
                     "already present is unsupported. "
                     "Did you already fill this region?")

    while stack:
        x, y = stack.pop()

        if data[x, y] == orig_value:
            data[x, y] = fill_value
            if [x, y] in cloud_pixel_list:
                cloud_pixel_list.remove([x, y])
            if [x, y] not in cloud_labels[label_number]:
                cloud_labels[label_number].append([x,y])
            if x > 0:
                stack.add((x - 1, y))
            if x < (xsize - 1):
                stack.add((x + 1, y))
            if y > 0:
                stack.add((x, y - 1))
            if y < (ysize - 1):
                stack.add((x, y + 1))


# %%
def check(values):
    sumv=np.sum(values)
    if sumv == 0.0 or sumv == 32.0:
        return 0.0
    return 1.0


def detection( tif_name, imageStore, coloredImageStore):
    image_file = tif_name
    sat_data = rasterio.open(image_file)

    # %%
    '''
    ### Calculating the dimensions of the image on earth in metres
    '''

    # %%
    width_in_projected_units = sat_data.bounds.right - sat_data.bounds.left
    height_in_projected_units = sat_data.bounds.top - sat_data.bounds.bottom

    print("Width: {}, Height: {}".format(width_in_projected_units, height_in_projected_units))

    # %%
    '''
    ### Rows and Columns
    '''

    # %%
    print("Rows: {}, Columns: {}".format(sat_data.height, sat_data.width))

    # %%
    '''
    ### Converting the pixel co-ordinates to longitudes and latitudes
    '''

    # %%
    # Upper left pixel
    row_min = 0
    col_min = 0

    # Lower right pixel.  Rows and columns are zero indexing.
    row_max = sat_data.height - 1
    col_max = sat_data.width - 1

    # Transform coordinates with the dataset's affine transformation.
    topleft = sat_data.transform * (row_min, col_min)
    botright = sat_data.transform * (row_max, col_max)

    print("Top left corner coordinates: {}".format(topleft))
    print("Bottom right corner coordinates: {}".format(botright))

    # %%
    '''
    ### Bands

    The image that we are inspecting is a multispectral image consisting of 1 band stored as a numpy array.
    '''

    # %%
    print(sat_data.count)

    # sequence of band indexes
    print(sat_data.indexes)

    # %%
    '''
    ## Visualising the Satellite Imagery

    We will use matplotlib to visualise the image since it essentially consists of arrays.
    '''

    # %%
    # Load the 4 bands into 2d arrays - recall that we previously learned PlanetScope band order is BGRN.
    b = sat_data.read(1)
    print(b.shape)
    flatten_b = b.flatten('F')

    # %%
    # Displaying the blue band.

    # fig = plt.imshow(b)
    # plt.gray()
    # plt.colorbar()
    # plt.show()
    # plt.savefig('satellite.png')

    # %%
    '''
    ## Feature Extraction

    Feature vector of length 4 consists of mean, standard deviation, busyness and entropy.
    '''

    # %%
    # %%
    mask = np.ones((3, 3))
    mask[1, 1] = 0
    mean_result = ndimage.generic_filter(b, feature_mean, footprint=mask, mode='constant', cval=np.NaN)
    print(mean_result)

    # %%
    std_result = ndimage.generic_filter(b, feature_std, footprint=mask, mode='constant', cval=np.NaN)
    print(std_result)

    # %%
    entropy_result = ndimage.generic_filter(b, feature_entropy, footprint=mask, mode='constant', cval=np.NaN)
    print(entropy_result)

    # %%
    #busyness_result = ndimage.generic_filter(b, feature_busyness, footprint=mask, mode='constant', cval=np.NaN)
    # print(busyness_result)

    # %%
    mean_result = mean_result.flatten('F')
    std_result = std_result.flatten('F')
    entropy_result = entropy_result.flatten('F')
    #busyness_result = busyness_result.flatten('F')

    # %%
    df = pd.DataFrame()
    df['mean_result'] = mean_result
    df['std_result'] = std_result
    df['entropy_result'] = entropy_result
    #df['busyness_result'] = busyness_result
    df = df.fillna(0)

    # %%
    

    # %%
    k = KMeans(n_clusters=6, init='k-means++', max_iter=300, n_init=10, random_state=0)
    k.fit(df)

    # %%
    k.cluster_centers_

    # %%
    k.labels_
    print(len(k.labels_))

    # %%
    sample = k.labels_
    sample = sample.astype(float)
    print(np.unique(sample))
    i=0
    new_list=[]
    while i<len(sample):
        new_list.append(list(sample[i:i+984]))
        i+=984
    print(type(new_list))

    # %%
    print(len(new_list))
    #print(new_list[:1])

    # %%
    y=np.array([np.array(xi) for xi in new_list])

    # %%
    print(type(y))
    print(y[:3])
    y.shape

    # %%
    print(len(y[:-3]))
    og=y
    plt.imshow(y)
    # plt.show()

    # %%
    avg_dict={}
    for val in np.unique(sample):
        val_index = list(np.where(sample==val))
        print(val_index)
        avg=0
        print(flatten_b[2])
        for i in val_index:
            avg+=flatten_b[i]
        print(len(val_index[0]))
        avg_dict[val] = np.sum(avg)/len(val_index[0])
    print(avg_dict)

    # %%
    for i in range(0, len(new_list)):
        for j in range(0, len(new_list[i])):
            if new_list[i][j] != 4.0:
                new_list[i][j] = 0
    y=np.array([np.array(xi) for xi in new_list])
    y=np.rot90(y,3)
    y=np.flip(y, 1)
    #y=np.rot90(y)
    #y=np.rot90(y)
    plt.imshow(y)
    #plt.show()plt.gca().invert_yaxis()
    #plt.gca().invert_xaxis()

    # %%
    fig = plt.imshow(b)
    plt.gray()
    plt.colorbar()


    # %%
    
    image=y
    edges = image - ndimage.morphology.binary_dilation(image) 
    print(edges[:1])

    # %%
    plt.imshow(b, cmap='gray')
    plt.imshow(edges, cmap='jet', alpha=0.4)


    # %%
    edge_result = ndimage.generic_filter(y, check, footprint=mask, mode='constant', cval=np.NaN)
    print(edge_result)
    #plt.imshow(b, cmap='gray')
    plt.imshow(b, cmap='gray')
    plt.imshow(edge_result, cmap='gray', alpha=0.4)
    plt.savefig(imageStore)
    # %%
    cloud_pixel_list=[]
    label_number = []
    for row in range(0, 984):
        for col in range(0, 1074):
            if y[row][col] == 4.0:
                cloud_pixel_list.append([row, col])
                label_number.append(1)
    print(cloud_pixel_list)


    temp=y
    cloud_labels = {}
    print([800, 600] in cloud_pixel_list)
    label_number=6
    print(type(cloud_pixel_list))
    while len(cloud_pixel_list) > 0:
        cloud_labels[label_number] = []
        fill(temp, cloud_pixel_list[0], label_number)
        label_number+=1
    plt.imshow(temp, cmap='jet')
    plt.savefig(coloredImageStore)
