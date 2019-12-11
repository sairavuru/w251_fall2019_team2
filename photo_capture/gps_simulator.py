# @Author: sai.ravuru
# @Date:   2019-12-02T11:42:19-08:00
# @Last modified by:   sai.ravuru
# @Last modified time: 2019-12-09T23:04:18-08:00

import pandas as pd
import numpy as np
import datetime
import geopy
from geopy import distance
import folium
from folium import IFrame
import base64
import osmnx as ox
#import shapely
#import geopandas as gpd
#from shapely.geometry import Point, Polygon
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

    #Street-level analysis using graph nodes
    try:
        graph = ox.graph_from_point(center_point = (gps_loc[0], gps_loc[1]), distance = 100)
        nodes, edges = ox.graph_to_gdfs(graph)
        nodes = nodes.dropna(subset=['maxspeed'])
        max_speed = min(nodes.loc[:, 'maxspeed'].apply(lambda x: int(str(x).split()[0])))

        if max_speed <= 40:
            sleepzone = 1
        else:
            sleepzone = 0

    except:
        sleepzone = 0
        max_speed = 60


    #<shapely polygon check>
    #coords = [(36.1521, -115.3838), (36.1521, -115.4076), (36.1301, -115.4076), (36.1301, -115.3838)]
    #poly = Polygon(coords)
    #poly_m = poly
    #crs = {'init': 'epsg:4326'}
    #polygon = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_geom])
    #poly_m = gpd.GeoDataFrame(index=[0], geometry=[poly])
    #poly_m.to_file(filename='polygon.geojson', driver='GeoJSON')


    # p1 = Point(gps_loc[0], gps_loc[1])
    # if p1.within(poly):
    #     sleepzone = 1

    return max_speed, sleepzone

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

    max_speed, sleepzone = sleep_zones(gps_loc)

    if speed > max_speed: #Speed check
        speedzone = 1
    else:
        speedzone = 0

    return speed, speedzone, sleepzone, max_speed

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
        try:
            encoded = base64.b64encode(open(list(point_dict.values())[i][2], 'rb').read())
            html = '<img src="data:image/png;base64,{}">'.format
            iframe = IFrame(html(encoded.decode('utf-8')), width=(width*resolution), height=(height*resolution))
            popup = folium.Popup(iframe, max_width=200)
            icon = folium.Icon(color='red')

        except:
            popup='<i>Speed is {} mph</i>'.format(int(point_dict[val][3]))
            icon = folium.Icon(color='green')

        folium.Marker([list(point_dict.values())[i][0],list(point_dict.values())[i][1]], popup=popup, tooltip=val, icon=icon).add_to(m)

    m.save('test.html')
    #webbrowser.open('test.html')

#if __name__ == "__main__":
def main():
    filename = '/usr/src/app/gps_logs.csv'
    gps_df = pd.read_csv(filename)
    gps_df.loc[:, 'Datetime'] = gps_df['Datetime'].apply(pd.to_datetime)
    #print(gps_df.head())

    speed_arr = [0]
    mph_arr = [0]
    point_dict = {}
    for i, row in gps_df.iterrows():
        #print(i, gps_df.shape[0])
        if i < gps_df.shape[0] - 1:
            gps_loc, gps_loc2, time_apart = gps_location(lat1=row['Latitude'], lon1=row['Longitude'], time1=row['Datetime'], \
            lat2=gps_df.loc[i+1,'Latitude'], lon2=gps_df.loc[i+1,'Longitude'], time2=gps_df.loc[i+1,'Datetime']) #Parse GPS locations and timestamps

            #print(gps_loc, gps_loc2, time_apart)
            speed, speedzone, sleepzone, max_speed = speed_compute(gps_loc, gps_loc2, time_apart) #Calculate speed, binary speed zone check, binary sleep zone check

            print('Max Speed[mph]: ', max_speed)
            print('Speed[mph]: ', speed)
            print('Speedzone?: ', speedzone)
            print('Sleepzone?: ', sleepzone)

            point_dict['Point '+str(i)] = [row['Latitude'], row['Longitude'], row['Image'], speed]
            speed_arr.append(speedzone)
            mph_arr.append(speed)


        else:
            print('End reached!')

    print(point_dict)
    gps_df.loc[:, 'Speed'] = speed_arr
    gps_df.loc[:, 'mph'] = [40 if x == 0 else x for x in mph_arr]

    gps_df.to_csv(filename, index=False)

    visual(point_dict) #Visualizes output into html
