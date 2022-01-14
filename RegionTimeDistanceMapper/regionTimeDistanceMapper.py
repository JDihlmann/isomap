import os
import math
import folium
import geopandas
import googlemaps
import numpy as np
import pandas as pd
from folium import plugins
import matplotlib.pyplot as plt
from dotenv import load_dotenv
# from transportationType import TransportationType

radiusEarth = 6371

class RegionTimeDistanceMapper(object):

    def __init__(self, origin, bounds, gridSize):
        self.coordsGrid = None
        self.origin = origin
        self.bounds = bounds
        self.gridSize = gridSize

        # Setup Google Maps API
        load_dotenv()
        googleMapsAPIKey = os.getenv('GOOGLE_API_KEY')
        self.gmaps = googlemaps.Client(key=googleMapsAPIKey)
        # originWorldCoords = self.gmaps.geocode(self.origin)[0]['geometry']['location']
        # self.originCoords = (originWorldCoords['lat'], originWorldCoords['lng'])

        # Generate grid on world map and get coordinates
        self.originCoords = (48.5204712, 9.0533085)
        self.calculateCoordsGrid()
        self.generateMap()

       

    def getTimeDistanceFor(self, transportationType):
        self.detailFrame.updateColor()

    
    def calculateCoordsGrid(self):
        self.coordsGrid = []
        for x in np.linspace(-self.bounds[0], self.bounds[0], self.gridSize[0]):
            for y in np.linspace(-self.bounds[1], self.bounds[1], self.gridSize[1]):
                latCoord = self.originCoords[0] + (y / radiusEarth) * (180 / math.pi)
                longCord = self.originCoords[1] + (x / radiusEarth) * (180 / math.pi) / math.cos(self.originCoords[0])
                self.coordsGrid.append((latCoord, longCord))
    
    def generateMap(self):
        map = folium.Map(location = [self.originCoords[0], self.originCoords[1]], tiles='OpenStreetMap' , zoom_start = 14)

        counter = 0
        for coords in self.coordsGrid:
            counter+= 1
            map.add_child(folium.Marker(location = [coords[0], coords[1]], popup = 'test', icon = plugins.BeautifyIcon(icon_shape="circle-dot", border_color="blue") ))

        print(counter)    

        map.save('map.html')