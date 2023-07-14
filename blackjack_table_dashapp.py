# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 19:16:39 2023

@author: clin4
"""

#dash app displaying blackjack table, uses classes from blackjack.py file
import numpy as np
import dash
from dash import html, Input, Output, State, callback, dash_table, dcc

import dash_bootstrap_components as dbc

app = dash.Dash(__name__,external_stylesheets = [dbc.themes.BOOTSTRAP])

section_head_style = {'color': 'white',
                      'padding': '1px',
                      'margin': '6px'}
section_style = {'border': '1px solid red','margin': '5px'}
component_grouping_style = {'margin': '6px',
                            'border': '3px solid white',
                            'padding': '1px'}
component_style = {'margin':'10px'}
input_form = html.Div(children = [
    dbc.Row(dbc.Col(html.H5(children = "Select BlackJack Options", className = "card-title", style = section_head_style), )), 
    dbc.Row(children = [dbc.Col(dbc.FormText(children = '# of Decks', className = "card-title", color = 'secondary', style = component_style),width = {'size':1}),
                        dbc.Col(dbc.FormText(children = '# of Players', className = "card-title", color = 'secondary', style = component_style ), width = {'size':1}),
                        dbc.Col(dbc.FormText(children = 'Application Mode', className = "card-title", color = 'secondary', style = component_style ), width = {'size':1})]),
    dbc.Row(children = [dbc.Col(dcc.Input(id = 'number of decks',type = 'number', 
                                          placeholder = 'Enter # Decks', 
                                          min=1, max=10,
                                          style = component_style,
                                          ), 
                                width = 1), 
                        dbc.Col(dcc.Input(id = 'number of players', type = 'number', 
                                          placeholder = 'Enter # of Players', 
                                          min=1, max=5,
                                          style = component_style), 
                                width = 1), 
                        dbc.Col(dcc.Dropdown(id = 'BlackJack-Mode', 
                                             options = [{'label':'Simulation', 'value': 'simulation'},
                                                        {'label':'Manual', 'value': 'manual'},],
                                             clearable = True,
                                             placeholder = 'Select Mode',
                                             maxHeight = 300,
                                             style = component_style), 
                                width = 1),
                        dbc.Col(html.Button("Lock Settings", id = 'lock-button',n_clicks = 0,
                                            style = component_style),
                                width = 1),
                        dbc.Col(dbc.FormText(children = "Status: Settings Unlocked", id = 'setting-status-display',
                                             className = 'card-title',
                                             style = component_style),
                                width = 1)
                        ],
            style = component_grouping_style
            
            ),
    ], style = section_style)

cards = [i for i in range(2,11)]
cards.extend(['J', 'Q', 'K', 'A'])

dealer_display = html.Div(
    children = [
        dbc.Row(children = [dbc.Col(html.H5("Dealer", className = "card-title", style = section_head_style),)],),
        dbc.Row(children = [dbc.Col(dcc.Dropdown(id = 'dealer-card',
                                                placeholder = 'Select Dealer Card',
                                                options = [{'label': i, 'value': i} for i in cards],
                                                style = component_style),
                                   width = {'size':1}),
                            dbc.Col(dbc.FormText(id = 'dealer-total', children = "Dealer Total, Bust Chance",color = 'secondary',
                                                 style = component_style),
                                    width = {'size':1}),
                            ],
                style = component_grouping_style
                
                ),
        #additional row to display the card
        dbc.Row(id = 'dealer-visualization', 
                children = [],
                style = component_grouping_style),
        ],
    style = section_style)

hand_display = html.Div(
    children = [
        #title
        dbc.Row(children = [dbc.Col(html.H5("Player Hands", className = "card-title", style = section_head_style))]),
        #inputs for each hand
        dbc.Row(id = 'player-inputs', 
                children = [],
                style = component_grouping_style),
        #metrics for each hand
        dbc.Row(id = 'player-metrics',
                children = [],
                style = component_grouping_style),
        #visualization for each hand
        dbc.Row(id = 'player-visualization',
                children = [],
                style = component_grouping_style)
        
        ],
    style = section_style)

form2 = dbc.Form([
    html.Div(id = 'tmp')], 
    style = section_style)

app.layout = html.Div(id = 'primary',
                      children = [input_form, dealer_display, form2, hand_display],
                      style = {'background-color': 'black', 'border': '5px solid blue'})

#selecting number of players and decks; changes display
@app.callback(
    Output('player-inputs', 'children'),
    [Input("number of decks", "value"), 
     Input("number of players", "value")]
)
def update_output(deck_count, player_count):
    player_marker_list = []
    input_list = []
    if deck_count and player_count:
        for p in range(player_count):
            player_marker_list.append(dbc.Col(dbc.FormText(id = 'player-{}-nameplate'.format(p), 
                                                           children = "Player #{}".format(p+1), 
                                                           color = 'secondary',
                                                           style = component_style),
                                              width = {'size':1})
                                      )
            
            input_list.append(dbc.Col(dcc.Dropdown(id = 'player-{}-input'.format(p), 
                                                   options = [{'label':i, 'value':i} for i in cards],
                                                   style = component_style,
                                                   placeholder = "Select Player Card"), 
                                      width = {'size':1},)
                              )
        return [dbc.Row(player_marker_list), dbc.Row(input_list)]

#lock or unlock setting selection
@app.callback(
    [Output('number of decks', 'disabled'),
     Output('number of players', 'disabled'),
     Output('BlackJack-Mode', 'disabled'),
     Output('setting-status-display', 'children')],
    [Input('lock-button', 'n_clicks')],
    [State('number of decks', 'value'),
     State('number of players', 'value'),
     State('setting-status-display', 'children'),]
)
def lock_unlock(button_clicked, num_decks, num_players, status):
    if num_players and num_decks:
        
        if status == "Status: Settings Unlocked":
            return True, True, True, "Status: Settings Locked"
        
    return False, False, False, "Status: Settings Unlocked"
        
    
if __name__ == '__main__':
    app.run_server(debug=True)
