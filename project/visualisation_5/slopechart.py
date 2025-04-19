import plotly.express as px

# Importation des modules de prétraitement et de gestion des templates pour les infobulles
import project.visualisation_5.preprocess as preprocess
import project.visualisation_5.hover_template as hover_template

# Liste des pays disponibles pour la visualisation
pays_disponibles = preprocess.pays_dispo


def viz_5(df, pays, season):
    ## Prétraitement des données :
    # Filtrer les données pour les années à partir de 1991 et selon la saison (été ou hiver)
    df_years = preprocess.rejet_annees(df, 1991, ete=(season == "ete"))
    # Extraire et trier les années uniques
    years = sorted(df_years["Year"].unique())
    # Calculer les points pour chaque pays
    df_points = preprocess.points(df_years)
    # Obtenir les données sans les athlètes multi-médaillés
    df_without = preprocess.data_without(df_points)
    # Ajouter les points des pays avec et sans athlètes multi-médaillés
    df_final = preprocess.pays_points(df_points, df_without)
    # Obtenir un DataFrame utile pour la visualisation en fonction du pays et des années
    usefull_df = preprocess.get_usefull_dataframe(df_final, pays, years)

    # Vérifier si le pays est dans la liste des pays disponibles et récupérer son nom complet
    _, full_pays = preprocess.is_value_in_tuples(pays, pays_disponibles)

    ## Création de la figure :
    # Créer un graphique en ligne avec Plotly Express
    fig = px.line(
        usefull_df, 
        x="Type", 
        y="Points", 
        color="Year",
        color_discrete_sequence=px.colors.sequential.Blues[1:],  # Palette de couleurs
        markers=True,  # Ajouter des marqueurs sur les lignes
        title=str(full_pays + " points with and without multi-medalists athletes"),  # Titre du graphique
        hover_data={"Year": True, "Type": True}  # Données affichées dans les infobulles
    )

    # Mise en page du graphique
    fig.update_layout(
        height=700,  # Hauteur de la figure
        font=dict(family="Inter"),  # Définir la police "Inter"
        font_size=14,  # Taille du texte
        margin=dict(l=500, r=500, t=100, b=0),  # Marges
        plot_bgcolor='lightgrey',  # Couleur de fond du graphique

        # Configuration des axes
        xaxis=dict(type='category'),  # Axe X catégoriel
        xaxis_showgrid=False,  # Désactiver la grille sur l'axe X
        yaxis_showgrid=False,  # Désactiver la grille sur l'axe Y
        xaxis_title="",  # Pas de titre pour l'axe X

        # Configuration d'un axe secondaire (non utilisé ici)
        yaxis2=dict(
            title="Secondary Axis",
            overlaying="y",
            side="right",
            showgrid=False
        ),

        # Configuration de la légende
        legend=dict(
            x=1.5,  # Position horizontale
            y=0.5,  # Position verticale
            xanchor="center",  # Ancrage horizontal
            yanchor="bottom"  # Ancrage vertical
        ),

        # Centrer le titre du graphique
        title=dict(text=fig.layout.title.text, x=0.5),
    )
    
    # Personnalisation des ticks de l'axe X
    fig.update_xaxes(
        tickmode="array",
        tickvals=["With", "Without"],  # Valeurs des ticks
        ticktext=["With multi medalists", "Without multi medalists"]  # Texte des ticks
    )

    # Personnalisation des infobulles pour chaque trace
    for trace in fig.data:
        trace.hovertemplate = hover_template.get_hovertemplate(pays)
    
    # Personnalisation des lignes (épaisseur)
    fig.update_traces(line=dict(width=2))

    # Retourner la figure finale
    return fig
