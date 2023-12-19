from dash import Dash, html, dcc, dash_table
import dash_daq as daq
import pandas as pd
import plotly.express as px
import numpy as np
import datetime
import pytz

df = pd.read_csv('sample_AQdata.csv')
df_door = pd.read_csv('door_status.csv')

# Water Tank Plot
df['waterColor'] = np.where(df['Water Tank Level [%]']<10, 'red', 'blue')
figW = px.bar(df, x='Time', y='Water Tank Level [%]', title='Water Tank Level', color='waterColor', template='plotly_dark')
figW.update_xaxes(nticks=10,tickangle=45)
figW.update_layout(title_x=0.5,title_y=0.85)
figW.update_layout(showlegend=False) 

# Initialize the app
MDRS_app = Dash(__name__)
MDRS_app.css.append_css({"external_url": "/assets/style.css"})

# Time Zones
Purdue_time = datetime.datetime.now()
MST = pytz.timezone('US/Mountain') 
MDRS_time = datetime.datetime.now(MST)

# App layout
MDRS_app.layout = html.Div(className='row', children=[
    html.H1("Mars Desert Research Station Monitoring System", className="app__header__title"),

    # Display Time
    html.Div([daq.LEDDisplay(
        label={'label':"Time at MDRS", 'style':{'color':'white'}},
        labelPosition='bottom',
        value=str(MDRS_time.strftime("%H:%M")),
        color="#FF5E5E", backgroundColor="#000000"
    )], style={'width': '50%', 'display': 'inline-block', 'label-color': 'white'}),
    html.Div([daq.LEDDisplay(
        label={'label':"Time at Purdue", 'style':{'color':'white'}},
        labelPosition='bottom',
        value=str(Purdue_time.strftime("%H:%M")),
        color="#66ff00", backgroundColor="#000000"
    )], style={'width': '50%', 'display': 'inline-block'}),

    html.Div([
        # Door table
        html.Div([dash_table.DataTable(df_door.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df_door.columns],
                style_table={'height': 200, 'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'border': '5px solid grey'}, style_as_list_view=True, 
                style_header={'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white', 'border': '1px solid black' },
                style_data={'backgroundColor': 'rgb(50, 50, 50)','color': 'white'},
                style_data_conditional=[{'if':{'filter_query': '{Status} eq "open"',
                'column_id': 'Status'},
                'backgroundColor': '#FF4136',
                'color': 'white'}]),
        ], style={'width': '40%', 'display': 'inline-block', 'padding-top': 150, 'padding-left': 20}),
        # Water Tank Plot
        html.Div([dcc.Graph(figure= figW)], style={'width': '60%', 'display': 'inline-block', 'margin-top': '20px', 'padding-left': 30}),
    ], style={'display': 'flex', 'columnCount': 2})

])


if __name__ == '__main__':
    MDRS_app.run(debug=True)
