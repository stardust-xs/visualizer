'''

XΛMESƎ's A . L . I . C . E . visualizer module
=====================================================

Module for creating webbrowser based graphs using Plotly and Dash.

'''

__author__ = 'XA'
__version__ = '1.9'

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
assets_dir = os.path.join(root_dir, 'assets')


def create_folder(folder_name):
    # Function for creating folder in case the folder does not exists. If the
    # folder is already present it'll skip this function and move on to the
    # next line.
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


create_folder(assets_dir)

app = dash.Dash('VMSTAT Visualizer')
df = pd.read_csv('vm.csv')
url = 'http://127.0.0.1:8050/'
run_queue = df['r'].tolist()
blocked_process = df['b'].tolist()
swap_memory = (df['swpd']/1024).tolist()
free_memory = (df['free']/1024).tolist()
buffer_memory = (df['buff']/1024).tolist()
cache_memory = (df['cache']/1024).tolist()
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
        [html.H2('VM Stats Visualizer',
                 id='title',
                 style={'display': 'inline',
                        'float': 'left',
                        'font-size': '2.65em',
                        'margin-left': '0px',
                        'font-weight': 'bolder',
                        'font-family': 'Product Sans',
                        'color': 'rgba(117, 117, 117, 0.95)',
                        'margin-top': '40px',
                        'margin-bottom': '20px'
                        }),
        html.P('made by XA',
            id='sub-title',
                 style={'float': 'left',
                        'font-size': '1.00em',
                        'margin-left': '5px',
                        'font-weight': 'normal',
                        'font-family': 'Product Sans',
                        'color': 'rgba(117, 117, 117, 0.95)',
                        'margin-top': '67px',
                        'position': 'relative'}),
        html.Img(src='/assets/xa_image.png',
                 style={'height': '150',
                        'width': '150',
                        'float': 'right',
                        'position': 'relative'})]),
    dcc.Dropdown(id='alice-graph-name',
                 options=[{'label': s, 'value': s}
                          for s in data_dict.keys()],
                 value=['Free Memory (free)'],
                 multi=True),
    html.Div(children=html.Div(id='graphs'), className='row')
],
    className='container')


@app.callback(
    dash.dependencies.Output('graphs', 'children'),
    [dash.dependencies.Input('alice-graph-name', 'value')])
def update_graph(data_names):
    # Function for plotting graph on a browser based UI.
    graphs = []

    graphs.append(html.H4(
        'Combined Memory Utilization Dashboard',
        style={'font-size': '1.25em',
               'margin-left': '0px',
               'font-weight': 'normal',
               'font-family': 'Product Sans',
               'color': 'rgba(117, 117, 117, 0.95)',
               'margin-top': '20px',
               'margin-bottom': '0px'}))

    average_data = [
        dict(
            type='scatter',
            x=list(time_frame),
            y=swap_memory,
            name='Swap Memory (swpd)',
            hoveron='points+fills',
            line=dict(
                shape='spline',
                smoothing='0.3',
                color='#E74C3C',
                opacity=0.8,
                width=1.5)),
        dict(
            type='scatter',
            x=list(time_frame),
            y=buffer_memory,
            name='Buffer Memory (buff)',
            hoveron='points+fills',
            line=dict(
                shape='spline',
                smoothing='0.3',
                color='#3498DB',
                opacity=0.8,
                width=1.5)),
        dict(
            type='scatter',
            x=list(time_frame),
            y=cache_memory,
            name='Cache Memory (cache)',
            hoveron='points+fills',
            line=dict(
                shape='spline',
                smoothing='0.3',
                color='#F1C40F',
                opacity=0.8,
                width=1.5)),
        dict(
            type='scatter',
            x=list(time_frame),
            y=free_memory,
            name='Free Memory (free)',
            hoveron='points+fills',
            line=dict(
                shape='spline',
                smoothing='0.3',
                color='#52BE80',
                opacity=0.8,
                width=1.5)),
    ]

    graphs.append(html.Div(dcc.Graph(
        figure={'data': average_data,
                'layout': dict(
                    xaxis=dict(
                        rangeslider=dict(visible=True),
                        type='time',
                        title='Memory'),
                    yaxis=dict(
                        title='Utilization'),
                    hoverinfo='all',
                    hovermode='closest',
                    autosize=True,
                    showlegend=True
                )})))

    if not data_names:
        graphs.append(html.H5(
            'Choose VMSTAT parameter to display individual graphs',
            style={'font-size': '1.25em',
               'margin-left': '0px',
               'font-weight': 'normal',
               'font-family': 'Product Sans',
               'color': 'rgba(117, 117, 117, 0.95)',
               'margin-top': '20px',
               'margin-bottom': '0px'}))
    else:
        for data_name in data_names:
            def displayed_graph(color_code):
                display_data = [
                    dict(
                        type='scatter',
                        x=list(time_frame),
                        y=list(data_dict[data_name]),
                        name=data_name,
                        fill='tozeroy',
                        hoveron='points+fills',
                        line=dict(
                            shape='spline',
                            smoothing='0.3',
                            color=color_code,
                            opacity=0.8,
                            width=1.5))]

                return display_data

            if data_name == 'Run Queue (r)':
                data = displayed_graph('#003f5c')
            elif data_name == 'Blocked Process (b)':
                data = displayed_graph('#2f4b7c')
            elif data_name == 'Swap Memory (swpd)':
                data = displayed_graph('#E74C3C')
            elif data_name == 'Free Memory (free)':
                data = displayed_graph('#52BE80')
            elif data_name == 'Buffer Memory (buff)':
                data = displayed_graph('#3498DB')
            elif data_name == 'Cache Memory (cache)':
                data = displayed_graph('#F1C40F')
            elif data_name == 'Swap In (si)':
                data = displayed_graph('#ff7c43')
            elif data_name == 'Swap Out (so)':
                data = displayed_graph('#ffa600')
            elif data_name == 'Block In (bi)':
                data = displayed_graph('#00851d')
            elif data_name == 'Block Out (bo)':
                data = displayed_graph('#FF99FF')
            elif data_name == 'Interrupts (in)':
                data = displayed_graph('#FF99FF')
            elif data_name == 'Context Switch (cs)':
                data = displayed_graph('#FF99FF')
            elif data_name == 'User Space (us)':
                data = displayed_graph('#FF99FF')
            elif data_name == 'Kernel Space (sy)':
                data = displayed_graph('#FF99FF')
            elif data_name == 'Idle Operation (id)':
                data = displayed_graph('#FF99FF')
            elif data_name == 'Wait Idle (wa)':
                data = displayed_graph('#FF99FF')
            else:
                data = displayed_graph('#FF99FF')

            graphs.append(html.Div(dcc.Graph(
                id=data_name,
                figure={'data': data,
                        'layout': dict(
                            xaxis=dict(
                                rangeslider=dict(visible=True),
                                type='time',
                                yaxis=data_dict[data_name],
                                title=data_name),
                            yaxis=dict(
                                title='Utilization'),
                            hoverinfo='all',
                            hovermode='closest',
                            autosize=True,
                            showlegend=True
                        )})))

    return graphs


external_css = os.path.join(assets_dir, 'stylesheet.css')
app.css.append_css({"external_url": external_css})

external_js = os.path.join(assets_dir, 'plotly_ga.js')
app.scripts.append_script({'external_url': external_js})


if __name__ == '__main__':
    webbrowser.open(url, new=0, autoraise=True)
    app.run_server(debug=True)
