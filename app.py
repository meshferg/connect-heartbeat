# -*- coding: utf-8 -*-
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc  # dash core components
import dash_gif_component as gif
from dash import html  # dash html components
from dash import Input, Output
# import dash_daq as daq
import dash_bootstrap_components as dbc
import dash_player as dp
import plotly.express as px

# My python modules
import connect_heartbeat

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

my_hb = connect_heartbeat.ConnectHeartbeat(demo_mode=True)
my_hb.update_data()

fig = px.bar(my_hb.participant_demo_df, x='Sex', y='Count',)
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    font={'size': 20},
    )

l2 = 'Last update: {} (UTC - you do the math)'
l3 = 'Total active participants: {}'
def draw_titles(upd_t, act_ptc) -> html.Div:
    return html.Div(children=[
        html.H1(children='Connect Heartbeat (plotly dash example)', style={'text-align': 'center', 'color': colors['text']}),
        html.H2(children=l2.format(upd_t), id='last_upd', style={'text-align': 'center', 'color': colors['text']}),
        html.H3(children=l3.format(act_ptc), id='active_ptc', style={'text-align': 'center', 'color': colors['text']}),
    ])

def draw_heartbeat() -> html.Div:
    return html.Div(children=[
        gif.GifPlayer(gif='assets/heartme-heart.gif', still='assets/heart_still.gif', autoplay=True),

    ])

def draw_figure(f: px.bar) -> html.Div:
    return html.Div([
        dbc.Card(dbc.CardBody([
            html.Div(dcc.Graph(id='graph', figure=f), style={'textAlign': 'center'}),
            ])
        ),
    ])

def draw_text(t=None) -> html.Div:
    t = 'Text' if not t else t
    return html.Div([
        dbc.Card(dbc.CardBody([
            html.Div([html.H6(t), ], style={'textAlign': 'center'}),
            ])
        ),
    ])

def draw_controls() -> html.Div:
    return html.Div([
        html.Div(children=[
            html.Div(dp.DashPlayer(id="music-player", width=416, height=234, url='/assets/TaylorDayne_Heart.mp4')),
            html.Br(),
            html.Div([dbc.Button(children='', color='primary', size='lg', outline=True, id='music-toggle-button', n_clicks=0),]),
            html.Br(),
            html.Div([dbc.Button('Reload API data', color='primary', size='lg', outline=True, id='reload_api_data_button', n_clicks=0)]),
        ], style={'text-align': 'center', 'color': colors['text']})
    ])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
app.layout = html.Div([
    dbc.Card(dbc.CardBody([
            dbc.Row([
                dbc.Col([draw_titles(my_hb.last_heartbeat_date, my_hb.active_participant_count)], width=12),
            ], align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([draw_heartbeat()], width=3, align='center'),
                dbc.Col([draw_figure(fig)], width=6),
                dbc.Col([draw_controls()], width=3),
            ], align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([draw_text('Demo mode: real API call on each "Reload API data" button push, but locally increments "Male" count each time.')], width=12),
            ], align='center'),
        ]), color='dark'
    )
])

@app.callback(
    Output(component_id='music-toggle-button', component_property='children'),
    Output(component_id='music-player', component_property='playing'),
    Input(component_id='music-toggle-button', component_property='n_clicks')
    )
def music_button(n_clicks):
    disabled = n_clicks % 2
    print('clicks: {} {}'.format(n_clicks, disabled))
    return "Stop the music" if disabled else "Start the music", disabled

@app.callback(
    Output(component_id='last_upd', component_property='children'),
    Output(component_id='active_ptc', component_property='children'),
    Output(component_id='graph', component_property='figure'),
    Input(component_id='reload_api_data_button', component_property='n_clicks'),
    )
def update_data_button(n_clicks):
    my_hb.update_data() if n_clicks else None
    f = px.bar(my_hb.participant_demo_df, x='Sex', y='Count', ).update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        font={'size': 20},
    )
    return l2.format(my_hb.last_heartbeat_date), l3.format(my_hb.active_participant_count), f

if __name__ == '__main__':
    app.run_server(debug=True)
