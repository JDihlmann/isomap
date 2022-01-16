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

radiusEarth = 6371
class TransportationType(Enum):
    Driving = 1
    Walking = 2
    Bicycling = 3

class RegionTimeDistanceMapper(object):

    def __init__(self, origin, bounds, gridSize):
        self.origin = origin
        self.bounds = bounds
        self.gridSize = gridSize

        # Setup Google Maps API
        load_dotenv()
        googleMapsAPIKey = os.getenv('GOOGLE_API_KEY')
        self.gmaps = googlemaps.Client(key=googleMapsAPIKey)
        originWorldCoords = self.gmaps.geocode(self.origin)[0]['geometry']['location']
        self.originCoords = (originWorldCoords['lat'], originWorldCoords['lng'])
        
        # Coords Grid
        self.coordsGrid = []
        for x in np.linspace(-self.bounds[0], self.bounds[0], self.gridSize[0]):
            for y in np.linspace(-self.bounds[1], self.bounds[1], self.gridSize[1]):
                latCoord = self.originCoords[0] + (y / radiusEarth) * (180 / math.pi)
                longCord = self.originCoords[1] + (x / radiusEarth) * (180 / math.pi) / math.cos(self.originCoords[0])
                self.coordsGrid.append((latCoord, longCord))

        # self.generateMap()
        # self.generateDistanceTimeGridFor(TransportationType.Driving)

    def generateDistanceTimeGridFor(self):
        
        # Query Google Maps API
        responses = []
        for coords in tqdm(self.coordsGrid):
            # print(str(self.originCoords[0]) + ", " + str(self.originCoords[1]) + " ::: " + str(coords[0]) + ", " + str(coords[1]))
            resp = self.gmaps.directions([self.originCoords[0], self.originCoords[1]], [coords[0], coords[1]], mode=transportationMode)
            resp[0]['search_coords'] = {"start_location": {"lat": self.originCoords[0], "lng": self.originCoords[1]}, "end_location": {"lat": coords[0], "lng": coords[1]}}
            responses.append(resp)

        # Save
        with open("" + transportationMode + ".json", 'w') as fout:
            json.dump(responses , fout)
    
    
    def generateMap(self):
        map = folium.Map(location = [self.originCoords[0], self.originCoords[1]], tiles='OpenStreetMap' , zoom_start = 14)

        for coords in self.coordsGrid:
            map.add_child(folium.Marker(location = [coords[0], coords[1]], popup = 'test', icon = plugins.BeautifyIcon(icon_shape="circle-dot", border_color="blue") ))

        map.save("index.html")