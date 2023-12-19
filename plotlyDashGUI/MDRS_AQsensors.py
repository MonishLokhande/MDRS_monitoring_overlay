from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px

# Initialize the app
sensor_app = Dash(__name__)
sensor_app.css.append_css({"external_url": "/assets/style.css"})

colorscales = px.colors.named_colorscales()  # add colormaps

# App layout
sensor_app.layout = html.Div(className='row', children=[
    html.H1("MDRS Air Quality Monitoring"),
    
    # Dropdown list
    dcc.Dropdown(['Upper Deck', 'Lower Deck', 'Science Dome', 'Green Hab'], 'Upper Deck', id='dropdown',style={'background-color': '#0f0f10'}),
    html.Div([html.H2(id='output_title')]),
    # Plots
    html.Div([dcc.Graph(id='CO2')], style={'width': '50%', 'display': 'inline-block'}),
    html.Div([dcc.Graph(id='Temp')], style={'width': '50%', 'display': 'inline-block'}),
    html.Div([dcc.Graph(id='VOC')], style={'width': '50%', 'display': 'inline-block'}),
    html.Div([dcc.Graph(id='Hum')], style={'width': '50%', 'display': 'inline-block'}),
    html.Div([dcc.Graph(id='Dust')], style={'width': '50%', 'display': 'inline-block'}),
    html.Div([dcc.Graph(id='Ozo')], style={'width': '50%', 'display': 'inline-block'}),
    # html.Div([dcc.Graph(id='H2O')], style={'width': '34%', 'display': 'inline-block'}),
])

@callback(
    Output('output_title', 'children'),
    Output('CO2', 'figure'),
    Output('VOC', 'figure'),
    Output('Temp', 'figure'),
    Output('Hum', 'figure'),
    Output('Dust', 'figure'),
    Output('Ozo', 'figure'),
    # Output('H2O', 'figure'),
    Input('dropdown', 'value')
)
def dropdown_output(value):
    if value == 'Upper Deck':
        df = pd.read_csv('sample_AQdata.csv')
    elif value == 'Lower Deck':
        df = pd.read_csv('sample_AQdata_LowerHab.csv')
    elif value == 'Science Dome':
        df = pd.read_csv('sample_AQdata.csv')
    elif value == 'Green Hab':
        df = pd.read_csv('sample_AQdata.csv')

    # CO2 Plot
    figC = px.scatter(df, x='Time', y='Carbon dioxide [ppm]', title='Carbon Dioxide', color_continuous_scale='turbo', color='Carbon dioxide [ppm]', template='plotly_dark')
    figC.update_layout(title_x=0.5,title_y=0.85)
    figC.add_trace(px.line(df, x='Time', y='Carbon dioxide [ppm]', line_shape="linear", render_mode="svg").data[0])
    figC.update_traces(line_color='rgba(128,128,128,0.5)')
    figC.update_layout(coloraxis=dict(cmax=900, cmin=300),coloraxis_colorbar_title_text = '')
    figC.update_xaxes(nticks=10,tickangle=45)

    # VOCs Plot
    figV = px.scatter(df, x='Time', y='VOCs [ppm]', title='Volatile Compounds', color_continuous_scale='viridis', color='VOCs [ppm]', template='plotly_dark')
    figV.update_layout(title_x=0.5,title_y=0.85)
    figV.add_trace(px.line(df, x='Time', y='VOCs [ppm]', line_shape="linear", render_mode="svg").data[0])
    figV.update_traces(line_color='rgba(128,128,128,0.5)')
    figV.update_layout(coloraxis=dict(cmax=1000, cmin=200),coloraxis_colorbar_title_text = '')
    figV.update_xaxes(nticks=10,tickangle=45)

    # Temperature Plot
    figT = px.line(df, x='Time', y='Temperature [C]', title='Temperature', line_shape="linear", render_mode="svg", template='plotly_dark')
    figT.update_layout(title_x=0.5,title_y=0.85)
    figT.update_traces(line_color='rgba(128,128,128,0.5)')
    figT.add_trace(px.scatter(df, x='Time', y='Temperature [C]', color='Temperature [C]').data[0])
    figT.update_layout(coloraxis=dict(cmax=40, cmin=10))
    figT.update_xaxes(nticks=10,tickangle=45)
    figT.add_hrect(y0=18, y1=26, line_width=0, fillcolor="gray", opacity=0.2)

    # Humidity Plot
    figH = px.line(df, x='Time', y='Humidity [%]', title='Humidity', line_shape="linear", render_mode="svg", template='plotly_dark')
    figH.update_layout(title_x=0.5,title_y=0.85)
    figH.update_traces(line_color='rgba(128,128,128,0.5)')
    figH.add_trace(px.scatter(df, x='Time', y='Humidity [%]', color='Humidity [%]').data[0])
    figH.update_layout(coloraxis=dict(cmax=100, cmin=0))
    figH.update_xaxes(nticks=10,tickangle=45)

    # Dust Plot
    figD = px.line(df, x='Time', y='Dust [ug/m3]', title='Dust', line_shape="linear", render_mode="svg", template='plotly_dark')
    figD.update_layout(title_x=0.5,title_y=0.85)
    figD.update_traces(line_color='rgba(128,128,128,0.5)')
    figD.add_trace(px.scatter(df, x='Time', y='Dust [ug/m3]', color='Dust [ug/m3]').data[0])
    figD.update_layout(coloraxis=dict(cmax=200, cmin=0))
    figD.update_xaxes(nticks=10,tickangle=45)

    # Ozone Plot
    figO = px.scatter(df, x='Time', y='Ozone [ppm]', title='Ozone', color_continuous_scale='cividis', color='Ozone [ppm]', template='plotly_dark')
    figO.update_layout(title_x=0.5,title_y=0.85)
    figO.add_trace(px.line(df, x='Time', y='Ozone [ppm]', line_shape="linear", render_mode="svg").data[0])
    figO.update_traces(line_color='rgba(128,128,128,0.5)')
    figO.update_layout(coloraxis=dict(cmax=0.05, cmin=0),coloraxis_colorbar_title_text = '')
    figO.update_xaxes(nticks=10,tickangle=45)

    # # Water Level
    # df['waterColor'] = np.where(df['Water Tank Level [%]']<10, 'red', 'blue')
    # figW = px.bar(df, x='Time', y='Water Tank Level [%]', title='Water Tank Level', color='waterColor', template='plotly_dark')
    # figW.update_xaxes(nticks=10,tickangle=45)
    # figW.update_layout(title_x=0.5,title_y=0.85)
    # figW.update_layout(showlegend=False) 

    return f'{value} Sensors', figC, figV, figT, figH, figD, figO
    

# Run the app
if __name__ == '__main__':
    sensor_app.run(debug=True)