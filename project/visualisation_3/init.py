# Importation du module plotly.graph_objects pour créer des visualisations interactives
import plotly.graph_objects as go

def get_figure():
    """
    Fonction qui crée une figure Plotly avec un message indiquant que la visualisation 3 n'est pas encore implémentée.
    """
    # Création d'une figure vide
    fig = go.Figure()
    
    # Ajout d'une annotation au centre de la figure pour indiquer que la visualisation n'est pas implémentée
    fig.add_annotation(
        text="Visualisation 3 non implémentée",  # Texte de l'annotation
        xref="paper", yref="paper",  # Références pour positionner l'annotation par rapport à la figure
        x=0.5, y=0.5,  # Position de l'annotation (au centre de la figure)
        showarrow=False,  # Pas de flèche pour l'annotation
        font=dict(size=16)  # Taille de la police du texte
    ) 
    
    # Mise à jour de la mise en page de la figure
    fig.update_layout(
        xaxis=dict(visible=False),  # Masquer l'axe des x
        yaxis=dict(visible=False),  # Masquer l'axe des y
        plot_bgcolor="rgba(0,0,0,0)",  # Fond du graphique transparent
        paper_bgcolor="rgba(0,0,0,0)"  # Fond de la figure transparent
    )
    
    # Retourne la figure créée
    return fig
