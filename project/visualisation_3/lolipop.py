import project.visualisation_3.hover_template as hover_template
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from project.visualisation_3.hover_template import get_host_years_by_country, get_hover_template

# Fonction principale pour créer une figure de type "lollipop"
def create_lollipop_figure(df, season, top_margin=240):
    # Récupère les années où chaque pays a été hôte pour une saison donnée
    host_years_map = get_host_years_by_country(season)

    # Crée une figure avec plusieurs sous-graphiques (3 lignes, 2 colonnes)
    fig = make_subplots(
        rows=3, cols=2, shared_yaxes=False,
        vertical_spacing=0.13,  # Espacement vertical entre les sous-graphiques
        horizontal_spacing=0.03  # Espacement horizontal entre les sous-graphiques
    )

    # Ajoute des traces factices pour personnaliser la légende
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='black'),
        name='Home advantage',  # Avantage à domicile
        legendgroup='lines',
        hoverinfo='skip',
        showlegend=True
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='blue'),
        name='Away advantage',  # Avantage à l'extérieur
        legendgroup='lines',
        hoverinfo='skip',
        showlegend=True
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(color='red', size=8),
        name='Home',  # Marqueurs pour les valeurs à domicile
        legendgroup='points',
        hoverinfo='skip',
        showlegend=True
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(color='green', size=8),
        name='Away',  # Marqueurs pour les valeurs à l'extérieur
        legendgroup='points',
        hoverinfo='skip',
        showlegend=True
    ))

    # Définit les métriques et périodes à afficher
    metrics = [
        ('Athletes', 'Number of Athletes'),
        ('Medals', 'Number of Medals'),
        ('Ratio', 'Number of Medals per Athlete')
    ]
    periods = ['1945-1991', '1992-2020']
    n_rows = len(metrics)

    # Boucle sur les périodes (colonnes)
    for j, period in enumerate(periods):
        # Filtre les données pour la période actuelle
        df_period = df[(df['Period'] == period) & (df['Athletes_Host'] > 0)].copy()
        df_period = df_period.sort_values(f"{metrics[0][0]}_Away", ascending=False)
        y_labels = df_period['Team'].tolist()  # Liste des pays
        y_pos = list(range(len(y_labels)))  # Positions sur l'axe Y

        # Boucle sur les métriques (lignes)
        for i, (metric, label_name) in enumerate(metrics):
            away_vals = df_period[f"{metric}_Away"].tolist()  # Valeurs à l'extérieur
            host_vals = df_period[f"{metric}_Host"].tolist()  # Valeurs à domicile
            row, col = i + 1, j + 1  # Ligne et colonne du sous-graphe

            # Ajoute les traces pour chaque pays
            for y_idx, (country, away, host) in enumerate(zip(y_labels, away_vals, host_vals)):
                color = 'black' if host >= away else 'blue'  # Couleur de la ligne selon l'avantage
                host_years = host_years_map.get(period, {}).get(country, [])  # Années où le pays a été hôte
                host_years_str = ", ".join(map(str, host_years)) if host_years else "N/A"

                # Ajuste les valeurs pour éviter les chevauchements
                delta = 0.001 if metric == "Ratio" else 1
                if abs(host - away) < delta:
                    away -= 2 * delta
                    host += 2 * delta

                away = float(away) if away is not None else 0
                host = float(host) if host is not None else 0

                # Trace une ligne entre les valeurs à domicile et à l'extérieur
                fig.add_trace(go.Scatter(
                    x=[away, host],
                    y=[y_idx, y_idx],
                    mode='lines',
                    line=dict(color=color),
                    hoverinfo='skip',
                    showlegend=False
                ), row=row, col=col)

                # Ajoute un marqueur pour la valeur à l'extérieur
                fig.add_trace(go.Scatter(
                    x=[away],
                    y=[y_idx],
                    mode='markers',
                    marker=dict(color='green', size=8),
                    customdata=[[country]],
                    hovertemplate=hover_template.get_hover_template(label_name, is_host=False),
                    showlegend=False
                ), row=row, col=col)

                # Ajoute un marqueur pour la valeur à domicile
                fig.add_trace(go.Scatter(
                    x=[host],
                    y=[y_idx],
                    mode='markers',
                    marker=dict(color='red', size=8),
                    customdata=[[country, host_years_str]],
                    hovertemplate=hover_template.get_hover_template(label_name, is_host=True),
                    showlegend=False
                ), row=row, col=col)

            # Met à jour les axes Y avec les noms des pays
            fig.update_yaxes(
                tickvals=list(range(len(y_labels))),
                ticktext=y_labels,
                side="right" if col == 2 else "left",  # Position des étiquettes
                row=row,
                col=col
            )

    # Ajoute des annotations pour les titres des métriques
    title_annotations = [
        dict(
            text=f"<b>{label}</b>",
            x=0.5,
            y=1 - (i*1.18 / n_rows) + 0.04,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=20, family="Roboto Slab"),
            xanchor="center"
        )
        for i, (key, label) in enumerate(metrics)
    ]

    # Définit les positions pour les lignes de séparation
    h_spacing = 0.03
    x_left = h_spacing / 2
    x_mid = 0.5
    x_right = 1 - h_spacing / 2

    # Définit les formes pour les lignes de séparation et les bordures
    shapes = []

    shapes += [
        dict(
            type='line',
            x0=0.5, x1=0.5,
            y0=0, y1=1,
            xref='paper', yref='paper',
            line=dict(color='lightgray', width=2, dash='dot')
        ),
        dict(
            type='line',
            x0=x_left, x1=x_mid - h_spacing / 2,
            y0=1.08, y1=1.08,
            xref='paper', yref='paper',
            line=dict(color='gray', width=1.5)
        ),
        dict(
            type='line',
            x0=x_mid + h_spacing / 2, x1=x_right,
            y0=1.08, y1=1.08,
            xref='paper', yref='paper',
            line=dict(color='gray', width=1.5)
        )
    ]

    # Met à jour la mise en page de la figure
    fig.update_layout(
        font=dict(family="Inter"),
        height=950,  # Hauteur de la figure
        font_size=14,  # Taille du texte
        margin=dict(t=top_margin),  # Marge supérieure
        annotations=title_annotations + [
            # Annotations pour les périodes
            dict(
                text="1945–1991",
                x=(x_left + x_mid) / 2,
                y=1.14,
                xref="paper", yref="paper",
                xanchor="center",
                showarrow=False,
                font=dict(size=16, family="Roboto Slab", color="gray")
            ),
            dict(
                text="1992–2020",
                x=(x_mid + x_right) / 2,
                y=1.14,
                xref="paper", yref="paper",
                xanchor="center",
                showarrow=False,
                font=dict(size=16, family="Roboto Slab", color="gray")
            )
        ],
        shapes=shapes,  # Ajoute les formes définies
        legend=dict(
            title=dict(text="Legend"),  # Titre de la légende
            orientation="v",  # Orientation verticale
            yanchor="top",
            y=1.33,
            xanchor="left",
            x=0,
            tracegroupgap=10  # Espacement entre les groupes de traces
        )
    )

    return fig  # Retourne la figure finale