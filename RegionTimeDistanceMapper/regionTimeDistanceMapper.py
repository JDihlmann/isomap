import os
import googlemaps
from dotenv import load_dotenv
# from transportationType import TransportationType

class RegionTimeDistanceMapper(object):

    def __init__(self, origin, bounds, gridSize):
        self.origin = origin
        self.bounds = bounds
        self.gridSize = gridSize

        # Setup Google Maps API
        load_dotenv()
        googleMapsAPIKey = os.getenv('GOOGLE_API_KEY')
        self.gmaps = googlemaps.Client(key=googleMapsAPIKey)
        self.originCoords = self.gmaps.geocode(self.origin)[0]['geometry']['location']
        print(self.originCoords)

        # Generate grid on world map and get coordinates
        
       

    def getTimeDistanceFor(self, transportationType):
        self.detailFrame.updateColor()