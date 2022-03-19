#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 10:59:57 2022

@author: krish
"""

from fastapi import FastAPI
from nowcast_api import nowcast
from pydantic import BaseModel # Pydantic is used for data handling

app = FastAPI()

@app.get("/")
def read_main():
    return 'Nowcast API designed for Federal Aviation Administration'

# Define data shapes that you want to receive using BaseModel
class NowCastParams(BaseModel):
    lat: float
    lon: float
    radius: float
    time_utc: str
    catalog_path: str = "C:\\Users\\krish\\Documents\\Northeastern University\\Spring22\\DAMG 7245\\Assignment-4\\CATALOG.csv"
    data_path: str = "C:\\Users\\krish\\Documents\\Northeastern University\\Spring22\\DAMG 7245\\Assignment-4\\sevir"
    out_path: str = "C:\\Users\\krish\\Documents\\Northeastern University\\Spring22\\DAMG 7245\\Assignment-4\\output"
    model_path:str = "C:\\Users\\krish\\Documents\\Northeastern University\\Spring22\\DAMG 7245\\Assignment-4\\\models\\nowcast"
    model_type:str = "gan"
    closest_radius:str = 'False'

# We need to send JSON data, hence POST method which is our write method
# Endpoint
@app.post("/nowcast/")
def nowcast_predict(params: NowCastParams): # Receive whatever is in the body
    """
    **SEVIR Nowcast API using FastAPI, for Federal Aviation Administration usecase.**
    
    Submitted by - Team 2
    * Aditi Krishna
    * Abhishek Jaiswal
    * Sushrut Mujumdar
    """
    try:
        closest_param = eval(params.closest_radius)
    except:
        return {'nowcast_error': 'closest_radius should be either "True" or "False". Please check the letter case carefully.'}
    output = nowcast(params.lat, params.lon, params.radius, params.time_utc, params.model_type, params.catalog_path, params.model_path, params.data_path, params.out_path,closest_param)
    if 'Error' in output.keys():
        return {'nowcast_error': output['Error']}
    else:
        return {"nowcast_path": output['data'], "gif_path": output['display']}
