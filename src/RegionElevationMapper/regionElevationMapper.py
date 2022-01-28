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



class RegionElevationMapper(object):

    def __init__(self, filenames):

        # Setup Google Maps API
        load_dotenv()
        googleMapsAPIKey = os.getenv('GOOGLE_API_KEY')
        self.gmaps = googlemaps.Client(key=googleMapsAPIKey)
        
        # Collect Coords
        self.coords = set()
        for filename in filenames:
            file = open(os.getcwd() + filename, "r")
            data = json.load(file)
            
            start_coords = data[0][0]["search_coords"]["start_location"]
            self.coords.add((start_coords["lat"], start_coords["lng"]))
            
            for query in data:
                end_coords = query[0]['legs'][0]['end_location']
                self.coords.add((end_coords["lat"], end_coords["lng"]))
	



    def generateElevation(self):

        # Query Google Maps API
        responses = []
        for coords in tqdm(self.coords):
            resp = self.gmaps.elevation(coords)
            responses.append(resp)

         # Save
        with open("elevation.json", 'w') as fout:
            json.dump(responses , fout)
    
    def generateMap(self, zoom_start=14, zoom_control=False, scrollWheelZoom=False, dragging=False):

        allCoords = list(self.coords)
        latCenter = np.mean([coord[0] for coord in allCoords])
        longCenter = np.mean([coord[1] for coord in allCoords])

        map = folium.Map(location = [latCenter, longCenter], tiles='OpenStreetMap' , zoom_start = zoom_start, zoom_control=zoom_control, scrollWheelZoom=scrollWheelZoom, dragging=dragging)

        for coords in self.coords:
            map.add_child(folium.Marker(location = [coords[0], coords[1]], popup = 'test', icon = plugins.BeautifyIcon(icon_shape="circle-dot", border_color="blue") ))

        self.map = map