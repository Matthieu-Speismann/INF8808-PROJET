# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Olivia Gélinas
    Course: INF8808
    Python Version: 3.8

    This file contains the source code for TP4.
'''

# Importation des modules nécessaires pour Dash et Plotly
from dash import callback
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import plotly.graph_objects as go

# Importation des modules personnalisés pour le prétraitement et les graphiques
import project.visualisation_2.src.preprocess as preprocess
import project.visualisation_2.src.bubble as bubble
from pathlib import Path
import os
import pandas as pd 

# Définition des chemins vers les fichiers de données
DATA_FOLDER = Path(os.path.abspath(__file__)).parent
PATH_PROCESSED_NON_SEASONAL_DATA = DATA_FOLDER / "vis_2_processed_data_1.csv"
PATH_PROCESSED_SEASONAL_DATA = DATA_FOLDER / "vis_2_processed_data_2.csv"

# Fonction pour générer une figure Plotly à partir d'un DataFrame
def generate_fig(df, graph_id: int = 1):
    # Conversion des colonnes en types numériques
    df["Population"] = pd.to_numeric(df["Population"] , errors="coerce")
    df["nb_medals"] = pd.to_numeric(df["nb_medals"] , errors="coerce")
    df["PIB_per_Capita"] = pd.to_numeric(df["PIB_per_Capita"] , errors="coerce")

    # Arrondir les décimales et trier les données selon le type de graphique
    df = preprocess.round_decimals(df)
    if graph_id == 1:
        df = preprocess.sort_dy_by_yr_continent(df)
    else:
        df = preprocess.sort_dy_by_yr_climate(df)

    # Génération et personnalisation du graphique
    fig = bubble.get_plot(df, graph_id)
    fig = bubble.update_animation_hover_template(fig)
    fig = bubble.update_animation_menu(fig)
    fig = bubble.update_axes_labels(fig)
    fig = bubble.update_template(fig)
    fig = bubble.update_legend(fig)

    # Mise à jour des dimensions et des paramètres de mise en page
    fig.update_layout(height=650,
                      width=650,
                      font=dict(family="Inter"),  # Définir la police "Inter"
                      font_size=14)  # Définir la taille du texte à 14
    fig.update_layout(dragmode=False)

    return fig

# Chargement des données prétraitées
non_sesonal_df = preprocess.get_df(PATH_PROCESSED_NON_SEASONAL_DATA)
seasonal_df = preprocess.get_df(PATH_PROCESSED_SEASONAL_DATA)

# Génération des figures pour les deux graphiques
fig1 = generate_fig(non_sesonal_df, 1)
fig2 = generate_fig(seasonal_df, 2)

# Fonction pour mettre à jour le graphique en fonction des saisons sélectionnées
def update_figure(selected_seasons):
    # Filtrer les données selon les saisons sélectionnées
    if len(selected_seasons) == 2:
        filtered_df = non_sesonal_df
    else:
        print(selected_seasons)
        filtered_df = seasonal_df[seasonal_df['Season'] == selected_seasons[0]]
    
    # Trier les données par climat
    filtered_df = preprocess.sort_dy_by_yr_climate(filtered_df)

    # Recréer le graphique avec les données filtrées
    fig = bubble.get_plot(filtered_df, 2)
    fig = bubble.update_animation_hover_template(fig)
    fig = bubble.update_animation_menu(fig)
    fig = bubble.update_axes_labels(fig)
    fig = bubble.update_template(fig)
    fig = bubble.update_legend(fig)
    fig.update_layout(height=600,
                      width=650,
                      font=dict(family="Inter"),  # Définir la police "Inter"
                      font_size=14)  # Définir la taille du texte à 14

    return fig

# Définition du callback pour mettre à jour le graphique en fonction des filtres
callback(
    Output('bubble-graph-2', 'figure'),
    Input('viz2-season-filter', 'value')
)(update_figure)

# Fonction pour générer le HTML de la visualisation
def get_viz_2_html():
    return html.Div(className='content', children=[
        # Titre et description de la visualisation
        html.Div(children=[
            html.H1('🥇 1. Is Olympic Success Reserved for Superpowers?', 
                    style={'textAlign': 'center', 'marginBottom': '20px', "fontFamily": "Playfair Display"}),
            html.P(
            "Are the same nations always at the top of the podium — and why? "
            "From the Cold War era to modern-day dominance, we explore how wealth, population, and historical presence " \
            "shape Olympic power hierarchies — and whether the gap is growing or narrowing.",
            style={"textAlign": "justify", "backgroundColor": "#fdfdfd",'marginBottom': '40px',"fontFamily": "Inter"},
            className="viz-description"
            ),
            html.H2("Total Medals / PIB per Capita ($ USD)", 
                    style={"textAlign": "center", "color":"#0085C7","fontFamily": "Playfair Display"}),
            html.P([
                "Behind every Olympic medal lies a complex mix of factors that influence success on the global stage. "
                "While athleticism and training are key, a country’s population size, wealth, and even its climate may "
                "play an unexpected role in determining who takes home the gold. ",
                html.Br(), html.Br(),
                "Larger populations might have more athletes to choose from, but do they really win more medals ? "
                "Wealthier nations often have better resources for training, but does that translate into Olympic glory ? "
                "And how do the climates of countries impact their performance in summer versus winter Games ? ",
                html.Br(), html.Br(),
                "This visualization explores the relationship between GDP, population, and climate with Olympic performance over time, "
                "revealing fascinating trends and geographical insights that go beyond the sports themselves."
                ],
            style={"textAlign": "justify","fontFamily": "Inter"},
            className="viz-description"
            )
        ]),

        # Conteneur pour les graphiques
        html.Div(className='viz-container', 
                 style={'display': 'flex', 'justifyContent': 'center', 'gap': '40px', 'backgroundColor': 'white'}, children=[
            
            # Premier graphique
            dcc.Graph(className='graph', figure=fig1, config=dict(
            scrollZoom=False,
            showTips=False,
            showAxisDragHandles=False,
            doubleClick=False,
            displayModeBar=False
            )),

            # Deuxième graphique avec les cases à cocher
            html.Div(style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}, children=[
            # Cases à cocher pour filtrer les saisons
            html.Div([
                dcc.Checklist(
                id='viz2-season-filter',
                options=[
                    {'label': 'Summer Olympics', 'value': 'Summer'},
                    {'label': 'Winter Olympics', 'value': 'Winter'}
                ],
                value=['Winter', 'Summer'],
                labelStyle={'display': 'inline-block', 'margin-right': '15px', 'fontFamily': 'Inter'},
                inputStyle={'margin-right': '6px'}
                )
            ], style={'marginBottom': '20px', 'textAlign': 'center'}),

            # Deuxième graphique
            dcc.Graph(id='bubble-graph-2', className='graph', figure=fig2, config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            )),
            ])
        ]),
        
        # Description des graphiques
        html.Div([
            html.P([
                "The graph on the left illustrates the number of medals won per Olympic Games, segmented by GDP and categorized by "
                "continents. An analysis of the data from 1945 to 1990 reveals no distinct trend in medal distribution. However, "
                "when the graph is animated to cover the period from 1991 to 2020, a clear linear trend emerges. This shift suggests "
                "a developing correlation between a country's GDP and its Olympic medal count in recent decades.",
                html.Br(), html.Br(),
                "The graph on the right displays the number of Olympic medals won per Games in relation to GDP, grouped by climate "
                "zones. From 1945 to 1990, both the Summer and Winter Olympics show no clear correlation between GDP and medal count. "
                "However, when the graph animates to reflect the period from 1991 to 2020, a linear trend becomes apparent. "
                "This suggests that, during this more recent period, a relationship between economic power and Olympic success has "
                "emerged.",
                html.Br(), html.Br(),
                "Other correlations can be identified by exploring different time periods and types of Olympic Games—Summer or Winter. "
                "Were you able to spot them?"],
                style={
                    'textAlign': 'justify',  # Centrer le texte
                    'fontFamily': 'Inter'
                },
            className="viz-description"
            )
        ],
        className="centered"
        )

        ])
