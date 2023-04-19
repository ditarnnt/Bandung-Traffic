import pandas as pd
import numpy as np
import json
import pickle
import datetime
import geopandas as gpd
# from shapely.geometry import Point, LineString,MultiLineString,Polygon
# from shapely import ops
import matplotlib.pyplot as plt
# %matplotlib inline
import os
import folium
import streamlit as st

attr='(c) <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors (c) <a href="http://cartodb.com/attributions">CartoDB</a>, CartoDB <a href ="http://cartodb.com/attributions">attributions</a>'
# from selenium import webdriver
# import PIL
# import PIL.Image as Image
# import PIL.ImageDraw as ImageDraw
# import PIL.ImageFont as ImageFont
import glob
# import moviepy.editor as mpy
# from flask import request

# from shapely.geometry import Point, LineString
import geopandas as gpd

import pandas as pd
import json

def dataframe(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    rows = []
    for result in data['results']:
        location = result['location']
        description = location.get('description', None) # use the .get() method to avoid KeyError
        length = location.get('length', None) # use the .get() method to avoid KeyError
        links = location['shape']['links']
        latitudes = []
        longitudes = []
        for link in links:
            if 'points' in link:
                for point in link['points']:
                    latitudes.append(point['lat'])
                    longitudes.append(point['lng'])
        currentFlow = result.get('currentFlow', {})
        speed = currentFlow.get('speed', None) # use the .get() method to avoid KeyError
        freeflow = currentFlow.get('freeFlow', None) # use the .get() method to avoid KeyError
        jamfactor = currentFlow.get('jamFactor', None) # use the .get() method to avoid KeyError
        rows.append([description, length, latitudes, longitudes, speed, freeflow, jamfactor])

    return pd.DataFrame(rows, columns=['Description', 'Length', 'Latitudes', 'Longitudes', 'Speed', 'FreeFlow', 'JamFactor'])

def process_here_maps_outputs(directory_path):
    # Get a list of all JSON files in the directory
    json_files = glob.glob(os.path.join(directory_path, '*.json'))

    # Define empty DataFrame before the loop
    df = pd.DataFrame(columns=['Time', 'Date', 'Day', 'Description', 'Length', 'Latitudes', 'Longitudes', 'Speed', 'FreeFlow', 'JamFactor'])
    error_count = 0
    error_files = []
    
    for json_file in json_files:
        # Get the filename and parse the date and time
        filename = os.path.basename(json_file)
        date, time = os.path.splitext(filename)[0].split()
        year, month, day = date.split('-')
        hour, minute, second = time.split('-')
        
        # Get the day of the week as a string
        day_of_week = datetime.datetime(int(year), int(month), int(day)).strftime('%A')
        
        # Process each JSON file using the existing logic
        try: 
            df_temp = dataframe(json_file)
            print(f'{filename} ok dataframe')
        except:
            print(f'{filename} error dataframe')
            error_count += 1
            error_files.append(filename)
            continue
        
        # Add the date, time, and day columns to the DataFrame
        df_temp['Date'] = date
        df_temp['Time'] = time
        df_temp['Day'] = day_of_week
        
        # Append to the DataFrame after processing each file
        df = pd.concat([df, df_temp])
    
    print(f'Total number of error files: {error_count}')  
    print("Files with errors:")
    print(error_files)
    return df

#to make dataframe
df_00 = process_here_maps_outputs('E:/FASTRACK/SMT10/Bandung-Traffic/json_00')

#to make tab for traffic jam factor
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(['Monday', 'Tuesday', 'Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday' ])

with tab1:
    df_senin = df_00.loc[df_00['Day'] == 'Monday']
    df_senin_mean = df_senin.groupby('Time')[['JamFactor']].mean()
    st.header('Monday')
    st.bar_chart(df_senin_mean)

with tab2:
    df_selasa = df_00.loc[df_00['Day'] == 'Tuesday']
    df_selasa_mean = df_selasa.groupby('Time')[['JamFactor']].mean()
    st.header('Tuesday')
    st.bar_chart(df_selasa_mean)

with tab3:
    df_rabu = df_00.loc[df_00['Day'] == 'Wednesday']
    df_rabu_mean = df_rabu.groupby('Time')[['JamFactor']].mean()
    st.header('Wednesday')
    st.bar_chart(df_rabu_mean)

with tab4:
    df_kamis = df_00.loc[df_00['Day'] == 'Thursday']
    df_kamis_mean = df_kamis.groupby('Time')[['JamFactor']].mean()
    st.header('Thursday')
    st.bar_chart(df_kamis_mean)

with tab5:
    df_jumat = df_00.loc[df_00['Day'] == 'Friday']
    df_jumat_mean = df_jumat.groupby('Time')[['JamFactor']].mean()
    st.header('Friday')
    st.bar_chart(df_jumat_mean)

with tab6:
    df_sabtu = df_00.loc[df_00['Day'] == 'Saturday']
    df_sabtu_mean = df_sabtu.groupby('Time')[['JamFactor']].mean()
    st.header('Saturday')
    st.bar_chart(df_sabtu_mean)

with tab7:
    df_minggu = df_00.loc[df_00['Day'] == 'Sunday']
    df_minggu_mean = df_minggu.groupby('Time')[['JamFactor']].mean()
    st.header('Sunday')
    st.bar_chart(df_minggu_mean)