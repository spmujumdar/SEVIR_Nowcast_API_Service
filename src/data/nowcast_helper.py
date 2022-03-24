#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 10:59:57 2022

@author: krish
"""
import tensorflow as tf
import numpy as np
import os
import h5py
import dateutil.parser
import matplotlib as mpl
import pandas as pd
from geopy import distance
import imageio
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (10,10)

##############################################################################
# Filtering Catalog 

def filterCatalog(lat, lon, radius, time_utc, catalog_path, closest_radius):
    # read catalog
    catalog = pd.read_csv(catalog_path, parse_dates = ['time_utc'], low_memory = False)
    
    # parse date
    time = dateutil.parser.parse(time_utc)
    
    # image_type filter
    catalog = catalog[catalog.img_type == 'vil']
    
    # datetime filter
    catalog = catalog.loc[(catalog.time_utc.dt.hour <= time.hour)&(catalog.time_utc.dt.hour >= time.hour - 1)]
    
    catalog = catalog[catalog.pct_missing == 0]
    if len(catalog) == 0:
        raise Exception('Catalog Error: Requested time not present in the given location')
    
    # aoi filter, get center lat/lon
    catalog['cntrlat'] = catalog.apply(lambda row: (row.llcrnrlat + row.urcrnrlat)/2, axis=1)
    catalog['cntrlon'] = catalog.apply(lambda row: (row.llcrnrlon + row.urcrnrlon)/2, axis=1)
    
    # applying geopy.diatance.distance
    catalog['distance'] = catalog.apply(lambda row: distance.distance((row.cntrlat,row.cntrlon), (lat,lon)).miles, axis=1)
    catalog = catalog.sort_values(by=['distance'])
    
    # next closest point check
    if closest_radius == True:
        close_dist = catalog.iloc[0].distance
        catalog = catalog[catalog.distance <= close_dist]
    else:
        catalog = catalog[catalog.distance < radius]
        if len(catalog) == 0:
            raise Exception('Catalog Error: Requested location not present in the given radius. Try increasing the radius or set closest_radius=True in the query')
    
    catalog = catalog.iloc[0]
    return str(catalog.file_name), int(catalog.file_index)

############################################################################## 
# Read Data from filename and index

def readData(filename, fileindex, data_path):
    file = os.path.join(data_path, filename)
    if not os.path.exists(file):
        raise Exception(f'Data Error: {file} does not exist')
    try:
        f = h5py.File(file,'r')
        data = f['vil'][fileindex]
        x1,x2,x3 = data[:,:,:13], data[:,:,13:26], data[:,:,26:39]
    except Exception:
        raise Exception(f'Data Error: {file} is corrupt. Please request another time or AOI')
    return np.stack((x1,x2,x3))  

############################################################################## 
# Defining our own data generator with the help of make_nowcast_dataset 
# Functions to filter the catalog and reading data in desired format

def get_nowcast_data(lat, lon, radius, time_utc, catalog_path, data_path,closest_radius):
    
    try:    
        filename, fileindex = filterCatalog(lat, lon, radius, time_utc, catalog_path, closest_radius)
        data = readData(filename, fileindex, data_path)
    except Exception as e:
        raise Exception(e)
    
    return data

##############################################################################
# Display VIL images through matplotlib

# get_cmap function from src.display.display
# vil_cmap function from src.display.display

def get_cmap(type, encoded=True):
   
    if type.lower() == 'vil':
        cmap, norm = vil_cmap(encoded)
        vmin, vmax = None, None
    else:
        cmap, norm = 'jet', None
        vmin, vmax = (-7000, 2000) if encoded else (-70, 20)

    return cmap, norm, vmin, vmax


def vil_cmap(encoded = True):
    cols=[   [0,0,0],
              [0.30196078431372547, 0.30196078431372547, 0.30196078431372547],
              [0.1568627450980392,  0.7450980392156863,  0.1568627450980392],
              [0.09803921568627451, 0.5882352941176471,  0.09803921568627451],
              [0.0392156862745098,  0.4117647058823529,  0.0392156862745098],
              [0.0392156862745098,  0.29411764705882354, 0.0392156862745098],
              [0.9607843137254902,  0.9607843137254902,  0.0],
              [0.9294117647058824,  0.6745098039215687,  0.0],
              [0.9411764705882353,  0.43137254901960786, 0.0],
              [0.6274509803921569,  0.0, 0.0],
              [0.9058823529411765,  0.0, 1.0]]
    lev = [0.0, 16.0, 31.0, 59.0, 74.0, 100.0, 133.0, 160.0, 181.0, 219.0, 255.0]
    #TODO:  encoded=False
    nil = cols.pop(0)
    under = cols[0]
    over = cols.pop()
    cmap = mpl.colors.ListedColormap(cols)
    cmap.set_bad(nil)
    cmap.set_under(under)
    cmap.set_over(over)
    norm = mpl.colors.BoundaryNorm(lev, cmap.N)
    return cmap, norm
       
##############################################################################
# Create multiple temporary images of VIL and save as GIF, then delete temp files

def save_gif(data, file_name, time_utc):
    try:
        count = 0
        # From visualize_result function in AnalyzeNowcast notebook
        cmap_dict = lambda s: {'cmap':get_cmap(s,encoded=True)[0],
                                'norm':get_cmap(s,encoded=True)[1],
                                'vmin':get_cmap(s,encoded=True)[2],
                                'vmax':get_cmap(s,encoded=True)[3]}
        filenames = []
        for pred in data:
            for i in range(pred.shape[-1]):
                plt.imshow(pred[:,:,i],**cmap_dict('vil'))
                # plt.imshow(pred[:,:,i],cmap="gist_heat")
    #            plt.colorbar(c)
                plt.axis('off')
                plt.title(f'Nowcast prediction at time {time_utc}+{(count+1)*5}minutes')
                plt.savefig(f"Pred_{time_utc.replace(':','')}_{count}.png", bbox_inches='tight')
                plt.close()
                filenames.append(f"Pred_{time_utc.replace(':','')}_{count}.png")
                count+=1
        # Saving files as GIF (https://stackoverflow.com/questions/41228209/making-gif-from-images-using-imageio-in-python)
    except:
        raise Exception('IO Error: Could not write GIF. Try reinstalling matplotlib (version<=3.2.0)')
    try:    
        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))
            os.remove(filename)
        imageio.mimsave(file_name, images)
    except:
        raise Exception('IO Error: Could not write GIF. Check imageio library in your environment')
    return file_name



##############################################################################
# Saving the model's output as h5

def save_h5(data, file_name):
    try:
        hf = h5py.File(file_name, 'w')
        hf.create_dataset('nowcast_predict', data = data)
        hf.close()
    except:
        raise Exception('IO Error: Could not write H5 file. Check the out_path correctly or try reinstalling h5py')
    return file_name

##############################################################################
# Initializing and running the model
# Link to download pre-trained model (https://www.dropbox.com/s/9y3m4axfc3ox9i7/gan_generator.h5?dl=0Downloading%20mse_and_style.h5)

def run_model(data, model_path, scale, model_type):
    MEAN=33.44
    SCALE=47.54
    data = (data.astype(np.float32)-MEAN)/SCALE
    norm = {'scale':47.54, 'shift':33.44}
    file = None
    # Model type
    try:
        if model_type == 'gan':
            file = os.path.join(model_path, 'gan_generator.h5')
            model = tf.keras.models.load_model(file, compile=False, custom_objects = {"tf": tf})
        elif model_type == 'mse':    
            file  = os.path.join(model_path, 'mse_model.h5')
            model = tf.keras.models.load_model(file, compile=False, custom_objects = {"tf": tf})
        elif model_type == 'style':    
            file = os.path.join(model_path, 'style_model.h5')
            model = tf.keras.models.load_model(file, compile=False, custom_objects = {"tf": tf})
        elif model_type in ['mse+style', 'style+mse']:    
            file = os.path.join(model_path, 'mse_and_style.h5')
            model = tf.keras.models.load_model(file, compile=False, custom_objects = {"tf": tf})
        else:
            raise Exception('Model Error: Did not find the specified model for nowcast!')
    except:
        raise Exception(f'Model Error: Model file {model_type} does not exist')
        
    # Output
    try:
        output = model.predict(data)
        if scale:
            output = output*norm['scale'] + norm['shift']
    except:
        raise Exception('Model Error: Run Error in Model. Try re-downloading the model file')
    return output

