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
        self.data = json.load(file)
        coords = self.data[0][0]["search_coords"]["start_location"]
        self.originCoords = (coords["lat"], coords["lng"])
    
    
    def generateMap(self, zoom_start=14, zoom_control=False, scrollWheelZoom=False, dragging=False):

        map = folium.Map(location = [self.originCoords[0], self.originCoords[1]], tiles='OpenStreetMap' , zoom_start = zoom_start, zoom_control=zoom_control, scrollWheelZoom=scrollWheelZoom, dragging=dragging)

        lats = []
        lngs = []
        times = []

        map.add_child(folium.Marker(location = [self.originCoords[0], self.originCoords[1]] ))

        for query in self.data:
            leg = query[0]['legs'][0]
            coords = leg['end_location']
            duration = leg['duration']['value']
            # coords =  query[0]["search_coords"]["end_location"]

            lats.append(coords['lat'])
            lngs.append(coords['lng'])
            times.append(duration)


        max_duration = np.array(times).max()
        for query in self.data:
            leg = query[0]['legs'][0]
            coords = leg['end_location']
            duration = leg['duration']['value']
            c = ((duration / max_duration) * 2 * 255) 
            col1 = c = 255 if c > 255 else c
            col2 = c - 255 if c > 255 else 0
            rgb = 'rgb(' + str(col1) + ',' + str(col2) + ',255)'
            map.add_child(folium.Marker(location = [coords["lat"], coords["lng"]], popup = '' + str(duration), icon = plugins.BeautifyIcon(icon_shape="circle-dot", border_color=rgb) ))

        ''' heatmap = HeatMap( list(zip(lats, lngs, times)),
                   min_opacity=0.2,
                   radius=40, blur=10, 
                   overlay=True,
                   max_zoom=1)

        map.add_child(heatmap) '''
        self.map = map
        # map.save( transportationMode + '.html')