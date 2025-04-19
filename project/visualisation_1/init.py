# Importation du module Plotly pour créer des graphiques interactifs
import plotly.graph_objects as go

def get_figure():
    """
    Fonction qui crée et retourne une figure Plotly avec une annotation indiquant que la visualisation 1 n'est pas implémentée.
    """
    # Création d'une figure vide avec Plotly
    fig = go.Figure()
    
    # Ajout d'une annotation au centre de la figure
    fig.add_annotation(
        text="Visualisation 1 non implémentée",  # Texte affiché dans l'annotation
        xref="paper", yref="paper",  # Positionnement relatif à la figure entière (et non aux axes)
        x=0.5, y=0.5,  # Coordonnées de l'annotation (au centre de la figure)
        showarrow=False,  # Désactive l'affichage d'une flèche pointant vers l'annotation
        font=dict(size=16)  # Définit la taille de la police pour le texte de l'annotation
    ) 
    
    # Mise à jour de la mise en page de la figure
    fig.update_layout(
        xaxis=dict(visible=False),  # Cache l'axe des x pour ne pas afficher de graduations ou de labels
        yaxis=dict(visible=False),  # Cache l'axe des y pour ne pas afficher de graduations ou de labels
        plot_bgcolor="rgba(0,0,0,0)",  # Définit un fond transparent pour la zone de tracé
        paper_bgcolor="rgba(0,0,0,0)"  # Définit un fond transparent pour l'ensemble de la figure
    )
    
    # Retourne l'objet figure créé avec les annotations et le style définis
    return fig
