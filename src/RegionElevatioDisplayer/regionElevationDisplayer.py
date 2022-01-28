import os
import json
import math
import folium
import numpy as np
from os import path
import pandas as pd
from tqdm import tqdm
from enum import Enum
from folium import plugins
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import tilemapbase
import matplotlib.tri as tri
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from PIL import ImageOps
from tueplots import bundles
from mpl_toolkits.axes_grid1 import make_axes_locatable



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

            map.add_child(folium.Marker(location = coords, popup = 'Height: ' + str(elevation) + 'm', icon = plugins.BeautifyIcon(icon_shape="circle-dot", border_color=rgb) ))

        self.map = map

    def generateInterpolationPlot(self, ax, title, originElvevation = 337.0936584472656, mapDelta=[0.0015, 0.0015], interpolationMethode='cubic', cmap='Reds', contourDivisions=10):
        plt.rcParams.update(bundles.neurips2021(usetex=False))

        values = self.elevations
        elevations = self.elevations
        coords = self.coords
        originCoords = self.originCoords

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
        pCoordsLower = []
        elevationLower = []
        for i in range(len(coords)):
            coord = coords[i]
            elevation = elevations[i]
            x, y = tilemapbase.project(coord[1], coord[0])
            pCoords.append((x, y))

            if elevation < originElvevation:
                pCoordsLower.append((x, y))
                elevationLower.append(elevation)

        pLats = np.array(pCoords)[:,0]
        pLons = np.array(pCoords)[:,1]


        # Generate grid
        gridDivision = 1000j
        gridX, gridY = np.mgrid[pLats.min():pLats.max():gridDivision, pLons.min():pLons.max():gridDivision]
        grid = griddata(pCoords, values, (gridX, gridY), method=interpolationMethode)

        # Plot filled contours
        dmin = np.array(values).min()
        dmax = np.array(values).max()
        step = math.ceil((dmax - dmin) / contourDivisions)
        levels = np.arange(dmin, dmax + step, step ) 
        contours = ax.contourf(gridX, gridY, grid, levels=levels, alpha=1, cmap=cmap) 

        # Plot colour bars
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = plt.colorbar(contours, cax=cax, orientation='vertical')
        cbar.ax.set_ylabel('Height [meters]')
        

        # Plot map 
        scale = 2 ** plotter.zoom
        tile = plotter.as_one_image(False)
        tile = ImageOps.grayscale(tile)
        x0, y0 = plotter.extent.project(plotter.xtilemin / scale, plotter.ytilemin / scale)
        x1, y1 = plotter.extent.project((plotter.xtilemax + 1) / scale, (plotter.ytilemax + 1) / scale)
        ax.imshow(tile, interpolation="lanczos", extent=(x0,x1,y1,y0), zorder = 2, alpha=0.8, cmap='gray')
        ax.set(xlim = plotter.extent.xrange, ylim = plotter.extent.yrange) 

        # Plot contours on top
        contours = ax.contour(gridX, gridY, grid, levels=levels, alpha=0.7, colors="black", linewidths=0.1) 

        # Plot lower points
        pOriginCoords = tilemapbase.project(originCoords[1], originCoords[0])
        ax.scatter(np.array(pCoordsLower)[:,0], np.array(pCoordsLower)[:,1], c=elevationLower, cmap="Purples_r", marker=".", s=0.4, zorder=3)
    