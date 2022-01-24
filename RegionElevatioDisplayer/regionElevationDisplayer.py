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
        dictData = json.load(file)

        self.coords = []
        self.elevations= []
        for query in dictData:
            coords = query[0]['location']
            elevation = query[0]['elevation']

            self.coords.append((coords["lat"], coords["lng"]))
            self.elevations.append(elevation)
        
        meanCoords = np.array(self.coords).mean(axis=0)
        self.originCoords = (meanCoords[0], meanCoords[1])

    def generateMap(self, zoom_start=14, zoom_control=False, scrollWheelZoom=False, dragging=False):

        map = folium.Map(location = self.originCoords, tiles='OpenStreetMap' , zoom_start = zoom_start, zoom_control=zoom_control, scrollWheelZoom=scrollWheelZoom, dragging=dragging)

        min_elevation = np.array(self.elevations).min()
        max_elevation = np.array(self.elevations).max()

        for i in range(len(self.coords)):
            coords = self.coords[i]
            elevation = self.elevations[i]

            # Coloring
            c = (((elevation - min_elevation) / (max_elevation -  min_elevation)) * 2 * 255) 
            col1 = c = 255 if c > 255 else c
            col2 = c - 255 if c > 255 else 0
            rgb = 'rgb(' + str(col1) + ',' + str(col2) + ',255)'

            map.add_child(folium.Marker(location = coords, popup = '' + str(elevation), icon = plugins.BeautifyIcon(icon_shape="circle-dot", border_color=rgb) ))

        self.map = map


    
    