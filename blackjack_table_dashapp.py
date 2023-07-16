# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 19:16:39 2023

@author: clin4
"""

#dash app displaying blackjack table, uses classes from blackjack.py file
import blackjack
import numpy as np
import dash
from dash import html, Input, Output, State, callback, dash_table, dcc

import dash_bootstrap_components as dbc

deck = blackjack.deck()

app = dash.Dash(__name__,external_stylesheets = [dbc.themes.BOOTSTRAP], 
                suppress_callback_exceptions = True, 
                #allow_duplicate=True
                )

section_head_style = {'color': 'white',
                      'padding': '1px',
                      'margin': '6px'}
section_style = {'border': '1px solid red','margin': '5px'}
component_grouping_style = {'margin': '6px',
                            'border': '3px solid white',
                            'padding': '1px'}
component_style = {'margin':'10px'}

default_remaining_string = "Total:","2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, J:0, Q:0, K:0, A:0"

def create_remaining_cards_string(deck):
    output_string = ''
    for card in deck:
        output_string += "{}:{}, ".format(card, deck[card])
    return output_string[:-1]

input_form = dbc.Row(children = [
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
                                          #value = 5,
                                          min=1, max=5,
                                          style = component_style
                                          ), 
                                width = 1), 
                        dbc.Col(dcc.RadioItems(id = 'BlackJack-Mode', 
                                               options = [{'label':'Simulation',  
                                                           'value': 'simulation', 
                                                           'disabled':False,
                                                           },
                                                        {'label':'Manual', 
                                                         'value': 'manual', 
                                                         'disabled':False,
                                                         },],
                                               inline = False,
                                               style = component_style,
                                               labelStyle={'display':'block'}), 
                                className = "fs-5",
                                width = 1),
                        dbc.Col(html.Button("Lock Settings", id = 'lock-button',n_clicks = 0,
                                            style = component_style),
                                width = 1),
                        dbc.Col(dbc.FormText(children = "Status: Settings Unlocked", id = 'setting-status-display',
                                             className = 'card-title',
                                             style = component_style
                                             ),
                                width = 2),
                        dbc.Col(children = [dbc.Row(dbc.FormText(children = "Cards remaining", 
                                             className = 'card-title',
                                             style = component_style)),
                                            dbc.Row(dbc.FormText(children = default_remaining_string, 
                                                                 id = 'cards-remaining-display', 
                                                                 className = 'card-text',
                                                                 style = component_style))], 
                                width = 1),
                        ],
            style = component_grouping_style,
            ),
    ], style = section_style, className = 'g-3')

cards = [i for i in range(2,11)]
cards.extend(['J', 'Q', 'K', 'A'])

dealer_display = dbc.Row(
    children = [
        dbc.Col(
            children = [
                    dbc.Row(children = [dbc.Col(html.H5("Dealer", className = "card-title", style = section_head_style),)],),
                    dbc.Row(children = [dbc.Col(dcc.Dropdown(id = 'dealer-card',
                                                             placeholder = 'Select Dealer Card',
                                                             options = [{'label': i, 'value': i} for i in cards],
                                                             style = component_style),
                                                width = {'size':2}),
                                        dbc.Col(html.Button('Set Dealer Value',id = 'set-dealer-button', n_clicks = 0, style = component_style), 
                                                width = {'size':2}),
                                        dbc.Col(dbc.Label(id = 'dealer-total', children = "Dealer Total, Bust Chance", color = 'secondary',
                                                          style = component_style),
                                                width = {'size':2}),
                                    ],
                            style = component_grouping_style,
                            ),
                    #additional row to display the card
                    dbc.Row(id = 'dealer-visualization', 
                            children = [],
                            style = component_grouping_style),
                    ], 
            width = {'size':6}), 
        dbc.Col(
            children = [
                dbc.Row(children = [dbc.Col(html.H5("Player Buttons", className = "card-title", style = section_head_style),)],),
                #dbc.Row(children = [html.Div('tmp')], style = component_grouping_style),
                dbc.Row(children = [dbc.Col(html.Button("P1", id = 'p0-deal-button', n_clicks=0, disabled = True), width = 1),
                                    dbc.Col(html.Button("P2", id = 'p1-deal-button', n_clicks=0, disabled = True), width = 1),
                                    dbc.Col(html.Button("P3", id = 'p2-deal-button', n_clicks=0, disabled = True), width = 1),
                                    dbc.Col(html.Button("P4", id = 'p3-deal-button', n_clicks=0, disabled = True), width = 1),
                                    dbc.Col(html.Button("P5", id = 'p4-deal-button', n_clicks=0, disabled = True), width = 1),
                                    ])
                        ],
                width = {'size':6}, ),
        ],
    className = 'g-3',
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


app.layout = html.Div(id = 'primary',
                      children = [input_form, dealer_display, hand_display],
                      style = {'background-color': 'black', 'border': '5px solid blue'})

@app.callback(
    [Output('dealer-total', 'children')],
    [Input('set-dealer-button', 'n_clicks')],
    [State('dealer-card', 'value')]
    
    )
def update_dealer_card(n_clicks, card):
    if card:
        deck.deal_dealer(card)
    return ["Dealer Total, Bust Chance {}".format(card)]

#selecting number of players and decks; changes display
@app.callback(
    [Output('player-inputs', 'children'),
     Output('player-metrics', 'children')],
    [Input("number of decks", "value"), 
     Input("number of players", "value"),],
     State("player-inputs", "children"), prevent_initial_call=True
)
def update_output(deck_count, player_count, player_input_children):
    player_marker_list = []
    input_list = []
    metrics_display = []
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
            metrics_display.append(dbc.Col(dbc.FormText(id = 'player-{}-metrics'.format(p),
                                                        children = "Total: ",
                                                        color = 'secondary',
                                                        style = component_style),
                                           width = {'size':1})
                                   )
        return [[dbc.Row(player_marker_list), dbc.Row(input_list)], metrics_display]
    return [[None, None], None]
    
@app.callback(
    [Output('p0-deal-button', 'disabled'),
    Output('p1-deal-button', 'disabled'),
    Output('p2-deal-button', 'disabled'),
    Output('p3-deal-button', 'disabled'),
    Output('p4-deal-button', 'disabled'),],
    [Input("number of players", "value")]
 )
def freeze_player_buttons(player_count):
    disable_list = []
    if player_count:
        disable_list.extend([False] * (player_count))
        disable_list.extend([True]*(5-player_count))
        
        return disable_list
    return [True] * 5


#lock or unlock setting selection
@app.callback(
    [Output('number of decks', 'disabled'),
     Output('number of players', 'disabled'),
     Output('BlackJack-Mode', 'options'),
     Output('setting-status-display', 'children'), 
     #Output('cards-remaining-display', 'children', allow_duplicate = True)
     ],
    [Input('lock-button', 'n_clicks')],
    [State('number of decks', 'value'),
     State('number of players', 'value'),
     State('setting-status-display', 'children',),
     State('BlackJack-Mode', 'options'),
     State('BlackJack-Mode', 'value')]
)
def lock_unlock(button_clicked, num_decks, num_players, status,options, mode):
    if num_players and num_decks and mode:
        
        if status == "Status: Settings Unlocked":
            #return True, True, True, "Status: Settings Locked"
            for i in range(len(options)):
                options[i]['disabled'] = True
            
            #reset everything anytime settings locked
            deck.new_deck(deck_count = num_decks,total_hands = num_players)
            #remaining_string = create_remaining_cards_string(deck.deck)
            #need to reset totals displays
            return True, True, options, "Status: Settings Locked for {}".format(mode)#, remaining_string
    for i in range(len(options)):
        options[i]['disabled'] = False
        
    return False, False,options, "Status: Settings Unlocked"#, default_remaining_string

"""
implement button to reset deck counts
"""


#draw card for player 0
#when drawn 1) from deck, draw card via deck.card_drawn(card_value, hand_number=0))
#           2) update bust chance displays
#           3) reset player 0 input dropdown value to None
#update 
@app.callback(
    [Output('player-0-input', 'value'),
     Output('player-0-metrics', 'children'), 
     Output('cards-remaining-display', 'children')],
    [Input('p0-deal-button', 'n_clicks')],
    [State('setting-status-display', 'children'),
     State('player-0-input', 'value'),], prevent_initial_call = True
)
def p1_draw_function(button_clicked, status, card_val):
    if card_val and 'Status: Settings Locked' in status:
        deck.card_drawn(card_val, 0)
        
        remaining_string = create_remaining_cards_string(deck.deck)
        return [None, "Total: {}".format(deck.hand_totals[0]), remaining_string]
    
    card_val.extend(remaining_string)
    return card_val

    
if __name__ == '__main__':
    app.run_server(debug=True)
