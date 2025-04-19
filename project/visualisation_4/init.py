import circlify  # Bibliothèque pour créer des graphiques de cercles imbriqués
import plotly.graph_objects as go  # Bibliothèque pour créer des graphiques interactifs
from project.visualisation_4.preprocess import load_csv  # Fonction personnalisée pour charger des fichiers CSV
from dash import html, dcc  # Composants Dash pour créer des interfaces web
import math
import pandas as pd  # Bibliothèque pour manipuler des données tabulaires

def split_name(full_name):
    """
    Sépare un nom complet en prénom et nom.
    On considère que le premier mot est le prénom et le reste constitue le nom.
    """
    parts = full_name.split()
    if len(parts) >= 2:
        first_name = parts[0]
        last_name = " ".join(parts[1:])
    else:
        first_name = full_name
        last_name = ""
    return first_name, last_name

def get_output(season, discipline):
    """
    Génère une visualisation HTML pour une saison et une discipline données.
    """
    # Charger les données des fichiers CSV
    df_pays = load_csv(f"top10_pays_{season.lower()}.csv")  # Top 10 pays
    df_athletes_top = load_csv(f"top10_athletes_{season.lower()}.csv")  # Top 10 athlètes
    all_athletes = load_csv("all_athlete_games.csv")  # Données complètes des athlètes

    # Filtrer les données pour inclure uniquement les années >= 1992
    if "Year" in all_athletes.columns:
        all_athletes = all_athletes[all_athletes["Year"] >= 1992]
    elif "année" in all_athletes.columns:
        all_athletes = all_athletes[all_athletes["année"] >= 1992]
    
    # Définir les noms des colonnes en fonction des fichiers chargés
    country_col = "pays" if "pays" in df_pays.columns else "NOC"
    athlete_country_col = "pays"
    name_col = "nom_norm"
    medal_col = "médaille"
    disc_col = "discipline"
    
    # Liste pour stocker les composants HTML de sortie
    output_components = []
    output_components.append(html.H2(f"Visualisation pour {season} - Discipline sélectionnée : {discipline}"))
    output_components.append(html.P("Top 10 pays par score :"))
    
    country_components = []  # Liste pour stocker les composants HTML pour chaque pays
    
    # Parcourir les pays du top 10
    for _, row in df_pays.iterrows():
        country = row[country_col]  # Nom du pays
        score = row.get("score", row.get("Score", ""))  # Score du pays
        header = html.H3(f"Pays : {country} - Score : {score}")  # En-tête pour le pays
        
        # Filtrer les athlètes du pays
        df_country = df_athletes_top[df_athletes_top[athlete_country_col] == country]
        if df_country.empty:
            # Si aucun athlète trouvé, afficher un message
            comp = html.Div([header, html.P("Aucun athlète trouvé.")],
                            style={'marginBottom': '40px', 'border': '1px solid #ccc', 'padding': '10px'})
            country_components.append(comp)
            continue
        
        # Construire une liste des athlètes avec leurs informations
        athletes = []
        for _, arow in df_country.iterrows():
            try:
                medals = float(arow.get(medal_col, 0))  # Nombre de médailles
            except:
                medals = 0.0
            athletes.append({
                "name": arow.get(name_col, "Inconnu"),  # Nom de l'athlète
                "discipline": arow.get(disc_col, "Non renseigné"),  # Discipline
                "medals": medals  # Nombre de médailles
            })
        
        # Trier les athlètes par nombre de médailles décroissant
        athletes = sorted(athletes, key=lambda x: x["medals"], reverse=True)
        medal_values = [ath["medals"] for ath in athletes]  # Liste des médailles pour les cercles
        
        # Générer les cercles imbriqués avec circlify
        circles = circlify.circlify(
            medal_values,
            show_enclosure=False,
            target_enclosure=circlify.Circle(x=0, y=0, r=1)
        )
        circles = sorted(circles, key=lambda c: c.r, reverse=True)  # Trier les cercles par taille
        
        TAILLE = 450  # Taille du graphique
        fig = go.Figure()  # Créer une figure Plotly
        fig.update_xaxes(range=[-1.1, 1.1], showgrid=False, zeroline=False, visible=False)  # Configurer l'axe X
        fig.update_yaxes(range=[-1.1, 1.1], showgrid=False, zeroline=False, visible=False)  # Configurer l'axe Y
        
        # Variables pour les données du graphique
        x_scatter, y_scatter, hover_text_list, marker_sizes, marker_color_list = [], [], [], [], []
        for ath, circle in zip(athletes, circles):
            # Séparer le prénom et le nom de l'athlète
            first_name, last_name = split_name(ath["name"])
            total_medals = int(ath["medals"])  # Total des médailles
            # Déterminer la couleur du cercle (rouge pour la discipline sélectionnée, sinon bleu)
            color = "red" if ath["discipline"].lower() == discipline.lower() else "blue"
            x, y, r = circle.x, circle.y, circle.r  # Coordonnées et rayon du cercle
            
            # Ajouter un cercle à la figure
            fig.add_shape(
                type="circle",
                xref="x", yref="y",
                x0=x - r, y0=y - r, x1=x + r, y1=y + r,
                line_color=color,
                fillcolor=color,
                opacity=0.5
            )
            # Ajouter une annotation avec le nom de famille et le total de médailles
            fig.add_annotation(
                x=x, y=y,
                text=f"{last_name}<br>({total_medals})",
                showarrow=False,
                font=dict(color="white", size=10)
            )
            
            # Calculer les détails des médailles pour cet athlète
            df_ath = all_athletes[
                (all_athletes["Name"] == ath["name"]) &
                (all_athletes["Season"] == season) &
                (all_athletes["Sport"] == ath["discipline"])
            ]
            # Calculer le total des médailles (or, argent, bronze)
            total = int((df_ath["Medal"] == "Gold").sum() + (df_ath["Medal"] == "Silver").sum() + (df_ath["Medal"] == "Bronze").sum())
            # Texte pour le survol
            hover_text = (
                f"<b>Nom :</b> {last_name}<br>"
                f"<b>Prénom :</b> {first_name}<br>"
                f"<b>Pays :</b> {country}<br>"
                f"<b>Discipline :</b> {ath['discipline']}"
            )
            # Ajouter les données pour le scatter plot
            x_scatter.append(x)
            y_scatter.append(y)
            hover_text_list.append(hover_text)
            marker_sizes.append(r * 200)
            marker_color_list.append(color)
        
        # Ajouter un scatter plot invisible pour gérer les survols
        fig.add_trace(go.Scatter(
            x=x_scatter,
            y=y_scatter,
            mode='markers',
            marker=dict(
                size=marker_sizes,
                color=marker_color_list,
                opacity=0
            ),
            hoverinfo='text',
            hovertext=hover_text_list,
            showlegend=False
        ))
        
        # Configurer la mise en page du graphique
        fig.update_layout(
            width=TAILLE, height=TAILLE,
            font=dict(family="Inter"),  # Définir la police "Inter"
            font_size=14,  # Définir la taille du texte à 14
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor="white"
        )
        
        # Créer un composant HTML pour le graphique
        graph_component = dcc.Graph(figure=fig)
        comp = html.Div([header, graph_component],
                        style={'marginBottom': '40px', 'border': '1px solid #ccc', 'padding': '10px', 'width': f'{TAILLE}px'})
        country_components.append(comp)
    
    # Organiser les graphiques par lignes (3 par ligne)
    rows = []
    for i in range(0, len(country_components), 3):
        row = html.Div(country_components[i:i+3],
                       style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-around'})
        rows.append(row)
    
    # Ajouter les composants finaux à la sortie
    output_components = [
        html.P("Top 10 pays par score (or = 3 pts / argent = 2 pts / bronze = 1 pt)"),
        html.Div(rows)
    ]
    
    return output_components
