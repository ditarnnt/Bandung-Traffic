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
import altair as alt
import plotly.express as px
attr='(c) <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors (c) <a href="http://cartodb.com/attributions">CartoDB</a>, CartoDB <a href ="http://cartodb.com/attributions">attributions</a>'
import geopandas as gpd
import pandas as pd
import json
#read csv 
import pandas as pd
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

df_00 = pd.read_csv('traffic_bandung_00_v2.csv',sep=',')
df_00_lebaran = pd.read_csv('traffic_bandung_00_lebaran.csv',sep=',')
df_00_pre = pd.read_csv('traffic_bandung_00_pre.csv',sep=',')
df_00_post = pd.read_csv('traffic_bandung_00_post.csv',sep=',')

st.set_page_config(layout="wide")

tab_puasa,tab_lebaran = st.tabs(['Puasa Traffic', 'Pre and Lebaran Traffic'])

df_00['Time'] = pd.to_datetime(df_00['Time'], format='%H-%M-%S')
df_00['Hour'] = df_00['Time'].dt.hour
df_00['Time Range'] = df_00['Time'].apply(lambda x:f"0-{x.hour}" if x.hour < 12 else f"12-{x.hour-12}")

df_00_lebaran['Time'] = pd.to_datetime(df_00_lebaran['Time'], format='%H-%M-%S')
df_00_lebaran['Hour'] = df_00_lebaran['Time'].dt.hour
df_00_lebaran['Time Range'] = df_00_lebaran['Time'].apply(lambda x:f"0-{x.hour}" if x.hour < 12 else f"12-{x.hour-12}")

df_00_pre['Time'] = pd.to_datetime(df_00_pre['Time'], format='%H-%M-%S')
df_00_pre['Hour'] = df_00_pre['Time'].dt.hour
df_00_pre['Time Range'] = df_00_pre['Time'].apply(lambda x:f"0-{x.hour}" if x.hour < 12 else f"12-{x.hour-12}")

df_00_post['Time'] = pd.to_datetime(df_00_post['Time'], format='%H-%M-%S')
df_00_post['Hour'] = df_00_post['Time'].dt.hour
df_00_post['Time Range'] = df_00_post['Time'].apply(lambda x:f"0-{x.hour}" if x.hour < 12 else f"12-{x.hour-12}")

with tab_puasa:
        #TRAFFIC DISTRIBUTION
        st.title ("Road Line Trend Traffic Puasa")
        video_file = open('puasa.mp4', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
    

        # JAM FACTOR DISTRIBUTION
        st.header("Jam Factor Distribution Throught Time ")
        senin, selasa, rabu, kamis, jumat, sabtu, minggu = st.tabs(['Monday', 'Tuesday', 'Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday'])
        with senin:
            left, right = st.columns ([1,1])
            with left:
                df_senin = df_00.loc[df_00['Day'] == 'Monday']
                df_senin_mean = df_senin.groupby('Time')[['JamFactor']].mean()
                st.header('Monday')
                st.line_chart(df_senin_mean)

                #TOP 5 - Senin
                time_range_senin = st.slider('Select time range here:', 0, 23, (8, 18), 1)
                # Filter the data based on the selected inputs
                filtered_data_senin = df_00[ 
                                (df_00['Day'] == 'Monday') & 
                                (df_00['Hour'] >= time_range_senin[0]) & 
                                (df_00['Hour'] <= time_range_senin[1])]

                # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
                grouped_data_senin = filtered_data_senin.groupby(['Description','Hour'])[['JamFactor']].max().reset_index()
                top_5_data_senin = grouped_data_senin.sort_values(['Hour', 'JamFactor'], ascending=[True, False]).groupby('Hour').head(5)
            
            with right:
                chart_senin = alt.Chart(top_5_data_senin).mark_bar().encode(
                    y=alt.Y('Description:O', sort='-x'),#alt.EncodingSortField(field='Description',order='ascending')),
                    x='JamFactor:Q',
                    color='Description:N',
                    tooltip =['Description:N', 'JamFactor:Q']
                ).properties(
                    width=800,
                    height=500,
                    title = f"Top Crowded Locations by Hour on Monday"
                ).interactive()

                st.altair_chart(chart_senin, use_container_width=True)


        with selasa:
            left, right = st.columns([1,1])
            with left:
                df_selasa = df_00.loc[df_00['Day'] == 'Tuesday']
                df_selasa_mean = df_selasa.groupby('Time')[['JamFactor']].mean()
                st.header('Tuesday')
                st.line_chart(df_selasa_mean)

                #TOP 5 - Selasa
                time_range_selasa = st.slider('Select time range here: ', 0, 23, (8, 18), 1)
                # Filter the data based on the selected inputs
                filtered_data_selasa = df_00[ 
                                (df_00['Day'] == 'Tuesday') & 
                                (df_00['Hour'] >= time_range_selasa[0]) & 
                                (df_00['Hour'] <= time_range_selasa[1])]

                # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
                grouped_data_selasa = filtered_data_selasa.groupby(['Description','Hour'])[['JamFactor']].max().reset_index()
                top_5_data_selasa = grouped_data_selasa.sort_values(['Hour', 'JamFactor'], ascending=[True, False]).groupby('Hour').head(5)
            
            with right:
                chart_selasa = alt.Chart(top_5_data_selasa).mark_bar().encode(
                    y=alt.Y('Description:O', sort='-x'),#alt.EncodingSortField(field='Description',order='ascending')),
                    x='JamFactor:Q',
                    color='Description:N',
                    tooltip =['Description:N', 'JamFactor:Q']
                ).properties(
                    width=800,
                    height=500,
                    title = f"Top Crowded Locations by Hour on Tuesday"
                ).interactive()

                st.altair_chart(chart_selasa, use_container_width=True)


        with rabu:
            left, right = st.columns([1,1])
            with left:
                df_rabu = df_00.loc[df_00['Day'] == 'Wednesday']
                df_rabu_mean = df_rabu.groupby('Time')[['JamFactor']].mean()
                st.header('Wednesday')
                st.line_chart(df_rabu_mean)
           
                time_range_rabu = st.slider('Select time range here:  ', 0, 23, (8, 18), 1)
                # Filter the data based on the selected inputs
                filtered_data_rabu = df_00[ 
                                (df_00['Day'] == 'Wednesday') & 
                                (df_00['Hour'] >= time_range_rabu[0]) & 
                                (df_00['Hour'] <= time_range_rabu[1])]

                # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
                grouped_data_rabu = filtered_data_rabu.groupby(['Description','Hour'])[['JamFactor']].max().reset_index()
                top_5_data_rabu = grouped_data_rabu.sort_values(['Hour', 'JamFactor'], ascending=[True, False]).groupby('Hour').head(5)
            
            with right:
                chart_rabu = alt.Chart(top_5_data_rabu).mark_bar().encode(
                    y=alt.Y('Description:O', sort='-x'),#alt.EncodingSortField(field='Description',order='ascending')),
                    x='JamFactor:Q',
                    color='Description:N',
                    tooltip =['Description:N', 'JamFactor:Q']
                ).properties(
                    width=800,
                    height=500,
                    title = f"Top Crowded Locations by Hour on Wednesday"
                ).interactive()

                st.altair_chart(chart_rabu, use_container_width=True)


        with kamis:
            left, right = st.columns([1,1])
            with left:
                df_kamis = df_00.loc[df_00['Day'] == 'Thursday']
                df_kamis_mean = df_kamis.groupby('Time')[['JamFactor']].mean()
                st.header('Thursday')
                st.line_chart(df_kamis_mean)

                time_range_kamis = st.slider('Select time range here:   ', 0, 23, (8, 18), 1)
                # Filter the data based on the selected inputs
                filtered_data_kamis = df_00[ 
                                (df_00['Day'] == 'Thursday') & 
                                (df_00['Hour'] >= time_range_kamis[0]) & 
                                (df_00['Hour'] <= time_range_kamis[1])]

                # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
                grouped_data_kamis = filtered_data_kamis.groupby(['Description','Hour'])[['JamFactor']].max().reset_index()
                top_5_data_kamis = grouped_data_kamis.sort_values(['Hour', 'JamFactor'], ascending=[True, False]).groupby('Hour').head(5)
            
            with right:
                chart_kamis = alt.Chart(top_5_data_kamis).mark_bar().encode(
                    y=alt.Y('Description:O', sort='-x'),#alt.EncodingSortField(field='Description',order='ascending')),
                    x='JamFactor:Q',
                    color='Description:N',
                    tooltip =['Description:N', 'JamFactor:Q']
                ).properties(
                    width=800,
                    height=500,
                    title = f"Top Crowded Locations by Hour on Thursday"
                ).interactive()

                st.altair_chart(chart_kamis, use_container_width=True)


        with jumat:
            left, right = st.columns([1,1])
            with left:
                df_jumat = df_00.loc[df_00['Day'] == 'Friday']
                df_jumat_mean = df_jumat.groupby('Time')[['JamFactor']].mean()
                st.header('Friday')
                st.line_chart(df_jumat_mean)

                time_range_sabtu = st.slider('Select time range here:     ', 0, 23, (8, 18), 1)
                # Filter the data based on the selected inputs
                filtered_data_jumat = df_00[ 
                                (df_00['Day'] == 'Friday') & 
                                (df_00['Hour'] >= time_range_kamis[0]) & 
                                (df_00['Hour'] <= time_range_kamis[1])]

                # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
                grouped_data_jumat = filtered_data_jumat.groupby(['Description','Hour'])[['JamFactor']].max().reset_index()
                top_5_data_jumat = grouped_data_jumat.sort_values(['Hour', 'JamFactor'], ascending=[True, False]).groupby('Hour').head(5)
            
            with right:
                chart_jumat = alt.Chart(top_5_data_jumat).mark_bar().encode(
                    y=alt.Y('Description:O', sort='-x'),#alt.EncodingSortField(field='Description',order='ascending')),
                    x='JamFactor:Q',
                    color='Description:N',
                    tooltip =['Description:N', 'JamFactor:Q']
                ).properties(
                    width=800,
                    height=500,
                    title = f"Top Crowded Locations by Hour on Friday"
                ).interactive()

                st.altair_chart(chart_jumat, use_container_width=True)


        with sabtu:
            left, right = st.columns([1,1])
            with left:
                df_sabtu = df_00.loc[df_00['Day'] == 'Saturday']
                df_sabtu_mean = df_sabtu.groupby('Time')[['JamFactor']].mean()
                st.header('Saturday')
                st.line_chart(df_sabtu_mean)

                time_range_sabtu = st.slider('Select time range here:       ', 0, 23, (8, 18), 1)
                # Filter the data based on the selected inputs
                filtered_data_sabtu = df_00[ 
                                (df_00['Day'] == 'Saturday') & 
                                (df_00['Hour'] >= time_range_kamis[0]) & 
                                (df_00['Hour'] <= time_range_kamis[1])]

                # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
                grouped_data_sabtu = filtered_data_kamis.groupby(['Description','Hour'])[['JamFactor']].max().reset_index()
                top_5_data_sabtu = grouped_data_sabtu.sort_values(['Hour', 'JamFactor'], ascending=[True, False]).groupby('Hour').head(5)
            
            with right:
                chart_sabtu = alt.Chart(top_5_data_sabtu).mark_bar().encode(
                    y=alt.Y('Description:O', sort='-x'),#alt.EncodingSortField(field='Description',order='ascending')),
                    x='JamFactor:Q',
                    color='Description:N',
                    tooltip =['Description:N', 'JamFactor:Q']
                ).properties(
                    width=800,
                    height=500,
                    title = f"Top Crowded Locations by Hour on Saturday"
                ).interactive()

                st.altair_chart(chart_sabtu, use_container_width=True)


        with minggu:
            left, right = st.columns([1,1])
            with left:
                df_minggu = df_00.loc[df_00['Day'] == 'Sunday']
                df_minggu_mean = df_minggu.groupby('Time')[['JamFactor']].mean()
                st.header('Sunday')
                st.line_chart(df_minggu_mean)

                time_range_minggu = st.slider('Select time range here:                 ', 0, 23, (8, 18), 1)
                # Filter the data based on the selected inputs
                filtered_data_minggu = df_00[ 
                                (df_00['Day'] == 'Sunday') & 
                                (df_00['Hour'] >= time_range_minggu[0]) & 
                                (df_00['Hour'] <= time_range_minggu[1])]

                # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
                grouped_data_minggu = filtered_data_minggu.groupby(['Description','Hour'])[['JamFactor']].max().reset_index()
                top_5_data_minggu = grouped_data_minggu.sort_values(['Hour', 'JamFactor'], ascending=[True, False]).groupby('Hour').head(5)
            
            with right:
                chart_minggu = alt.Chart(top_5_data_minggu).mark_bar().encode(
                    y=alt.Y('Description:O', sort='-x'),#alt.EncodingSortField(field='Description',order='ascending')),
                    x='JamFactor:Q',
                    color='Description:N',
                    tooltip =['Description:N', 'JamFactor:Q']
                ).properties(
                    width=800,
                    height=500,
                    title = f"Top Crowded Locations by Hour on Sunday"
                ).interactive()

                st.altair_chart(chart_minggu, use_container_width=True)
      

        # AREA MAP KECAMATAN DISTRIBUTION
        left,right = st.columns([1,2])

        with left:
        # Load data
            df = pd.read_csv('new_file.csv', sep =',')

            # Selectbox day
            days = df['Day'].unique()
            day_filter = st.selectbox('Select day here', days)

            df['Time'] = pd.to_datetime(df['Time'], format='%H-%M-%S')
            df['Hour'] = df['Time'].dt.hour

            df['Time Range'] = df['Time'].apply(lambda x:f"0-{x.hour}" if x.hour < 12 else f"12-{x.hour-12}")

            # Slider for time
            time_filter = st.slider('Select time range here', 0, 23, (8, 18), 1)

            # Filter the data based on the selected inputs
            filtered_data = df[(df['Day'] == day_filter) & (df['Hour'] >= time_filter[0]) & (df['Hour'] <= time_filter[1])]

            #grouped_heatmap = filtered_data_3.groupby('Time Range','Kecamatan')


        with right:
        # Create the heatmap
            fig = px.density_mapbox(filtered_data, lat='latitude_kecamatan', lon='longitude_kecamatan', z='JamFactor',
                                    radius=15, center=dict(lat=-6.91474, lon=107.60981), zoom=10, mapbox_style='carto-positron',
                                    hover_name='Kecamatan', hover_data=['Description', 'Speed', 'JamFactor'])

            # Display the heatmap
            st.plotly_chart(fig, use_container_width=True)


        #JAM FACTOR PREDICTION
        left, right  = st.columns([1,2])
        with left:
            import altair as alt
            df_00['Time'] = pd.to_datetime(df_00['Time'], format='%H-%M-%S')

            df_00['Time Range'] = df_00['Time'].apply(lambda x:f"0-{x.hour}" if x.hour < 12 else f"12-{x.hour-12}")
            # Searching bar multiselect Bandung's street
            descriptions_2 = st.multiselect('Select descriptions here', df_00['Description'].unique())
            # Selectbox day 
            days_2 = st.selectbox('Select day here   ', df_00['Day'].unique())
            # Slider for time 
            time_range_2 = st.slider('Select time range here                 ', 0, 23, (8, 18), 1)

            df_00['Hour'] = df_00['Time'].dt.hour

            # Filter the data based on the selected inputs
            filtered_data_2 = df_00[(df_00['Description'].isin(descriptions_2)) & 
                                (df_00['Day'] == days_2) & 
                                (df_00['Hour'] >= time_range_2[0]) & 
                                (df_00['Hour'] <= time_range_2[1])]


        # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
            grouped_data_2 = filtered_data_2.groupby(['Description','Time Range', 'JamFactor']).mean().reset_index()
            
        with right:
            chart2 = alt.Chart(grouped_data_2).mark_bar().encode(
                x='Hour:Q',
                y=alt.Y('JamFactor:Q', stack=True),
                color='Description:N',
                tooltip =['Description:N', 'Time:T', 'JamFactor:Q']
            ).properties(
                width=800,
                height=500,
                title = f"Mean Jam Factor by Time Range {days_2}"
            ).interactive()

            # Display the chart
            st.altair_chart(chart2, use_container_width=True)


        #FOR COMPARING JAM FACTOR
        import altair as alt
        df_00['Time'] = pd.to_datetime(df_00['Time'], format='%H-%M-%S')
        df_00['Time Range'] = df_00['Time'].apply(lambda x:f"0-{x.hour}" if x.hour < 12 else f"12-{x.hour-12}")
        # Searching bar multiselect Bandung's street
        descriptions = st.multiselect('Select descriptions', df_00['Description'].unique())
        # Selectbox day 
        days = st.selectbox('Select day', df_00['Day'].unique())
        # Slider for time 
        time_range = st.slider('Select time range', 0, 23, (8, 18), 1)

        df_00['Hour'] = df_00['Time'].dt.hour

        # Filter the data based on the selected inputs
        filtered_data = df_00[(df_00['Description'].isin(descriptions)) & 
                            (df_00['Day'] == days) & 
                            (df_00['Hour'] >= time_range[0]) & 
                            (df_00['Hour'] <= time_range[1])]

        # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
        grouped_data = filtered_data.groupby(['Description', 'Time Range']).mean().reset_index()

        chart = alt.Chart(grouped_data, width=75, height=200).mark_bar(size=20).encode(
            column =alt.Column('Hour:O', spacing = 0),
            x=alt.X('Description:N'),
            y=alt.Y('JamFactor:Q'),
            color='Description:N', 
            tooltip =['Description:N', 'JamFactor:Q']
        ).properties(
            # width=400,
            # height=500,
            title = f"Mean Jam Factor by Time Range {days}"
        ).configure_view(stroke='transparent'
        ).interactive()

        # Display the chart
        st.altair_chart(chart, use_container_width=True)
















with tab_lebaran:
    #TRAFFIC DISTRIBUTION
    st.title ("Road Line Trend Traffic Lebaran")
    video_file = open('lebaran.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)


    # JAM FACTOR DISTRIBUTION
    st.header("Jam Factor Distribution Throught Time ")
    selasa_pre, rabu_pre, kamis_pre, jumat_pre, sabtu, minggu,senin_post, selasa_post, rabu_post = st.tabs(['Tuesday -pre', 'Wednesday -pre', 'Thursday -pre','Friday -pre', 
                                                                                                                       'Saturday', 'Sunday', 'Monday -post','Tuesday -post', 'Wednesday -post'  ])
    with selasa_pre:
        left, right = st.columns ([1,1])
        with left:
            df_selasa_pre = df_00_pre.loc[df_00_pre['Day'] == 'Tuesday']
            df_selasa_pre_mean = df_selasa_pre.groupby('Time')[['JamFactor']].mean()
            st.header('Tuesday -pre')
            st.line_chart(df_selasa_pre_mean)

            #TOP 5 - Senin
            time_range_selasa_pre = st.slider('Select time range here:                           ', 0, 23, (8, 18), 1)
            # Filter the data based on the selected inputs
            filtered_data_selasa_pre = df_00_pre[ 
                            (df_00_pre['Day'] == 'Tuesday') & 
                            (df_00_pre['Hour'] >= time_range_selasa_pre[0]) & 
                            (df_00_pre['Hour'] <= time_range_selasa_pre[1])]

            # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
            grouped_data_selasa_pre = filtered_data_selasa.groupby(['Description','Hour'])[['JamFactor']].max().reset_index()
            top_5_data_selasa_pre = grouped_data_selasa_pre.sort_values(['Hour', 'JamFactor'], ascending=[True, False]).groupby('Hour').head(5)
        
        with right:
            chart_selasa_pre = alt.Chart(top_5_data_selasa_pre).mark_bar().encode(
                y=alt.Y('Description:O', sort='-x'),#alt.EncodingSortField(field='Description',order='ascending')),
                x='JamFactor:Q',
                color='Description:N',
                tooltip =['Description:N', 'JamFactor:Q']
            ).properties(
                width=800,
                height=500,
                title = f"Top Crowded Locations by Hour on Tuesday"
            ).interactive()

            st.altair_chart(chart_selasa_pre, use_container_width=True)


    with rabu_pre:
        left, right = st.columns([1,1])
        with left:
            df_rabu_pre = df_00_pre.loc[df_00_pre['Day'] == 'Wednesday']
            df_rabu_pre_mean = df_rabu_pre.groupby('Time')[['JamFactor']].mean()
            st.header('Wednesday')
            st.line_chart(df_rabu_pre_mean)

            #TOP 5 - Selasa
            time_range_rabu_pre = st.slider('Select time range here:                            ', 0, 23, (8, 18), 1)
            # Filter the data based on the selected inputs
            filtered_data_rabu_pre = df_00_pre[ 
                            (df_00_pre['Day'] == 'Wednesday') & 
                            (df_00_pre['Hour'] >= time_range_rabu_pre[0]) & 
                            (df_00_pre['Hour'] <= time_range_rabu_pre[1])]

            # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
            grouped_data_rabu_pre = filtered_data_rabu_pre.groupby(['Description','Hour'])[['JamFactor']].max().reset_index()
            top_5_data_rabu_pre = grouped_data_rabu_pre.sort_values(['Hour', 'JamFactor'], ascending=[True, False]).groupby('Hour').head(5)
        
        with right:
            chart_rabu_pre = alt.Chart(top_5_data_rabu_pre).mark_bar().encode(
                y=alt.Y('Description:O', sort='-x'),#alt.EncodingSortField(field='Description',order='ascending')),
                x='JamFactor:Q',
                color='Description:N',
                tooltip =['Description:N', 'JamFactor:Q']
            ).properties(
                width=800,
                height=500,
                title = f"Top Crowded Locations by Hour on Wednesday"
            ).interactive()

            st.altair_chart(chart_rabu_pre, use_container_width=True)


    with kamis_pre:
        left, right = st.columns([1,1])
        with left:
            df_kamis_pre = df_00_pre.loc[df_00_pre['Day'] == 'Thursday']
            df_kamis_pre_mean = df_kamis_pre.groupby('Time')[['JamFactor']].mean()
            st.header('Thursday')
            st.line_chart(df_kamis_pre_mean)
        
            time_range_kamis_pre = st.slider('Select time range here:                                   ', 0, 23, (8, 18), 1)
            # Filter the data based on the selected inputs
            filtered_data_kamis_pre = df_00_pre[ 
                            (df_00_pre['Day'] == 'Thursday') & 
                            (df_00_pre['Hour'] >= time_range_kamis_pre[0]) & 
                            (df_00_pre['Hour'] <= time_range_kamis_pre[1])]

            # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
            grouped_data_kamis_pre  = filtered_data_kamis_pre.groupby(['Description','Hour'])[['JamFactor']].max().reset_index()
            top_5_data_kamis_pre  = grouped_data_kamis_pre.sort_values(['Hour', 'JamFactor'], ascending=[True, False]).groupby('Hour').head(5)
        
        with right:
            chart_kamis_pre  = alt.Chart(top_5_data_kamis_pre ).mark_bar().encode(
                y=alt.Y('Description:O', sort='-x'),#alt.EncodingSortField(field='Description',order='ascending')),
                x='JamFactor:Q',
                color='Description:N',
                tooltip =['Description:N', 'JamFactor:Q']
            ).properties(
                width=800,
                height=500,
                title = f"Top Crowded Locations by Hour on Thursday"
            ).interactive()

            st.altair_chart(chart_kamis_pre, use_container_width=True)


    with jumat_pre:
        left, right = st.columns([1,1])
        with left:
            df_jumat_pre = df_00_pre.loc[df_00_pre['Day'] == 'Friday']
            df_jumat_pre_mean = df_jumat_pre.groupby('Time')[['JamFactor']].mean()
            st.header('Friday')
            st.line_chart(df_jumat_pre_mean)

            time_range_jumat_pre = st.slider('Select time range here:                                 ', 0, 23, (8, 18), 1)
            # Filter the data based on the selected inputs
            filtered_data_jumat_pre = df_00_pre[ 
                            (df_00_pre['Day'] == 'Friday') & 
                            (df_00_pre['Hour'] >= time_range_jumat_pre[0]) & 
                            (df_00_pre['Hour'] <= time_range_jumat_pre[1])]

            # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
            grouped_data_jumat_pre = filtered_data_jumat_pre.groupby(['Description','Hour'])[['JamFactor']].max().reset_index()
            top_5_data_jumat_pre = grouped_data_jumat_pre.sort_values(['Hour', 'JamFactor'], ascending=[True, False]).groupby('Hour').head(5)
        
        with right:
            chart_jumat_pre = alt.Chart(top_5_data_jumat_pre).mark_bar().encode(
                y=alt.Y('Description:O', sort='-x'),#alt.EncodingSortField(field='Description',order='ascending')),
                x='JamFactor:Q',
                color='Description:N',
                tooltip =['Description:N', 'JamFactor:Q']
            ).properties(
                width=800,
                height=500,
                title = f"Top Crowded Locations by Hour on Friday"
            ).interactive()

            st.altair_chart(chart_jumat_pre, use_container_width=True)


    with sabtu:
        left, right = st.columns([1,1])
        with left:
            df_sabtu_lebaran = df_00_pre.loc[df_00_pre['Day'] == 'Saturday']
            df_sabtu_lebaran_mean = df_sabtu_lebaran.groupby('Time')[['JamFactor']].mean()
            st.header('Friday')
            st.line_chart(df_sabtu_lebaran_mean)

            time_range_sabtu_lebaran = st.slider('Select time range here:                                         ', 0, 23, (8, 18), 1)
            # Filter the data based on the selected inputs
            filtered_data_sabtu_lebaran  = df_00_pre[ 
                            (df_00_pre['Day'] == 'Saturday') & 
                            (df_00_pre['Hour'] >= time_range_sabtu_lebaran [0]) & 
                            (df_00_pre['Hour'] <= time_range_sabtu_lebaran [1])]

            # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
            grouped_data_sabtu_lebaran  = filtered_data_sabtu_lebaran.groupby(['Description','Hour'])[['JamFactor']].max().reset_index()
            top_5_data_sabtu_lebaran = grouped_data_sabtu_lebaran.sort_values(['Hour', 'JamFactor'], ascending=[True, False]).groupby('Hour').head(5)
        
        with right:
            chart_sabtu_lebaran  = alt.Chart(top_5_data_sabtu_lebaran ).mark_bar().encode(
                y=alt.Y('Description:O', sort='-x'),#alt.EncodingSortField(field='Description',order='ascending')),
                x='JamFactor:Q',
                color='Description:N',
                tooltip =['Description:N', 'JamFactor:Q']
            ).properties(
                width=800,
                height=500,
                title = f"Top Crowded Locations by Hour on Saturday"
            ).interactive()

            st.altair_chart(chart_sabtu_lebaran, use_container_width=True)


    with minggu:
        left, right = st.columns([1,1])
        with left:
            df_minggu_lebaran  = df_00_pre.loc[df_00_pre['Day'] == 'Sunday']
            df_minggu_lebaran_mean = df_minggu_lebaran.groupby('Time')[['JamFactor']].mean()
            st.header('Saturday')
            st.line_chart(df_minggu_lebaran_mean)

            time_range_minggu_lebaran = st.slider('Select time range here:                                        ', 0, 23, (8, 18), 1)
            # Filter the data based on the selected inputs
            filtered_data_minggu_lebaran = df_00_pre[ 
                            (df_00_pre['Day'] == 'Sunday') & 
                            (df_00_pre['Hour'] >= time_range_minggu_lebaran[0]) & 
                            (df_00_pre['Hour'] <= time_range_minggu_lebaran[1])]

            # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
            grouped_data_minggu_lebaran = filtered_data_minggu_lebaran.groupby(['Description','Hour'])[['JamFactor']].max().reset_index()
            top_5_data_minggu_lebaran = grouped_data_minggu_lebaran.sort_values(['Hour', 'JamFactor'], ascending=[True, False]).groupby('Hour').head(5)
        
        with right:
            chart_minggu_lebaran = alt.Chart(top_5_data_minggu_lebaran).mark_bar().encode(
                y=alt.Y('Description:O', sort='-x'),#alt.EncodingSortField(field='Description',order='ascending')),
                x='JamFactor:Q',
                color='Description:N',
                tooltip =['Description:N', 'JamFactor:Q']
            ).properties(
                width=800,
                height=500,
                title = f"Top Crowded Locations by Hour on Saturday"
            ).interactive()

            st.altair_chart(chart_minggu_lebaran, use_container_width=True)


    with senin_post:
        left, right = st.columns([1,1])
        with left:
            df_senin_post = df_00_post.loc[df_00_post['Day'] == 'Monday']
            df_senin_post_mean = df_senin_post.groupby('Time')[['JamFactor']].mean()
            st.header('Monday')
            st.line_chart(df_senin_post_mean)

            time_range_senin_post = st.slider('Select time range here:                                                       ', 0, 23, (8, 18), 1)
            # Filter the data based on the selected inputs
            filtered_data_senin_post = df_00_post[ 
                            (df_00_post['Day'] == 'Monday') & 
                            (df_00_post['Hour'] >= time_range_senin_post[0]) & 
                            (df_00_post['Hour'] <= time_range_senin_post[1])]

            # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
            grouped_data_senin_post = filtered_data_senin_post.groupby(['Description','Hour'])[['JamFactor']].max().reset_index()
            top_5_data_senin_post = grouped_data_senin_post.sort_values(['Hour', 'JamFactor'], ascending=[True, False]).groupby('Hour').head(5)
        
        with right:
            chart_senin_post = alt.Chart(top_5_data_senin_post).mark_bar().encode(
                y=alt.Y('Description:O', sort='-x'),#alt.EncodingSortField(field='Description',order='ascending')),
                x='JamFactor:Q',
                color='Description:N',
                tooltip =['Description:N', 'JamFactor:Q']
            ).properties(
                width=800,
                height=500,
                title = f"Top Crowded Locations by Hour on Monday"
            ).interactive()

            st.altair_chart(chart_senin_post, use_container_width=True)

    with selasa_post:
        left, right = st.columns([1,1])
        with left:
            df_selasa_post = df_00_post.loc[df_00_post['Day'] == 'Tuesday']
            df_selasa_post_mean = df_selasa_post.groupby('Time')[['JamFactor']].mean()
            st.header('Tuesday')
            st.line_chart(df_selasa_post_mean)

            time_range_selasa_post = st.slider('Select time range here:                                                               ', 0, 23, (8, 18), 1)
            # Filter the data based on the selected inputs
            filtered_data_selasa_post = df_00_post[ 
                            (df_00_post['Day'] == 'Tuesday') & 
                            (df_00_post['Hour'] >= time_range_selasa_post[0]) & 
                            (df_00_post['Hour'] <= time_range_selasa_post[1])]

            # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
            grouped_data_selasa_post = filtered_data_selasa_post.groupby(['Description','Hour'])[['JamFactor']].max().reset_index()
            top_5_data_selasa_post = grouped_data_selasa_post.sort_values(['Hour', 'JamFactor'], ascending=[True, False]).groupby('Hour').head(5)
        
        with right:
            chart_selasa_post = alt.Chart(top_5_data_selasa_post).mark_bar().encode(
                y=alt.Y('Description:O', sort='-x'),#alt.EncodingSortField(field='Description',order='ascending')),
                x='JamFactor:Q',
                color='Description:N',
                tooltip =['Description:N', 'JamFactor:Q']
            ).properties(
                width=800,
                height=500,
                title = f"Top Crowded Locations by Hour on Tuesday"
            ).interactive()

            st.altair_chart(chart_selasa_post, use_container_width=True)

    with rabu_post:
        left, right = st.columns([1,1])
        with left:
            df_rabu_post = df_00_post.loc[df_00_post['Day'] == 'Wednesday']
            df_rabu_post_mean = df_rabu_post.groupby('Time')[['JamFactor']].mean()
            st.header('Wednesday')
            st.line_chart(df_rabu_post_mean)

            time_range_rabu_post = st.slider('Select time range here:                                                   ', 0, 23, (8, 18), 1)
            # Filter the data based on the selected inputs
            filtered_data_rabu_post = df_00_post[ 
                            (df_00_post['Day'] == 'Wednesday') & 
                            (df_00_post['Hour'] >= time_range_rabu_post[0]) & 
                            (df_00_post['Hour'] <= time_range_rabu_post[1])]

            # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
            grouped_data_rabu_post = filtered_data_rabu_post.groupby(['Description','Hour'])[['JamFactor']].max().reset_index()
            top_5_data_rabu_post = grouped_data_rabu_post.sort_values(['Hour', 'JamFactor'], ascending=[True, False]).groupby('Hour').head(5)
        
        with right:
            chart_rabu_post = alt.Chart(top_5_data_rabu_post).mark_bar().encode(
                y=alt.Y('Description:O', sort='-x'),#alt.EncodingSortField(field='Description',order='ascending')),
                x='JamFactor:Q',
                color='Description:N',
                tooltip =['Description:N', 'JamFactor:Q']
            ).properties(
                width=800,
                height=500,
                title = f"Top Crowded Locations by Hour on Wednesday"
            ).interactive()

            st.altair_chart(chart_rabu_post, use_container_width=True)
    

    # left,right = st.columns([1,2])

    # with left:
    # # Load data
    #     df = pd.read_csv('new_file.csv', sep =',')

    #     # Selectbox day
    #     days = df['Day'].unique()
    #     day_filter = st.selectbox('Select day here', days)

    #     df['Time'] = pd.to_datetime(df['Time'], format='%H-%M-%S')
    #     df['Hour'] = df['Time'].dt.hour

    #     df['Time Range'] = df['Time'].apply(lambda x:f"0-{x.hour}" if x.hour < 12 else f"12-{x.hour-12}")

    #     # Slider for time
    #     time_filter = st.slider('Select time range here', 0, 23, (8, 18), 1)

    #     # Filter the data based on the selected inputs
    #     filtered_data = df[(df['Day'] == day_filter) & (df['Hour'] >= time_filter[0]) & (df['Hour'] <= time_filter[1])]

    #     #grouped_heatmap = filtered_data_3.groupby('Time Range','Kecamatan')


    # with right:
    # # Create the heatmap
    #     fig = px.density_mapbox(filtered_data, lat='latitude_kecamatan', lon='longitude_kecamatan', z='JamFactor',
    #                             radius=15, center=dict(lat=-6.91474, lon=107.60981), zoom=10, mapbox_style='carto-positron',
    #                             hover_name='Kecamatan', hover_data=['Description', 'Speed', 'JamFactor'])

    #     # Display the heatmap
    #     st.plotly_chart(fig, use_container_width=True)


    # #JAM FACTOR PREDICTION
    # left, right  = st.columns([1,2])
    # with left:
    #     import altair as alt
    #     df_00['Time'] = pd.to_datetime(df_00['Time'], format='%H-%M-%S')

    #     df_00['Time Range'] = df_00['Time'].apply(lambda x:f"0-{x.hour}" if x.hour < 12 else f"12-{x.hour-12}")
    #     # Searching bar multiselect Bandung's street
    #     descriptions_2 = st.multiselect('Select descriptions here', df_00['Description'].unique())
    #     # Selectbox day 
    #     days_2 = st.selectbox('Select day here   ', df_00['Day'].unique())
    #     # Slider for time 
    #     time_range_2 = st.slider('Select time range here                 ', 0, 23, (8, 18), 1)

    #     df_00['Hour'] = df_00['Time'].dt.hour

    #     # Filter the data based on the selected inputs
    #     filtered_data_2 = df_00[(df_00['Description'].isin(descriptions_2)) & 
    #                         (df_00['Day'] == days_2) & 
    #                         (df_00['Hour'] >= time_range_2[0]) & 
    #                         (df_00['Hour'] <= time_range_2[1])]


    # # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
    #     grouped_data_2 = filtered_data_2.groupby(['Description','Time Range', 'JamFactor']).mean().reset_index()
        
    # with right:
    #     chart2 = alt.Chart(grouped_data_2).mark_bar().encode(
    #         x='Hour:Q',
    #         y=alt.Y('JamFactor:Q', stack=True),
    #         color='Description:N',
    #         tooltip =['Description:N', 'Time:T', 'JamFactor:Q']
    #     ).properties(
    #         width=800,
    #         height=500,
    #         title = f"Mean Jam Factor by Time Range {days_2}"
    #     ).interactive()

    #     # Display the chart
    #     st.altair_chart(chart2, use_container_width=True)


    # #FOR COMPARING JAM FACTOR
    # import altair as alt
    # df_00['Time'] = pd.to_datetime(df_00['Time'], format='%H-%M-%S')
    # df_00['Time Range'] = df_00['Time'].apply(lambda x:f"0-{x.hour}" if x.hour < 12 else f"12-{x.hour-12}")
    # # Searching bar multiselect Bandung's street
    # descriptions = st.multiselect('Select descriptions', df_00['Description'].unique())
    # # Selectbox day 
    # days = st.selectbox('Select day', df_00['Day'].unique())
    # # Slider for time 
    # time_range = st.slider('Select time range', 0, 23, (8, 18), 1)

    # df_00['Hour'] = df_00['Time'].dt.hour

    # # Filter the data based on the selected inputs
    # filtered_data = df_00[(df_00['Description'].isin(descriptions)) & 
    #                     (df_00['Day'] == days) & 
    #                     (df_00['Hour'] >= time_range[0]) & 
    #                     (df_00['Hour'] <= time_range[1])]

    # # Group the filtered data by description and time, and calculate the mean of 'JamFactor' for each group
    # grouped_data = filtered_data.groupby(['Description', 'Time Range']).mean().reset_index()

    # chart = alt.Chart(grouped_data, width=75, height=200).mark_bar(size=20).encode(
    #     column =alt.Column('Hour:O', spacing = 0),
    #     x=alt.X('Description:N'),
    #     y=alt.Y('JamFactor:Q'),
    #     color='Description:N', 
    #     tooltip =['Description:N', 'JamFactor:Q']
    # ).properties(
    #     # width=400,
    #     # height=500,
    #     title = f"Mean Jam Factor by Time Range {days}"
    # ).configure_view(stroke='transparent'
    # ).interactive()

    # # Display the chart
    # st.altair_chart(chart, use_container_width=True)
