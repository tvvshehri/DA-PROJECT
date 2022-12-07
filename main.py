import numpy as np    
import pandas as pd
import matplotlib.pyplot as plt 
import plotly
import plotly.graph_objects as go
import plotly.express as px


#read excel file
excel_file = pd.read_excel("DATASET FIRST.xlsb" , sheet_name="Final_Dataset", engine='pyxlsb')

# clean the file by checking the null values
excel_file.isnull().any()

# fill null value
excel_file["program_desc2"].fillna("0", inplace = True)
excel_file.isnull().any()

#copy before working
data =excel_file.copy()

# extract total watch, total duration seconds, number of users
combined = data.copy()
combined.loc[combined['program_class'] == 'SERIES/EPISODES', 'program_name2'] = combined['program_name2']+'_season'+ combined['season'].astype(str)+'episode'+ combined['episode'].astype(str)
combined = combined.groupby(['program_name2','program_class'])\
.agg({'user_id_maped': [('co1', 'nunique'),('co2', 'count')],\
      'duration_seconds': [('co3', 'sum')]}).reset_index()
combined.columns = ['program_name2','program_class','No.users', 'total_watch', 'total_duration_sec']
combined = combined.sort_values(by=['total_duration_sec', 'total_watch','No.users'], ascending=False).reset_index(drop=True)
print(combined.head(30))


# top 10 in total watch
total_watch_figure = px.pie(combined.head(10), values='total_watch', names='program_name2',\
             hover_data=['program_class'],title=' Top 10 in total watch')
total_watch_figure.show() 


# user expeirence with program class
combined =data.copy()
combined = combined.groupby('program_class')\
.agg({'user_id_maped': [('co1', 'nunique'),('co2', 'count')],\
      'duration_seconds': [('co3', 'sum')]}).reset_index()
combined.columns = ['program_class','No.Users', 'total_watch', 'total_duration_sec']
combined = combined.sort_values(by=['total_duration_sec', 'total_watch','No.Users'], ascending=False).reset_index(drop=True)
print(combined.head())


Total_duration_figure = px.pie(combined, values='total_duration_sec', names='program_class',\
             hover_data=['program_class'],title='Total duration by program_class')

Total_users_figure = px.pie(combined, values='No.Users', names='program_class',\
             hover_data=['program_class'],title='Total Users watching by program_class')
Total_duration_figure.update_traces(sort=False)
Total_users_figure.update_traces(sort=False)
Total_duration_figure.show()
Total_users_figure.show() 


# relationship of users using HD OR SD 
combined=data.copy()
combined = combined.groupby('hd')\
.agg({'user_id_maped': [('co1', 'nunique')]}).reset_index()
combined.columns = ['hd','No.Users']
combined = combined.sort_values(by=['hd', 'No.Users'], ascending=False).reset_index(drop=True)
print(combined.head())


HD_SD_figure = px.pie(combined, values='No.Users', names='hd',\
             hover_data=['hd'], title='Relationship of users with viewing resolution HD or SD')
HD_SD_figure.show() 
