# @Author: sai.ravuru
# @Date:   2019-12-02T11:42:19-08:00
# @Last modified by:   sai.ravuru
# @Last modified time: 2019-12-09T08:37:52-08:00

import pandas as pd
import numpy as np
import datetime
import geopy
from geopy import distance
import folium
from folium import IFrame
import base64
import shapely
#import geopandas as gpd
from shapely.geometry import Point, Polygon
#import webbrowser, os


def gps_location(lat1, lon1, time1, lat2, lon2, time2):
    '''Function to read and parse GPS coordinates.
    INPUTS:
    lat1 - Latitude 1
    lon1 - Longitude 1
    time1 - Timestamp 1
    lat2 - Latitude 2
    lon2 - Longitude 2
    time2 - Timestamp 2
    '''

    # gps_loc = [36.1526, -115.3672] #1st GPS interrogation
    # gps_loc2 = [36.153, -115.3672] #2nd GPS interrogation
    # time_apart = 2 #seconds
    #print(lat1, lon1, time1, lat2, lon2, time2)
    gps_loc = [lat1, lon1] #1st GPS interrogation
    gps_loc2 = [lat2, lon2] #2nd GPS interrogation
    time_apart = pd.Timedelta(time2 - time1).seconds/3600 #hours

    return gps_loc, gps_loc2, time_apart


def sleep_zones(gps_loc):
    '''Function to compare gps location against sleep zones.
    INPUTS:
    gps_loc - gps location [latitude, longitude]
    '''

    sleepzone = 0
    #<shapely polygon check required>
    coords = [(36.1521, -115.3838), (36.1521, -115.4076), (36.1301, -115.4076), (36.1301, -115.3838)]
    poly = Polygon(coords)
    poly_m = poly
    #crs = {'init': 'epsg:4326'}
    #polygon = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_geom])
    #poly_m = gpd.GeoDataFrame(index=[0], geometry=[poly])
    #poly_m.to_file(filename='polygon.geojson', driver='GeoJSON')


    p1 = Point(gps_loc[0], gps_loc[1])
    if p1.within(poly):
        sleepzone = 1

    return poly_m, sleepzone

def speed_compute(gps_loc, gps_loc2, time_apart):
    '''Function to use 2 gps coordinates to calculate speed
    INPUTS:
    gps_loc - gps location [latitude, longitude]
    gps_loc2 - gps location 2 [latitude, longitude]
    time_apart - time between points in hours
    '''

    dist = distance.distance(gps_loc, gps_loc2).miles
    if (dist == 0) | (time_apart == 0):
        speed = 0
    else:
        speed = dist/time_apart

    poly_m, sleepzone = sleep_zones(gps_loc)

    if speed > 80: #Speed check
        speedzone = 1
    else:
        speedzone = 0

    return speed, speedzone, sleepzone, poly_m

def visual(point_dict):
    '''Function to map GPS coordinates and picture onto map
    INPUTS:
    point_dict - dictionary of points {Point: [Latitude, Longitude, Picture, Speed]}
    '''
    width = 200
    height = 5
    resolution = 50

    m = folium.Map(location=[list(point_dict.values())[0][0],list(point_dict.values())[0][1]], zoom_start=12)


    for i, val in enumerate(list(point_dict.keys())):
        encoded = base64.b64encode(open(list(point_dict.values())[i][2], 'rb').read())
        html = '<img src="data:image/png;base64,{}">'.format
        iframe = IFrame(html(encoded.decode('utf-8')), width=(width*resolution), height=(height*resolution))
        popup = folium.Popup(iframe, max_width=200)

        tooltip = val
        #folium.Marker([list(point_dict.values())[i][0],list(point_dict.values())[i][1]], popup='<i>'+val+'</i>', tooltip=tooltip).add_to(m)
        folium.Marker([list(point_dict.values())[i][0],list(point_dict.values())[i][1]], popup=popup, tooltip=tooltip).add_to(m)
        #folium.GeoJson(poly).add_to(m)
        #folium.LatLngPopup().add_to(m)
    m.save('test.html')
    #webbrowser.open('test.html')

if __name__ == "__main__":
    filename = 'gps_logs.csv'
    gps_df = pd.read_csv(filename)
    gps_df.loc[:, 'Datetime'] = gps_df['Datetime'].apply(pd.to_datetime)
    #print(gps_df.head())

    point_dict = {}
    for i, row in gps_df.iterrows():
        #print(i, gps_df.shape[0])
        if i < gps_df.shape[0] - 1:
            gps_loc, gps_loc2, time_apart = gps_location(lat1=row['Latitude'], lon1=row['Longitude'], time1=row['Datetime'], \
            lat2=gps_df.loc[i+1,'Latitude'], lon2=gps_df.loc[i+1,'Longitude'], time2=gps_df.loc[i+1,'Datetime']) #Parse GPS locations and timestamps

            #print(gps_loc, gps_loc2, time_apart)
            speed, speedzone, sleepzone, poly = speed_compute(gps_loc, gps_loc2, time_apart) #Calculate speed, binary speed zone check, binary sleep zone check

            print('Speed[mph]: ', speed)
            print('Speedzone?: ', speedzone)
            print('Sleepzone?: ', sleepzone)

            point_dict['Point '+str(i)] = [row['Latitude'], row['Longitude'], row['Image'], speed]
        else:
            print('End reached!')

    print(point_dict)
    visual(point_dict) #Visualizes output into html
