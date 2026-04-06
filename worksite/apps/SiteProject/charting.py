#import pandas as pd
import plotly.express as px
import datetime as dt
from config import CHARTS_PATH

if CHARTS_PATH.exists():
    pass
else:
    CHARTS_PATH.mkdir(exist_ok=True)


def file_path(file_name:str):
    return CHARTS_PATH / file_name

def heatMap(chart_data:dict={}):
    f_name = 'heatmap.html'
    file = file_path(f_name)
    data=[[1, 25, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, 5, 20]]
    fig = px.imshow(data,
                labels=dict(x="Day of Week", y="Time of Day", color="Productivity"),
                x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                y=['Morning', 'Afternoon', 'Evening']
               )
    fig.update_xaxes(side="top")
    #fig.write_html(file)
    return fig.to_html()
    

        
