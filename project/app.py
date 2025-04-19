import dash
import os
from dash import html
from visualisation_1.app import get_viz_1_html
from visualisation_2.src.app import get_viz_2_html
from visualisation_3.app import get_viz_3_html
from visualisation_4.app import get_viz_4_html
from visualisation_5.app import get_viz_5_html

# Initialisation de l'application Dash
app = dash.Dash(__name__)
server = app.server  # Serveur Flask sous-jacent pour déploiement
app.title = "Projet INF8808"  # Titre de l'application

# Définition de la mise en page principale de l'application
app.layout = html.Div([
    html.Main([
        # Section principale avec le titre et la description
        html.Div([
            html.Div([
                # Titre principal
                html.H1(
                    "What Makes a Nation Shine at the Olympics?",
                    className="section-title"
                ),
                # Description de l'application
                html.P([
                    html.Br(),
                    "Every four years, the world turns its eyes to the Olympic Games.",
                    html.Br(),
                    "But behind the medals and the flags lies a deeper question:",
                    html.Br(),
                    html.Span("What really drives a country’s success on the world’s biggest stage?", style={"fontWeight": "bold"}),
                    html.Br(), html.Br(),
                    "Through this data-driven story, we explore three key dynamics that have shaped Olympic performance over the decades.",
                ], className="section-title"),
                # Liens de navigation vers les différentes visualisations
                html.Div([
                    html.A(
                        "Country Conditions",
                        href="#viz2-section",
                        id="btn1"
                    ),
                    html.A(
                        "Sport Specialization",
                        href="#viz1-section",
                        id="btn2"
                    ),
                    html.A(
                        "Home Advantage",
                        href="#viz3-section",
                        id="btn3"
                    ),
                    html.A(
                        "National Heroes",
                        href="#viz4-section",
                        id="btn4"
                    ),
                    html.A(
                        "Individual Impact",
                        href="#viz5-section",
                        id="btn5"
                    ),
                ], className="ring-grid", style={'margin': '50px auto', 'width': 'fit-content'})
                ],
                className="section-column start p-40"    
            ),
            # Image principale de la page d'accueil
            html.Div([
                    html.Img(src="assets/images/home_image.png", className="home-image")
                ],
                className="section-column center"    
            ),
            ], 
            className="section-row"
        ),
        # Section pour la visualisation 2
        html.Div(
            [get_viz_2_html()],  # Contenu généré par la fonction get_viz_2_html
            id="viz2-section"
        ),
        # Section pour la visualisation 1
        html.Div(
            [get_viz_1_html()],  # Contenu généré par la fonction get_viz_1_html
            id="viz1-section"
        ),
        # Section pour la visualisation 3
        html.Div(
            [get_viz_3_html()],  # Contenu généré par la fonction get_viz_3_html
            id="viz3-section"
        ),
        # Section pour la visualisation 4
        html.Div(
            [get_viz_4_html()],  # Contenu généré par la fonction get_viz_4_html
            id="viz4-section"
        ),
        # Section pour la visualisation 5
        html.Div(
            [get_viz_5_html()],  # Contenu généré par la fonction get_viz_5_html
            id="viz5-section"
        ),
    ])
])

# Point d'entrée principal de l'application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))  # Récupération du port depuis les variables d'environnement (par défaut 8050)
    app.run(host="0.0.0.0", port=port)  # Lancement de l'application sur le port spécifié
