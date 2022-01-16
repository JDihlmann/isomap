import os
import sys
from RegionElevationMapper.regionElevationMapper import RegionElevationMapper
from RegionTimeDistanceMapper.regionTimeDistanceMapper import TransportationType
from RegionElevatioDisplayer.regionElevationDisplayer import RegionElevationDisplayer
from RegionTimeDistanceMapper.regionTimeDistanceMapper import RegionTimeDistanceMapper
from RegionTimeDistanceDisplayer.regionTimeDistanceDisplayer import RegionTimeDistanceDisplayer


"""
Main File
Description:
Loads arguments from command line and starts up application.
"""

def main(argv):
    
    # Generating Data
    ''' regionTimeDistanceMapper = RegionTimeDistanceMapper(
        origin="Tübingen Rathaus",
        bounds=(0.8, 2.8),
        gridSize=(40, 40)
    ) '''

    # WARNING: API COST DO NOT UNCOMMENT
    ''' regionTimeDistanceMapper.generateDistanceTimeGridFor(transportationType=TransportationType.Bicycling) '''


    # Displaying Distance Data
    ''' regionTimeDistanceDisplayer = RegionTimeDistanceDisplayer(filename="/data/bicycling.json")
    regionTimeDistanceDisplayer.generateMap() '''

    # Generating Elevation Data
    ''' regionElevationMapper = RegionElevationMapper(filenames=["/data/bicycling.json", "/data/driving.json", "/data/walking.json"])
    regionElevationMapper.generateElevation() '''

    # Displaying Elevation Data
    regionElevationDisplayer = RegionElevationDisplayer()
    regionElevationDisplayer.generateMap()


if __name__ == "__main__":
    main(sys.argv[1:])