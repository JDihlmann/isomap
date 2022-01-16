import os
import json
import math
import folium
import geopandas
import googlemaps
import numpy as np
from os import path
import pandas as pd
from tqdm import tqdm
from enum import Enum
from folium import plugins
import matplotlib.pyplot as plt
from dotenv import load_dotenv



class RegionElevationDisplayer(object):

    def __init__(self):
        file = open(os.getcwd() + "/data/elevation.json", "r")
        self.data = json.load(file)

    def generateMap(self):

        lats = []
        lngs = []
        elevations = []
        for query in self.data:
            elevation = query[0]['elevation']
            coords = query[0]['location']
            lats.append(coords['lat'])
            lngs.append(coords['lng'])
            elevations.append(elevation)

        center_lat = np.array(lats).mean()
        center_lng = np.array(lngs).mean()
        map = folium.Map(location = [center_lat, center_lng], tiles='OpenStreetMap' , zoom_start = 14)
        map.add_child(folium.Marker(location = [center_lat, center_lng] ))

        min_elevation = np.array(elevations).min()
        max_elevation = np.array(elevations).max()
        for query in self.data:
            elevation = query[0]['elevation']
            coords = query[0]['location']

            c = (((elevation - min_elevation) / (max_elevation -  min_elevation)) * 2 * 255) 
            col1 = c = 255 if c > 255 else c
            col2 = c - 255 if c > 255 else 0
            rgb = 'rgb(' + str(col1) + ',' + str(col2) + ',255)'
            map.add_child(folium.Marker(location = [coords["lat"], coords["lng"]], popup = '' + str(elevation), icon = plugins.BeautifyIcon(icon_shape="circle-dot", border_color=rgb) ))

        map.save('elevation.html')


    
    