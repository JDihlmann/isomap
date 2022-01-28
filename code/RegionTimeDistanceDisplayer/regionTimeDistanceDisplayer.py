import os
import json
import math
import folium
import numpy as np
from os import path
import pandas as pd
from time import time
from enum import Enum
from folium import plugins
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import tilemapbase
import matplotlib.tri as tri
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from PIL import ImageOps
from tueplots import bundles
from mpl_toolkits.axes_grid1 import make_axes_locatable

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

            map.add_child(folium.Marker(location = coords, popup = 'Duration: ' + str(duration / 60) + 'min', icon = plugins.BeautifyIcon(icon_shape="circle-dot", border_color=rgb) ))

        self.map = map
        # map.save( transportationMode + '.html')

    def generateInterpolationPlot(self, ax, title, mapDelta=[0.0015, 0.0015], interpolationMethode='cubic', cmap='magma_r', contourDivisions=10, maxValue=None, minValue=None):
        plt.rcParams.update(bundles.neurips2021(usetex=False))

        coords = self.coords
        durations = self.durations
        originCoords = self.originCoords

        # Map duration to minutes
        values = []
        for duration in durations:
            values.append(duration / 60)

        # Plot settings
        ax.set_title(title)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

        # Build tilemap 
        tm = tilemapbase.tiles.Carto_Light
        latBounds = (np.array(coords)[:,0].min() + mapDelta[0], np.array(coords)[:,0].max() - mapDelta[0])
        lonBounds = (np.array(coords)[:,1].min() + mapDelta[1], np.array(coords)[:,1].max() - mapDelta[1])
        extent = tilemapbase.Extent.from_lonlat(lonBounds[0], lonBounds[1], latBounds[0], latBounds[1])
        extent = extent.to_aspect(1.0)
        plotter = tilemapbase.Plotter(extent, tm,  zoom=13)

        # Project Coords
        pCoords = []
        for coord in coords:
            x, y = tilemapbase.project(coord[1], coord[0])
            pCoords.append((x, y))
        pLats = np.array(pCoords)[:,0]
        pLons = np.array(pCoords)[:,1]


        # Generate grid
        gridDivision = 1000j
        gridX, gridY = np.mgrid[pLats.min():pLats.max():gridDivision, pLons.min():pLons.max():gridDivision]
        grid = griddata(pCoords, values, (gridX, gridY), method=interpolationMethode)

        # Plot filled contours
        dmax = np.array(values).max() if maxValue == None else maxValue
        step = math.ceil(dmax  / contourDivisions)
        levels = np.arange(0, dmax + step, step ) 
        contours = ax.contourf(gridX, gridY, grid, levels=levels, alpha=1, cmap=cmap) 

        # Plot colour bars
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = plt.colorbar(contours, cax=cax, orientation='vertical', alpha=0.6)
        cbar.ax.set_ylabel('Duration [minutes]')
        
        # Plot map 
        scale = 2 ** plotter.zoom
        tile = plotter.as_one_image(False)
        tile = ImageOps.grayscale(tile)
        x0, y0 = plotter.extent.project(plotter.xtilemin / scale, plotter.ytilemin / scale)
        x1, y1 = plotter.extent.project((plotter.xtilemax + 1) / scale, (plotter.ytilemax + 1) / scale)
        ax.imshow(tile, interpolation="lanczos", extent=(x0,x1,y1,y0), zorder = 2, alpha=0.6, cmap='gray')
        ax.set(xlim = plotter.extent.xrange, ylim = plotter.extent.yrange) 

        # Plot contours on top
        contours = ax.contour(gridX, gridY, grid, levels=levels, alpha=0.7, colors="black", linewidths=0.1) 

        # Plot center point
        pOriginCoords = tilemapbase.project(originCoords[1], originCoords[0])
        ax.scatter([pOriginCoords[0]], [pOriginCoords[1]], color="black", marker=".", s=0.8, zorder=3)