import dash
from dash import html, dcc, Input, Output, callback
import project.visualisation_3.preprocess_ete_hiver as preprocess_ete_hiver
import project.visualisation_3.lolipop as lolipop

# Chargement initial des données
df = preprocess_ete_hiver.load_csv("all_athlete_games.csv")  # Charge le fichier CSV contenant les données des Jeux Olympiques
df_filtered = preprocess_ete_hiver.preprocess_data(df, season="Summer")  # Filtre les données pour la saison "Summer" par défaut
fig = lolipop.create_lollipop_figure(df_filtered, season="Summer")  # Crée une figure lollipop pour la saison "Summer"

# Fonction pour générer le contenu HTML de la visualisation
def get_viz_3_html():
    return html.Div([
        # Titre principal et description de la visualisation
        html.Div([
            html.H1("🏟️ 2. Do Host Nations Really Have an Advantage?", 
                    style={'textAlign': 'center', 'marginBottom': '20px', "fontFamily": "Playfair Display"}),
            html.P([
                "Does being the host country boost your performance — or is it just a myth?",
                html.Br(),                
                "We compare how countries perform at home versus abroad to reveal if hosting gives athletes a psychological "
                "or logistical edge. The results may surprise you.",
            ], style={"textAlign": "justify", "backgroundColor": "#fdfdfd", 'marginBottom': '40px', "fontFamily": "Inter"}, 
                className="viz-description"
                )
        ]),
        # Section principale avec le titre et la description détaillée
        html.Div([
            html.H2("Home Advantage at the Olympics: Myth or Reality?", 
                    style={"textAlign": "center", "color": "#DF0024", 'marginBottom': '40px', "fontFamily": "Playfair Display"}),
            html.Div(
                html.P(["It’s a question that sparks debate every few years — and now, the data speaks. This interactive visualization "
                "takes you on a journey through 75 years of Olympic history, comparing the performance of host nations at home versus "
                "abroad. For each country that has hosted the Games since 1945, we show how they’ve fared across three key indicators:",
                html.Br(), html.Br(),
                "• The average number of athletes they sent to compete",
                html.Br(),
                "• The average number of medals they won",
                html.Br(),
                "• And the efficiency of their teams, measured by medals per athlete",
                html.Br(), html.Br(),
                "The charts are split into two eras — 1945–1991 and 1992–2020 — to help you explore how the impact of hosting may "
                "have evolved over time."\
                "Each country appears twice: once for its performance as host, and once for when it competed away. Green dots "
                "represent results away from home, red dots show results on home ground, and the lines between them tell the story — "
                "of gains, gaps, and sometimes surprising reversals.",
                html.Br(), html.Br(),
                "👉 Hover over the charts to explore individual countries and uncover the patterns behind the podium." ,
                ], style={"textAlign": "justify", "fontFamily": "Inter"}
                ),
                className="viz-description"
            ),
            # Filtre pour sélectionner la saison (été ou hiver)
            html.Div([
                dcc.RadioItems(
                    id='season-filter',  # Identifiant pour le filtre
                    options=[
                        {"label": "Summer Olympics", "value": "Summer"},  # Option pour les Jeux d'été
                        {"label": "Winter Olympics", "value": "Winter"}   # Option pour les Jeux d'hiver
                    ],
                    value="Summer",  # Valeur par défaut
                    labelStyle={'display': 'inline-block', 'margin': '0 10px',"fontFamily": "Inter"},
                    inputStyle={"margin-right": "5px"}
                )
            ], style={'textAlign': 'center', 'margin': '20px 20px'}),
            # Graphique lollipop initial
            dcc.Graph(id='lollipop-graph', figure=fig)
        ]),
        # Section supplémentaire avec des observations sur les tendances olympiques
        html.Div([
            html.P([
                "As expected, the first chart shows that every host country sends more athletes when the Games take place at home — a direct effect of Olympic rules that ease qualification for the host nation.",
                html.Br(), html.Br(),
                "But to understand why, we look at the third chart:",
                html.Br(),
                "Some countries, like South Korea (Summer) or France (Winter), also show a higher medals per athlete ratio at home — meaning their athletes perform better individually.",
                html.Br(),
                "Others, like the United States, show little change in efficiency, suggesting their higher medal counts come more from the larger team size than improved performance.",
                html.Br(), html.Br(),
                "Conclusion: Hosting the Olympics usually leads to better results — partly because countries send more athletes, and sometimes because those athletes also perform better."
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

# Callback pour mettre à jour le graphique en fonction de la saison sélectionnée
@callback(
    Output('lollipop-graph', 'figure'),  # Met à jour la figure du graphique
    Input('season-filter', 'value')     # Prend la valeur sélectionnée dans le filtre comme entrée
)
def update_figure(selected_season):
    # Filtre les données en fonction de la saison sélectionnée
    df_filtered = preprocess_ete_hiver.preprocess_data(df, season=selected_season)
    # Crée une nouvelle figure lollipop pour la saison sélectionnée
    fig = lolipop.create_lollipop_figure(df_filtered, season=selected_season)
    return fig  # Retourne la figure mise à jour
