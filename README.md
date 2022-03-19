SEVIR Nowcast API using FastAPI web-framework
============================================================

Report link (GoogleDoc): https://docs.google.com/document/d/1XSUotbV7bAod1QYp7f28zVP2qf2TTP5Fij_wSKRQ-ww/edit?usp=sharing

============================================================

Weather briefing is a vital part of any flight preparation. The National Weather Service (NWS), Federal Aviation Administration (FAA), Department of Defense and other aviation groups are responsible for coherent and accurate weather reporting. The combined efforts of thorough scientific study and modeling techniques are able to predict the weather patterns with increasing accuracy. These weather forecasts enable pilots to make informed decisions regarding weather and flight safety.

### Weather Radar Observations
The weather radar data is provided by the national network of WSR-88D (NEXRAD) radars. This data is the major source of weather sensing used for Nowcasting. The WSR-88D (NEXRAD), also known as the Doppler Radar has two operational modes- clear air and precipitation. The mode is changed based on the weather condition. 

The NEXRAD radar image is not real time and can be upto 5 minutes old. If these images are older than it can lead to fatal accidents, as they have in the past. They are displayed as mosaic images that have some latency in creation, and in some cases the age of the oldest NEXRAD data in the mosaic can exceed the age indication in the cockpit by 15 to 20 minutes. Even small-time differences between age-indicator and actual conditions can be important for safety of flight. 
A better approach to solving this problem is by using the SEVIR Nowcast model which predicts a sequence of 12 images corresponding to the next hour of weather, based on the previously captured 13 images sampled at 5 minute intervals. 

#### Objective

The goal of the project is to implement a REST API to execute the GAN model, which takes a sequence of 13 images as input and generates 12 images as output. The end users, who are a bunch of developers who want to integrate our API with their system, pass a JSON file as a blueprint with all required parameters through CURL, POSTMAN, or a Python-Client to execute the model. 

#### Assumptions

Scope for false alarms or misses
Area of interest parameters, i.e. llcrnrlat, llcrnrlon, urcrnrlat, urcrnrlon format match the ones stored in the CATALOG.csv file
Data is available for the user specified datatime input
Enough time to download the specific raw data (h5 file) for the user specified parameters

The API can be used as a foundation to be built upon and integrated with the existing Electronic Flight Display (EFD) or Multi-Function Display (MFD) that gives the pilot access to several data links to weather services that are made available through multiple resources. Along with Graphical NEXRAD data, city forecast data, graphical wind data, the system will also have near-term forecasted images for the requested area of interest and time.

#### Requirements

To test pretrained models and train API requires 
```
- Python 3.7
- tensorflow 2.1.0
- pandas
- numpy
```
To visualize the outputs basemap library is required, which needs to following libraries
```
- h5py 2.8.0
- matplotlib 3.2.0
```
#### Sample outputs

1. Test case 1:

![](https://github.com/krishna-aditi/Nowcast-API-using-FastAPI/blob/main/reports/figures/latest_nowcast_display_30.54711887_-92.28496258.gif)

2. Test case 2:

![](https://github.com/krishna-aditi/Nowcast-API-using-FastAPI/blob/main/reports/figures/latest_nowcast_display_30.58070007_-91.57206541.gif)

#### References

- First Steps - FastAPI (https://fastapi.tiangolo.com/tutorial/first-steps/)
- Talks # 8: Sebastián Ramírez; Build a machine learning API  from scratch  with FastAPI (https://www.youtube.com/watch?v=1zMQBe0l1bM&ab_channel=AbhishekThakur)
- making gif from images using imageio in python - Stack Overflow (https://stackoverflow.com/questions/41228209/making-gif-from-images-using-imageio-in-python)
- Testing - FastAPI (https://fastapi.tiangolo.com/tutorial/testing/)


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Download all pre-trained Nowcast models
    │   ├── download_models.py
    |   └── model_urls
    |
    ├── notebooks          <- Jupyter notebook to invoke API
    │   └── invoke-api
    │
    ├── reports            <- Screenshots
    │   ├── figures
    |       ├── Curl-1.png
    |       ├── pytest_command.png
    |       ├── response.png
    │       └── Uvicorn.png
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   ├── nowcast_api.py
    │   │   ├── nowcast_helper.py
    │   │   ├── nowcast_main.py
    │   │   ├── nowcast_utils.py
    │   │   └── test-api.py
    │   │
    │   ├── features       
    │   │   └── build_features.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io
 

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

--------

#### Submitted by:

![image](https://user-images.githubusercontent.com/37017771/153502035-dde7b1ec-5020-4505-954a-2e67528366e7.png)
