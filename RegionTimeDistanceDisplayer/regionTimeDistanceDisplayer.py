import os
import json
from time import time
import folium
import geopandas
import numpy as np
from os import path
import pandas as pd
from enum import Enum
from folium import plugins
from folium.plugins import HeatMap
import matplotlib.pyplot as plt

class TransportationType(Enum):
    Driving = 1
    Walking = 2
    Bicycling = 3

class RegionTimeDistanceDisplayer(object):

    def __init__(self, filename):
        file = open(os.getcwd() + filename, "r")
        dictData = json.load(file)

        self.coords = []
        self.durations = []
        for query in dictData:
            leg = query[0]['legs'][0]
            coords = leg['end_location']
            duration = leg['duration']['value']
            self.coords.append((coords["lat"], coords["lng"]))
            self.durations.append(duration)

        dictOriginCoords = dictData[0][0]["search_coords"]["start_location"]
        self.originCoords = (dictOriginCoords["lat"], dictOriginCoords["lng"])

    
    
    def generateMap(self, zoom_start=14, zoom_control=False, scrollWheelZoom=False, dragging=False):

        map = folium.Map(location = [self.originCoords[0], self.originCoords[1]], tiles='OpenStreetMap' , zoom_start = zoom_start, zoom_control=zoom_control, scrollWheelZoom=scrollWheelZoom, dragging=dragging)
        map.add_child(folium.Marker(location = [self.originCoords[0], self.originCoords[1]] ))
        
        maxDuration = np.array(self.durations).max()
        
        for i in range(len(self.coords)):
            coords = self.coords[i]
            duration = self.durations[i]

            # Coloring
            c = ((duration / maxDuration) * 2 * 255) 
            col1 = c = 255 if c > 255 else c
            col2 = c - 255 if c > 255 else 0
            rgb = 'rgb(' + str(col1) + ',' + str(col2) + ',255)'

            map.add_child(folium.Marker(location = coords, popup = '' + str(duration), icon = plugins.BeautifyIcon(icon_shape="circle-dot", border_color=rgb) ))

        self.map = map
        # map.save( transportationMode + '.html')