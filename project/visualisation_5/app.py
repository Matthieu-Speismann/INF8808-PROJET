# Importation des bibliothèques nécessaires
import dash  # Framework pour créer des applications web interactives
from dash import html, dcc, Dash, callback  # Composants de Dash pour créer l'interface utilisateur
import plotly.graph_objects as go  # Pour créer des graphiques personnalisés
import plotly.express as px  # Pour créer des graphiques simples et rapides
from dash.dependencies import Input, Output  # Pour gérer les interactions utilisateur

# Importation des modules internes pour le prétraitement et la génération de graphiques
import project.visualisation_5.preprocess as preprocess  # Module pour charger et préparer les données
import project.visualisation_5.slopechart as slopechart  # Module pour créer des graphiques en pente

# Chargement des données depuis un fichier CSV
df = preprocess.load_csv("all_athlete_games.csv")  # Chargement des données des Jeux Olympiques

# Initialisation des valeurs par défaut pour le pays et la saison
pays = "USA"  # Pays par défaut
season = "ete"  # Saison par défaut (été)

# Génération initiale du graphique en pente (slopechart) pour les valeurs par défaut
fig = slopechart.viz_5(df, pays, season)  # Création du graphique pour le pays et la saison par défaut

# Liste des pays disponibles pour la sélection dans le menu déroulant
pays_disponibles = preprocess.pays_dispo  # Liste des pays disponibles, extraite via le module preprocess

# Fonction pour générer le contenu HTML de la visualisation
def get_viz_5_html():
    return html.Div([
        # Titre principal de la visualisation
        html.Div([
            html.H2(
                "Tracking Olympic Glory: Points Earned by Country Over the Years",  # Titre de la visualisation
                style={"textAlign": "center", "color": "#009F3D", "fontFamily": "Playfair Display"}  # Style du titre
            ),
            # Description détaillée de la visualisation
            html.Div(
                html.P([
                    # Texte expliquant le contexte et l'objectif de la visualisation
                    "This slopechart illustrates the evolution of Olympic performance by country across different editions of "
                    "the Games, using a points-based system rather than the traditional medal count." \
                    " Each country's score is calculated by assigning a fixed number of points to each medal type (e.g., 3 "
                    "for gold, 2 for silver, 1 for bronze), allowing for a more nuanced comparison of overall performance." \
                    " By focusing on total points instead of just medal total, this visualization highlights countries whose "
                    "athletic excellence may be underappreciated when only gold medals are considered.",
                    html.Br(), html.Br(),
                    # Suite de la description
                    "This approach aims to better reflect the contributions of multi-medal-winning athletes, whose repeated "
                    "successes can significantly influence their country's standing. " \
                    "It also allows us to observe trends over time—revealing periods of dominance, decline, or resurgence "
                    "in Olympic history.",
                    html.Br(), html.Br(),
                    # Invitation à explorer les données
                    "Now, feel free to explore the countries' propositions in both Summer and Winter Olympic Games to discover "
                    "the countries that are dependant (or not) of their best athletes."
                ], style={"textAlign": "justify", "fontFamily": "Inter"}),  # Style du texte
                className="viz-description"  # Classe CSS pour styliser cette section
            ),
        ]),
        # Menu déroulant pour sélectionner un pays
        html.Div(
            dcc.Dropdown(
                id='dropdown-pays',  # Identifiant pour le menu déroulant
                options=[{'label': p, 'value': s} for (s, p) in pays_disponibles],  # Options basées sur les pays disponibles
                value=pays,  # Valeur par défaut
                placeholder="Select a country",  # Texte d'invite
                style={"width": "200px", 'margin': '20px 20px', 'textAlign': 'center'},  # Style du menu déroulant
            ),
            className='centered'  # Classe CSS pour centrer le menu
        ),
        # Boutons radio pour sélectionner la saison (été ou hiver)
        dcc.RadioItems(
            id='viz5-season-toggle',  # Identifiant pour les boutons radio
            options=[
                {'label': 'Summer Olympics', 'value': 'ete'},  # Option pour les Jeux d'été
                {'label': 'Winter Olympics', 'value': 'hiver'}  # Option pour les Jeux d'hiver
            ],
            value='ete',  # Valeur par défaut (été)
            labelStyle={'display': 'inline-block', 'margin': '0 10px', "fontFamily": "Inter"},  # Style des étiquettes
            inline=True,  # Affichage en ligne
            style={'textAlign': 'center', 'margin': '10px 0'}  # Style global des boutons radio
        ),
        # Graphique interactif pour afficher le slopechart
        dcc.Graph(
            id='slopechart'  # Identifiant pour le graphique
        ),
        # Section avec des exemples intéressants pour guider l'utilisateur
        html.Div([
            html.P([
                # Exemples d'observations intéressantes
                "Here are some interesting examples:",
                html.Br(), html.Br(),
                "1. The USA seems dependant of their best athletes during Summer Olympic Games, which is clearly visible due "
                "to the steep slopes that most of their participations shows, however, during the Winter ones, their global level "
                "is much more homogeneous.",
                html.Br(), html.Br(),
                "2. France have the opposite results, with most of their participations reflecting a stable level, both in Summer "
                "and Winter. 2 editions seems to be an exception: 2020 in Summer and 2010 in Winter.",
                html.Br(), html.Br(),
                "3. Brasil is interesting because of its progression throught the years in the Summer Games. With time, it scores "
                "more and more point, and it reached a breakthrough since 2016, when they hosted the Summer Olympic Games. However "
                "since this edition, they also are a bit dependant to some multi-medalist, when they were not in the past dates.",
            ], style={"textAlign": "justify", "fontFamily": "Inter"},  # Style du texte
            className="viz-description"  # Classe CSS pour styliser cette section
            )
        ],
        className="centered"  # Classe CSS pour centrer cette section
        )
    ], style={'textAlign': 'center'})  # Centrer tout le contenu

# Callback pour mettre à jour le graphique en fonction des sélections utilisateur
@callback(
    Output('slopechart', 'figure'),  # Sortie : le graphique à mettre à jour
    [Input('dropdown-pays', 'value'),  # Entrée : pays sélectionné
     Input('viz5-season-toggle', 'value')]  # Entrée : saison sélectionnée
)
def update_slopechart(pays, season):
    # Génération du graphique en pente avec les nouvelles valeurs
    fig = slopechart.viz_5(df, pays, season)  # Mise à jour du graphique avec les nouvelles sélections
    return fig  # Retourne le graphique mis à jour