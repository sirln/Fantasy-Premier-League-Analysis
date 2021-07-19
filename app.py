import json
import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Output, Input, State



url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

def get(url):
    response = requests.get(url)
    return json.loads(response.content)

response = get(url)


players_df = pd.DataFrame(response['elements'])
clubs_df = pd.DataFrame(response['teams'])
season_df = pd.DataFrame(response['phases'])
gameweek_df = pd.DataFrame(response['events'])
position_df = pd.DataFrame(response['element_types'])
 

players_df['team']=players_df.team.map(clubs_df.set_index('id').name)

trim_clubs_df = clubs_df[['id','short_name','strength','position',\
                          'win','draw','loss','points','form','strength_overall_home',\
                          'strength_overall_away','strength_attack_home',\
                          'strength_attack_away','strength_defence_home',\
                          'strength_defence_away']]

trim_clubs_df_1 = clubs_df[['id','short_name','strength','position',\
                          'win','draw','loss','points','form']]

trim_clubs_df_2 = clubs_df[['id','short_name','strength_overall_home',\
                          'strength_overall_away','strength_attack_home',\
                          'strength_attack_away','strength_defence_home',\
                          'strength_defence_away']]


fig1 = px.pie(trim_clubs_df,names='short_name',values='strength',color='short_name',\
              labels='strength') ##title='Fantasy Teams Strength',
##fig2 = px.pie(trim_clubs_df,names='short_name',values='strength_overall_home',color='short_name',\
##              title='Fantasy Teams Overall Home Strength',labels='strength_overall_home')
fig2 = px.sunburst(trim_clubs_df,path=['strength','short_name'],values='strength_overall_home',color='strength_overall_home',\
              hover_data=['strength_overall_home']) ##title='Fantasy Teams Overall Home Strength',

fig3 = px.scatter(players_df.sort_values('team', ascending=True), x='ict_index_rank', y='total_points',\
                  size="total_points", color="team",  log_x=True, hover_data=['web_name','value_season','now_cost'])

##fig1.update_layout(height=450, width=560)
##fig2.update_layout(height=450, width=560)


table1=dbc.Table.from_dataframe(trim_clubs_df_1,striped=True,bordered=True,\
                               hover=True,dark=True,responsive=True)
table2=dbc.Table.from_dataframe(trim_clubs_df_2,striped=True,bordered=True,\
                               hover=True,dark=True,responsive=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]



app = dash.Dash(__name__, external_stylesheets=[external_stylesheets,dbc.themes.CERULEAN])
server = app.server
app.title = 'Fantasy Premier League Stats!'

app.layout = html.Div(
    children=[
        dbc.Container(
            [
                html.Div(
                    [
                        html.P(children='⚽', className="header-emoji"),
                        html.H1(
                            children="Fantasy Premier League Dashboard", className="header-title"
                        ),
                    ],
                    className='head'
                ),
                
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Container(
                                    [
                                        html.H6(
                                            children=['Table : FPL Clubs (2021/2022 Season)'],
                                            style={
                                                'textAlign': 'center'
                                            }
                                        ),
                                        html.Div(
                                            table1
                                        ),
                                    ],
                                    fluid=True,
                                ),
                            ],
                            width=7,
                        ),
                        
                        dbc.Col(
                            [
                                dbc.Container(
                                    [
                                        dbc.Row(
                                            dbc.Container(
                                                html.Div(
                                                    [
                                                        html.H6(
                                                            children=['Pie Chart : FPL Team Strength'],
                                                            style={
                                                                'textAlign': 'center'
                                                            }
                                                        ),
                                                        dcc.Graph(
                                                            id='Fantasy Teams Strength',
                                                            figure=fig1
                                                        ),
                                                    ],
                                                    className='pie_chart'
                                                ),
                                                fluid=True,
                                            ),
                                        ),
                                        dbc.Row(
                                            dbc.Container(
                                                html.Div(
                                                    [
                                                        html.H6(
                                                            children=['Pie Chart : FPL Team Overall Home Strength'],
                                                            style={
                                                                'textAlign': 'center'
                                                            }
                                                        ),
                                                        dcc.Graph(
                                                            id='Fantasy Teams Overall Home Strength',
                                                            figure=fig2
                                                        ),
                                                    ],
                                                    className='pie_chart'
                                                ),
                                                fluid=True,
                                            ),
                                        ),
                                    ],
                                    fluid=True,
                                ),
                            ],
                            width=5,
                        ),
                    ]
                ),
                dbc.Row(
                    dbc.Container(
                        html.Div(
                            dcc.Graph(
                                id='Fantasy Players Scatter Chart',
                                figure=fig3
                            ),
                            className='scatter_graph'
                        ),
                        fluid=True,
                    )
                )
            ],
            fluid=True,
        ),
        
    ]
)





if __name__ =='__main__':
    app.run_server(debug=True)
