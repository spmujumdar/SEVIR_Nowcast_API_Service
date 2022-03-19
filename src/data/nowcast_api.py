#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 10:59:57 2022

@author: krish
"""

import os
from nowcast_helper import get_nowcast_data, run_model, save_gif, save_h5
import dateutil.parser

# Use the following for testing nowcast(lat=37.318363, lon=-84.224203, radius=100, time_utc='2019-06-02 18:33:00', catalog_path='C:\\Users\\krish\\Documents\\Northeastern University\\Spring22\\DAMG 7245\\Assignment-4\\CATALOG.csv', model_path='C:\\Users\\krish\\Documents\\Northeastern University\\Spring22\\DAMG 7245\\Assignment-4\\models', data_path='C:\\Users\\krish\\Documents\\Northeastern University\\Spring22\\DAMG 7245\\Assignment-4\\sevir',out_path='C:\\Users\\krish\\Documents\\Northeastern University\\Spring22\\DAMG 7245\\Assignment-4\\output', model_type='gal', closest_radius=True)
def nowcast(lat, lon, radius, time_utc, model_type, catalog_path, model_path, data_path, out_path, closest_radius=False):
    Error = None
    # Parse time
    try:
        user_time = dateutil.parser.parse(time_utc)
    except Exception:
        Error = 'Invalid date time format. Please provide a valid format (refer to https://dateutil.readthedocs.io/en/stable/parser.html)'
        return {'Error': Error}
    # Data cannot be older than 2019 June 1st (As per paper)
    if user_time.month < 6:
        if user_time.year < 2019:
           Error = 'Request date is too old! Try dates after 2019, June 1st'
           return {'Error': Error}
    
    
    try:
        # Filter to get data
        data = get_nowcast_data(lat= lat, lon=lon, radius= radius, time_utc = time_utc, catalog_path = catalog_path, data_path = data_path, closest_radius=closest_radius)
        # Run model
        output = run_model(data,model_path,scale=True,model_type=model_type)
        # Output as h5/GIF
        display_path = save_gif(data = output,file_name =os.path.join(out_path,f'latest_nowcast_display_{lat}_{lon}.gif'), time_utc=time_utc)
        output_path = save_h5(output,os.path.join(out_path,f'nowcast_output_{lat}_{lon}.h5'))
    except Exception as e:
        return {'Error': str(e)}
    
    # Return path for output
    return {'data': output_path, 'display':display_path}
