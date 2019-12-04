# @Author: sai.ravuru
# @Date:   2019-12-02T11:42:19-08:00
# @Last modified by:   sai.ravuru
# @Last modified time: 2019-12-04T14:51:22-08:00

import pandas as pd
import numpy as np
import datetime
import geopy
from geopy import distance
import folium
import shapely
#import geopandas as gpd
from shapely.geometry import Point, Polygon
#import webbrowser, os

def gps_location():

    gps_loc = [36.1526, -115.3672] #1st GPS interrogation
    gps_loc2 = [36.153, -115.3672] #2nd GPS interrogation
    time_apart = 2 #seconds

    return gps_loc, gps_loc2, time_apart


def sleep_zones(gps_loc):

    sleepzone = 0
    #<shapely polygon check required>
    coords = [(36.1521, -115.3838), (36.1521, -115.4076), (36.1301, -115.4076), (36.1301, -115.3838)]
    poly = Polygon(coords)
    poly_m = 0
    #crs = {'init': 'epsg:4326'}
    #polygon = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_geom])
    #poly_m = gpd.GeoDataFrame(index=[0], geometry=[poly])
    #poly_m.to_file(filename='polygon.geojson', driver='GeoJSON')


    p1 = Point(gps_loc[0], gps_loc[1])
    if p1.within(poly):
        sleepzone = 1

    return poly_m, sleepzone

def speed(gps_loc, gps_loc2, time_apart):
    dist = distance.distance(gps_loc, gps_loc2).miles
    speed = dist/(time_apart/3600)

    poly_m, sleepzone = sleep_zones(gps_loc)

    if speed > 80:
        speedzone = 1
    else:
        speedzone = 0

    return speed,speedzone, sleepzone

def visual(gps_loc):
    m = folium.Map(location=gps_loc, zoom_start=15)
    tooltip = 'Start Location'

    folium.Marker(gps_loc, popup='<i>Start</i>', tooltip=tooltip).add_to(m)
    #folium.GeoJson(poly_m).add_to(m)
    m.save('test.html')
    #webbrowser.open('test.html')

gps_loc, gps_loc2, time_apart = gps_location()
speed, speedzone, sleepzone = speed(gps_loc, gps_loc2, time_apart)
print('Speed[mph]: ', speed)
print('Speedzone?: ', speedzone)
print('Sleepzone?: ', sleepzone)
visual(gps_loc)
