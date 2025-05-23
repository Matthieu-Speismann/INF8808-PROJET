# Importation des bibliothèques nécessaires pour créer une application Dash
import dash
from dash import html, dcc, callback  # Importation des composants HTML et des callbacks
import plotly.graph_objects as go  # Importation pour créer des graphiques avec Plotly
from dash.dependencies import Input, Output  # Importation pour gérer les interactions utilisateur

# Importation des fonctions et modules spécifiques à la visualisation 1
from project.visualisation_1.init import get_figure as viz1_get_figure  # Fonction pour obtenir une figure vide
import project.visualisation_1.preprocess as preprocess  # Module pour le prétraitement des données
import project.visualisation_1.heatmap as heatmap  # Module pour créer des heatmaps

# Prétraitement des données pour la saison "Summer" (par défaut)
data = preprocess.convert_data('Summer')

# Création d'une figure vide pour la visualisation 1
empty_fig = viz1_get_figure()

# Définition de la mise en page de l'application
def get_viz_1_html():
    return html.Div([  # Conteneur principal de la page
        # En-tête de l'application
        html.Div([
            html.H2(  # Titre principal de la page
                "Who Rules the Podium ? Medal Count by Country Through the Years",
                style={'textAlign': 'center',  # Centrer le texte
                       'fontFamily': 'Playfair Display',  # Police d'écriture
                       'color': '#000000'}  # Couleur du texte
            ),
            html.Div(  # Description de la visualisation
                html.P([
                    # Texte explicatif sur les Jeux Olympiques et les questions explorées
                    "Every four years, the Olympic Games bring together the best athletes from around the world. But behind the "
                    "medals and records lies another competition — one between nations, strategy, and sometimes... opportunity. ",
                    html.Br(), html.Br(),  # Sauts de ligne
                    "Have certain countries historically dominated the same sports over and over again ? Are powerhouses like the USA, "
                    "China, or Russia unbeatable in specific disciplines ? And what happens when a country hosts the Olympics — do they "
                    "influence the list of sports to improve their chances of winning more medals ? ",
                    html.Br(), html.Br(),
                    "Adding new sports, removing old ones, or adjusting event formats can sometimes raise eyebrows. Is it coincidence, "
                    "or a clever tactic to tip the balance in favor of the host nation ? ",
                    html.Br(), html.Br(),
                    "This visualization explores decades of Olympic history to uncover patterns of dominance, national specialties, "
                    "and the possible impact of hosting the Games. ",
                    html.Br(), html.Br(),
                    "Let’s see what the data reveals."
                ],
                style={
                    'textAlign': 'justify',  # Justifier le texte
                    'fontFamily': 'Inter',  # Police d'écriture
                }),
                className="viz-description"  # Classe CSS pour styliser la description
            )
        ]),
        # Contenu principal de l'application
        html.Div([
            # Bouton radio pour basculer entre les saisons (Summer/Winter)
            dcc.RadioItems(
                id='season-toggle',  # Identifiant pour le composant
                options=[
                    {'label': 'Summer Olympics', 'value': 'Summer'},  # Option pour les Jeux d'été
                    {'label': 'Winter Olympics', 'value': 'Winter'}   # Option pour les Jeux d'hiver
                ],
                value='Summer',  # Valeur par défaut (Summer)
                labelStyle={'display': 'inline-block', 'margin': '0 10px', "fontFamily": "Inter"},  # Style des étiquettes
                style={
                    'textAlign': 'center',  # Centrer le composant
                    'margin': '10px 0',  # Marges
                    'display': 'flex',  # Disposition en flexbox
                    'justify-content': 'center',  # Centrer horizontalement
                    'gap': '20px'  # Espacement entre les options
                }
            ),
            # Graphique pour afficher les visualisations
            dcc.Graph(
                id='viz1-graph',  # Identifiant pour le graphique
                figure=heatmap.create_multiple_heatmaps(data),  # Génération initiale du graphique avec les données prétraitées
                config=dict(
                    scrollZoom=False,  # Désactiver le zoom avec la molette
                    showTips=False,  # Désactiver les infobulles
                    showAxisDragHandles=False,  # Désactiver les poignées de glissement des axes
                    doubleClick=False,  # Désactiver le double-clic
                    displayModeBar=False  # Masquer la barre d'outils
                )
            )
        ]),
        # Section supplémentaire avec des observations sur les tendances olympiques
        html.Div([
            html.P([
                "When analyzing Olympic trends, it becomes clear that certain countries have long held dominance in specific sports. "
                "The United States, for example, continues to lead the way in basketball and swimming, consistently outperforming other "
                "nations with a remarkable number of medals.",
                html.Br(), html.Br(),
                "But what happens when a country hosts the Games? In 2008, when China welcomed the world to Beijing, its medal tally "
                "saw a dramatic increase—jumping from 12 to 24 medals. Was this surge a result of improved athletic performance, a "
                "coincidence, or does hosting the Olympics offer a genuine competitive edge?",
                html.Br(), html.Br(),
                "The data suggests that the home-field advantage might be more than just a myth."
            ],
            style={
                'textAlign': 'justify',  # Justifier le texte
                'fontFamily': 'Inter'  # Police d'écriture
            },
            className="viz-description"  # Classe CSS pour styliser la description
            )
        ],
        className="centered"  # Classe CSS pour centrer le contenu
        )
    ])

# Définition du callback pour mettre à jour le graphique en fonction de la saison sélectionnée
@callback(
    Output('viz1-graph', 'figure'),  # Mise à jour de la figure du graphique
    [Input('season-toggle', 'value')]  # Entrée : valeur sélectionnée dans le bouton radio
)
def update_figure(selected_season):
    # Prétraitement des données pour la saison sélectionnée (Summer ou Winter)
    data = preprocess.convert_data(selected_season)
    # Génération du graphique mis à jour avec les nouvelles données
    return heatmap.create_multiple_heatmaps(data)