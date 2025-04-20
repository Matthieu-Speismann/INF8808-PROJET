import dash
from dash import dcc, html, Input, Output, callback
from project.visualisation_4.init import get_output  # Fonction pour obtenir le texte de sortie
from project.visualisation_4.preprocess import load_csv  # Fonction pour charger un fichier CSV

# Fonction pour générer le contenu HTML de la visualisation
def get_viz_4_html():
    return html.Div([
        # Section d'introduction avec un titre et une description
        html.Div([
            html.H1("🌟 3. Can Individual Talent Elevate an Entire Nation?", 
                    style={'textAlign': 'center', 'marginBottom': '20px', "fontFamily": "Playfair Display"}),  # Titre principal
            html.P([
                "Does being the host country boost your performance — or is it just a myth?",
                html.Br(),
                "We compare how countries perform at home versus abroad to reveal if hosting gives athletes a psychological "
                "or logistical edge. The results may surprise you.",
            ], style={"textAlign": "justify", "backgroundColor": "#fdfdfd", 'marginBottom': '40px', "fontFamily": "Inter"},
                className="viz-description"  # Classe CSS pour styliser la description
            )
        ]), 

        # Section avec un sous-titre et une description détaillée
        html.Div([
            html.H2("Where are Olympic Champions from ? A Global Map of Sport Legends", 
                    style={"textAlign": "center", 'color': '#F4C300', 'marginBottom': '40px', "fontFamily": "Playfair Display"}),  # Sous-titre
            html.Div(
                html.P([
                    "Behind every Olympic champion, there’s not just talent — there’s also a country, a culture, and sometimes, "
                    "a system built to create greatness.",
                    html.Br(), html.Br(),
                    "Some nations seem to have an extraordinary ability to produce legendary athletes — those rare competitors "
                    "who collect medal after medal and leave a lasting mark on Olympic history. But are these sporting icons just "
                    "isolated cases of individual brilliance? Or do certain countries consistently shape and nurture these exceptional "
                    "talents?",
                    html.Br(), html.Br(),
                    "This visualization dives into the origins of the most decorated Olympians — athletes who have won more than 5 "
                    "medals in their career — to uncover which countries truly dominate when it comes to producing greatness.",
                    html.Br(), html.Br(),
                    "Talent might be universal… but is Olympic glory?",
                ], style={
                    'textAlign': 'justify',
                    "fontFamily": "Inter"  # Police utilisée pour le texte
                }),
                className="viz-description"  # Classe CSS pour styliser la description
            )
        ]),

        # Section pour sélectionner le type de Jeux (été ou hiver)
        html.Div([
            html.Label("Sélectionner le type de Jeux:", style={"fontFamily": "Inter"}),  # Étiquette pour le choix
            dcc.RadioItems(
                id='season-radio',  # ID pour identifier cet élément dans les callbacks
                options=[{'label': 'Summer Olympics', 'value': 'Summer'},  # Option pour les Jeux d'été
                         {'label': 'Winter Olympics', 'value': 'Winter'}],  # Option pour les Jeux d'hiver
                value='Summer',  # Valeur par défaut
                labelStyle={'display': 'inline-block', 'margin-right': '10px', "fontFamily": "Inter"},  # Style des options
            ),
        ], style={'margin': '20px 20px'}),

        # Section pour sélectionner une discipline
        html.Div([
            html.Label("Sélectionner une discipline:", style={"fontFamily": "Inter"}),  # Étiquette pour le choix
            dcc.Dropdown(
                id='discipline-dropdown',  # ID pour identifier cet élément dans les callbacks
                options=[],  # Les options seront mises à jour dynamiquement par un callback
                value=None,  # Valeur par défaut
                style={"fontFamily": "Inter"}  # Style du dropdown
            ),
        ], style={'width': '20%', 'margin-bottom': '20px'}),

        # Section pour la légende
        html.Div([
            html.Label("Légende:", style={"fontFamily": "Inter", "fontWeight": "bold"}),  # Étiquette pour la légende
            html.Div([
            html.Span(style={'display': 'inline-block', 'width': '15px', 'height': '15px', 
                 'backgroundColor': 'red', 'borderRadius': '50%', 'marginRight': '10px'}),
            html.Span("Athlète pour la discipline sélectionnée", style={"fontFamily": "Inter"})  # Texte pour le cercle rouge
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
            html.Div([
            html.Span(style={'display': 'inline-block', 'width': '15px', 'height': '15px', 
                 'backgroundColor': 'blue', 'borderRadius': '50%', 'marginRight': '10px'}),
            html.Span("Athlète pour une autre discipline", style={"fontFamily": "Inter"})  # Texte pour le cercle bleu
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], style={'margin': '20px 0', 'textAlign': 'left', 'float': 'left'}),

        # Ligne de séparation
        html.Hr(),
        # Zone de texte pour afficher les résultats
        html.Div(id='output-text', style={'whiteSpace': 'pre-line', 'fontFamily': 'monospace'})
    ], 
    className="centered")  # Classe CSS pour centrer le contenu

# Callback pour mettre à jour la liste des disciplines en fonction de la saison sélectionnée
@callback(
    [Output('discipline-dropdown', 'options'),  # Met à jour les options du dropdown
     Output('discipline-dropdown', 'value')],  # Met à jour la valeur sélectionnée par défaut
    [Input('season-radio', 'value')]  # Prend en entrée la valeur sélectionnée dans le radio button
)
def update_discipline_dropdown(season):
    # Charger le fichier CSV des disciplines correspondant à la saison (par exemple disciplines_summer.csv)
    filename = f"disciplines_{season.lower()}.csv"  # Nom du fichier basé sur la saison
    df_disc = load_csv(filename)  # Chargement du fichier CSV
    # Extraire la liste des disciplines uniques (en minuscules) et les trier
    disciplines = sorted(df_disc["discipline"].dropna().unique())
    # Créer une liste d'options pour le dropdown
    options = [{'label': d, 'value': d} for d in disciplines]
    # Sélectionner la première discipline par défaut, si disponible
    value = options[0]['value'] if options else None
    return options, value  # Retourne les options et la valeur par défaut

# Callback pour mettre à jour l'affichage en fonction de la saison et de la discipline sélectionnées
@callback(
    Output('output-text', 'children'),  # Met à jour le texte affiché dans la zone de sortie
    [Input('season-radio', 'value'),  # Prend en entrée la saison sélectionnée
     Input('discipline-dropdown', 'value')]  # Prend en entrée la discipline sélectionnée
)
def update_output(season, discipline):
    # Si aucune saison ou discipline n'est sélectionnée, afficher un message d'erreur
    if not season or not discipline:
        return "Veuillez sélectionner un type de Jeux et une discipline."
    # Appeler la fonction get_output pour obtenir le texte à afficher
    return get_output(season, discipline)