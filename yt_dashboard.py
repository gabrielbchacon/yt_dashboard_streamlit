
#Importing libs 
import json
import pandas as pd

import numpy as np 
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import streamlit as st

#Data Load and preparation

file = 'cha_con_tech.json'
data = None
with open(file, 'r') as f:
    data = json.load(f)

channel_id, stats = data.popitem()
channel_stats = stats['channel_statistics']
video_stats = stats['video_data']


sorted_vids = sorted(video_stats.items(), key=lambda item: int(item[1]['viewCount']), reverse=True)
stats = []

for vid in sorted_vids:
    video_id = vid[0]
    title = vid[1]['title']
    views = vid[1]['viewCount']
    likes = vid[1]['likeCount']
    duration = vid[1]['duration']
    #dislikes = vid[1]['dislikeCount']
    thumb_link = vid[1]['thumbnails']['high']['url']
    comments = vid[1]['commentCount']
    tags = vid[1]['tags']
    description = vid[1]['description']
    stats.append([video_id, title, views, likes, duration,thumb_link, comments, tags, description])


df = pd.DataFrame(stats, columns=['video_id', 'title', 'views', 'likes', 'duration','thumb_link', 'comments', 'tags', 'description'])

#Some basic feature engineer
df[['minutes','seconds']] = df['duration'].str.extract(r'PT(\d+)M(\d+)S', expand=True).astype('int')
df['total_seconds'] = 60*df['minutes'] + df['seconds']

#Building the Streamlit app
add_sidebar = st.sidebar.selectbox('Aggregate or Individual Video', ('Aggregate Metrics','Individual Video Analysis'))

if add_sidebar == 'Aggregate Metrics':
    st.write('Aggregate Metrics')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Views', channel_stats['viewCount'])
    
    with col2:
        col2 = st.metric('Subs', channel_stats['subscriberCount'])

    with col3:
        col3 = st.metric('videos', channel_stats['videoCount'])

    st.dataframe(df.style, 1200, 900)


if add_sidebar == 'Individual Video Analysis':
    st.title('Individual Video Performance')
    videos = tuple(df['title'])
    video_select = st.selectbox('Pick a Video:', videos)
    agg_filtered = df[df['title'] == video_select]
    st.header(agg_filtered.iloc[0]['title'])

    for tag in agg_filtered.iloc[0]['tags']:
        tag_string = ''
        tag_string + f'#{tag}' 
    
    st.write(tag_string)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Views', agg_filtered.iloc[0]['views'])
    
    with col2:
        col2 = st.metric('Likes', agg_filtered.iloc[0]['likes'])

    with col3:
        col3 = st.metric('Comments', agg_filtered.iloc[0]['comments'])
    
    with col4:
        col3 = st.metric('Durations (s)', agg_filtered.iloc[0]['total_seconds'])

    
    st.image(agg_filtered.iloc[0]['thumb_link'], use_column_width = True)