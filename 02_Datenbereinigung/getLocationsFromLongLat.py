"""

@author: Joshua Hammesfahr
"""

#Purpose: Enrich geo information in crash data set with geo information from Google Maps Geocode API

import pandas as pd
import utm # package to generate lat long from given data -
import geopandas as gpd
import requests

from pyproj import Proj

def get_lat_long(df: object):
    myProj = Proj(init="epsg:5555", proj="utm")
    df['LON'], df['LAT'] = myProj(mergedData['LINREFX'].values, mergedData['LINREFY'].values, inverse=True)
    return df
    
mergedData = gpd.read_file('U_VM_A_L_BRW_TL.geojson')
pd.options.display.float_format = '{0:.10f}'.format
mergedData = get_lat_long(mergedData)

import json

#coord = get_lat_long(mergedData)
#mergedDataEntity = mergedData.iloc[0,:]
#queryParameter = 'latlng=' + str(mergedDataEntity['LAT']) + ',' + str(mergedDataEntity['LON'])

df = pd.DataFrame(columns = ["OBJECTID","LAT","LON","formatted_address","address_components"])
mergedData = mergedData.loc[:,["OBJECTID","LAT","LON"]]

for index, row in mergedData.iterrows():
    print(index)
    queryParameter = 'latlng=' + str(row['LAT']) + ',' + str(row['LON'])
    key = '[]'
    geoDataRequest = requests.get('https://maps.googleapis.com/maps/api/geocode/json?' + queryParameter + key)
    if (len(geoDataRequest.json()["results"]) != 0):    
        address_components = geoDataRequest.json()["results"][0]["address_components"]
        address_components_as_string = json.dumps(address_components)
        formatted_address = geoDataRequest.json()["results"][0]["formatted_address"]  
        row = row.append(pd.Series(address_components_as_string,["address_components"]))
        row = row.append(pd.Series(formatted_address,["formatted_address"]))
        df = df.append(row, ignore_index=True)
        
rzmerged = rzmerged.append(df, ignore_index=True, sort=True)

rzmerged.to_csv(current_directory + "src/geo_information.csv", sep=";" )


   