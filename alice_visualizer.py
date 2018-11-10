'''

XΛMESƎ's A . L . I . C . E . visualizer module
=====================================================

Module for creating webbrowser based graphs using Plotly and Dash.

'''

__author__ = 'XA'
__version__ = '1.8'

import os
import csv
import time
import random
import webbrowser
from collections import deque

import dash
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from plotly.graph_objs import *

import pandas as pd


root_dir = os.getcwd()

print(root_dir)
assets_dir = os.path.join(root_dir,'assets')

def create_folder(folder_name):
    # Function for creating folder in case the folder does not exists. If the
    # folder is already present it'll skip this function and move on to the
    # next line.
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


create_folder(assets_dir)


app = dash.Dash('XA Visualizer')
df = pd.read_csv('vm.csv')
url = 'http://127.0.0.1:8050/'
run_queue = df['r'].tolist()
blocked_process = df['b'].tolist()
swap_memory = df['swpd'].tolist()
free_memory = df['free'].tolist()
buffer_memory = df['buff'].tolist()
cache_memory = df['cache'].tolist()
swap_in = df['si'].tolist()
swap_out = df['so'].tolist()
block_in = df['bi'].tolist()
block_out = df['bo'].tolist()
interrupts = df['in'].tolist()
context_switch = df['cs'].tolist()
user_space = df['us'].tolist()
kernel_space = df['sy'].tolist()
idle_operation = df['id'].tolist()
wait_idle = df['wa'].tolist()
steal_time = df['st'].tolist()
time_frame = df['time_frame']

data_dict = {'Run Queue (r)': run_queue,
             'Blocked Process (b)': blocked_process,
             'Swap Memory (swpd)': swap_memory,
             'Free Memory (free)': free_memory,
             'Buffer Memory (buff)': buffer_memory,
             'Cache Memory (cache)': cache_memory,
             'Swap In (si)': swap_in,
             'Swap Out (so)': swap_out,
             'Block In (bi)': block_in,
             'Block Out (bo)': block_out,
             'Interrupts (in)': interrupts,
             'Context Switch (cs)': context_switch,
             'User Space (us)': user_space,
             'Kernel Space (sy)': kernel_space,
             'Idle Operation (id)': idle_operation,
             'Wait Idle (wa)': wait_idle,
             'Steal Time (st)': steal_time}

app.layout = html.Div([
    html.Div(
        [html.H2('XA\'s Visualizer',
                 style={'display': 'inline',
                        'float': 'left',
                        'font-size': '2.65em',
                        'margin-left': '7px',
                        'font-weight': 'bolder',
                        'font-family': 'Product Sans',
                        'color': 'rgba(117, 117, 117, 0.95)',
                        'margin-top': '20px',
                        'margin-bottom': '0'
                        })]),
    dcc.Dropdown(id='alice-graph-name',
                 options=[{'label': s, 'value': s}
                          for s in data_dict.keys()],
                 value=['Buffer Memory (buff)', 'Cache Memory (cache)'],
                 multi=True),
    html.Div(children=html.Div(id='graphs'), className='row')],
    className='container')


@app.callback(
    dash.dependencies.Output('graphs', 'children'),
    [dash.dependencies.Input('alice-graph-name', 'value')])
def update_graph(data_names):
    # Function for plotting graph on a browser based UI.
    graphs = []

    if not data_names:
        graphs.append(html.H4(
            'Choose a VMSTAT parameter',
            style={'marginTop': 20, 'marginBottom': 20}
        ))
    else:
        for data_name in data_names:
            data = [dict(
                type='scatter',
                x=list(time_frame),
                y=free_memory,
                name='Free Memory (free)',
                line=dict(
                    shape='linear',
                    smoothing='0.4',
                    fill='tozeroy',
                    color='#7F7F7F',
                    opacity=1,
                    width=1)),
                    dict(
                type='scatter',
                x=list(time_frame),
                y=list(data_dict[data_name]),
                name=data_name,
                line=dict(
                    shape='linear',
                    smoothing='0.4',
                    color='#17BECF',
                    opacity=0.8,
                    width=1)
            )]

            graphs.append(html.Div(dcc.Graph(
                id=data_name,
                figure={'data': data,
                        'layout': dict(
                            xaxis=dict(
                                rangeslider=dict(visible=True),
                                type='time',
                                yaxis=data_dict[data_name],
                                autosize=True,
                                hoverinfo='all',
                                title=data_name))})))

    return graphs


external_css = os.path.join(assets_dir, 'stylesheet.css')
app.css.append_css({"external_url": external_css})

external_js = os.path.join(assets_dir, 'plotly_ga.js')
app.scripts.append_script({'external_url': external_js})

if __name__ == '__main__':
    webbrowser.open(url)
    app.run_server(debug=True)
